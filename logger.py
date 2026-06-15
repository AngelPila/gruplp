from __future__ import annotations

from datetime import datetime
from pathlib import Path


def generar_log(tipo_analisis, nombre, tokens_encontrados, errores):
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
    archivo_log = logs_dir / f"{tipo_analisis}-{nombre}-{fecha_hora}.txt"

    with archivo_log.open("w", encoding="utf-8") as salida:
        salida.write(f"Análisis: {tipo_analisis}\n")
        salida.write(f"Autor: {nombre}\n")
        salida.write(f"Fecha: {fecha_hora}\n\n")

        salida.write("TOKENS RECONOCIDOS\n")
        salida.write("-" * 60 + "\n")
        if tokens_encontrados:
            for token in tokens_encontrados:
                salida.write(
                    f"[{token.type}] {repr(token.value)} | línea {token.lineno} | columna {token.lexpos}\n"
                )
        else:
            salida.write("Sin tokens reconocidos\n")

        salida.write("\nERRORES\n")
        salida.write("-" * 60 + "\n")
        if errores:
            for error in errores:
                salida.write(f"{error}\n")
        else:
            salida.write("Sin errores\n")

    return str(archivo_log)