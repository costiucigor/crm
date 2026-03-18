import frappe
try:
	from frappe.tests import IntegrationTestCase as BaseCase
except Exception:
	try:
		from frappe.tests.utils import FrappeTestCase as BaseCase
	except Exception:
		from unittest import TestCase as BaseCase

from crm.integrations.api import link_call_logs_to_reference_by_numbers

def create_test_call_log(**kwargs):
	import uuid
	unique_id = kwargs.pop("id", str(uuid.uuid4())[:10])
	data = {
		"doctype": "CRM Call Log",
		"id": unique_id,
		"type": "Incoming",
		"status": "Completed",
		"to": "+1234567890",
		"from": "+0987654321",
	}
	data.update(kwargs)
	call_log = frappe.get_doc(data)
	call_log.insert()
	return call_log


class TestCallLogRelinking(BaseCase):
	def tearDown(self):
		frappe.db.rollback()

	def test_links_call_log_to_lead_by_phone_number(self):
		phone = "+37360001000"
		lead = frappe.get_doc(
			{
				"doctype": "CRM Lead",
				"first_name": "Phone",
				"last_name": "Match",
				"mobile_no": phone,
			}
		).insert(ignore_permissions=True)

		call_log = create_test_call_log(**{"from": phone, "to": "+1111111111"})
		call_log.reference_doctype = None
		call_log.reference_docname = None
		call_log.save(ignore_permissions=True)

		linked = link_call_logs_to_reference_by_numbers("CRM Lead", lead.name, [phone])
		self.assertGreaterEqual(linked, 1)

		call_log.reload()
		self.assertTrue(
			any(l.link_doctype == "CRM Lead" and l.link_name == lead.name for l in call_log.links)
		)

	def test_does_not_override_call_log_linked_to_other_lead(self):
		phone = "+37360002000"
		lead1 = frappe.get_doc(
			{"doctype": "CRM Lead", "first_name": "L1", "last_name": "A", "mobile_no": phone}
		).insert(ignore_permissions=True)
		lead2 = frappe.get_doc(
			{"doctype": "CRM Lead", "first_name": "L2", "last_name": "B", "mobile_no": phone}
		).insert(ignore_permissions=True)

		call_log = create_test_call_log(**{"from": phone, "to": "+1111111111"})
		call_log.link_with_reference_doc("CRM Lead", lead1.name)
		call_log.save(ignore_permissions=True)

		linked = link_call_logs_to_reference_by_numbers("CRM Lead", lead2.name, [phone])
		self.assertEqual(linked, 0)

		call_log.reload()
		self.assertTrue(
			any(l.link_doctype == "CRM Lead" and l.link_name == lead1.name for l in call_log.links)
		)
