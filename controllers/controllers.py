from crypt import methods
import json

from odoo import http, models, fields
from odoo.http import request


class Srikost(http.Controller):
    @http.route('/srikost/getkost', auth='public', method=['GET'])
    def getkost(self, **kw):
        # Mengambil semua barang dari table barang
        kost = request.env['srikost.kost'].search([])
        items = []

        for item in kost:
            items.append({
                'nama_kost': item.name,
                'alamat_kost': item.alamat,
                'waktu_sewa': item.waktu_sewa,
                'harga_sewa': item.harga_sewa,
                'stok_kamar': item.stok_kamar,
                'ukuran_kost': item.ukuran_kost
            })
        
        return json.dumps(items)

	# Perubhannya di sini
    @http.route('/srikost/getpemilikkost', auth='public', method=['GET'])
    def getpemilikkost(self, **kw):
        pemilikkost = request.env['srikost.pemilikkost'].search([])
        items = []

        for item in pemilikkost:
            items.append({
                'nama_pemilik': item.name,
                'alamat': item.alamat,
                'no_telepon': item.no_telp,
                'kost_id': item.kost_id[0].name
            })
        
        return json.dumps(items)