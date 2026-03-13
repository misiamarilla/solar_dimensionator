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
        return f"${int(valor):,}".replace(",", ".") + " COP"
    except Exception:
        return "$0 COP"

# ---------- DIMENSIONAMIENTO OFF GRID ----------
def dimensionar_off_grid(p, COST_PANEL_COP_PER_KWP, COST_INV_COP_PER_KW, COST_BAT_COP_PER_UNIT, INSTALL_RATE):
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
    panel_w = f(p["panel_watt"])
    if panel_w <= 0:
        raise ValueError("La potencia del panel debe ser mayor que cero")
    num_paneles = ceil((potencia_kwp * 1000) / panel_w)

    inversor_kw = ceil(potencia_kwp * 1.25)

    autonomia = f(p["autonomia_dias"])
    dod = f(p["profundidad_descarga"])
    tension = f(p["tension_sistema"])
    bat_ah = f(p["bateria_nominal_ah"])

    if autonomia <= 0:
        raise ValueError("La autonomía debe ser mayor que cero")
    if not (0.3 <= dod <= 0.8):
        raise ValueError("El DoD debe estar entre 0.3 y 0.8")
    if tension <= 0:
        raise ValueError("La tensión del sistema debe ser mayor que cero")
    if bat_ah <= 0:
        raise ValueError("La capacidad de la batería debe ser mayor que cero")

    eta_bateria = 0.9
    energia_bateria_wh = consumo * 1000 * autonomia / (dod * inv_eff * eta_bateria)
    capacidad_total_ah = energia_bateria_wh / tension
    num_baterias = ceil(capacidad_total_ah / bat_ah)

    costo_paneles = potencia_kwp * COST_PANEL_COP_PER_KWP
    costo_inversor = inversor_kw * COST_INV_COP_PER_KW
    costo_baterias = num_baterias * COST_BAT_COP_PER_UNIT
    total = round((costo_paneles + costo_inversor + costo_baterias) * (1 + INSTALL_RATE))

    return {
        "potencia_instalada_kwp": round(potencia_kwp, 2),
        "produccion_mensual_kwh": round(potencia_kwp * hsp * 30 * inv_eff, 1),
        "num_paneles": num_paneles,
        "potencia_inversor_kw": inversor_kw,
        "num_baterias": num_baterias,
        "total_estimado_COP": format_cop(total),
        "ahorro_mensual_COP": format_cop(0),
        "retorno_inversion_anios": "N/A",
    }