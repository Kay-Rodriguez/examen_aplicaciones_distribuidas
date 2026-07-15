#!/bin/sh

set -e

echo "=================================================="
echo "       INICIO DEL PROCESAMIENTO MAPREDUCE"
echo "=================================================="

echo ""
echo "1. Esperando que el endpoint /datos este disponible..."

INTENTO=1
MAX_INTENTOS=20

while [ "$INTENTO" -le "$MAX_INTENTOS" ]; do

    if wget -q -O entrada.txt http://nginx/datos; then

        if [ -s entrada.txt ]; then
            echo "Endpoint disponible."
            break
        fi
    fi

    echo "Intento $INTENTO de $MAX_INTENTOS: endpoint no disponible."
    sleep 3

    INTENTO=$((INTENTO + 1))
done

if [ ! -s entrada.txt ]; then
    echo "ERROR: No se pudieron descargar datos desde NGINX."
    exit 1
fi

TOTAL=$(wc -l < entrada.txt)
TOTAL=$(echo "$TOTAL" | tr -d ' ')

echo "Registros descargados: $TOTAL"

echo ""
echo "2. Dividiendo archivo de entrada..."

sh split_entrada.sh

echo ""
echo "3. Ejecutando fase MAP..."

rm -f salida_map.txt

for ARCHIVO in splits/parte_*; do
    echo "Procesando $ARCHIVO"

    python mapper.py \
        < "$ARCHIVO" \
        >> salida_map.txt
done

if [ ! -s salida_map.txt ]; then
    echo "ERROR: mapper.py no genero resultados."
    exit 1
fi

TOTAL_MAP=$(wc -l < salida_map.txt)
TOTAL_MAP=$(echo "$TOTAL_MAP" | tr -d ' ')

echo "Registros generados por MAP: $TOTAL_MAP"

echo ""
echo "4. Ejecutando fase SHUFFLE..."

sort salida_map.txt > salida_shuffle.txt

if [ ! -s salida_shuffle.txt ]; then
    echo "ERROR: no se genero salida_shuffle.txt."
    exit 1
fi

echo ""
echo "5. Ejecutando fase REDUCE..."

python reducer.py \
    < salida_shuffle.txt \
    > resultados_finales.txt

if [ ! -s resultados_finales.txt ]; then
    echo "ERROR: reducer.py no genero resultados."
    exit 1
fi

echo ""
echo "6. Resultados obtenidos:"

cat resultados_finales.txt

echo ""
echo "=================================================="
echo "       PROCESAMIENTO FINALIZADO CORRECTAMENTE"
echo "=================================================="