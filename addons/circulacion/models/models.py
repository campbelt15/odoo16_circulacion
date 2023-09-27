# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import re

class cliente(models.Model):
    _name = "circulacion.cliente"
    _description = "circulacion.cliente"

    name = fields.Char(string="Nombre(s)*", required=True)
    fotografia = fields.Binary(string="Fotografía")
    apellido = fields.Char(string="Apellido(s)*", required=True)
    empresa = fields.Char(string="Nombre de Compañia")
    nit = fields.Char(string="NIT", default="C/F", input_mask='^[0-9]+$')
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    no_documento = fields.Char()
    talla = fields.Char()
    nombre_facturacion = fields.Char(string="Nombre de Facturación*", required=True)
    dir_facturacion = fields.Char(string="Dirección de Facturación*", required=True)
    telefono = fields.Char(string="Teléfonos*", required=True)
    correo = fields.Char(string="Correo Electrónico")
    ruta_ids = fields.One2many("circulacion.ruta", "cliente_id", string="Rutas")
    sector_ids = fields.One2many('circulacion.sector', 'cliente', string="Sectores")
    precio_unidad = fields.Float(
        compute="_compute_precio_dias",
        readonly=True,
        store=True,
        digits=(16, 2),
        string="Precio por Unidad*",
    )

    dias_validos_devolucion = fields.Integer(
        compute="_compute_precio_dias",
        inverse="_inverse_dias_validos_devolucion",
        store=True,
        string="Días Válidos para Devolución*",
        required=True,
    )

    cantidad_pedido = fields.Integer(
        default=0, string="Cantidad de Pedido Ordinario*", required=True
    )
    cantidad_flete = fields.Integer(
        default=0, string="Cantidad de Flete*", required=True
    )
    cantidad_promocion = fields.Integer(
        default=0, string="Cantidad de Promoción*", required=True
    )
    tipo_documento = fields.Selection(
        [
            ("cedula", "Cedula"),
            ("dpi", "DPI"),
            ("pasaporte", "Pasaporte"),
            ("otros", "Otros"),
        ],
        string="Tipo de Documento",
        default="cedula",
        required=True,
    )
    tipo_persona = fields.Selection(
        [
            ("individual", "Individual"),
            ("juridica", "Jurídica"),
        ],
        string="Tipo de Persona*",
        default="individual",
        required=True,
    )

    talla = fields.Selection(
        [
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
            ("xxl", "XXL"),
            ("xxxl", "XXXL"),
        ],
        string="Talla*",
        default="s",
        required=True,
    )

    canal_facturacion = fields.Selection(
        [
            ("sectores_metropolitanos", "Sectores Metropolitanos"),
            ("sectores_departamentales", "Sectores Departamentales"),
            ("tiendas_barrio", "Tiendas de Barrio"),
            ("tiendas_conveniencia", "Tiendas de Conveniencia"),
            ("suscripciones", "Suscripciones"),
            ("suscripciones_cortesia", "Suscripciones de Cortesia"),
            ("agencias_publicidad", "Agencias de Publicidad"),
            ("oficinas_zona_12", "Oficinas Zona 12"),
            ("envios_usa", "Envios a USA"),
            ("otros", "Otros"),
        ],
        string="Canales de Facturación*",
        default="sectores_metropolitanos",
        required=True,
    )

    tipo_documento = fields.Selection(
        [
            ("cedula", "Cedula"),
            ("dpi", "DPI"),
            ("pasaporte", "Pasaporte"),
            ("otros", "Otros"),
        ],
        string="Tipo de Documento",
        default="cedula",
    )
    tipo_persona = fields.Selection(
        [
            ("individual", "Individual"),
            ("juridica", "Jurídica"),
        ],
        string="Tipo de Persona",
        default="individual",
        required=True,
    )

    talla = fields.Selection(
        [
            ("s", "S"),
            ("m", "M"),
            ("l", "L"),
            ("xl", "XL"),
            ("xxl", "XXL"),
            ("xxxl", "XXXL"),
        ],
        string="Talla",
        default="s",
    )

    canal_distribucion = fields.Selection(
        [
            ("sectores_metropolitanos", "Sectores Metropolitanos"),
            ("sectores_departamentales", "Sectores Departamentales"),
            ("tiendas_barrio", "Tiendas de Barrio"),
            ("tiendas_conveniencia", "Tiendas de Conveniencia"),
            ("suscripciones", "Suscripciones"),
            ("suscripciones_cortesia", "Suscripciones de Cortesia"),
            ("agencias_publicidad", "Agencias de Publicidad"),
            ("oficinas_zona_12", "Oficinas Zona 12"),
            ("envios_usa", "Envios a USA"),
            ("otros", "Otros"),
        ],
        string="Canales de Distribución*",
        required=True,
    )

    canal_facturacion = fields.Selection(
        [
            ("sectores_metropolitanos", "Sectores Metropolitanos"),
            ("sectores_departamentales", "Sectores Departamentales"),
            ("tiendas_barrio", "Tiendas de Barrio"),
            ("tiendas_conveniencia", "Tiendas de Conveniencia"),
            ("suscripciones", "Suscripciones"),
            ("suscripciones_cortesia", "Suscripciones de Cortesia"),
            ("agencias_publicidad", "Agencias de Publicidad"),
            ("oficinas_zona_12", "Oficinas Zona 12"),
            ("envios_usa", "Envios a USA"),
            ("otros", "Otros"),
        ],
        string="Canales de Facturación*",
        required=True,
    )

    estado = fields.Selection(
        [
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo"),
        ],
        string="Estado*",
        default="Activo",
        required=True,
    )

    facturar_pedidos = fields.Selection(
        [
            ("si", "Si"),
            ("no", "No"),
        ],
        string="Facturar Pedidos*",
        default="si",
        required=True,
    )

    @api.depends("canal_distribucion")
    def _compute_precio_dias(self):
        for record in self:
            if record.canal_distribucion == "sectores_metropolitanos":
                record.precio_unidad = 1.66
                record.dias_validos_devolucion = 5
            elif record.canal_distribucion == "sectores_departamentales":
                record.precio_unidad = 1.71
                record.dias_validos_devolucion = 3
            else:
                record.precio_unidad = 0
                record.dias_validos_devolucion = 0

    def _inverse_dias_validos_devolucion(self):
        pass

    #Validadores de inputs

    @api.constrains("nit")
    def _check_nit(self):
        regex = re.compile('^[0-9]+$|C/F$')
        for dev in self:
            if not regex.match(dev.nit):
                raise ValidationError('Nit Invalido')


    # @api.constrains("dias_validos_devolucion")
    # def _check_dias_validos_devolucion(self):
    #     regex = re.compile('^[0-9]+$|C/F$')
    #     for dev in self:
    #         if not regex.match(dev.dias_validos_devolucion):
    #             raise ValidationError('')            
     


class Country(models.Model):
    _name = "circulacion.country"
    name = fields.Char(string="Country Name")


class State(models.Model):
    _name = "circulacion.state"
    name = fields.Char(string="State Name")
    country_id = fields.Many2one("circulacion.country", string="Country")
    municipio = fields.One2many("circulacion.city", inverse_name="state_id", string="Municipios")

class City(models.Model):
    _name = "circulacion.city"
    name = fields.Char(string="City Name")
    state_id = fields.Many2one("circulacion.state", string="State")
    precio_unidad = fields.Float(string="Precio por Unidad", default=0)
    ruta_id = fields.Many2one("circulacion.ruta", string="Ruta")


class Ruta(models.Model):
    _name = "circulacion.ruta"
    name = fields.Char(string="Sector *")
    state_id = fields.Many2one("circulacion.state", string="Departamento")
    city_id = fields.Many2one("circulacion.city", string="Municipio")
    cliente_id = fields.Many2one("circulacion.cliente", string="Cliente")
    lugar = fields.Char(string="Pueblo/Aldea/Lugar Poblado")
    porcentaje = fields.Float(string="Porcentaje *")
    

    @api.onchange("state_id")
    def _onchange_state_id(self):
        self.city_id = False
        return {"domain": {"city_id": [("state_id", "=", self.state_id.id)]}}



# Empresa
class Empresa(models.Model):
    _name = "circulacion.empresa"
    _description = "Informacion sobre Empresa"
    
    name = fields.Char(string="Nombre *", required=True)
    representante = fields.Char(string="Representante Legal *", required=True)
    nit = fields.Char(string="NIT *", required=True, default="C/F")
    direccion = fields.Char(string="Dirección")
    face = fields.Char(string="FACE Empresa *", required=True, default="ND")
    css = fields.Selection(
        [
            ("azul", "Azul"),
            ("verde", "Verde"),
            ("celeste", "Celeste"),
            ("naranja", "Naranja"),
            ("rojo", "Rojo"),

        ],
        string="CSS Class",
        default="azul",
    )
    logo = fields.Binary(string="Logo")
    invoice = fields.Selection(
        [
            ("unificado", "Unificado"),
            ("detallado", "Detallado"),
        ],
        string="Invoice Option",
        default="unificado",
    )
    estado = fields.Selection(
        [
            ("activo", "Activo"),
            ("inactivo", "Inactivo"),
        ],
        string="Estado*",
        default="activo",
        required=True,
    )


# Publicación
class Publicacion(models.Model):
    _name = "circulacion.publicacion"
    name = fields.Char(string="Nombre de la Publicación")
    empresa_id = fields.Many2one("circulacion.empresa", string="Empresa")


# Tipo de Publicación
class TipoPublicacion(models.Model):
    _name = "circulacion.tipopublicacion"
    name = fields.Char(string="Tipo de Publicación")
    publicacion_id = fields.Many2one("circulacion.publicacion", string="Publicación")


# Tipo de Portada
class TipoPortada(models.Model):
    _name = "circulacion.tipoportada"
    name = fields.Char(string="Tipo de Portada")
    publicacion_id = fields.Many2one("circulacion.publicacion", string="Publicación")


class sector(models.Model):
    _name = "circulacion.sector"
    _description = "circulacion.sector"

    name = fields.Char(string="Nombre del Sector*", required=True, default="Dirección")
    calle_avenida = fields.Char(string="Calle o Avenida*", required=True, default="N/A")
    no_casa = fields.Char(string="No. de Casa*", required=True, default="N/A")
    no_apartamento = fields.Char(
        string="No. de Apartamento*", required=True, default="N/A"
    )
    zona = fields.Char(string="Zona*", required=True, default="N/A")
    colonia_barrio_aldea = fields.Char(
        string="Colonia, Barrio o Aldea*", required=True, default="N/A"
    )
    cliente = fields.Many2one("circulacion.cliente")
    # id_cliente = fields.Integer(
    #     string="ID del Cliente", compute="_compute_cliente_id", readonly=True
    # )
    cliente_info = fields.Char(
        string="Información del Cliente", compute="_compute_cliente_info"
    )

    orden_ruta = fields.Integer(default=1, string="Orden de la Ruta*", required=True)
    tipo_direccion = fields.Selection(
        [
            ("entrega", "Entrega"),
            ("facturacion", "Facturación"),
            ("ambas", "Ambas"),
        ],
        string="Tipo de Direccion*",
        default="ambas",
        required=True,
    )

    # Configuracion
    tasa_devolucion = fields.Integer(string="Tasa de Devolución *", required=True)
    dias_valido_devolucion = fields.Integer(
        string="Días Válidos para Devolución *", required=True
    )
    cantidad_pedido_ordinario = fields.Integer(
        string="Cantidad de Pedido Ordinario *", required=True
    )
    cantidad_flete = fields.Integer(string="Cantidad de Flete *", required=True)
    cantidad_promocion = fields.Integer(string="Cantidad de Promoción *", required=True)
    supervisor = fields.Many2one("circulacion.supervisor")
    transportista = fields.Many2one("circulacion.transportista")
    cobrador = fields.Many2one("circulacion.cobrador", required=True)

    # Campos para Paises
    country_id = fields.Many2one("circulacion.country", string="Pais*", required=True)
    state_id = fields.Many2one(
        "circulacion.state", string="Departamento*", required=True
    )
    city_id = fields.Many2one("circulacion.city", string="Municipio*", required=True)
    ruta = fields.Many2one("circulacion.ruta", string="Ruta*", required=True)

    # publicacion
    empresa_id = fields.Many2one("circulacion.empresa", string="Empresa")
    publicacion_id = fields.Many2one("circulacion.publicacion", string="Publicación")
    tipo_publicacion_id = fields.Many2one(
        "circulacion.tipopublicacion", string="Tipo de Publicación"
    )
    tipo_portada_id = fields.Many2one(
        "circulacion.tipoportada", string="Tipo de Portada"
    )
    asesor = fields.Many2one("circulacion.asesor")
    no_voceadores = fields.Integer(string="No. de Voceadores")
    anotaciones = fields.Text(string="Anotaciones")
    estado = fields.Char(
        compute="_compute_estado_cliente",
        store=True,
        string="Estado",
    )

    # @api.depends("cliente")
    # def _compute_cliente_id(self):
    #     for record in self:
    #         record.id_cliente = record.cliente.id if record.cliente else False

    @api.depends("cliente")
    def _compute_estado_cliente(self):
        for record in self:
            if record.cliente:
                record.estado = record.cliente.estado
            else:
                record.cliente_info = ""

    @api.depends("cliente")
    def _compute_cliente_info(self):
        for record in self:
            if record.cliente:
                record.cliente_info = "{} {} (ID: {})".format(
                    record.cliente.name, record.cliente.apellido, record.cliente.id
                )
            else:
                record.cliente_info = ""

    @api.onchange("country_id")
    def _onchange_country_id(self):
        self.state_id = False
        self.city_id = False
        return {"domain": {"state_id": [("country_id", "=", self.country_id.id)]}}

    @api.onchange("state_id")
    def _onchange_state_id(self):
        self.city_id = False
        return {"domain": {"city_id": [("state_id", "=", self.state_id.id)]}}

    @api.onchange("city_id")
    def _onchange_city_id(self):
        self.ruta = False
        return {"domain": {"ruta": [("city_id", "=", self.city_id.id)]}}


    @api.onchange("empresa_id")
    def _onchange_empresa_id(self):
        self.publicacion_id = False
        self.tipo_publicacion_id = False
        self.tipo_portada_id = False
        return {
            "domain": {
                "publicacion_id": [
                    (
                        "empresa_id",
                        "=",
                        self.empresa_id.id if self.empresa_id else False,
                    )
                ]
            }
        }

    @api.onchange("publicacion_id")
    def _onchange_publicacion_id(self):
        self.tipo_publicacion_id = False
        self.tipo_portada_id = False
        return {
            "domain": {
                "tipo_publicacion_id": [
                    (
                        "publicacion_id",
                        "=",
                        self.publicacion_id.id if self.publicacion_id else False,
                    )
                ]
            }
        }

    @api.onchange("tipo_publicacion_id")
    def _onchange_tipo_publicacion_id(self):
        self.tipo_portada_id = False
        return {
            "domain": {
                "tipo_portada_id": [
                    (
                        "publicacion_id",
                        "=",
                        self.publicacion_id.id if self.publicacion_id else False,
                    )
                ]
            }
        }


class asesor(models.Model):
    _name = "circulacion.asesor"
    _description = "circulacion.asesor"

    name = fields.Char(string="Nombre")


class supervisor(models.Model):
    _name = "circulacion.supervisor"
    _description = "circulacion.supervisor"

    name = fields.Char(string="Nombre")


class transportista(models.Model):
    _name = "circulacion.transportista"
    _description = "circulacion.transportista"

    name = fields.Char(string="Nombre")


class cobrador(models.Model):
    _name = "circulacion.cobrador"
    _description = "circulacion.cobrador"

    name = fields.Char(string="Nombre")


class bancos(models.Model):
    _name = "circulacion.bancos"
    _description = "circulacion.bancos"

    name = fields.Char(string="Nombre*", required=True)
    url = fields.Char(string="URL*", required=True)
    telefono = fields.Char(string="Télefonos*", required=True)
    contactos = fields.Char(string="Contactos*", required=True)
    siglascodigo = fields.Char(string="Siglas/Código*", required=True)
    oebs = fields.Char(string="OEBS Método de Pago*", required=True)
    estado = fields.Selection(
        [
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo"),
        ],
        string="Estado*",
        default="Activo",
        required=True,
    )


class cuenta_banco(models.Model):
    _name = "circulacion.cuenta_banco"
    _description = "Cuenta de Banco"

    name = fields.Char(string="Nombre *", required=True)
    @api.model
    def _get_empresas_selection(self):
        empresas = self.env['circulacion.empresa'].search([])
        return [(str(empresa.id), empresa.name) for empresa in empresas]
    empresa_selection = fields.Selection(selection='_get_empresas_selection', string="Empresa")
    @api.model
    def _get_bancos_selection(self):
        banco = self.env['circulacion.bancos'].search([])
        return [(str(bancos.id), bancos.name) for bancos in banco]
    banco_selection = fields.Selection(selection='_get_bancos_selection', string="Banco", required=True)
    no_cuenta = fields.Char(string="No. de Cuenta *", required=True)
    moneda = fields.Selection(
        [
            ("quetzal", "Quetzal"),
            ("dollar", "Dollar"),
            ("euro", "Euro"),
        ],
        string="Moneda *",
        default="quetzal",
        required=True,
    )
    desde = fields.Date(string="Desde *", required=True)
    saldo = fields.Float(string="Saldo *", required=True)
    debito = fields.Float(string="Débitos *", required=True)
    credito = fields.Float(string="Créditos *", required=True)
    exportar = fields.Boolean(string="Exportar *", required=True)
    oebs_no_cuenta = fields.Char(string="OEBS No. de Cuenta")
    estado = fields.Selection(
        [
            ("activo", "Activo"),
            ("inactivo", "Inactivo"),
        ],
        string="Estado*",
        default="activo",
        required=True,
    )

   
class canal_distribucion(models.Model):
    _name = "circulacion.canal_distribucion"
    _description = "Canal de Distribución"

    name = fields.Char(string="Tipo de Canal de Distribución *", required=True, default="Normal") 
    nombre = fields.Char(string="Nombre *", required=True) 
    descripcion = fields.Text(string="Descripción *", required=True) 
    persona_individual = fields.Boolean(string="Persona Individual *") 
    dias_validos_devolucion = fields.Integer(string="Días Válidos de Devolución *", required=True) 
    serie = fields.Char(string="Serie") 
    no_factura = fields.Integer(string="No. de Factura *", required=True, default=0) 
    precio_unidad = fields.Float(string="Precio por Unidad *", required=True, default=0) 
    porcentaje_devolucion = fields.Float(string="Porcentaje de Devolución *", required=True, default=0)
    face_establecimiento =  fields.Char(string="FACE Establecimiento *", required=True, default="Z1")
    face_negocio =  fields.Char(string="FACE Negocio *", required=True, default="SECTOR")
      

 