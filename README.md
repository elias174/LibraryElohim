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

### Configure MYSQL (MariaDB)
#### Windows
First download the next packages:

MariaDB 64 bits: https://downloads.mariadb.org/mariadb/10.1.21/
Download and install mysql drivers: 

First install C connector:
http://dev.mysql.com/downloads/file.php?id=378025

Now install the connector python
http://arquivos.victorjabur.com/python/modules/MySQL-python-1.2.3.win-amd64-py2.7.exe

#### Linux
Install all packages necessary for MariaDB or MySQL, and install the connector with
```
sudo apt-get install python-mysqldb

sudo apt-get install build-essential python-dev libmysqlclient-dev
```