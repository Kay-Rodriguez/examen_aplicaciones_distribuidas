import sys
from collections import defaultdict


videos = defaultdict(
    lambda: {
        "view": 0,
        "like": 0,
        "comment": 0,
        "shared": 0
    }
)

usuarios = defaultdict(int)
horas = defaultdict(int)


def cargar_datos() -> None:
    for linea in sys.stdin:
        linea = linea.strip()

        if not linea:
            continue

        try:
            clave, valor = linea.split("\t", 1)
            cantidad = int(valor)
        except ValueError:
            print(
                f"Registro invalido: {linea}",
                file=sys.stderr
            )
            continue

        partes = clave.split("|")
        tipo = partes[0]

        if tipo == "VIDEO" and len(partes) == 3:
            video = partes[1]
            accion = partes[2]

            if accion in videos[video]:
                videos[video][accion] += cantidad

        elif tipo == "USUARIO" and len(partes) == 2:
            usuario = partes[1]
            usuarios[usuario] += cantidad

        elif tipo == "HORA" and len(partes) == 2:
            hora = partes[1]
            horas[hora] += cantidad


def obtener_maximos(diccionario):
    if not diccionario:
        return ["Sin datos"], 0

    mayor_valor = max(diccionario.values())

    elementos = sorted(
        clave
        for clave, valor in diccionario.items()
        if valor == mayor_valor
    )

    return elementos, mayor_valor


def formatear_lista(elementos):
    return ", ".join(elementos)


def generar_resultados() -> None:
    if not videos:
        print("No se procesaron datos.")
        print("Verifique entrada.txt, mapper.py y salida_shuffle.txt.")
        return

    vistas = {
        video: datos["view"]
        for video, datos in videos.items()
    }

    likes = {
        video: datos["like"]
        for video, datos in videos.items()
    }

    comentarios = {
        video: datos["comment"]
        for video, datos in videos.items()
    }

    videos_mas_vistos, total_vistas = obtener_maximos(vistas)
    videos_mas_likes, total_likes = obtener_maximos(likes)
    videos_mas_comentados, total_comentarios = obtener_maximos(
        comentarios
    )

    usuarios_recurrentes, total_usuario = obtener_maximos(usuarios)
    horas_mayores, total_hora = obtener_maximos(horas)

    ratios = {}

    for video, datos in videos.items():
        vistas_video = datos["view"]

        interacciones = (
            datos["like"]
            + datos["comment"]
            + datos["shared"]
        )

        if vistas_video > 0:
            ratios[video] = interacciones / vistas_video

    videos_mayor_ratio, mayor_ratio = obtener_maximos(ratios)

    print("==================================================")
    print("       RESULTADOS FINALES MAPREDUCE")
    print("==================================================")
    print()

    print(
        f"Video mas visto: "
        f"{formatear_lista(videos_mas_vistos)} "
        f"con {int(total_vistas)} vistas"
    )

    print(
        f"Video con mas likes: "
        f"{formatear_lista(videos_mas_likes)} "
        f"con {int(total_likes)} likes"
    )

    print(
        f"Video mas comentado: "
        f"{formatear_lista(videos_mas_comentados)} "
        f"con {int(total_comentarios)} comentarios"
    )

    print(
        f"Usuario mas recurrente: "
        f"{formatear_lista(usuarios_recurrentes)} "
        f"con {int(total_usuario)} interacciones"
    )

    print(
        f"Hora con mayor interaccion: "
        f"{formatear_lista(horas_mayores)}:00 "
        f"con {int(total_hora)} interacciones"
    )

    print(
        f"Video con mayor ratio de interaccion: "
        f"{formatear_lista(videos_mayor_ratio)} "
        f"con ratio {mayor_ratio:.4f}"
    )

    print()
    print("Formula utilizada:")
    print("Ratio = (likes + comments + shares) / views")

    print()
    print("==================================================")
    print("              DETALLE POR VIDEO")
    print("==================================================")

    for video in sorted(
        videos.keys(),
        key=lambda valor: int(valor.replace("video", ""))
    ):
        datos = videos[video]

        vistas_video = datos["view"]

        interacciones = (
            datos["like"]
            + datos["comment"]
            + datos["shared"]
        )

        ratio = (
            interacciones / vistas_video
            if vistas_video > 0
            else 0
        )

        print(
            f"{video}: "
            f"views={datos['view']}, "
            f"likes={datos['like']}, "
            f"comments={datos['comment']}, "
            f"shares={datos['shared']}, "
            f"ratio={ratio:.4f}"
        )


def main() -> None:
    cargar_datos()
    generar_resultados()


if __name__ == "__main__":
    main()