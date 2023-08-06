import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import os


def generate(invoices_path, pdfs_path, company_name, image_path, product_id,
             product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files into PDF invoices.
    :param invoices_path:
    :param pdfs_path:
    :param company_name:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f'{invoices_path}/*.xlsx')

    for filepath in filepaths:
        # Get the data
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Create the PDF
        pdf = FPDF(orientation='P', unit='mm', format='A4')

        # Set the page
        pdf.add_page()

        # Get the date and doc nr
        filename = Path(filepath).stem
        invoice_nr = filename.split('-')[0]
        date = filename.split('-')[1]

        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, ln=1, txt=f'Invoice nr.{invoice_nr}')

        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, ln=1, txt=f'Date: {date}')

        columns = list(df.columns)
        columns = [item.replace('_', ' ').title() for item in columns]

        # Add a header
        pdf.set_font(family='Times', size=10, style='B')
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], ln=1, border=1)

        # Add rows
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), ln=1, border=1)

        total_value = df['total_price'].sum()

        pdf.set_font(family='Times', size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=70, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt='', border=1)
        pdf.cell(w=30, h=8, txt=str(total_value), ln=1, border=1)

        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=30, h=8, txt=f'The total price is {total_value}', ln=1)

        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=25, h=8, txt=company_name)
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f'{pdfs_path}/{filename}.pdf')
