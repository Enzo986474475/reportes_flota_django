from django.shortcuts import render
from pathlib import Path

from .services.lectores_excel import (
    leer_hoja_flota,
    leer_hoja_flota_maestro,
)


def inicio(request):
    base_dir = Path(__file__).resolve().parent.parent

    df_flota = leer_hoja_flota(base_dir)
    df_flota_maestro = leer_hoja_flota_maestro(base_dir)

    total_vehiculos = len(df_flota)

    if "Antiguamiento" in df_flota.columns:
        antig_incumplimiento = (
            df_flota["Antiguamiento"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("incumplimiento")
            .sum()
        )
    else:
        antig_incumplimiento = 0

    # Hoja Flota_Maestro leída desde columna C
    # Posiciones relativas:
    # E=2, G=4, H=5, L=9, P=13, Q=14, R=15, S=16, V=19, X=21, Y=22, Z=23, AG=30
    columnas_idx = [2, 5, 9, 13, 14, 15, 16, 19, 4, 21, 22, 23, 30]

    df_tabla = df_flota_maestro.iloc[:, columnas_idx].copy()

    df_tabla.columns = [
        "Placa Vehiculo",   # E
        "Tipo",             # H
        "Año",              # L
        "Propietario",      # P
        "Gestión Ope",      # Q
        "Gestión LA",       # R
        "Gestión Final",    # S
        "Antiguedad",       # V
        "Grupo",            # G
        "Clase",            # X
        "Antiguamiento",    # Y
        "Criterio de Ant.", # Z
        "Usuario Final",    # AG
    ]


    # resumen por fuente usando la columna Gestión Final
    if "Gestión Final" in df_tabla.columns:
        serie_gestion = df_tabla["Gestión Final"].astype(str).str.strip()

        placas_los_andes = serie_gestion.str.contains("los andes", case=False, na=False).sum()
        placas_operaciones = serie_gestion.str.contains("operaciones", case=False, na=False).sum()
    else:
        placas_los_andes = 0
        placas_operaciones = 0

    resumen_fuentes = [
        {"fuente": "Los Andes", "n_placas": int(placas_los_andes)},
        {"fuente": "Operaciones Tecsur", "n_placas": int(placas_operaciones)},
    ]

    contexto = {
        "total_vehiculos": total_vehiculos,
        "antig_incumplimiento": antig_incumplimiento,

        # nuevo cuadro resumen
        "resumen_fuentes": resumen_fuentes,

        # por si luego los usamos
        "columnas": df_tabla.columns.tolist(),
        "registros": df_tabla.head(20).to_dict(orient="records"),
        "total_registros": len(df_tabla),

        "total_registros_flota": len(df_flota),
        "total_registros_flota_maestro": len(df_flota_maestro),
    }



    return render(request, "dashboard/inicio.html", contexto)