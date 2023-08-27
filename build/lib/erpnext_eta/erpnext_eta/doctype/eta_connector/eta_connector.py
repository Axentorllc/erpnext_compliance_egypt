# Copyright (c) 2022, Axentor, LLC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from datetime import datetime
from erpnext_eta.erpnext_eta.utils import get_eta_invoice


class ETAConnector(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.PREPROD_URL = "https://api.preprod.invoicing.eta.gov.eg/api/v1"
        self.PREPROD_ID_URL = "https://id.preprod.eta.gov.eg/connect/token"
        self.PROD_URL = "https://api.invoicing.eta.gov.eg/api/v1"
        self.PROD_ID_URL = "https://id.eta.gov.eg/connect/token"

        self.ETA_BASE = self.PREPROD_URL
        self.ID_URL = self.PREPROD_ID_URL

        if self.environment == "Production":
            self.ETA_BASE = self.PROD_URL
            self.ID_URL = self.PROD_ID_URL

        self.DOCUMET_SUBMISSION = self.ETA_BASE + "/documentsubmissions"
        self.DOCUMENT_TYPES = self.ETA_BASE + "/documenttypes"

    def get_eta_access_token(self):
        # eta_token = frappe.get_doc(
        # 	"ETA Company Setting", "HCH Supply For Import & Export LTD-Pre-Production")
        if self.access_token:
            access_token = self.get_password(fieldname="access_token")
        else:
            access_token = self.refresh_eta_token()
        return (
            access_token
            if (access_token and frappe.utils.add_to_date(datetime.now(), minutes=3) < self.expires_in)
            else self.refresh_eta_token()
        )

    def refresh_eta_token(self):
        # URL = self.PRE_PROD_ID_URL
        headers = {"content-type": "application/x-www-form-urlencoded"}
        # eta_token = frappe.get_doc(
        response = requests.post(
            self.ID_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.get_password(fieldname="client_secret"),
                "scope": "InvoicingAPI",
            },
            headers=headers,
        )
        if response.status_code == 200:
            eta_response = response.json()
            if eta_response.get("access_token"):
                self.access_token = eta_response.get("access_token")
                self.expires_in = frappe.utils.add_to_date(datetime.now(), seconds=eta_response.get("expires_in"))
                self.save()
                frappe.db.commit()
                return eta_response.get("access_token")

    def submit_eta_documents(self, eta_invoice):
        headers = {
            "content-type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.get_eta_access_token(),
        }
        data = {"documents": [eta_invoice]}
        data = json.dumps(data, ensure_ascii=False).encode("utf8")
        eta_response = requests.post(self.DOCUMET_SUBMISSION, data=data, headers=headers)
        eta_response = frappe._dict(eta_response.json())
        if eta_response.get("acceptedDocuments"):
            for doc in eta_response.get("acceptedDocuments"):
                if doc.get("internalId"):
                    _id = doc.get("internalId")
                    frappe.db.set_value("Sales Invoice", _id, "eta_submission_id", eta_response.get("submissionId"))
                    frappe.db.set_value("Sales Invoice", _id, "eta_uuid", doc.get("uuid"))
                    frappe.db.set_value("Sales Invoice", _id, "eta_hash_key", doc.get("hashKey"))
                    frappe.db.set_value("Sales Invoice", _id, "eta_long_key", doc.get("longId"))
                    frappe.db.set_value("Sales Invoice", _id, "eta_status", "Submitted")
                    frappe.db.commit()
        return eta_response

    def update_eta_docstatus(self, docname):
        headers = {
            "content-type": "application/json;charset=utf-8",
            "Authorization": "Bearer " + self.get_eta_access_token(),
        }
        uuid = frappe.get_value("Sales Invoice", docname, "eta_uuid")
        UUID_PATH = self.ETA_BASE + f"/documents/{uuid}/raw"
        eta_response = requests.get(UUID_PATH, headers=headers)
        if eta_response.ok:
            eta_response = eta_response.json()
            frappe.db.set_value(
                "Sales Invoice", eta_response.get("internalId"), "eta_status", eta_response.get("status")
            )
            return eta_response.get("status")
        return "Didn't update Status"

    def get_document_type(self, doc_id=""):
        headers = {
            "content-type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.get_eta_access_token(),
        }
        _path = self.DOCUMENT_TYPES + f"/{doc_id}"
        eta_response = requests.get(_path, headers=headers)
        print(eta_response.text)

    def submit_signed_invoices(self):
        docs = frappe.get_all(
            "Sales Invoice",
            filters=[["eta_signature", "!=", ""], ["eta_status", "=", ""], ["eta_submission_id", "=", ""]],
            pluck="name",
        )
        for docname in docs:
            inv = get_eta_invoice(docname)
            self.submit_eta_documents(inv)


# eta_token = frappe.get_doc(
# 		"ETA Connector", "HCH Supply For Import & Export LTD-Pre-Production")
# 	access_token = eta_token.get_password(
# 		fieldname="access_token")
# 	print(eta_token.get_password(fieldname="access_token"))
# 	return access_token if (access_token and frappe.utils.add_to_date(datetime.now(), minutes=3) < eta_token.expires_in) else refresh_eta_token(eta_token)
