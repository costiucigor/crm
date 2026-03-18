import json
import os

import frappe


def before_tests():
	frappe.flags.mute_emails = True
	frappe.flags.in_test = True
	# Skip loading user fixtures to avoid welcome email side-effects


def load_crm_user_test_records():
	"""Load CRM user test records from crm/tests/test_records.json"""
	test_records_path = os.path.join(os.path.dirname(__file__), "test_records.json")

	if os.path.exists(test_records_path):
		with open(test_records_path) as f:
			test_records = json.load(f)

		for record in test_records:
			if not frappe.db.exists("User", record.get("email")):
				record = record.copy()
				record.pop("new_password", None)
				doc = frappe.get_doc(record)
				doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
