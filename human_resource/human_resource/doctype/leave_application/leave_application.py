# Copyright (c) 2023, mahmood and contributors
# For license information, please see license.txt

# import frappe
from frappe import *
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from datetime import datetime,date

class LeaveApplication(Document):
	
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leave_allocation()
		self.check_balance_leave()
		# self.update_leave_balance_after_cancel()
		self.check_max_continuous_days()
		self.check_applicable_after()
			
	def on_submit(self):
		self.update_leave_balance_after_submit()

	def on_cancel(self):
		self.update_leave_balance_after_cancel()

	def set_total_leave_days(self):
		# we have a problem when we make a submit the function in validate run 
		if self.from_date and self.to_date:
			# leave_allocation_in_same_time = True
			# leave_allocations_for_same_employee = frappe.db.sql(""" select from_date, to_date, employee, leave_type from `tabLeave Application`  where employee = %s and leave_type = %s """, (self.employee, self.leave_type), as_dict=1)
			# new_from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
			# for x in leave_allocations_for_same_employee:
			# 	if x.from_date <= new_from_date <= x.to_date and self.employee == x.employee and self.leave_type == x.leave_type:
			# 		leave_allocation_in_same_time = False
			# 		print(leave_allocations_for_same_employee)


			if self.from_date <= self.to_date:
				# print("*" * 100)
				self.total_leave_days = date_diff(self.to_date, self.from_date) +1 
			else:
				throw("We can put from date after to date")
		else:
			throw("Enter From Date and To Date")

	def get_total_leave_allocation(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			total_allocated = frappe.db.sql(""" select total_leaves_allocated from `tableave Allocation` where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)

			# print("*" * 100)
			# print(str(total_allocated[0].total_leaves_allocated))
			if total_allocated:
				self.leave_balance_before_application = str(total_allocated[0].total_leaves_allocated)

		return str(total_allocated[0].total_leaves_allocated)

	def check_balance_leave(self):
		if self.leave_balance_before_application and self.total_leave_days:
			if float(self.leave_balance_before_application) < float(self.total_leave_days):
				throw("You don't have enough days left ")

	def update_leave_balance_after_submit(self):
		new_balance_allocat = float(self.leave_balance_before_application)-float(self.total_leave_days)
		if self.employee and self.from_date and self.to_date and self.leave_type:
			frappe.db.sql(""" UPDATE `tableave Allocation` SET total_leaves_allocated = %s WHERE  employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (new_balance_allocat, self.employee, self.leave_type, self.from_date, self.to_date))
			


	def update_leave_balance_after_cancel(self):
		# total_allocated = frappe.db.sql(""" select total_leave_days from `tabLeave Application` where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		leave_balance_before_application = self.get_total_leave_allocation()
		print("*" *100)
		print(leave_balance_before_application)

		if leave_balance_before_application:
			new_leave_balance = float(leave_balance_before_application) + float(self.total_leave_days)
			
			if self.employee and self.from_date and self.to_date and self.leave_type:
				frappe.db.sql(""" UPDATE `tableave Allocation` SET total_leaves_allocated = %s WHERE  employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (new_leave_balance, self.employee, self.leave_type, self.from_date, self.to_date))
				frappe.db.commit

	def check_max_continuous_days(self):
		# today = date.today()
		continuous_days = date_diff(self.to_date, self.from_date)
		max_continuous_days = frappe.db.sql(""" select max_continuous_days_allowed from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		print("*" * 100)
		print(continuous_days)
		print(max_continuous_days)
		if  float(continuous_days) > float(max_continuous_days[0].max_continuous_days_allowed):
			throw(f"You can not reservation leave over Max Continuous Days Allowed thats {max_continuous_days[0].max_continuous_days_allowed}")


	def check_applicable_after(self):
		today = date.today()
		applicable_after_days = date_diff(today, self.from_date)
		max_applicable_after_days = frappe.db.sql(""" select applicable_after from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		print("*" * 100)
		print(max_applicable_after_days)
		if float(applicable_after_days) > float(max_applicable_after_days[0].applicable_after):
			throw(f"You should reservation before Applicable After Days thats {max_applicable_after_days[0].applicable_after} days")
