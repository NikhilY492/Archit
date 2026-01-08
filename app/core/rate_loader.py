def load_rates(materials):
    """
    Convert MasterMaterial rows into a name → rate map.
    """
    return {
        material.name: float(material.base_rate)
        for material in materials
    }
