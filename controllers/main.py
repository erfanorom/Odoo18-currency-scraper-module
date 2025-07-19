from odoo import http
from odoo.http import request
import json

class CurrencyScraperUI(http.Controller):

    @http.route('/currency_scraper/ui', auth='user', website=True)
    def scraper_ui(self, **kw):
        return request.render('currency_rate.template_ui', {})  

    @http.route('/currency_scraper/data', type='http', auth='user', methods=['GET'], csrf=False)
    def currency_data_json(self, **kw):
        records = request.env['currency.scraper'].sudo().search([])

        data = [
            {
                'cName': r.cName,
                'cPrice': r.cPrice,
                'cFlag': r.cFlag,
                'cDate': r.cDate,
            } for r in records
        ]

        return http.Response(
            json.dumps(data, ensure_ascii=False),
            content_type='application/json;charset=utf-8'
        )
