from escpos.printer import Serial

printer = Serial('COM1')


def print_ticket(file):
    instance_file = open(file, 'r')
    ticket = instance_file.read()
    printer.text(ticket)
    printer.cut()
