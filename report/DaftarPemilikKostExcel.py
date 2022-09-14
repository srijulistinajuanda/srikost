from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.srikost.report_pemilikkost_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, pemilikkost):
        # One sheet by partner
        sheet = workbook.add_worksheet('Daftar Pemilik Kost')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'Nama Pemilik')
        sheet.write(1, 1, 'Alamat')
        sheet.write(1, 2, 'No. Telepon')
        sheet.write(1, 3, 'Kost')
        
        row = 2
        col = 0
        for obj in pemilikkost:
            col = 0
            # Text style bold, jjika tidak perlu bisa dihapus
            # bold = workbook.add_format({'bold': True})

            # write(row, col, title, style)
            # style bersifat opsional
            # sheet.write(0, 0, obj.name, bold)
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.alamat)
            sheet.write(row, col + 2, obj.no_telp)

            for item in obj.kost_id:
                sheet.write(row, col + 3, item.name)
                col += 1
            row += 1