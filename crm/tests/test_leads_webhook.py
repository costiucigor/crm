import frappe
try:
	from frappe.tests import IntegrationTestCase as BaseCase
except Exception:
	try:
		from frappe.tests.utils import FrappeTestCase as BaseCase
	except Exception:
		from unittest import TestCase as BaseCase

from crm.api.leads_webhook import webhook


class TestLeadsWebhook(BaseCase):
	def tearDown(self):
		frappe.db.rollback()

	def test_webhook_creates_lead_and_note(self):
		email = "ion.webhook@example.com"
		phone = "+37360000001"

		if frappe.db.exists("CRM Lead", {"email": email}):
			for name in frappe.get_all("CRM Lead", filters={"email": email}, pluck="name"):
				frappe.delete_doc("CRM Lead", name, force=1)

		result = webhook(
			{
				"name": "Ion Popescu",
				"phone": phone,
				"email": email,
				"message": "Salut!",
				"source": "Website",
			}
		)

		self.assertTrue(result["ok"])
		self.assertTrue(result["created"])
		self.assertTrue(frappe.db.exists("CRM Lead", result["lead"]))

		lead = frappe.get_doc("CRM Lead", result["lead"])
		self.assertEqual(lead.email, email)
		self.assertEqual(lead.mobile_no, phone)
		self.assertEqual(lead.source, "Website")

		note = frappe.db.get_value(
			"FCRM Note",
			{"reference_doctype": "CRM Lead", "reference_docname": lead.name, "content": "Salut!"},
			"name",
		)
		self.assertTrue(note)

	def test_webhook_dedupes_by_email(self):
		email = "dup.webhook@example.com"
		lead = frappe.get_doc(
			{
				"doctype": "CRM Lead",
				"first_name": "Existing",
				"last_name": "Lead",
				"email": email,
				"converted": 0,
			}
		).insert(ignore_permissions=True)

		result = webhook(
			{
				"name": "Someone Else",
				"phone": "+37360000002",
				"email": email,
				"message": "Second message",
				"source": "Website",
			}
		)

		self.assertTrue(result["ok"])
		self.assertFalse(result["created"])
		self.assertEqual(result["lead"], lead.name)

		note = frappe.db.get_value(
			"FCRM Note",
			{"reference_doctype": "CRM Lead", "reference_docname": lead.name, "content": "Second message"},
			"name",
		)
		self.assertTrue(note)
