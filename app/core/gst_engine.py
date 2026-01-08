def calculate_gst(amount: float, gst_type: str = "works_contract") -> float:
    if gst_type == "works_contract":
        return round(amount * 0.18, 2)

    raise ValueError("Unsupported GST type")
