from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class CurrencyTopUp(models.Model):
    _name = "currency.topup"
    _description = "Currency Top-Up"
    _order = "state desc, create_date asc"

    user_id = fields.Many2one(
        'res.users', string="User",
        required=True,
        default=lambda self: self.env.user
    )
    amount = fields.Float(string="Amount", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="State", default='draft')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        if not self.env.user.has_group('base.group_system'):
            args = [('user_id', '=', self.env.user.id)] + (args or [])
        return super()._search(args, offset=offset, limit=limit, order=order)

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'confirmed' and self._origin and self._origin.state == 'draft':
            self._add_to_wallet()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.state == 'confirmed':
                rec._add_to_wallet()
        return records

    def write(self, vals):
        state_changed = (
            'state' in vals and
            vals['state'] == 'confirmed' and
            any(rec.state == 'draft' for rec in self)
        )
        res = super().write(vals)
        if state_changed:
            self.filtered(lambda rec: rec.state == 'confirmed')._add_to_wallet()
        return res

    def _add_to_wallet(self):
        for rec in self:
            if rec.state != 'confirmed':
                continue

            wallet = self.env['currency.wallet'].sudo().search([
                ('user_id', '=', rec.user_id.id),
                ('currency_code', '=', 'IRR')
            ], limit=1)

            if wallet:
                wallet.sudo().amount += rec.amount
            else:
                self.env['currency.wallet'].sudo().create({
                    'user_id': rec.user_id.id,
                    'currency_code': 'IRR',
                    'amount': rec.amount,
                })

    def action_confirm(self):
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can confirm top-up requests."))
        self.write({'state': 'confirmed'})
