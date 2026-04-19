from django.shortcuts import render
import pandas as pd
from pathlib import Path

def inicio(request):
    base_dir = Path(__file__).resolve().parent.parent
    archivo_excel = base_dir / "data" / "Flota.xlsx"

    df = pd.read_excel(archivo_excel)

    columnas = df.columns.tolist()
    registros = df.head(20).to_dict(orient="records")

    total_vehiculos = len(df)

    if "Antiguamiento" in df.columns:
        antig_incumplimiento = (
            df["Antiguamiento"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("incumplimiento")
            .sum()
        )
    else:
        antig_incumplimiento = 0

    contexto = {
        "columnas": columnas,
        "registros": registros,
        "total_registros": len(df),
        "total_vehiculos": total_vehiculos,
        "antig_incumplimiento": antig_incumplimiento,
    }

    return render(request, "dashboard/inicio.html", contexto)