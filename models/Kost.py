from odoo import api, fields, models


class Kost(models.Model):
    _name = 'srikost.kost'
    _description = 'New Description'

    name = fields.Char(string='Nama Kost')
    alamat = fields.Char(string='Alamat Kost')
    waktu_sewa = fields.Selection([
        ('1 tahun', '1 Tahun'),
        ('1 bulan', '1 Bulan'),
        ('1 minggu', '1 Minggu')
    ],string='Waktu Sewa') 

    harga_sewa = fields.Integer(string='Harga Sewa')

    @api.onchange('waktu_sewa')
    def _onchange_harga_penyewaan(self):
        if self.waktu_sewa== '1 tahun':
            self.harga_sewa = '6000000'
        elif self.waktu_sewa == '1 bulan':
            self.harga_sewa = '700000'
        elif self.waktu_sewa == '1 minggu':
            self.harga_sewa = '100000'

    stok_kamar = fields.Integer(string="Stok Kamar")
    klp_kost = fields.Char(string='Kelompok Kost')
    ukuran_kost = fields.Char(string='Ukuran Kost')

    # Perubahannya ada di sini
    kelompokkost_id = fields.Many2one(comodel_name='srikost.kelompokkost',
                                        string='Kelompok Kost',
                                        ondelete='cascade')

    # Perubahannya di sini
    pemilikkost_id = fields.Many2many(comodel_name='srikost.pemilikkost', string='Pemilik Kost')
    