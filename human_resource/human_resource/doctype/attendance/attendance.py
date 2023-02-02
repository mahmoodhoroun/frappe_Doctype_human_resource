# Copyright (c) 2023, mahmood and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils import time_diff
from datetime import datetime,date


class Attendance(Document):
	
	def on_submit(self):
		self.get_work_hours()
		self.update_status_value_in_attendance()


	def get_work_hours(self):
		if self.check_out and self.check_in:
			start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')
			start_time = datetime.strptime(str(start_time), '%H:%M:%S')
			end_time = frappe.db.get_single_value('Attendance Settings', 'end_time')
			end_time = datetime.strptime(str(end_time), '%H:%M:%S')

			late_entry_grace_period = frappe.db.get_single_value('Attendance Settings', 'late_entry_grace_period')
			early_exit_grace_period = frappe.db.get_single_value('Attendance Settings', 'early_exit_grace_period')
			
			check_in = datetime.strptime(self.check_in, '%H:%M:%S')
			check_out = datetime.strptime(self.check_out, '%H:%M:%S')

			late_in_the_entry_hours = start_time.hour - check_in.hour 
			late_in_the_entry_minutes = start_time.minute - check_in.minute  + late_entry_grace_period
			late_in_the_entry = late_in_the_entry_hours - (-late_in_the_entry_minutes / 60)
			
			early_in_the_exit_hours = check_out.hour - end_time.hour  
			early_in_the_exit_minutes =  end_time.minute - check_out.minute - early_exit_grace_period
			early_in_the_exit = early_in_the_exit_hours - (early_in_the_exit_minutes / 60)

			
			
			if late_in_the_entry > 0:
				late_in_the_entry = 0.

			if early_in_the_exit > 0:
				early_in_the_exit = 0

			self.late_hours = -late_in_the_entry + -early_in_the_exit
			self.work_hours = 8 - self.late_hours

	def update_status_value_in_attendance(self):
		working_hours_threshold_for_absent = frappe.db.get_single_value('Attendance Settings','working_hours_threshold_for_absent')
		print(type(working_hours_threshold_for_absent))
		if self.work_hours <=  working_hours_threshold_for_absent:
			self.status = "Absent"
		else:
			self.status = "Present"

	
@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out):
    # Check if the required fields are present
    if  not attendance_date or not check_in or not check_out:
        frappe.throw("Attendance Date, Check In, and Check Out are required")
    # create new attendance record for the requesting employee
    new_attendance = frappe.new_doc("Attendance")
    user = frappe.session.user
    new_attendance.employee = frappe.get_doc("Employee", {"user": user}).name
    new_attendance.attendance_date = attendance_date
    new_attendance.check_in = check_in
    new_attendance.check_out = check_out
    new_attendance.insert()
    return {"message": "Attendance created successfully "}