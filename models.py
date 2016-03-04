from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Cliente = Table('Cliente', metadata,
                    Column('id_cliente', Integer, primary_key=True, autoincrement=True),
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
                    Column('num_detalle', Integer, primary_key=True, autoincrement=True),
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

''' Creacion de las relacion ''' 

class Cliente(Base):
	__tablename__ = 'Cliente'
	id_cliente = Column(Integer, primary_key=True, autoincrement=True)

class Factura(Base):
	__tablename__ = 'Factura'
	num_factura = Column(Integer, primary_key=True)
	id_cliente = Column(Integer, ForeignKey('Cliente.id_cliente'))

class Categoria(Base):
    __tablename__ = 'Categoria'
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)

class Producto(Base):
    __tablename__ = 'Producto'
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria = Column(Integer, ForeignKey('Categoria.id_categoria'))

class Detalle(Base):
    __tablename__ = 'Detalle'
    num_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_factura = Column(Integer, ForeignKey('Factura.num_factura'))
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'))