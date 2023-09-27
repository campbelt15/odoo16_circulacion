# -*- coding: utf-8 -*-
# from odoo import http


# class WbPos(http.Controller):
#     @http.route('/wb_pos/wb_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_pos/wb_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_pos.listing', {
#             'root': '/wb_pos/wb_pos',
#             'objects': http.request.env['wb_pos.wb_pos'].search([]),
#         })

#     @http.route('/wb_pos/wb_pos/objects/<model("wb_pos.wb_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_pos.object', {
#             'object': obj
#         })
