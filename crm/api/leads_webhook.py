from __future__ import annotations

import json

import frappe
from frappe import _

from crm.integrations.api import get_contact_by_phone_number


def _split_name(full_name: str | None) -> tuple[str, str | None]:
	full_name = (full_name or "").strip()
	if not full_name:
		return "Unknown", None

	parts = [p for p in full_name.split(" ") if p]
	if len(parts) == 1:
		return parts[0], None
	return parts[0], " ".join(parts[1:])


def _get_request_json() -> dict:
	if frappe.request:
		body = frappe.request.get_data(as_text=True) or ""
		if body.strip():
			try:
				return frappe.parse_json(body) or {}
			except Exception:
				pass
	return frappe.local.form_dict.copy() if hasattr(frappe.local, "form_dict") else {}


def _validate_webhook_secret():
	secret = frappe.conf.get("crm_leads_webhook_secret")
	if not secret:
		return

	provided = None
	if frappe.request:
		provided = frappe.request.headers.get("X-CRM-Webhook-Secret")

	if not provided or provided != secret:
		frappe.throw(_("Unauthorized"), frappe.PermissionError)


def _ensure_lead_source(source_name: str) -> str:
	source_name = (source_name or "").strip()
	if not source_name:
		return ""

	existing = frappe.db.exists("CRM Lead Source", {"source_name": source_name})
	if existing:
		return source_name

	frappe.get_doc({"doctype": "CRM Lead Source", "source_name": source_name}).insert(
		ignore_permissions=True
	)
	return source_name


def _create_note(reference_doctype: str, reference_docname: str, title: str, content: str):
	frappe.get_doc(
		{
			"doctype": "FCRM Note",
			"title": title,
			"content": content,
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname,
		}
	).insert(ignore_permissions=True)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def webhook(payload: dict | None = None) -> dict:
	_validate_webhook_secret()
	previous_user = getattr(getattr(frappe, "session", None), "user", None) or "Guest"
	system_user = frappe.conf.get("crm_leads_webhook_user") or "Administrator"
	frappe.set_user(system_user)

	try:
		data = payload if isinstance(payload, dict) else None
		if data is None:
			data = _get_request_json()

		name = frappe.utils.cstr(data.get("name") or "").strip()
		phone = frappe.utils.cstr(data.get("phone") or "").strip()
		email = frappe.utils.cstr(data.get("email") or "").strip()
		message = frappe.utils.cstr(data.get("message") or "").strip()
		source = frappe.utils.cstr(data.get("source") or "").strip()

		first_name, last_name = _split_name(name)
		source = _ensure_lead_source(source)

		existing_lead = None
		if phone:
			contact = get_contact_by_phone_number(phone)
			existing_lead = contact.get("lead")

		if not existing_lead and email:
			existing_lead = frappe.db.get_value("CRM Lead", {"email": email, "converted": 0}, "name")

		if existing_lead:
			if message:
				_create_note("CRM Lead", existing_lead, _("Webhook message"), message)
			return {"ok": True, "lead": existing_lead, "created": False}

		lead = frappe.new_doc("CRM Lead")
		lead.first_name = first_name
		lead.last_name = last_name
		lead.lead_owner = system_user
		if email:
			lead.email = email
		if phone:
			lead.mobile_no = phone
		if source:
			lead.source = source

		lead.flags.ignore_email_validation = 1
		lead.insert(ignore_permissions=True)

		if message:
			_create_note("CRM Lead", lead.name, _("Webhook message"), message)

		return {"ok": True, "lead": lead.name, "created": True}
	finally:
		frappe.set_user(previous_user)
