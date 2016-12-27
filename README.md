# Sistema Facturacion

Simple Software to manage sales and services payments

## Getting Started

Please before to develop install this requisites
### Prerequisites

You can install the packages with the tool pip

```
pyqt4, sqlalchemy, PIL, escpos
```
How orm we use sqlalchemy
Escpos is the interface for use a ticket printer Epson (but the magic is in PIL)

### Configuring the project

Before to develop please set in config.py the interface for the printer:

Ex:

```
PRINTER = Usb(0x04b8, 0x0e15)
```

If we dont have a printer, use the flag no print as True:

```
NO_PRINT = True
```
