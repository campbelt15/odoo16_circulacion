
from odoo import models, fields, api

class puestos(models.Model):
    _name = "circulacion.puestos"
    _description = "Puestos de Trabajo"

    name = fields.Char(string="Nombre *", required=True)
    descripcion = fields.Text(string="Descripción")
    clase_puesto = fields.Selection(
        [
            ("general", "General"),
            ("delivery", "Delivery"),
        ],
        string="Clase de Puesto *",
        default="general",
        required=True,
    )


class dist_repartidores(models.Model):
    _name = "circulacion.dist_repartidores"
    _description = "Distribucion - Repartidores"

    name = fields.Char(string="Nombre *", required=True)
    telefonos = fields.Char(string="Teléfonos *", required=True)
    nombre_facturacion = fields.Char(string="Nombre Facturación *", required=True)
    direccion = fields.Char(string="Dirección *", required=True)
    nit = fields.Char(string="NIT *", required=True, default="C/F")
    estado = fields.Selection(
        [
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo"),
        ],
        string="Estado*",
        default="Activo",
        required=True,
    )
    fecha_ingreso = fields.Date(string="Ingresado el *", required=True)
    anotaciones = fields.Text(string="Anotaciones *")
    orden = fields.Integer(string="Orden *", default=1)
    comision = fields.Float(string="% Comisión *")

class tipo_devolucion(models.Model):
    _name = "circulacion.tipo_devolucion"
    _description = "Tipo de Devolucion"

    name = fields.Char(string="Nombre *", required=True)    


class estados_documentos(models.Model):
    _name = "circulacion.estados_documentos"
    _description = "Estados de Documentos"

    name = fields.Char(string="Nombre *", required=True)        
    descripcion = fields.Text(string="Descripción *", required=True)        
    tipo_movimiento_genera = fields.Selection(
        [
            ("dp", "Debito por Pedido, DP"),
            ("cd", "Crédito por Devolución, CD"),
            ("ccp", "Crédito por Pedido NO Entregado, CD"),
            ("cr", "Crédito por Redistribución, CR"),
            ("dxs", "Nota de Debito Suscripcion, CR"),
        ],
        string="Tipo de Movimiento que genera*",
    )
    afecta_saldo_flotante = fields.Selection(
        [
            ("si", "Si"),
            ("no", "No"),
        ],
        string="Afecta Saldo Flotante",
        default="si",
    )
    puede_ser_editado = fields.Selection(
        [
            ("si", "Si"),
            ("no", "No"),
        ],
        string="Puede ser Editado",
        default="si",
    )
    anula_valores_anteriores = fields.Selection(
        [
            ("si", "Si"),
            ("no", "No"),
        ],
        string="Anula Valores Anteriores",
        default="si",
    )
    aplicable = fields.Selection(
        [
            ("si", "Si"),
            ("no", "No"),
        ],
        string="Aplicable",
        default="si",
    )
    aplica_para = fields.Selection(
        [
            ("ordenes", "Ordenes"),
            ("devoluciones", "Devoluciones"),
        ],
        string="Aplicable para",
        default="ordenes",
    )


class publicacion_ediciones(models.Model):
    _name = "circulacion.publicacion_ediciones"
    _description = "publicacion_ediciones"

    anio = fields.Integer(string="Año *", required=True)     
    numero = fields.Integer(string="Número *", required=True)     
    fecha_edicion = fields.Date(string="Fecha Edición *", required=True)
    precio_venta = fields.Float(string="Precio de Venta *", required=True)         
    paginas = fields.Integer(string="Páginas *", required=True)         
    descripcion = fields.Text(string="Descripción *", required=True)    
    # empresa = fields     
    # publicacion = fields   
    estado = fields.Boolean(string="Estado *")  
    # estado_edicion = fields
    estado_pagos = fields.Selection(
        [
            ("abierta", "Abierta"),
            ("control", "Control"),
            ("cerrada", "Cerrada"),
        ],
        string="Estado de los Pagos *",
        default="abierta",
    ) 
    estado_devoluciones = fields.Selection(
        [
            ("abierta", "Abierta"),
            ("cerrada", "Cerrada"),
        ],
        string="Estado de las Devoluciones *",
        default="abierta",
    ) 