import pandas as pd
from pathlib import Path


def limpiar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def normalizar_nombre_hoja(nombre: str) -> str:
    return str(nombre).strip().lower().replace(" ", "").replace("-", "_")


def leer_hoja_flota_maestro(base_dir: Path) -> pd.DataFrame:
    archivo = base_dir / "data" / "Control-de-Flota-Vehicular-Tecsur 12.xlsx"

    xls = pd.ExcelFile(archivo)
    hojas = xls.sheet_names

    hoja_objetivo = None
    for hoja in hojas:
        if normalizar_nombre_hoja(hoja) == "flota_maestro":
            hoja_objetivo = hoja
            break

    if hoja_objetivo is None:
        raise ValueError(f"No se encontró una hoja equivalente a 'Flota_Maestro'. Hojas disponibles: {hojas}")


    df = pd.read_excel(
        archivo,
        sheet_name=hoja_objetivo,
        header=4,
        engine="openpyxl",
        engine_kwargs={"data_only": True},
    )

    df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed", na=False)]
    df = df.iloc[:, 2:].copy()
    df = limpiar_columnas(df)

    return df