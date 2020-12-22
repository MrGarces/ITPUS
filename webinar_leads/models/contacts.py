# -*- coding: utf-8 -*-

import re
from odoo import fields, models, api
from odoo.exceptions import UserError

VALID_EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class Contacts(models.Model):
    _name = 'contact'

    name = fields.Char(string='Name')
    phone = fields.Integer(string='Phone no.')
    email = fields.Char(string='E-mail')

    @api.model
    def create(self, vals):
        # Check on contact
        contact_id = self.check_registry('contact', vals)
        lead_id = False
        # if not on contacts, check on leads
        if not contact_id:
            lead_id = self.check_registry('leads', vals)

        if contact_id:
            raise UserError('A contact is already created having the same phone/email.')
        elif lead_id:
            raise UserError('A lead is already created having the same phone/email.')

        res = super(Contacts, self).create(vals)
        return res

    def check_registry(self, model, data):
        email = data.get('email')
        phone = data.get('phone')
        registry_id = False
        # 1. Try to match registrant's email to our contact list
        if email:
            registry_id = self.env[model].search([('email', '=', email)], limit=1)

        # 2. if not matched, try registrant's phone to our contact
        if phone and not registry_id:
            registry_id = self.env[model].search([('phone', '=', phone)], limit=1)

        return registry_id

    def register(self, json_data):
        # This is a wrapper method/API to be invoke to create webinar registry
        # Assumption: Valid Json format

        registrant_data = json_data.get('registrant')
        email = registrant_data.get('email')
        phone = registrant_data.get('phone')

        vals = {'name': registrant_data.get('name', '')}
        if re.search(VALID_EMAIL_REGEX, email) and email:
            raise UserError('Invalid email format.')
        else:
            vals.update({'email': email})

        if phone:
            try:
                phone = int(phone)
                vals.update({'phone': phone})
            except:
                raise UserError('Invalid phone format.')

        result = self.create(vals)
        return True