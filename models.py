from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

db = create_engine('sqlite:///dataBase.db', echo = True)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

Cliente = Table('Cliente', metadata,
                    Column('id_cliente', Integer, primary_key=True),
                    Column('nombre', String(40)),
                    Column('apellido', String(40)),
                    Column('direccion', String(60)),
                    Column('fecha_nacimiento', Date),
                    Column('telefono', Integer),
                    )

Factura = Table('Factura', metadata,
                    Column('num_factura', Integer, primary_key=True),
                    Column('id_cliente',Integer, ForeignKey('Cliente.id_cliente')),
                    Column('fecha', DateTime),
                    )

Categoria = Table('Categoria', metadata,
                    Column('id_categoria', Integer, primary_key=True),
                    Column('nombre', String(40)),
                    Column('descripcion', String(60)),
                    )

Producto=Table('Producto', metadata,
                    Column('id_producto', Integer, primary_key=True),
                    Column('id_categoria', Integer, ForeignKey('Categoria.id_categoria')),
                    Column('nombre',String(40)),
                    Column('precio_compra',Numeric(15,2)),
                    Column('precio_venta',Numeric(15,2)),
                    Column('stock', Integer),
                    Column('detalle',String(80)),
                    )

Detalle = Table('Detalle', metadata,
                    Column('num_detalle', Integer, primary_key=True),
                    Column('id_factura',Integer, ForeignKey('Factura.num_factura')),
                    Column('id_producto', Integer, ForeignKey('Producto.id_producto')),
                    Column('cantidad', Integer),
                    Column('precio_total', Numeric(15,2)),
                    )


Gasto = Table('Gasto', metadata,
                Column('id_gasto', Integer, primary_key=True),
                Column('detalle', String(80)),
                Column('monto', Numeric(15,2)),
                )

Caja = Table('Caja', metadata,
                Column('id_caja', Integer, primary_key=True),
                Column('saldo_anterior', Numeric(15,2)),
                Column('ingresos', Numeric(15,2)),
                Column('egresos', Numeric(15,2)),
                Column('saldo_actual', Numeric(15,2)),
                Column('fecha', Date)
                )