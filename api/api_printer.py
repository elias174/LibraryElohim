from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from config import PRINTER, NO_PRINT


def printer_render(context, color = "#000", bgcolor = "#FFF",
             fontfullpath=None, fontsize=19, leftpadding=3,
             rightpadding=3, width=575):

    text_to_draw = [
        '---------------------',
        'TICKET ELOHIM',
        '---------------------',
        '\n',
        'Ticket Nro: %s' % str(context['factura'].id),
        'Fecha: %s' % context['factura'].fecha.strftime('%m/%d/%Y'),
        'Cliente: %s %s' % (str(context['client'].id), context['client'].nombre),
        '\n',
        'Productos Comprados:',
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
        name = detail[1].nombre
        cantidad = str(detail[0].cantidad)
        p_unidad = str(detail[1].precio_venta)
        total = str(detail[0].precio_total)
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

    if NO_PRINT:
        img.show()
        return
    PRINTER.image(img)
    PRINTER.cut()
