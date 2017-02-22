import sys
import stopit
import threading
import functools
import logging

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PyQt4 import QtCore
from serial.serialutil import SerialException

from config import PRINTER, NO_PRINT, TIME_OUT_PRINTER


class TimeOutPrinter(Exception):
    pass


def timeout(duration, default=None):
    def decorator(func):
        class InterruptableThread(threading.Thread):
            def __init__(self, args, kwargs):
                threading.Thread.__init__(self)
                self.args = args
                self.kwargs = kwargs
                self.result = default
                self.daemon = True

            def run(self):
                try:
                    self.result = func(*self.args, **self.kwargs)
                except Exception:
                    pass

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            it = InterruptableThread(args, kwargs)
            it.start()
            it.join(duration)
            if it.isAlive():
                raise TimeOutPrinter
            return it.result
        return wrap
    return decorator


@timeout(TIME_OUT_PRINTER)
def printer_render(context, color = "#000", bgcolor = "#FFF",
             fontfullpath=None, fontsize=19, leftpadding=3,
             rightpadding=3, width=575, img_default=None, no_print=NO_PRINT):

    # try:
    #     PRINTER.device.open()
    # except:
    #     raise TIME_OUT_PRINTER

    if img_default and not no_print:
        PRINTER.image(img_default)
        PRINTER.cut()
        return

    text_to_draw = [
        '---------------------',
        'TICKET ELOHIM',
        '---------------------',
        '\n',
        'Ticket Nro: %s' % str(context['factura'].id),
        'Fecha: %s' % context['factura'].fecha.strftime('%m/%d/%Y'),
        'Cliente: %s %s' % (str(context['client'].id), context['client'].nombre),
        '\n',
        'Detalles:',
        '\n',
    ]

    text_products_draw = [
        '-' * 81,
        'Nombre,Cant.,P.Unidad,P.Total',
        '-' * 81
    ]

    text_finished = [
        '-'*81,
        '\n',
        'TOTAL: %s' % str(context['price_total']),
        '\n'
    ]
    for detail in context['details']:
        cantidad = str(detail[0].cantidad)
        total = str(detail[0].precio_total)
        name = detail[1][0]
        p_unidad = detail[1][1]

        text_products_draw.append('%s,%s,%s,%s' % (
            name[:23] + (name[:23] and '..'), cantidad, p_unidad, total))

    font = (
        ImageFont.load_default() if fontfullpath is None else
        ImageFont.truetype(fontfullpath, fontsize)
    )

    line_height = int(round(float(font.getsize(text_to_draw[1])[1] * 0.9)))
    img_height = line_height * (
        len(text_to_draw) + len(text_products_draw) + len(text_finished) + 1)

    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)

    y = 0
    for line in text_to_draw:
        draw.text((leftpadding, y), line, color, font=font)
        y += line_height

    draw.text((leftpadding, y), text_products_draw[0], color, font=font)
    y += line_height

    headers = text_products_draw[1].split(',')
    draw.text((leftpadding, y), headers[0], color, font=font)
    draw.text((leftpadding + 300, y), headers[1], color, font=font)
    draw.text((leftpadding + 380, y), headers[2], color, font=font)
    draw.text((leftpadding + 490, y), headers[3], color, font=font)
    y += line_height

    draw.text((leftpadding, y), text_products_draw[2], color, font=font)
    y += line_height

    for line in text_products_draw[3:]:
        products = line.split(',')
        draw.text((leftpadding, y), products[0], color, font=font)
        draw.text((leftpadding + 300, y), products[1], color, font=font)
        draw.text((leftpadding + 380, y), products[2], color, font=font)
        draw.text((leftpadding + 490, y), products[3], color, font=font)
        y += line_height

    for line in text_finished:
        draw.text((leftpadding, y), line, color, font=font)
        y += line_height

    if no_print:
        img.show()
        return

    PRINTER.image(img)
    PRINTER.cut()

    return img


def flush_printer():
    PRINTER.device.flush()
    PRINTER.device.flushInput()
    PRINTER.device.flushOutput()