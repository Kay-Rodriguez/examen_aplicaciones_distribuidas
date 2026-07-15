import sys
from datetime import datetime


ACCIONES_VALIDAS = {"view", "like", "comment", "shared"}


def procesar_linea(linea: str) -> None:
    linea = linea.strip()

    if not linea:
        return

    partes = [parte.strip() for parte in linea.split(",")]

    if len(partes) != 5:
        print(
            f"Linea invalida: {linea}",
            file=sys.stderr
        )
        return

    usuario, accion, fecha, hora, video = partes

    if accion not in ACCIONES_VALIDAS:
        print(
            f"Accion invalida: {accion}",
            file=sys.stderr
        )
        return

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        hora_objeto = datetime.strptime(hora, "%H:%M:%S")
    except ValueError:
        print(
            f"Fecha u hora invalida: {linea}",
            file=sys.stderr
        )
        return

    hora_interaccion = hora_objeto.strftime("%H")

    # Datos para calcular acciones por video.
    print(f"VIDEO|{video}|{accion}\t1")

    # Datos para calcular el usuario más recurrente.
    print(f"USUARIO|{usuario}\t1")

    # Datos para calcular la hora con más interacción.
    print(f"HORA|{hora_interaccion}\t1")


def main() -> None:
    for linea in sys.stdin:
        procesar_linea(linea)


if __name__ == "__main__":
    main()