from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CurrencyTransaction(models.Model):
    _name = "currency.transaction"
    _description = "Currency Transaction"
    _order = "create_date desc"

    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    transaction_type = fields.Selection([
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ], string="Type", required=True)
    currency_code = fields.Selection(
        selection=lambda self: self._get_currency_selection(),
        string='Currency',
        required=True
    )
    amount = fields.Float(string="Amount", required=True)
    price_at_transaction = fields.Float(string="Unit Price", readonly=True)
    total_value = fields.Float(string="Total (IRR)", compute="_compute_total", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            user_id = vals.get('user_id') or self.env.user.id
            vals['user_id'] = user_id

            currency = self.env['currency.scraper'].search([('cFlag', '=', vals['currency_code'])], limit=1)
            if not currency or not currency.cPrice:
                raise UserError(_("Currency not found or price unavailable."))

            try:
                price = float(currency.cPrice.replace(',', '').strip())
            except:
                raise UserError(_("Invalid currency price format."))

            vals['price_at_transaction'] = price
            total_price = price * vals['amount']

            wallet = self.env['currency.wallet'].search([
                ('user_id', '=', user_id),
                ('currency_code', '=', vals['currency_code'])
            ], limit=1)

            rial_wallet = self.env['currency.wallet'].search([
                ('user_id', '=', user_id),
                ('currency_code', '=', 'IRR')
            ], limit=1)

            if vals['transaction_type'] == 'buy':
                if not rial_wallet or rial_wallet.amount < total_price:
                    raise UserError(_("Insufficient IRR balance."))
                rial_wallet.amount -= total_price

                if wallet:
                    wallet.amount += vals['amount']
                else:
                    self.env['currency.wallet'].create({
                        'user_id': user_id,
                        'currency_code': vals['currency_code'],
                        'amount': vals['amount'],
                    })

            elif vals['transaction_type'] == 'sell':
                if not wallet or wallet.amount < vals['amount']:
                    raise UserError(_("Not enough currency balance to sell."))
                wallet.amount -= vals['amount']

                if rial_wallet:
                    rial_wallet.amount += total_price
                else:
                    self.env['currency.wallet'].create({
                        'user_id': user_id,
                        'currency_code': 'IRR',
                        'amount': total_price,
                    })

        return super().create(vals_list)

    @api.onchange('currency_code')
    def _onchange_currency_code(self):
        if self.currency_code:
            currency = self.env['currency.scraper'].search([('cFlag', '=', self.currency_code)], limit=1)
            if currency and currency.cPrice:
                try:
                    self.price_at_transaction = float(currency.cPrice.replace(',', '').strip())
                except:
                    self.price_at_transaction = 0.0

    @api.onchange('amount', 'price_at_transaction')
    def _onchange_total_value(self):
        if self.amount and self.price_at_transaction:
            self.total_value = self.amount * self.price_at_transaction

    @api.depends('amount', 'price_at_transaction')
    def _compute_total(self):
        for record in self:
            record.total_value = record.amount * record.price_at_transaction

    @api.model
    def _get_currency_selection(self):
        currencies = self.env['currency.scraper'].search([])
        return [(c.cFlag, c.cName or c.cFlag) for c in currencies if c.cFlag]
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        if not self.env.user.has_group('base.group_system'):
            args = [('user_id', '=', self.env.user.id)] + (args or [])
        return super()._search(args, offset=offset, limit=limit, order=order)
