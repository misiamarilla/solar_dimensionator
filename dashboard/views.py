from django.shortcuts import render
from .logic.on_logic import dimensionar_on_grid
from .logic.off_logic import dimensionar_off_grid


COST_PANEL = 2200000
COST_INV = 900000
COST_BAT = 1200000
INSTALL_RATE = 0.18
TARIFA = 850


def dashboard(request):

    resultados = None
    tipo = None

    if request.method == "POST":

        tipo = request.POST.get("tipo")

        data = {
            "consumo_diario_kwh": request.POST.get("consumo"),
            "horas_sol_pico": request.POST.get("hsp"),
            "eficiencia_sistema": request.POST.get("pr"),
            "inversor_rendimiento": request.POST.get("inv"),
            "panel_watt": request.POST.get("panel"),
        }

        if tipo == "on":

            resultados = dimensionar_on_grid(
                data,
                COST_PANEL,
                COST_INV,
                INSTALL_RATE,
                TARIFA
            )

        if tipo == "off":

            data.update({
                "autonomia_dias": request.POST.get("autonomia"),
                "profundidad_descarga": request.POST.get("dod"),
                "tension_sistema": request.POST.get("tension"),
                "bateria_nominal_ah": request.POST.get("bat")
            })

            resultados = dimensionar_off_grid(
                data,
                COST_PANEL,
                COST_INV,
                COST_BAT,
                INSTALL_RATE
            )

    return render(request, "dashboard.html", {
        "resultados": resultados,
        "tipo": tipo
    })