from odoo import api, fields, models


class KelompokKost(models.Model):
    _name = 'srikost.kelompokkost'
    _description = 'New Description'

    #tipe field selection
    name = fields.Selection([
        ('kost putra', 'Kost Putra'),
        ('kost putri', 'Kost Putri'),
        ('kost campuran', 'Kost Campuran')
    ], string='Nama Kelompok Kost')
    #akhir tipe fields selection
    
    #tipe fields onchange
    kode_kost = fields.Char(string='Kode Kelompok Kost')

    @api.onchange('name')
    def _onchange_kode_kelompok(self):
        if self.name == 'kost putra':
            self.kode_kost = 'kptra1'
        elif self.name == 'kost putri':
            self.kode_kost = 'kputri2'
        elif self.name == 'kost campuran':
            self.kode_kost = 'kcpr3'
	# Akhir perubahan

    #tipe fields compute
    jml_kost = fields.Char(compute='_compute_jml_kost', string=' Jumlah Kost')

    # Perubahannya di sini
    @api.depends('kost_ids')
    def _compute_jml_kost(self):
        for record in self:
            a = self.env['srikost.kost'].search([('kelompokkost_id', '=', record.id)]).mapped('name')
            b = len(a)
            record.jml_kost = b
            record.daftar_kost = a
    
    daftar_kost = fields.Char(String='Daftar Kost')

    # Perubahannya di sini
    kost_ids = fields.One2many(comodel_name='srikost.kost',
                                inverse_name='kelompokkost_id',
                                string='Daftar Kost')