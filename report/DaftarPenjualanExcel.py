from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.srikost.report_penjualan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, penjualan):
        sheet = workbook.add_worksheet('Daftar Penjualan')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(1, 0, 'No. Nota', bold)
        sheet.write(1, 1, 'Nama Pembeli', bold)
        sheet.write(1, 2, 'Tanggal Transaksi', bold)
        sheet.write(1, 3, 'Total Pembayaran', bold)
        sheet.write(1, 4, 'Daftar Kost', bold)
        row = 2
        col = 0
        for obj in penjualan:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.nama_pembeli)
            sheet.write(row, col+2, str(obj.tgl_penjualan))
            sheet.write(row, col+3, obj.total_bayar)
            for kost in obj.detailpenjualan_ids.kost_id:
                sheet.write(row, col+4, kost.name)
                col += 1
            row += 1