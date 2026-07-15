#!/bin/sh

set -e

ARCHIVO_ENTRADA="entrada.txt"
CARPETA_SPLITS="splits"

if [ ! -s "$ARCHIVO_ENTRADA" ]; then
    echo "ERROR: entrada.txt no existe o esta vacio."
    exit 1
fi

rm -rf "$CARPETA_SPLITS"
mkdir -p "$CARPETA_SPLITS"

TOTAL_LINEAS=$(wc -l < "$ARCHIVO_ENTRADA")
TOTAL_LINEAS=$(echo "$TOTAL_LINEAS" | tr -d ' ')

LINEAS_POR_SPLIT=$(( (TOTAL_LINEAS + 1) / 2 ))

split \
    -l "$LINEAS_POR_SPLIT" \
    -d \
    -a 2 \
    "$ARCHIVO_ENTRADA" \
    "$CARPETA_SPLITS/parte_"

echo "Total de registros: $TOTAL_LINEAS"
echo "Lineas aproximadas por fragmento: $LINEAS_POR_SPLIT"

ls -l "$CARPETA_SPLITS"