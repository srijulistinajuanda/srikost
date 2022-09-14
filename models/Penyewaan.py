from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Penjualan(models.Model):
    _name = 'srikost.penjualan'
    _description = 'Penjualan'

    name = fields.Char(string='No. Nota')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    tgl_penjualan = fields.Datetime(
        string='Tanggal Transaksi',
        default=fields.Datetime.now())
    total_bayar = fields.Integer(
        string='Total Pembayaran',
        compute='_compute_totalbayar')
    detailpenjualan_ids = fields.One2many(
        comodel_name='srikost.detailpenjualan',
        inverse_name='penjualan_id',
        string='Detail Penjualan')

    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for line in self:
            result = sum(self.env['srikost.detailpenjualan'].search(
                [('penjualan_id', '=', line.id)]).mapped('subtotal'))
            line.total_bayar = result
    
    #perprubahan field ondelete
    #@api.ondelete(at_uninstall=False)
    #def __ondelete_penjualan(self):
        #if self.detailpenjualan_ids:
           # a=[]
           # for rec in self:
             #   a = self.env[srimart.detailpenjualan].search([('penjualan_id', '=', rec.id)])
               # print(a)
          #  for ob in a:
           #     print(str(ob.barang_id.name) + ' ' + str(ob.qty))
          #      ob.barang_id.stok += ob.qty
    
    #perubahan method unlink hnya mmnghpus
    def unlink(self):
        if self.detailpenjualan_ids:
            a=[]
            for rec in self:
                a = self.env['srikost.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
                print(a)
            for ob in a:
                print(str(ob.kost_id.name) + ' ' + str(ob.qty))
                ob.kost_id.stok_kamar += ob.qty
        record = super(Penjualan,self).unlink()
    
    #Perubahan edit stok
    def write(self, vals):
      for line in self:
          data_asli = self.env['srikost.detailpenjualan'].search([('penjualan_id', '=', line.id)])
          print(data_asli)

          for data in data_asli:
              print(str(data.kost_id.name) + " " + str(data.qty) + ' ' + str(data.kost_id.stok_kamar))
              data.kost_id.stok_kamar += data.qty
      
      line = super(Penjualan, self).write(vals)
      
      for line in self:
          data_setelah_edit = self.env['srikost.detailpenjualan'].search([('penjualan_id', '=', line.id)])
          print(data_asli)
          print(data_setelah_edit)

          for data_baru in data_setelah_edit:
              if data_baru in data_asli:
                  print(data_baru.kost_id.name + " " + str(data_baru.qty) + ' ' + str(data_baru.kost_id.stok_kamar))
                  data_baru.kost_id.stok_kamar -= data_baru.qty
              else:
                  pass

      return line
    
    #Perubahan sql constraint
    _sql_constraints = [
        ('no_nota_unik', 'unique (name)', 'Nomor Nota tidak boleh sama!')
     ]


class DetailPenjualan(models.Model):
    _name = 'srikost.detailpenjualan'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(
        comodel_name='srikost.penjualan',
        string='Detail Penjualan')
    kost_id = fields.Many2one(
        comodel_name='srikost.kost',
        string='List Kost')
    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_kost_id')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.harga_satuan

    @api.onchange('kost_id')
    def _onchange_kost_id(self):
        if self.kost_id.harga_sewa:
            self.harga_satuan = self.kost_id.harga_sewa
    
    @api.model
    def create(self, vals):
        record = super(DetailPenjualan,self).create(vals)
        if record.qty:
            # Mendapatkan data berdasarkan ID pada barang_id
            self.env['srikost.kost'].search([('id', '=', record.kost_id.id)]).write({'stok_kamar' : record.kost_id.stok_kamar-record.qty})
        return record
    
    # MEMBUAT CONSTRAINT
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty <1:
                raise ValidationError("Mau Sewa {} berapa banyak kamar sih...".format(rec.kost_id.name))
            elif (rec.kost_id.stok_kamar < rec.qty):
                raise ValidationError('Stok_kamar {} tidak mencukupi, hanya tersedia {}'.format(rec.kost_id.name,rec.kost_id.stok_kamar)) 