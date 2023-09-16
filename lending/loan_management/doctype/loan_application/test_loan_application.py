# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

from erpnext.setup.doctype.employee.test_employee import make_employee

from lending.loan_management.doctype.loan.test_loan import create_loan_accounts, create_loan_type


class TestLoanApplication(unittest.TestCase):
	def setUp(self):
		create_loan_accounts()
		create_loan_type(
			"Home Loan",
			500000,
			9.2,
			0,
			1,
			0,
			"Cash",
			"Disbursement Account - _TC",
			"Payment Account - _TC",
			"Loan Account - _TC",
			"Interest Income Account - _TC",
			"Penalty Income Account - _TC",
			repayment_schedule_type="Monthly as per repayment start date",
		)
		self.applicant = make_employee("kate_loan@loan.com", "_Test Company")
		self.create_loan_application()

	def create_loan_application(self):
		loan_application = frappe.new_doc("Loan Application")
		loan_application.update(
			{
				"applicant": self.applicant,
				"loan_type": "Home Loan",
				"rate_of_interest": 9.2,
				"loan_amount": 250000,
				"repayment_method": "Repay Over Number of Periods",
				"repayment_periods": 18,
				"company": "_Test Company",
			}
		)
		loan_application.insert()

	def test_loan_totals(self):
		loan_application = frappe.get_doc("Loan Application", {"applicant": self.applicant})

		self.assertEqual(loan_application.total_interest_payable, 18599)
		self.assertEqual(loan_application.total_amount_payable, 268599)
		self.assertEqual(loan_application.monthly_repayment_amount, 14923)

		loan_application.repayment_periods = 24
		loan_application.save()
		loan_application.reload()

		self.assertEqual(loan_application.total_interest_payable, 24657)
		self.assertEqual(loan_application.total_amount_payable, 274657)
		self.assertEqual(loan_application.monthly_repayment_amount, 11445)
