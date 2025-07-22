# models/currency_topup.py
from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class CurrencyTopUp(models.Model):
    _name = "currency.topup"
    _description = "Currency Top-Up"
    _order = "create_date desc"

    user_id = fields.Many2one(
        'res.users', string="User",
        required=True,
        default=lambda self: self.env.user
    )
    amount = fields.Float(
        string="Amount",
        required=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft', string="Status")

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):

        if not self.env.user.has_group('base.group_system'):
            args = [('user_id', '=', self.env.user.id)] + (args or [])
        return super()._search(args, offset=offset, limit=limit, order=order)

    def action_confirm(self):

        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can confirm top-up requests."))
        for rec in self:
            if rec.state != 'draft':
                continue

            wallet = self.env['currency.wallet'].search([
                ('user_id', '=', rec.user_id.id),
                ('currency_code', '=', 'IRR')
            ], limit=1)
            if wallet:
                wallet.amount += rec.amount
            else:
                self.env['currency.wallet'].create({
                    'user_id': rec.user_id.id,
                    'currency_code': 'IRR',
                    'amount': rec.amount,
                })
            rec.state = 'confirmed'
