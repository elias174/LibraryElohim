import sys

from config import (ALCHEMY_BASE, ALCHEMY_METADATA, ALCHEMY_SESSION, db)

Base = ALCHEMY_BASE
metadata = ALCHEMY_METADATA
session = ALCHEMY_SESSION

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(40), nullable=False)
    apellido = Column(String(40), nullable=False)
    dni = Column(String(60))

class Alumno(Base):

    GRADOS = [
        u'Primer Grado Primaria',
        u'Segundo Grado Primaria',
    ]

    __tablename__ = 'alumno'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    nombres = Column(String(60), nullable=False)
    apellidos = Column(String(60), nullable=False)
    grado = Column(String(100), nullable=False)
    dni = Column(String(60), nullable=True)

    @classmethod
    def get_grados(cls):
        return cls.GRADOS


class Servicio(Base):
    __tablename__ = 'servicio'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    alumno_id = Column(Integer, ForeignKey('alumno.id'))
    alumno = relationship(Alumno)
    tipo = Column(String(50))
    cancelado = Column(Boolean, default=False, nullable=False)
    monto = Column(Numeric(15, 2), nullable=False)
    informacion_extra = Column(String(250), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'servicio',
        'polymorphic_on':tipo
    }


class Matricula(Servicio):
    matricula_anio = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity':'matricula'
    }


class Mensualidad(Servicio):
    mensualidad_anio = Column(String(250))
    mensualidad_mes = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity':'mensualidad'
    }


class Detalle(Base):
    __tablename__ = 'detalle'

    id = Column(Integer, primary_key=True)
    factura = Column(Integer, ForeignKey('factura.id'))
    servicio = Column(Integer, ForeignKey('servicio.id'), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Numeric(15, 2), nullable=False)


class Factura(Base):
    __tablename__ = 'factura'
    id = Column(Integer, primary_key=True)
    cliente = Column(Integer, ForeignKey('alumno.id'))
    fecha = Column(Date, nullable=False)


class Caja(Base):
    __tablename__ = 'caja'
    id = Column(Integer, primary_key=True)
    saldo_anterior = Column(Numeric(15, 2), nullable=False)
    ingresos = Column(Numeric(15, 2), nullable=False)
    egresos = Column(Numeric(15, 2), nullable=False)
    saldo_actual = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)


class Ingreso(Base):
    __tablename__ = 'ingreso'
    id = Column(Integer, primary_key=True)
    detalle = Column(String(80))
    monto = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)


class Gasto(Base):
    __tablename__ = 'Gasto'
    id = Column(Integer, primary_key=True)
    detalle = Column(String(80))
    monto = Column(Numeric(15, 2), nullable=False)
    fecha = Column(Date, nullable=False)


if len(sys.argv) > 1:
    if sys.argv[1] == 'create':
        Base.metadata.create_all(db)
    elif sys.argv[1] == 'create-test-data':
        print 'creating'
        matricula = Matricula(
            monto=234.5,
            matricula_anio='2019',
            alumno_id=1,
        )
        session.add(matricula)
        session.commit()

        mensualidad = Mensualidad(
            monto=166.53,
            mensualidad_anio='2019',
            mensualidad_mes='Marzo',
            alumno_id=1,
        )
        session.add(mensualidad)
        session.commit()
