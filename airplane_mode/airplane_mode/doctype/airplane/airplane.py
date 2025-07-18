# Copyright (c) 2025, Farouq and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Airplane(Document):
    def autoname(self):
        series_key = f"{self.airline}-"
        self.name = make_autoname(f"{series_key}.###")
