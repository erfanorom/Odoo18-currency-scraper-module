from odoo import models, fields, api
import logging
from .scraper import get_scraped_data

_logger = logging.getLogger(__name__)

class CurrencyScraper(models.Model):
    _name = "currency.scraper"
    _description = "Currency Scraper"

    cName = fields.Char(string="Country")
    cPrice = fields.Char(string="Price")
    cFlag = fields.Char(string="Country Code")
    cDate = fields.Char(string="Scraped at")

    @api.model
    def import_scraped_data(self):
        try:
            self.search([]).unlink()

            name, price, mini_flag, date = get_scraped_data()

            for n, p, f, d in zip(name, price, mini_flag, date):
                self.create({
                    'cName': n,
                    'cPrice': p,
                    'cFlag': f,
                    'cDate': d,
                })
        except Exception as e:
            _logger.error(f"Error importing scraped data: {str(e)}")