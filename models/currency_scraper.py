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
            name, price, mini_flag, date = get_scraped_data()

            if not (name and price and mini_flag and date):
                _logger.warning("No new scraped data found. Skipping update.")
                return  

            self.search([]).unlink()

            for n, p, f, d in zip(name, price, mini_flag, date):
                self.create({
                    'cName': n,
                    'cPrice': p,
                    'cFlag': f,
                    'cDate': d,
                })

        except Exception as e:
            _logger.error(f"Error importing scraped data: {str(e)}")
