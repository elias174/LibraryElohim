#!/usr/bin/env python
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from config import ALCHEMY_BASE, ALCHEMY_METADATA, ALCHEMY_SESSION

Base = ALCHEMY_BASE
metadata = ALCHEMY_METADATA
session = ALCHEMY_SESSION


Cliente = Table('Cliente', metadata,
                Column('id', Integer, Sequence('some_id_seq', start=1,
                                               increment=1), primary_key=True),
                Column('nombre', String(40), nullable=False),
                Column('apellido', String(40), nullable=False),
                Column('direccion', String(60)),
                Column('fecha_nacimiento', Date),
                )

Factura = Table('Factura', metadata,
                Column('id', Integer, primary_key=True, unique=True),
                Column('cliente', Integer, ForeignKey('Cliente.id')),
                Column('fecha', DateTime, nullable=False),
                )

Categoria = Table('Categoria', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('nombre', String(40), nullable=False),
                  Column('descripcion', String(60)),
                  )

TipoServicio = Table('TipoServicio', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('nombre', String(40), nullable=False),
                     Column('descripcion', String(60)),
                     )

Producto = Table('Producto', metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('categoria', Integer, ForeignKey('Categoria.id')),
                 Column('nombre', String(60), nullable=False),
                 Column('precio_compra', Numeric(15, 2)),
                 Column('precio_venta', Numeric(15, 2), nullable=False),
                 Column('stock', Integer, nullable=False),
                 Column('detalle', Text(80)),
                 )

Detalle = Table('Detalle', metadata,
                Column('id', Integer, primary_key=True),
                Column('factura', Integer, ForeignKey('Factura.id')),
                Column('producto', Integer, ForeignKey('Producto.id'),
                       nullable=True),
                Column('servicio', Integer, ForeignKey('Servicio.id'),
                       nullable=True),
                Column('cantidad', Integer, nullable=False),
                Column('precio_total', Numeric(15, 2), nullable=False),
                )

Servicio = Table('Servicio', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('tipo', Integer, ForeignKey('TipoServicio.id')),
                 Column('cancelado', Boolean, default=False, nullable=False),
                 Column('monto', Numeric(15, 2), nullable=False),
                 )

Gasto = Table('Gasto', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('detalle', String(80)),
              Column('monto', Numeric(15, 2), nullable=False),
              Column('fecha', Date, nullable=False)
              )

Caja = Table('Caja', metadata,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('saldo_anterior', Numeric(15, 2), nullable=False),
             Column('ingresos', Numeric(15, 2), nullable=False),
             Column('egresos', Numeric(15, 2), nullable=False),
             Column('saldo_actual', Numeric(15, 2), nullable=False),
             Column('fecha', Date, nullable=False)
             )

Ingreso = Table('Ingreso', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('detalle', String(80)),
              Column('monto', Numeric(15, 2), nullable=False),
              Column('fecha', Date, nullable=False)
              )

metadata.create_all()

''' Creacion de las relacion y modelos''' 


class Cliente(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, Sequence('some_id_seq', start=1, increment=1),
                primary_key=True)
    nombre = Column(String(40), nullable=False)
    apellido = Column(String(40), nullable=False)
    direccion = Column(String(60))
    fecha_nacimiento = Column(Date)

    def __init__(self, nombre, apellido, direccion, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.fecha_nacimiento = fecha_nacimiento


class Factura(Base):
    __tablename__ = 'Factura'
    id = Column(Integer, primary_key=True, unique=True)
    cliente = Column(Integer, ForeignKey('Cliente.id'))
    fecha = Column(DateTime, nullable=False)

    def __init__(self, cliente, fecha):
        self.cliente = cliente
        self.fecha = fecha


class Categoria(Base):
    __tablename__ = 'Categoria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(40), nullable=False)
    descripcion = Column(String(60))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


class TipoServicio(Base):
    __tablename__ = 'TipoServicio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(40), nullable=False)
    descripcion = Column(String(60))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


class Producto(Base):
    __tablename__ = 'Producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(Integer, ForeignKey('Categoria.id'))
    nombre = Column(String(40), nullable=False)
    precio_compra = Column(Numeric(15, 2))
    precio_venta = Column(Numeric(15, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    detalle = Column(String(80))

    def __init__(self, categoria, nombre, precio_compra, precio_venta, stock, detalle):
        self.categoria = categoria
        self.nombre = nombre
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.detalle = detalle


class Detalle(Base):
    __tablename__ = 'Detalle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    factura = Column(Integer, ForeignKey('Factura.id'))
    producto = Column(Integer, ForeignKey('Producto.id'), nullable=True)
    servicio = Column(Integer, ForeignKey('Servicio.id'), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Numeric(15, 2), nullable=False)

    def __init__(self, id_factura, cantidad, precio_total,
                 producto=None, servicio=None):
        self.factura = id_factura
        self.producto = producto
        self.servicio = servicio
        self.cantidad = cantidad
        self.precio_total = precio_total


class Servicio(Base):
    __tablename__ = 'Servicio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Integer, ForeignKey('TipoServicio.id'))
    cancelado = Column(Boolean, default=False, nullable=False)
    monto = Column(Numeric(15, 2), nullable=False)

    def __init__(self, tipo, cancelado, monto):
        self.tipo = tipo
        self.cancelado = cancelado
        self.monto = monto


class Gasto(Base):
    __tablename__ = 'Gasto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    detalle = Column(String(80))
    monto = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)

    def __init__(self, detalle, monto, fecha):
        self.detalle = detalle
        self.monto = monto
        self.fecha = fecha


class Caja(Base):
    __tablename__ = 'Caja'
    id = Column(Integer, primary_key=True, autoincrement=True)
    saldo_anterior = Column(Numeric(15, 2), nullable=False)
    ingresos = Column(Numeric(15, 2), nullable=False)
    egresos = Column(Numeric(15, 2), nullable=False)
    saldo_actual = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)

    def __init__(self, saldo_anterior, ingresos, egresos, saldo_actual, fecha):
        self.saldo_anterior = saldo_anterior
        self.ingresos = ingresos
        self.egresos = egresos
        self.saldo_actual = saldo_actual
        self.fecha = fecha


class Ingreso(Base):
    __tablename__ = 'Ingreso'
    id = Column(Integer, primary_key=True, autoincrement=True)
    detalle = Column(String(80))
    monto = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)

    def __init__(self, detalle, monto, fecha):
        self.detalle = detalle
        self.monto = monto
        self.fecha = fecha