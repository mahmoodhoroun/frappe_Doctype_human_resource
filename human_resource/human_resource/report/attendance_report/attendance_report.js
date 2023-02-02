// Copyright (c) 2023, mahmood and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Report"] = {
	"filters": [
		{
            fieldname: 'Employee',
            label: __('Employee'),
            fieldtype: 'Link',
            options: 'Employee',
        },
		{
            fieldname: 'attendance_date',
            label: __('Attendance Date'),
            fieldtype: 'Date',
        },
	]
};
