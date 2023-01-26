# Copyright (c) 2023, mahmood and contributors
# For license information, please see license.txt

# import frappe
from frappe import *
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class LeaveApplication(Document):
	
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leave_allocation()
		self.check_balance_leave()
			
	def on_submit(self):
		self.update_leave_allocation()


	def set_total_leave_days(self):
		if self.from_date and self.to_date:
			self.total_leave_days = date_diff(self.to_date, self.from_date) +1 
		else:
			throw("Enter From Date and To Date")

	def get_total_leave_allocation(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			total_allocated = frappe.db.sql(""" select total_leaves_allocated from `tableave Allocation` where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)

			# print("*" * 100)
			# print(str(total_allocated[0].total_leaves_allocated))
			if total_allocated:
				self.leave_balance_before_application = str(total_allocated[0].total_leaves_allocated)

	def check_balance_leave(self):
		if self.leave_balance_before_application and self.total_leave_days:
			if float(self.leave_balance_before_application) < float(self.total_leave_days):
				throw("You don't have enough days left ")

	def update_leave_allocation(self):
		new_balance_allocat = float(self.leave_balance_before_application)-float(self.total_leave_days)
		if self.employee and self.from_date and self.to_date and self.leave_type:
			frappe.db.sql(""" UPDATE `tableave Allocation` SET total_leaves_allocated = %s WHERE  employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (new_balance_allocat, self.employee, self.leave_type, self.from_date, self.to_date))