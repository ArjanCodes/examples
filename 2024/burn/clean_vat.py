def clean_vat_id(vat_id: str, country: str) -> str:
    # remove spaces
    vat_id = vat_id.replace(" ", "")

    # if the VAT ID has no numbers, it's invalid
    if not any(char.isdigit() for char in vat_id):
        raise ValueError("VAT ID must contain at least one number.")

    # add country code to VAT ID if it's not there
    if not vat_id.startswith(country):
        return f"{country.upper()}{vat_id}"

    return vat_id
