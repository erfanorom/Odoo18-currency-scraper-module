from odoo import models, fields, api

class CurrencyWallet(models.Model):
    _name = "currency.wallet"
    _description = "User Currency Wallet"

    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    currency_code = fields.Selection(selection='_get_currency_selection', string='Currency', required=True)
    amount = fields.Float(string="Amount", default=0.0)

    rial_balance = fields.Float(string="IRR Price", compute="_compute_rial_balance", store=True)
    total_assets = fields.Float(string="Total Asset (IRR)", compute="_compute_total_assets", store=True)

    @api.depends('currency_code')
    def _compute_rial_balance(self):
        for record in self:
            if record.currency_code == 'IRR':
                record.rial_balance = 1.0
            else:
                cur = self.env['currency.scraper'].search(
                    [('cFlag', '=', record.currency_code)],
                    order="create_date desc", limit=1
                )
                try:
                    record.rial_balance = float(cur.cPrice.replace(',', '').strip()) if cur.cPrice else 0.0
                except:
                    record.rial_balance = 0.0

    @api.depends('amount', 'rial_balance')
    def _compute_total_assets(self):
        for record in self:
            record.total_assets = record.amount * record.rial_balance

    @api.model
    def _get_currency_selection(self):
        currencies = self.env['currency.scraper'].search([])
        selection = [(c.cFlag, c.cName) for c in currencies if c.cFlag and c.cName]
        if not any(code == 'IRR' for code, _ in selection):
            selection.append(('IRR', 'Iranian Rial'))
        return selection

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        if not self.env.user.has_group('base.group_system'):
            args = [('user_id', '=', self.env.user.id)] + (args or [])
        return super()._search(args, offset=offset, limit=limit, order=order)
