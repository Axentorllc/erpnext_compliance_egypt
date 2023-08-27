# Copyright (c) 2022, Axentor LLC
# For license information, please see license.txt

import frappe
import requests
import json
from datetime import datetime

# PRE_PROD_URL = "https://api.preprod.invoicing.eta.gov.eg/api/v1"
# PRE_PROD_ID_URL = "https://id.preprod.eta.gov.eg/connect/token"
# ETA_BASE = PRE_PROD_URL
# DOCUMET_SUBMISSION = ETA_BASE + "/documentsubmissions"

# def get_company_eta_token(company=None):
# 	eta_token = frappe.get_doc(
# 		"ETA Company Setting", "HCH Supply For Import & Export LTD-Pre-Production")
# 	access_token = eta_token.get_password(
# 		fieldname="access_token")
# 	print(eta_token.get_password(fieldname="access_token"))
# 	return access_token if (access_token and frappe.utils.add_to_date(datetime.now(), minutes=3) < eta_token.expires_in) else refresh_eta_token(eta_token)

# def refresh_eta_token(eta_token=None):
# 	URL = PRE_PROD_ID_URL
# 	headers = {'content-type': 'application/x-www-form-urlencoded'}
# 	eta_token = frappe.get_doc(
# 		"ETA Company Setting", "HCH Supply For Import & Export LTD-Pre-Production") if not eta_token else eta_token
# 	response = requests.post(URL, data={
# 				'grant_type': 'client_credentials',
# 				'client_id': eta_token.client_id,
# 				'client_secret':  eta_token.get_password(fieldname="client_secret"),
# 				'scope': 'InvoicingAPI'
# 				}, headers=headers)
# 	if response.status_code == 200:
# 		eta_response = response.json()
# 		if eta_response.get('access_token'):
# 			eta_token.access_token = eta_response.get('access_token')
# 			eta_token.expires_in = frappe.utils.add_to_date(
# 				datetime.now(), seconds=eta_response.get('expires_in'))
# 			eta_token.save()
# 			frappe.db.commit()
# 			return eta_response.get('access_token')


# def submit_eta_documents(eta_invoice):
# 	headers = {
#      	'content-type': 'application/json; charset=utf-8',
# 		"Authorization": "Bearer " + get_company_eta_token()
# 	}
# 	data = {"documents": [eta_invoice]}
# 	data = json.dumps(data, ensure_ascii=False).encode('utf8')
# 	eta_response = requests.post(
# 		DOCUMET_SUBMISSION, data=data, headers=headers)
# 	eta_response = frappe._dict(eta_response.json())
# 	if eta_response.get('acceptedDocuments'):
# 		for doc in eta_response.get('acceptedDocuments'):
# 			if doc.get('internalId'):
# 				_id = doc.get('internalId')
# 				frappe.db.set_value('Sales Invoice', _id, 'eta_submission_id',
# 									eta_response.get('submissionId'))
# 				frappe.db.set_value('Sales Invoice', _id, 'eta_uuid',
# 									doc.get('uuid'))
# 				frappe.db.set_value('Sales Invoice', _id, 'eta_hash_key',
# 									doc.get('hashKey'))
# 				frappe.db.set_value('Sales Invoice', _id, 'eta_long_key',
# 									doc.get('longId'))
# 				frappe.db.commit()
# 	return eta_response

# def update_eta_docstatus(docname):
# 	headers = {
#             'content-type': 'application/json;charset=utf-8',
#           	"Authorization": "Bearer " + get_company_eta_token()
# 	}
# 	uuid = frappe.get_value('Sales Invoice', docname, "eta_uuid")
# 	UUID_PATH = ETA_BASE + f"/documents/{uuid}/raw"
# 	eta_response = requests.get(
# 		UUID_PATH, headers=headers)
# 	if eta_response.ok:
# 		eta_response = eta_response.json()
# 		frappe.db.set_value('Sales Invoice', eta_response.get('internalId'), 'eta_status',
#                       eta_response.get('status'))
# 		return eta_response.get('status')
# 	return "Didn't update Status"
