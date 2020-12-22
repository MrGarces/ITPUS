# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Leads(models.Model):
    _name = 'Leads'

    name = fields.Char(string='Name')
    phone = fields.Integer(string='Phone no.')
    email = fields.Char(string='E-mail')

