# Copyright (c) 2022, Axentor LLC
# For license information, please see license.txt

import frappe
import requests
import json
from datetime import datetime
from erpnext_eta.erpnext_eta.eta_helper import get_company_eta_connector
from erpnext_eta.erpnext_eta.utils import get_eta_invoice


@frappe.whitelist()
def get_invoice_names_to_sign(company):
    connector = get_company_eta_connector(company)
    docstatus = ["1"]
    if connector.get("all_docstatus"):
        docstatus = ["0", "1"]
    invoice_names = frappe.get_list(
        "Sales Invoice",
        filters=[
            ["docstatus", "in", docstatus],
            ["company", "=", company],
            ["posting_date", ">=", connector.signature_start_date],
            ["eta_signature", "=", ""],
        ],
        order_by="posting_date",
    )
    return invoice_names if invoice_names else []


@frappe.whitelist()
def get_eta_invoice_for_signer(docname):
    inv = get_eta_invoice(docname)
    inv.pop("signatures")
    inv.documentTypeVersion = "1.0"
    print(inv)
    return inv


@frappe.whitelist()
def set_invoice_signature(docname, signature, doctype="Sales Invoice"):
    frappe.set_value(doctype, docname, "eta_signature", signature)
    return "Signature Received"
