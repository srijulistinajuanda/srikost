from odoo import api, fields, models


class PemilikKost(models.Model):
    _name = 'srikost.pemilikkost'
    _description = 'New Description'

    name = fields.Char(string='Nama Pemilik')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No. Telepon')
    kost_id = fields.Many2many(comodel_name='srikost.kost', string='Kost')