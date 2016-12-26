from escpos.printer import Serial
from escpos.printer import Usb

PRINTER = Usb(0x04b8, 0x0e15)
# PRINTER = Serial('COM1')
