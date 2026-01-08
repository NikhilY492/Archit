def generate_invoice(snapshot, milestone: str):
    rules = {
        "retainer": 30,
        "design_approval": 40,
        "final_handover": 30
    }

    if milestone not in rules:
        raise ValueError("Invalid milestone")

    percentage = rules[milestone]
    amount = round(snapshot.total * (percentage / 100), 2)

    return percentage, amount
MILESTONE_RULES = {
    "retainer": 30,
    "design_approval": 40,
    "final_handover": 30,
}


MILESTONE_SEQUENCE = [
    "retainer",
    "design_approval",
    "final_handover"
]

MILESTONE_RULES = {
    "retainer": 30,
    "design_approval": 40,
    "final_handover": 30,
}


def calculate_invoice_amount(total: float, milestone: str):
    if milestone not in MILESTONE_RULES:
        raise ValueError("Invalid milestone")

    percentage = MILESTONE_RULES[milestone]
    amount = round(total * (percentage / 100), 2)

    return percentage, amount
