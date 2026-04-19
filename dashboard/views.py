from django.shortcuts import render
from pathlib import Path

from .services.lectores_excel import leer_hoja_flota_maestro


def buscar_columna(df, candidatos):
    columnas_limpias = {str(col).strip().lower(): col for col in df.columns}

    for candidato in candidatos:
        clave = candidato.strip().lower()
        if clave in columnas_limpias:
            return columnas_limpias[clave]

    return None


def inicio(request):
    base_dir = Path(__file__).resolve().parent.parent

    df_flota_maestro = leer_hoja_flota_maestro(base_dir).copy()
    df_flota_maestro.columns = [str(col).strip() for col in df_flota_maestro.columns]

    total_vehiculos = len(df_flota_maestro)

    # Buscar columnas reales del Excel por nombre
    col_antiguamiento = buscar_columna(df_flota_maestro, ["Antiguamiento"])
    col_gestion_final = buscar_columna(df_flota_maestro, ["Gestión Final", "Gestion Final"])
    col_origen = buscar_columna(df_flota_maestro, ["Origen"])

    # KPI Antiguamiento
    if col_antiguamiento:
        antig_incumplimiento = (
            df_flota_maestro[col_antiguamiento]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("incumplimiento")
            .sum()
        )
    else:
        antig_incumplimiento = 0

    # Resumen por fuente
    if col_gestion_final:
        serie_gestion_final = (
            df_flota_maestro[col_gestion_final]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )
        placas_los_andes = (serie_gestion_final == "LOS ANDES").sum()
    else:
        placas_los_andes = 0

    if col_origen:
        serie_origen = (
            df_flota_maestro[col_origen]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )
        placas_operaciones = (serie_origen == "OPERACIONES").sum()
    else:
        placas_operaciones = 0

    total_reportado = placas_los_andes + placas_operaciones

    resumen_fuentes = [
        {"fuente": "Los Andes", "n_placas": int(placas_los_andes)},
        {"fuente": "Operaciones Tecsur", "n_placas": int(placas_operaciones)},
        {"fuente": "Total Reportado (sin depurar)", "n_placas": int(total_reportado)},
    ]

    contexto = {
        "total_vehiculos": int(total_vehiculos),
        "antig_incumplimiento": int(antig_incumplimiento),
        "resumen_fuentes": resumen_fuentes,
    }

    return render(request, "dashboard/inicio.html", contexto)