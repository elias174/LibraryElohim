from escpos.printer import Serial
from escpos.printer import Usb


# You need use the correct interface
PRINTER = Usb(0x04b8, 0x0e15)
NO_PRINT = False
# PRINTER = Serial('COM1')
