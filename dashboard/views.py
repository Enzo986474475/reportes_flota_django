from django.shortcuts import render
from pathlib import Path

from .services.lectores_excel import leer_hoja_flota_maestro


def inicio(request):
    base_dir = Path(__file__).resolve().parent.parent

    df_flota_maestro = leer_hoja_flota_maestro(base_dir)

    total_vehiculos = len(df_flota_maestro)

    # Posiciones relativas en Flota_Maestro leyendo desde columna C:
    # E=2, G=4, H=5, L=9, P=13, Q=14, R=15, S=16, V=19, X=21, Y=22, Z=23, AG=30
    columnas_idx = [2, 5, 9, 13, 14, 15, 16, 19, 4, 21, 22, 23, 30]

    df_tabla = df_flota_maestro.iloc[:, columnas_idx].copy()

    df_tabla.columns = [
        "Placa Vehiculo",
        "Tipo",
        "Año",
        "Propietario",
        "Gestión Ope",
        "Gestión LA",
        "Gestión Final",
        "Antiguedad",
        "Grupo",
        "Clase",
        "Antiguamiento",
        "Criterio de Ant.",
        "Usuario Final",
    ]

    print("COLUMNAS df_tabla:", df_tabla.columns.tolist())

    print("MUESTRA Gestión Ope:")
    print(df_tabla["Gestión Ope"].head(10).tolist())

    print("MUESTRA Gestión LA:")
    print(df_tabla["Gestión LA"].head(10).tolist())

    print("MUESTRA Gestión Final:")
    print(df_tabla["Gestión Final"].head(10).tolist())

    gestion_ope = df_tabla["Gestión Ope"].fillna("").astype(str).str.strip().str.upper()
    gestion_la = df_tabla["Gestión LA"].fillna("").astype(str).str.strip().str.upper()

    print("UNIQUE Gestión Ope:", gestion_ope.unique()[:20])
    print("UNIQUE Gestión LA:", gestion_la.unique()[:20])


    df_tabla = df_tabla.loc[:, ~df_tabla.columns.str.contains("Sin nombre", case=False, na=False)]



    for col in df_tabla.columns:
        if df_tabla[col].dtype == float:
            df_tabla[col] = df_tabla[col].fillna(0).astype(int)

    if "Antiguamiento" in df_tabla.columns:
        antig_incumplimiento = (
            df_tabla["Antiguamiento"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("incumplimiento")
            .sum()
        )
    else:
        antig_incumplimiento = 0



    if "Gestión Final" in df_tabla.columns:
        serie_gestion = (
            df_tabla["Gestión Final"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        placas_los_andes = (serie_gestion == "LOS ANDES").sum()
        placas_operaciones = (serie_gestion == "OPERACIONES").sum()
    else:
        placas_los_andes = 0
        placas_operaciones = 0

    total_reportado = placas_los_andes + placas_operaciones

    resumen_fuentes = [
        {"fuente": "Los Andes", "n_placas": int(placas_los_andes)},
        {"fuente": "Operaciones Tecsur", "n_placas": int(placas_operaciones)},
        {"fuente": "Total Reportado (sin depurar)", "n_placas": int(total_reportado)},
    ]

    contexto = {
        "total_vehiculos": total_vehiculos,
        "antig_incumplimiento": antig_incumplimiento,
        "resumen_fuentes": resumen_fuentes,
        "total_registros_flota_maestro": len(df_flota_maestro),
    }

    return render(request, "dashboard/inicio.html", contexto)