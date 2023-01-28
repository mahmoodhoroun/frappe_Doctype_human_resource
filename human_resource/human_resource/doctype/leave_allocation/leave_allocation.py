# Copyright (c) 2023, mahmood and contributors
# For license information, please see license.txt

from datetime import datetime
from frappe import *
import frappe
from frappe.model.document import Document

class leaveAllocation(Document):
	def validate(self):
		self.validate_for_leave_allocation()
		

	def validate_for_leave_allocation(self):
		leave_allocation_in_same_time = True
		leave_allocations_for_same_employee = frappe.db.sql(""" select employee, leave_type,from_date, to_date from `tableave Allocation`  where employee = %s and leave_type = %s """, 
		(self.employee, self.leave_type), as_dict=1)
		print(leave_allocations_for_same_employee)
		new_from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
		new_to_date = datetime.strptime(self.to_date, '%Y-%m-%d').date()

		for x in leave_allocations_for_same_employee:
				if x.from_date <= new_from_date <= x.to_date and x.from_date <= new_to_date <= x.to_date and self.employee == x.employee and self.leave_type == x.leave_type:
					leave_allocation_in_same_time = False
					print(leave_allocations_for_same_employee)

		if not leave_allocation_in_same_time:
			throw("You have anther allocation in same date")

		

