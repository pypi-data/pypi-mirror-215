import os
from pathlib import Path
import pandas as pd
from fpdf import FPDF
import glob


def generate(invoices_path, pdfs_path, image_path, product_id="product_id",
             product_name="product_name", amount_purchased="amount_purchased",
             price_per_unit="price_per_unit", total_price="total_price"):
    """
    Generates invoices in pdf from Excel files using fpdf and pandas
    :param invoices_path: Invoices directory
    :type invoices_path: str
    :param pdfs_path: Directory for the PDFs
    :type pdfs_path: str
    :param image_path: Path of the image for the logo
    :type image_path: str
    :param product_id: Name of the ID column in the Excel file
    :type product_id: str
    :param product_name: Name of the product name column in the Excel file
    :type product_name: str
    :param amount_purchased: Name of the amount purchased column in the Excel file
    :type amount_purchased: str
    :param price_per_unit: Name of the price per unit column in the Excel file
    :type price_per_unit: str
    :param total_price: Name of the total price column in the Excel file
    :type total_price: str
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font("Times", "B", 16)
        pdf.cell(w=50, h=8, txt="Invoice no. " + invoice_nr, ln=1)

        pdf.set_font("Times", "B", 16)
        pdf.cell(w=50, h=8, txt=f"Data: {date}", ln=1)
        pdf.ln(3)

        # Pandas need openpyxl library to read xlsx files
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        columns = list(df.columns)
        columns = [column.replace("_", " ").title() for column in columns]

        pdf.set_font("Times", "B", 10)
        # pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=60, h=8, txt=columns[1], border=1)
        pdf.cell(w=40, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        for index, row in df.iterrows():

            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=60, h=8, txt=row[product_name], border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df[total_price].sum()

        pdf.set_font("Times", "B", 10)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=60, h=8, txt="", border=1)
        pdf.cell(w=40, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        pdf.set_font("Times", "B", 10)
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        pdf.set_font("Times", "B", 12)
        pdf.cell(w=30, h=8, txt=f"ShadyCompany")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")


if __name__ == "__main__":
    generate("../invoices", "PDF", "logo.png")
