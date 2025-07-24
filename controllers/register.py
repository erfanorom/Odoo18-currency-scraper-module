from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class UserRegistrationController(http.Controller):

    @http.route('/register', type='http', auth='public', methods=['GET'], website=True)
    def register_form(self, **kwargs):
        return request.render('currency_rate.registration_template', {})

    @http.route('/register/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def register_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        password = post.get('password')

        if not name or not email or not password:
            return request.render('currency_rate.registration_template', {
                'error': 'Please fill out all the fields.'
            })

        existing_user = request.env['res.users'].sudo().search([('login', '=', email.lower())], limit=1)
        
        if existing_user:
            return request.render('currency_rate.registration_template', {
                'error': 'This user has already registered.'
            })

        user_vals = {
            'name': name,
            'login': email.lower(),  
            'password': password,
        }

        user = request.env['res.users'].sudo().create(user_vals)
        _logger.info(f"New user created: {user.name} ({user.login})")

        return request.render('currency_rate.registration_success', {
            'user': user
        })
