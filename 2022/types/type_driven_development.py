def is_eligible_for_bonus(contracts_landed: int, hours_worked: int, is_family: bool):
    if is_family:
        return True
    if contracts_landed > 0 and hours_worked > 40:
        return True
