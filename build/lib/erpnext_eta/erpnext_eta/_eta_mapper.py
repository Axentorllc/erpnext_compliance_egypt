# # Copyright (c) 2022, Axentor LLC
# import frappe

# def get_eta_sales_invoice_map():
# 	"""
# 		# CALCULATED / POLYFILLED
# 		"documentType": "I",  								#*#
# 		"documentTypeVersion": "0.9",						#*#
# 		"dateTimeIssued": "2020-10-27T23:59:59Z",			#*#
# 		"taxpayerActivityCode": "4620",						#*#


# 		"internalID": "IID1", 								#*# [name]
# 		"totalSalesAmount": 1609.9,							#*#	[net_total] Sum all all InvoiceLine/SalesTotal items
# 		"netAmount": 1533.61,								#*# [net_total] TotalSales – TotalDiscount
# 		"totalDiscountAmount": 76.29,						#*# [0] sum of all Discount amount elements of InvoiceLine items

# 		"totalAmount": 5191.5,								#*# [grand_total] NetAmount + Totals of tax amounts. rounded(5)
# 		"extraDiscountAmount": 5.0,							#*#	[discount_amount]
# 		"totalItemsDiscountAmount": 14.0					#*#	 #=# [SUM(lineitems.discount_amount)] [0]

# 		# OPTIONAL
# 		"purchaseOrderReference": "P-233-A6375",					#*
# 		"purchaseOrderDescription": "purchase Order description",	#*
# 		"salesOrderReference": "1231",								#*
# 		"salesOrderDescription": "Sales Order description",			#*
# 		"proformaInvoiceNumber": "SomeValue",						#*

# 		# STRUCTS
# 		"invoiceLines" 		#MAPPED			#*#
# 		"receiver" 			#POLYFILLED		#*#
# 		"issuer" 			#POLYFILLED		#*#
# 		"taxTotals"			#OPTIONAL		#*
# 		"delivery"			#OPTIONAL		#*
# 		"payment"			#OPTIONAL		#*
# 	"""
# 	return frappe._dict({
# 			"internalID": "name",
# 			"totalSalesAmount": "net_total",
# 			"netAmount": "net_total",
# 			# "totalDiscountAmount"
# 			"totalAmount": "grand_total",
# 			"extraDiscountAmount": "discount_amount",
# 			# "totalItemsDiscountAmount"
# 		})

# def get_eta_sales_invoice_line_item_map():

# 	"""
# 		"description": "Computer1",				#*#		[item_name]
# 		"itemType": "GPC",						#*# 	[eta_code_type] GS1, EGS custom Field
# 		"itemCode": "10001774",					#*# 	[eta_item_code]	custom Field
# 		"unitType": "EA",						#*# 	[eta_uom] custom Field
# 		"quantity": 5,							#*# 	[qty]
# 		"internalCode": "IC0",					#*# 	[item_code]
# 		"salesTotal": 947.0,					#*# 	[amount]
# 		"total": 2969.89,						#*# #=# [amount] + [Item Tax]
# 		"valueDifference": 7.0,					???
# 		"totalTaxableFees": 817.42,				Extra Charges: Total amount of additional taxable fees
# 		"netTotal": 880.71,						#*# 	[amount]
# 		"itemsDiscount": 5.0,					#*# 	[0]
# 		"unitValue": {							#*# #=#	[CURRENCY]
# 			"currencySold": "EUR",
# 			"amountEGP": 189.4,
# 			"amountSold": 10.0,
# 			"currencyExchangeRate": 18.94
# 		},
# 		"discount": {							#*
# 			"rate": 7,
# 			"amount": 66.29
# 		},:
# 			"taxableItems": [						#*
# 				{
# 		"taxType": "T1",
# 		"amount": 272.07,
# 		"subType": "T1",
# 		"rate": 14.0
# 		},
# 	"""
# 	return {
# 		"description"	: "item_name",
# 		"itemType"		: "eta_code_type",
# 		"itemCode"		: "eta_item_code",
# 		"unitType"		: "eta_uom",
# 		"quantity"		: "qty",
# 		"internalCode" 	: "item_code",
# 		"salesTotal"	: "amount",
# 		# "total":
# 		# "valueDifference":
# 		# "totalTaxableFees":
# 		"netTotal"		: "amount"
# 		# "itemsDiscount":
# }


# def get_eta_inv_issuer(invoice):
# 	eta_issuer = frappe._dict()
# 	company = frappe.get_doc("Company", invoice.company)
# 	eta_issuer.type = company.eta_issuer_type
# 	eta_issuer.id = company.eta_tax_id
# 	eta_issuer.name = company.eta_issuer_name
# 	branch = frappe.get_doc("Branch", company.eta_default_branch)
# 	branch_address = frappe.get_doc("Address", branch.eta_branch_address)
# 	country_code = frappe.db.get_value("Country", branch_address.country, "code")
# 	eta_issuer.address = {
# 		"branchID": branch.eta_branch_id,
# 		"country": country_code,
# 		"governate": branch_address.state,
# 		"regionCity": branch_address.city,
# 		"street": branch_address.address_line1,
# 		"buildingNumber": branch_address.building_number
# 	}
# 	return eta_issuer

# def get_eta_inv_issuer_map():
# 	return {
# 		"Type": "eta_type",
# 		"Id": "eta_tax_id",
# 		"Name": "eta_name",
# 	}


# def get_eta_inv_receiver(invoice):
# 	eta_receiver = frappe._dict()
# 	customer = frappe.get_doc("Customer", invoice.customer)
# 	eta_receiver.type = customer.eta_receiver_type or "P"
# 	eta_receiver.id = customer.tax_id.replace("-", "")
# 	# eta_receiver.name = customer.customer_name
# 	eta_receiver.name = "MY NAME"
# 	# Address is optionsal
# 	return eta_receiver
