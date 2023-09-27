from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import re

class ordenes(models.Model):
    _name = "circulacion.ordenes"
    _description = "circulacion.ordenes"

    cliente = fields.Many2one("circulacion.cliente", string="Cliente")
    cliente_info = fields.Char(
        string="Información del Cliente", compute="_compute_cliente_info"
    )
    # sector_info = fields.Char(
    #     string="Sector Info", compute="_compute_sector_info"
    # )

    sector_id = fields.Many2one('circulacion.sector', string="Sector")
    sector_domain = fields.Many2many('circulacion.sector', compute='_compute_sector_domain')


    @api.depends('cliente')
    def _compute_sector_domain(self):
        for record in self:
            if record.cliente:
                record.sector_domain = record.cliente.sector_ids
            else:
                record.sector_domain = self.env['circulacion.sector'].search([])

    @api.depends("cliente")
    def _compute_cliente_info(self):
        for record in self:
            if record.cliente:
                record.cliente_info = "{} {} (ID: {})".format(
                    record.cliente.name, record.cliente.apellido, record.cliente.id
                )
            else:
                record.cliente_info = ""


    # @api.depends("cliente")
    # def _compute_sector_info(self):
    #     for record in self:
    #         if record.cliente:
    #             sectors = record.cliente.sector_ids.mapped('name')  # Obtiene los nombres de los sectores
    #             record.sector_info = ", ".join(sectors)  # Une los nombres con coma
    #         else:
    #             record.sector_info = ""
 