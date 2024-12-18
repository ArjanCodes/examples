from weasyprint import CSS, HTML


def generate_pdf(
    html_string: str,
    output: str,
    company_logo: str = None,
) -> None:
    # Read the contents of the template file
    with open("app/static/pdf_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders with the actual values
    html_content = template.format(html_string=html_string, company_logo=company_logo)

    # Generate the PDF using WeasyPrint
    html = HTML(string=html_content)
    html.write_pdf(output, stylesheets=[CSS(filename="app/static/pdf_template.css")])
