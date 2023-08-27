# Copyright (c) 2022, Axentor LLC
# For license information, please see license.txt
import frappe


def get_company_eta_connector(company):
    connectors = frappe.get_list("ETA Connector", filters={"company": company, "is_default": 1})
    if connectors:
        connector = frappe.get_doc("ETA Connector", connectors[0]["name"])
        return connector
    else:
        frappe.throw("No Default Connecter Set.")


def get_default_eta_connector_names():
    connectors = frappe.get_list("ETA Connector", filters={"is_default": 1}, pluck="name")
    if connectors:
        connector = frappe.get_doc("ETA Connector", connectors[0]["name"])
        return connector
    else:
        frappe.throw("No Default Connecter Set.")


def autofetch_eta_status(company):
    connector = get_company_eta_connector(company)
    # get list of submitted invoices:
    docs = frappe.get_all("Sales Invoice", filters=[["eta_status", "=", "Submitted"]], pluck="name")
    for docname in docs:
        connector.update_eta_docstatus(docname)
        frappe.db.commit()


def autosubmit_signed_documents(company):
    connector = get_company_eta_connector(company)
    connector.submit_signed_invoices()
