import os

from fpdf import FPDF

import datetime

import contractInfo


def create_pdf(user_id, order_id, contract):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Contract", ln=True, align='C')
    pdf.ln(10)

    def add_text(label, value):
        pdf.cell(50, 10, txt=label, border=1)
        pdf.cell(150, 10, txt=str(value), border=1)
        pdf.ln(10)

    match contract:
        case contractInfo.IndividualContract():
            add_text("Full Name:", contract.full_name)
            add_text("Birthday:", contract.birthday.strftime("%Y-%m-%d") if isinstance(contract.birthday,
                                                                                       datetime.datetime) else contract.birthday)
            add_text("Passport Number:", contract.passport_number)
            add_text("Issued By:", contract.issued_by)
            add_text("Issuer Number:", contract.issued_by_number)
            add_text("Address:", contract.address)
        case contractInfo.CompanyContract():
            add_text("Full Name:", contract.full_name)
            add_text("Position:", contract.position)
            add_text("Taxpayer Number:", contract.taxpayer_number)

    file_path = os.path.join(os.getcwd(), "frontend/saves/saves/" + str(user_id) + "/" + str(order_id) + "/" + "contract.pdf")
    pdf.output(file_path)
