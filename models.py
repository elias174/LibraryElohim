#!/usr/bin/env python
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)

session = Session()

Cliente = Table('Cliente', metadata,
                    Column('id_cliente', Integer, Sequence('some_id_seq', start=1, increment=1),primary_key=True),
                    Column('nombre', String(40), nullable=False),
                    Column('apellido', String(40), nullable=False),
                    Column('direccion', String(60)),
                    Column('fecha_nacimiento', Date),
                    Column('telefono', Integer),
                    )

Factura = Table('Factura', metadata,
                    Column('num_factura', Integer, primary_key=True),
                    Column('id_cliente',Integer, ForeignKey('Cliente.id_cliente')),
                    Column('fecha', DateTime, nullable=False),
                    )

Categoria = Table('Categoria', metadata,
                    Column('id_categoria', Integer, primary_key=True, autoincrement=True),
                    Column('nombre', String(40), nullable=False),
                    Column('descripcion', String(60)),
                    )

Producto=Table('Producto', metadata,
                    Column('id_producto', Integer, primary_key=True, autoincrement=True),
                    Column('id_categoria', Integer, ForeignKey('Categoria.id_categoria')),
                    Column('nombre',String(40), nullable=False),
                    Column('precio_compra',Numeric(15,2)),
                    Column('precio_venta',Numeric(15,2), nullable=False),
                    Column('stock', Integer, nullable=False),
                    Column('detalle',String(80)),
                    )

Detalle = Table('Detalle', metadata,
                    Column('num_detalle', Integer, primary_key=True),
                    Column('id_factura',Integer, ForeignKey('Factura.num_factura')),
                    Column('id_producto', Integer, ForeignKey('Producto.id_producto')),
                    Column('cantidad', Integer, nullable=False),
                    Column('precio_total', Numeric(15,2), nullable=False),
                    )

Gasto = Table('Gasto', metadata,
                Column('id_gasto', Integer, primary_key=True, autoincrement=True),
                Column('detalle', String(80)),
                Column('monto', Numeric(15,2), nullable=False),
                )

Caja = Table('Caja', metadata,
                Column('id_caja', Integer, primary_key=True, autoincrement=True),
                Column('saldo_anterior', Numeric(15,2), nullable=False),
                Column('ingresos', Numeric(15,2), nullable=False),
                Column('egresos', Numeric(15,2), nullable=False),
                Column('saldo_actual', Numeric(15,2), nullable=False),
                Column('fecha', Date, nullable=False)
                )

metadata.create_all()

''' Creacion de las relacion y modelos''' 

class Cliente(Base):
    __tablename__       = 'Cliente'
    id_cliente          = Column(Integer, Sequence('some_id_seq', start=1, increment=1), primary_key=True)
    nombre              = Column(String(40), nullable=False)
    apellido            = Column(String(40), nullable=False)
    direccion           = Column(String(60))
    fecha_nacimiento    = Column(Date)
    telefono            = Column(Integer)

    def __init__(self, nombre, apellido, direccion, fecha_nacimiento, telefono):
        self.nombre             = nombre    
        self.apellido           = apellido
        self.direccion          = direccion
        self.fecha_nacimiento   = fecha_nacimiento
        self.telefono           = telefono

class Factura(Base):
    __tablename__   = 'Factura'
    num_factura     = Column(Integer, primary_key=True)
    id_cliente      = Column(Integer, ForeignKey('Cliente.id_cliente'))
    fecha           = Column(DateTime, nullable=False)

    def __init__(self, num_factura, id_cliente, fecha):
        self.num_factura    = num_factura
        self.id_cliente     = id_cliente
        self.fecha          = fecha

class Categoria(Base):
    __tablename__   = 'Categoria'
    id_categoria    = Column(Integer, primary_key=True, autoincrement=True)
    nombre          = Column(String(40), nullable=False)
    descripcion     = Column(String(60))

    def __init__(self, nombre, descripcion):
        self.nombre         = nombre
        self.descripcion    =  descripcion


class Producto(Base):
    __tablename__   = 'Producto'
    id_producto     = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria    = Column(Integer, ForeignKey('Categoria.id_categoria'))
    nombre          = Column(String(40), nullable=False)
    precio_compra   = Column(Numeric(15,2))
    precio_venta    = Column(Numeric(15,2), nullable=False)
    stock           = Column(Integer, nullable=False)
    detalle         = Column(String(80))

    def __init__(self, id_producto, id_categoria, nombre, precio_compra, precio_venta, stock, detalle):
        self.id_producto    = id_producto
        self.id_categoria   = id_categoria
        self.nombre         = nombre
        self.precio_compra  = precio_compra
        self.precio_venta   = precio_venta
        self.stock          = stock
        self.detalle        = detalle

class Detalle(Base):
    __tablename__   = 'Detalle'
    num_detalle     = Column(Integer, primary_key=True)
    id_factura      = Column(Integer, ForeignKey('Factura.num_factura'))
    id_producto     = Column(Integer, ForeignKey('Producto.id_producto'))
    cantidad        = Column(Integer, nullable=False)
    precio_total    = Column(Numeric(15,2), nullable=False)

    def __init__(self, num_detalle, id_factura, id_producto, cantidad, precio_total):
        self.num_detalle    = num_detalle
        self.id_factura     = id_factura
        self.id_producto    = id_producto
        self.cantidad       = cantidad
        self.precio_total   = precio_total


class Gatos(Base):
    __tablename__   = 'Gasto'
    id_gasto        = Column(Integer, primary_key=True, autoincrement=True)
    detalle         = Column(String(80))
    monto           = Column(Numeric(15,2), nullable=False)

    def __init__(self, detalle, monto):
        self.detalle    = detalle
        self.monto      = monto


class Caja(Base):
    __tablename__   = 'Caja'
    id_caja         = Column(Integer, primary_key=True, autoincrement=True)
    saldo_anterior  = Column(Numeric(15,2), nullable=False)
    ingresos        = Column(Numeric(15,2), nullable=False)
    egresos         = Column(Numeric(15,2), nullable=False)
    saldo_actual    = Column(Numeric(15,2), nullable=False)
    fecha           = Column(Date, nullable=False)

    def __init__(self, saldo_anterior, ingresos, egresos, saldo_actual, fecha):
        self.saldo_anterior     = saldo_anterior
        self.ingresos           = ingresos
        self.egresos            = egresos
        self.saldo_actual       = saldo_actual
        self.fecha              = fecha