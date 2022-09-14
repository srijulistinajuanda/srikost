from odoo import api, fields, models


'''
Membuat model BarangDarang yang inherit
ke Transient Model, Odoo 14 ke atas harus
di daftarkan di security
'''
class KostBaru(models.TransientModel):
    _name = 'srikost.kostbaru'

    kost_id = fields.Many2one(comodel_name='srikost.kost', string='Nama Kost', required=True)
    jumlah = fields.Integer(string='Jumlah', required=False)

    def button_kost_baru(self):
        for line in self:
            self.env['srikost.kost'].search([('id', '=', line.kost_id.id)]).write(
                {'stok_kamar': line.kost_id.stok_kamar +  line.jumlah}
            )