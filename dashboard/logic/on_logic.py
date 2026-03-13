import math

# ---------- UTILIDADES ----------
def f(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return float(d)

def ceil(x):
    return int(math.ceil(x))

def format_cop(valor):
    try:
        # redondea al entero más cercano y aplica separador de miles con punto
        return f"${round(valor):,}".replace(",", ".") + " COP"
    except Exception:
        return "$0 COP"


# ---------- DIMENSIONAMIENTO ON GRID ----------
def dimensionar_on_grid(p, COST_PANEL_COP_PER_KWP, COST_INV_COP_PER_KW, INSTALL_RATE, TARIFA_PROMEDIO_COP_PER_KWH):
    consumo = f(p["consumo_diario_kwh"])
    hsp = f(p["horas_sol_pico"])
    pr = f(p["eficiencia_sistema"])
    inv_eff = f(p["inversor_rendimiento"])

    if consumo <= 0:
        raise ValueError("El consumo diario debe ser mayor que cero")
    if hsp <= 0:
        raise ValueError("Las horas sol pico deben ser mayores que cero")
    if not (0.6 <= pr <= 0.9):
        raise ValueError("El PR debe estar entre 0.6 y 0.9")
    if not (0.9 <= inv_eff <= 0.98):
        raise ValueError("La eficiencia del inversor debe estar entre 0.9 y 0.98")

    potencia_kwp = consumo / (hsp * pr)
    produccion_mensual = potencia_kwp * hsp * 30 * inv_eff

    panel_w = f(p["panel_watt"])
    if panel_w <= 0:
        raise ValueError("La potencia del panel debe ser mayor que cero")
    num_paneles = ceil((potencia_kwp * 1000) / panel_w)

    inversor_kw = ceil(potencia_kwp * 1.25)

    costo_paneles = potencia_kwp * COST_PANEL_COP_PER_KWP
    costo_inversor = inversor_kw * COST_INV_COP_PER_KW
    total = round((costo_paneles + costo_inversor) * (1 + INSTALL_RATE))

    factor_autoconsumo = 0.7
    ahorro_mensual = round(produccion_mensual * factor_autoconsumo * TARIFA_PROMEDIO_COP_PER_KWH)
    retorno_anios = round(total / (ahorro_mensual * 12), 2) if ahorro_mensual > 0 else 0

    return {
        "potencia_instalada_kwp": round(potencia_kwp, 2),
        "produccion_mensual_kwh": round(produccion_mensual, 1),
        "num_paneles": num_paneles,
        "potencia_inversor_kw": inversor_kw,
        "num_baterias": 0,
        "total_estimado_COP": format_cop(total),
        "ahorro_mensual_COP": format_cop(ahorro_mensual),
        "retorno_inversion_anios": retorno_anios,
    }