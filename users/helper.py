
from django.http import HttpResponse
from django.template.loader import get_template

from django.template.loader import render_to_string

import os
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO

from .models import CustomerUser,Product,Order
from datetime import datetime
from random import randrange
def download_invoice(request,id):

    logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo.jpg')
    order=Order.objects.get(id=id)
    print(order)
    products=order.order_items.all()
    print(products)
    context = {
        'company_name': 'USMA Enterprise',
        'mobile_number': '+91-92000178381',
        'website': 'https://usma.in',
        'tagline': 'Har Ghar Ki Pasand',
        'logo_path': logo_path,
        'products':products,
        'order':order,
        'today':datetime.now(),
        'invoice_no':"USMABILL"+str(randrange(111111,999999))

    }


    html_content = render_to_string('data.html', context)

    # Convert the HTML content to a PDF
    pdf_file = convert_html_to_pdf(html_content)

    # If the PDF was successfully generated, return it as a response
    if pdf_file:
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="report.pdf"'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)

def generate_invoice(request):

    logo_path = os.path.join(settings.BASE_DIR, 'static/img/logo.jpg')
    users = CustomerUser.objects.filter()
    context = {
        'company_name': 'USMA Enterprise',
        'mobile_number': '+91-92000178381',
        'website': 'https://usma.in',
        'tagline': 'Har Ghar Ki Pasand',
        'logo_path': logo_path,
        'users': users,
    }


    html_content = render_to_string('invoice.html', context)

    # Convert the HTML content to a PDF
    pdf_file = convert_html_to_pdf(html_content)

    # If the PDF was successfully generated, return it as a response
    if pdf_file:
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="report.pdf"'
        return response
    else:
        return HttpResponse('Error generating PDF', status=500)

def convert_html_to_pdf(source_html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(source_html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None