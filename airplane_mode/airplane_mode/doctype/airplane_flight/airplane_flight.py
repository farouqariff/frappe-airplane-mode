# Copyright (c) 2025, Farouq and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.flight_status = "Completed"
	
	def on_cancel(self):
		self.flight_status = "Cancelled"
