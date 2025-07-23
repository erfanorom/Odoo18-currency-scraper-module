from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    wallet_total_assets_display = fields.Char(
        string="Wallet Total (IRR)",
        compute='_compute_wallet_total_assets_display',
        store=False
    )

    @api.depends_context('uid')  
    def _compute_wallet_total_assets_display(self):
        Wallet = self.env['currency.wallet']
        current_user = self.env.user
        is_admin = current_user.has_group('base.group_system')

        for partner in self:
            users = partner.user_ids
            if not is_admin:
                users = users.filtered(lambda u: u.id == current_user.id)

            if users:
                wallets = Wallet.search([('user_id', 'in', users.ids)])
                total = sum(wallet.total_assets for wallet in wallets)
                partner.wallet_total_assets_display = f"{total:,.2f} IRR"
            else:
                partner.wallet_total_assets_display = "unknown"
