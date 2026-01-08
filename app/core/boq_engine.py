from app.schemas.boq import BOQLineItem, BOQResult


def calculate_mirrored_cupboard(component, rates: dict) -> BOQResult:
    """
    Deterministic BOQ calculation for mirrored cupboard.
    No DB access. Pure function.
    """

    width = component.dimensions["width"]
    height = component.dimensions["height"]
    area = width * height

    items = []

    # 1. BWP Plywood
    plywood_rate = rates.get("BWP Plywood")
    if plywood_rate is None:
        raise ValueError("Rate not found for BWP Plywood")

    items.append(
        BOQLineItem(
            description="BWP Plywood Storage",
            quantity=area,
            unit="sqft",
            rate=plywood_rate,
            amount=area * plywood_rate
        )
    )

    # 2. Mirror Finish
    mirror_rate = rates.get("Mirror Finish")
    if mirror_rate is None:
        raise ValueError("Rate not found for Mirror Finish")

    items.append(
        BOQLineItem(
            description="Mirror Finish Panel",
            quantity=area,
            unit="sqft",
            rate=mirror_rate,
            amount=area * mirror_rate
        )
    )

    # 3. Carpentry Labor
    labor_rate = rates.get("Carpentry Labor")
    if labor_rate is None:
        raise ValueError("Rate not found for Carpentry Labor")

    items.append(
        BOQLineItem(
            description="Carpentry Labor",
            quantity=area,
            unit="sqft",
            rate=labor_rate,
            amount=area * labor_rate
        )
    )

    subtotal = sum(item.amount for item in items)

    return BOQResult(
        items=items,
        subtotal=subtotal
    )
