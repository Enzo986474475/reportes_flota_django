import pandas as pd
from pathlib import Path


def limpiar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def leer_hoja_flota(base_dir: Path) -> pd.DataFrame:
    archivo = base_dir / "data" / "Control-de-Flota-Vehicular-Tecsur 12.xlsx"

    df = pd.read_excel(
        archivo,
        sheet_name="Flota",
        header=7,   # fila 8 en Excel
    )

    # cortar desde columna C en adelante
    df = df.iloc[:, 2:].copy()

    df = limpiar_columnas(df)
    return df


def leer_hoja_flota_maestro(base_dir: Path) -> pd.DataFrame:
    archivo = base_dir / "data" / "Control-de-Flota-Vehicular-Tecsur 12.xlsx"

    df = pd.read_excel(
        archivo,
        sheet_name="Flota_Maestro",
        header=4,   # fila 5 en Excel
    )

    # cortar desde columna C en adelante
    df = df.iloc[:, 2:].copy()

    df = limpiar_columnas(df)
    return df