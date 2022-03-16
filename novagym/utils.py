import datetime
import io
import os

import xlsxwriter
from backend.settings import MEDIA_ROOT, MEDIA_URL
from django.http.response import FileResponse
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from xhtml2pdf import context, pisa


def export_excel(columns, queryset, model_name):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    worksheet = workbook.add_worksheet('Data')
    row_num = 0
    columns = list(columns.keys())
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])
    for row in queryset:
        row_num += 1
        for col_num, col_data in enumerate(row):
            if isinstance(col_data, datetime.datetime):
                col_data = col_data.strftime("%m/%d/%Y")
            worksheet.write(row_num, col_num, col_data)
    workbook.close()
    output.seek(0)
    filename = 'reporte-{}-{}.{}'.format(model_name,
                                         str(timezone.now().astimezone()), 'xlsx')
    response = FileResponse(
        output,
        as_attachment=True,
        filename=filename
    )
    return response


def export_pdf(columns, queryset, model_name):
    output = io.BytesIO()
    filename = 'reporte-{}-{}.{}'.format(model_name,
                                         str(timezone.now().astimezone()), 'pdf')
    context = {'columns': columns, 'qs': queryset, 'model_name': model_name}
    template = get_template('export_records_pdf.html')
    html = template.render(context)
    pisa.CreatePDF(html, output)
    output.seek(0)
    response = FileResponse(
        output,
        as_attachment=True,
        filename=filename
    )
    return response


def pdf_orden(orden):
    sufix = str(timezone.now().astimezone().strftime('%d_%m_%Y_%H_%M_%S'))
    ruta = "{}/{}/{}_{}.pdf".format(MEDIA_ROOT, "ordenes",
                                    orden.codigo, sufix)
    ruta_media = "{}{}/{}_{}.pdf".format(MEDIA_URL,
                                         "ordenes", orden.codigo, sufix)
    result_file = open(ruta, "w+b")
    context = {'orden': orden}
    template = get_template('print_orders.html')
    html = template.render(context)
    pisa.CreatePDF(html, dest=result_file)
    result_file.close()
    orden.archivo_root = ruta
    orden.archivo = ruta_media
    orden.save()
    return ruta, ruta_media


def print_file(file_path):
    os.startfile(file_path, 'print')


def calculate_pages_to_render(context, page_obj):
    start_page = 1
    stop_page = context.max_pages_render
    half_pages = context.max_pages_render // 2
    if (page_obj.number - half_pages) > 0:
        start_page = page_obj.number - half_pages
    else:
        start_page = 1
        stop_page = context.max_pages_render + 1

    if (page_obj.number + half_pages) <= page_obj.paginator.num_pages:
        stop_page = page_obj.number + half_pages + 1
    else:
        stop_page = page_obj.paginator.num_pages + 1
    return [n for n in range(start_page, stop_page)]
