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
<<<<<<< HEAD
		leave_type = frappe.get_doc("Leave Type", self.leave_type)
		self.set_total_leave_days()
		self.get_total_leave_allocation()
		self.check_balance_leave()
		self.check_max_continuous_days(leave_type)
		self.check_applicable_after(leave_type)
=======
		self.set_total_leave_days()
		self.get_total_leave_allocation()
		self.check_balance_leave()
		self.check_max_continuous_days()
		self.check_applicable_after()
>>>>>>> bb74f23c3e1ec461c50e6b117fb09ba68054d6d1
			
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
			status_of_checkbox = frappe.db.sql(""" select allow_negative_balance from `tabLeave Type` where leave_type_name = %s """, (self.leave_type), as_dict=1)
			print("*" * 100)
			print(status_of_checkbox[0].allow_negative_balance)
			if self.from_date <= self.to_date or status_of_checkbox[0].allow_negative_balance == 1:
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
			# leaveall = frappe.get_doc("Leave Allocation", {
			# 	"employee": self.employee,
			# 	"leave_type": self.leave_type,
			# 	"from_date": ["<=", self.from_date],
			# 	"to_date": [">=", self.to_date],
			# })
			# if leaveall:
			# 	leaveall.db_set("total_leaves_allocated", new_balance_allocat)
			frappe.db.sql(""" UPDATE `tableave Allocation` SET total_leaves_allocated = %s WHERE  employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (new_balance_allocat, self.employee, self.leave_type, self.from_date, self.to_date))
			


	def update_leave_balance_after_cancel(self):
		# total_allocated = frappe.db.sql(""" select total_leave_days from `tabLeave Application` where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		leave_balance_before_application = self.get_total_leave_allocation()
		# print("*" *100)
		# print(leave_balance_before_application)

		if leave_balance_before_application:
			new_leave_balance = float(leave_balance_before_application) + float(self.total_leave_days)
			
			if self.employee and self.from_date and self.to_date and self.leave_type:
				frappe.db.sql(""" UPDATE `tableave Allocation` SET total_leaves_allocated = %s WHERE  employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (new_leave_balance, self.employee, self.leave_type, self.from_date, self.to_date))
<<<<<<< HEAD
				frappe.db.commit()

	def check_max_continuous_days(self, leave_type):
		# today = date.today()
		continuous_days = date_diff(self.to_date, self.from_date)
		# max_continuous_days = frappe.db.sql(""" select max_continuous_days_allowed from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		frappe.get_list("Leave Type",fields=["max_continuous_days_allowed"], filters={"leave_type_name": self.leave_type})
		if  float(continuous_days) > float(leave_type.max_continuous_days_allowed):
			throw(f"You can not reservation leave over Max Continuous Days Allowed thats {leave_type.max_continuous_days_allowed}")


	def check_applicable_after(self, leave_type):
		today = date.today()
		applicable_after_days = date_diff( self.from_date, today)
		# max_applicable_after_days = frappe.db.sql(""" select applicable_after from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		# print("*" * 100)
		# print(max_applicable_after_days)
		if float(applicable_after_days) < float(leave_type.applicable_after):
			throw(f"You should reservation before Applicable After Days thats {leave_type.applicable_after} days")
=======
				frappe.db.commit

	def check_max_continuous_days(self):
		# today = date.today()
		continuous_days = date_diff(self.to_date, self.from_date)
		max_continuous_days = frappe.db.sql(""" select max_continuous_days_allowed from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		# print("*" * 100)
		# print(continuous_days)
		# print(max_continuous_days)
		if  float(continuous_days) > float(max_continuous_days[0].max_continuous_days_allowed):
			throw(f"You can not reservation leave over Max Continuous Days Allowed thats {max_continuous_days[0].max_continuous_days_allowed}")


	def check_applicable_after(self):
		today = date.today()
		applicable_after_days = date_diff(today, self.from_date)
		max_applicable_after_days = frappe.db.sql(""" select applicable_after from `tabLeave Type` where leave_type_name = %s""",(self.leave_type), as_dict=1)
		# print("*" * 100)
		# print(max_applicable_after_days)
		if float(applicable_after_days) > float(max_applicable_after_days[0].applicable_after):
			throw(f"You should reservation before Applicable After Days thats {max_applicable_after_days[0].applicable_after} days")
>>>>>>> bb74f23c3e1ec461c50e6b117fb09ba68054d6d1

@frappe.whitelist()
def get_total_leaves(employee, leave_type, from_date, to_date):
	if employee and leave_type and from_date and to_date :
		total_allocated = frappe.db.sql(""" select total_leaves_allocated from `tableave Allocation` where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (employee, leave_type, from_date, to_date), as_dict=1)

		if total_allocated:
			return str(total_allocated[0].total_leaves_allocated)
		else:
			return 0


			
@frappe.whitelist()
def get_total_days(from_date, to_date):
	if from_date and to_date:
		return date_diff(to_date, from_date) +1 
