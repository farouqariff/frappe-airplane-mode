# Copyright (c) 2025, Farouq and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):
	def before_save(self):
		self.total_amount = 0
		for add_on in self.add_ons:
			self.total_amount += (add_on.quantity * add_on.price_per_item)
		self.total_amount += self.flight_price

	def validate(self):
		seen = set()
		self.add_ons = [a for a in self.add_ons if not (a.item in seen or seen.add(a.item))]

	def before_submit(self):
		if self.ticket_status != "Boarded":
			frappe.throw(
				title="Error",
				msg="The Ticket Cannot be Submitted Unless It Is Boarded"
			)

	def before_insert(self):
		flight = frappe.get_doc("Airplane Flight", self.flight)
		airplane = frappe.get_doc("Airplane", flight.airplane)
		capacity = airplane.capacity
		seats_per_row = 6
		num_rows = capacity // seats_per_row
		if capacity % seats_per_row != 0:
			num_rows += 1
		letters = ['A','B','C','D','E']
		all_possible_seats = []
		count = 0
		for row in range(1, num_rows+1):
			for letter in letters:
				seat = f"{row}{letter}"
				all_possible_seats.append(seat)
				count += 1
				if count >= capacity:
					break
			if count >= capacity:
				break
		existing_seats = frappe.get_all(
			"Airplane Ticket",
			filters={"flight":self.flight},
			pluck="seat"
		)
		available_seats = list(set(all_possible_seats) - set(existing_seats))
		if not available_seats:
			frappe.throw("All seats are taken for this flight")
		self.seat = random.choice(available_seats)