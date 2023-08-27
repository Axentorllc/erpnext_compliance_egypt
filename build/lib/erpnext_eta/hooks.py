from . import __version__ as app_version

app_name = "erpnext_eta"
app_title = "ERPNext ETA"
app_publisher = "Axentor, LLC"
app_description = "Integration for Egyptian Tax Authority"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "apps@axentor.co"
app_license = "CC"


doctype_js = {"Sales Invoice": "erpnext_eta/public/js/sales_invoice.js"}

# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {"doctype": "{doctype_4}"},
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpnext_eta.auth.validate"
# ]

fixtures = [
    {
        "dt": "Role",
        "filters": [
            # ["name", "in", [
            #     "Axentor Manager",
            # ]]
        ],
    },
    {"dt": "ETA UOM"},
    {"dt": "ETA Activity Code"},
    {"dt": "ETA Tax Type"},
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Item-eta_details",
                    "Item-eta_code_type",
                    "Item-eta_cb",
                    "Item-eta_item_code",
                    "Item-eta_cb_2",
                    "Item-gpc",
                    "UOM-eta_uom",
                    "Sales Invoice Item-eta_code_type",
                    "Sales Invoice Item-eta_item_code",
                    "Sales Invoice Item-eta_uom",
                    "Sales Invoice-eta_details",
                    "Sales Invoice-eta_status",
                    "Sales Invoice-eta_submission_id",
                    "Sales Invoice-eta_uuid",
                    # "Sales Invoice-signature_status",
                    "Sales Invoice-eta_response_cb",
                    "Sales Invoice-eta_hash_key",
                    "Sales Invoice-eta_long_key",
                    "Sales Invoice-eta_signature",
                    "Sales Invoice-eta_exchange_rate",
                    "Company-eta_details",
                    "Company-eta_issuer_type",
                    "Company-eta_tax_id",
                    "Company-eta_cb",
                    "Company-eta_issuer_name",
                    "Company-eta_default_branch",
                    "Company-eta_default_activity_code",
                    # "Company-eta_document_type_version",
                    # "Company-eta_company_environment",
                    "Address-building_number",
                    "Customer-eta_details",
                    "Customer-eta_receiver_type",
                    "Branch-eta_details",
                    "Branch-is_eta_branch",
                    "Branch-eta_sb",
                    "Branch-eta_branch_id",
                    "Branch-eta_cb1",
                    "Branch-eta_branch_address",
                    "Sales Taxes and Charges-eta_tax_type",
                    "Sales Taxes and Charges-eta_tax_sub_type",
                ],
            ]
        ],
    },
]
