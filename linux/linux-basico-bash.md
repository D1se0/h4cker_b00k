---
icon: redhat
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Linux básico (BASH)

## FILTRADO CON `grep`

```bash
# -i: Ignorar mayúsculas/minúsculas
grep -i "flag" archivo.txt

# -v: INVERTIR match (todo EXCEPTO lo que buscas)
grep -v "DEBUG\|ERROR" log.txt  # Solo líneas SIN debug ni error

# -E: Expresiones regulares extendidas (¡PODER!)
grep -E "^[0-9]{3}-[a-z]{5}$" datos  # Patrón exacto

# -o: Solo el MATCH, no toda la línea
echo "mi flag es: flag{abc123}" | grep -o "flag{[^}]*}"
# Output: flag{abc123}

# -A N: Líneas DESPUÉS del match
# -B N: Líneas ANTES del match
# -C N: Líneas ALREDEDOR del match
grep -A2 -B1 "password" config.txt  # Pass + 1 línea antes + 2 después

# -r: Recursivo (buscar en directorios)
grep -r "SECRET_KEY" ./

# --color=always: Colores aunque uses pipe
grep --color=always "admin" access.log | less -R
```

## Procesamiento de Columnas - `awk`

Concepto clave: `$1, $2, $NF`

```bash
# Por defecto separa por espacios/tabs
echo "john doe 25 hacker" | awk '{print $1}'      # john
echo "john doe 25 hacker" | awk '{print $NF}'     # hacker (último campo)
echo "john doe 25 hacker" | awk '{print $(NF-1)}' # 25 (penúltimo)

# Cambiar separador con -F
echo "john,doe,25,hacker" | awk -F',' '{print $3}'

# Filtrar por condición
awk '$3 > 100 {print $1, $3}' datos.txt        # Si col3 > 100
awk '/error/ {print NR ": " $0}' log.txt       # NR = número de línea
awk 'length($0) > 80' archivo.txt              # Líneas largas (>80 chars)

# Ejemplo real CTF: Extraer hashes de un dump
cat dump.sql | awk -F"'" '/INSERT INTO users/ {print $4" - "$6}'
# Asume: INSERT INTO users VALUES ('id', 'hash', 'salt')
```

#### **Awk one-liners útiles:**

```bash
# Sumar columna
awk '{sum+=$3} END {print "Total:", sum}' datos.txt

# Contar líneas únicas en columna 2
awk '{print $2}' log.txt | sort | uniq -c

# Extraer entre dos patrones (como strings pero mejor)
awk '/BEGIN FLAG/,/END FLAG/' archivo.txt

# Promedio de columna
awk '{sum+=$1; count++} END {print "Avg:", sum/count}'

# Formatear output
awk '{printf "User: %-15s Score: %03d\n", $1, $2}' scores.txt
```

## Edición en Stream - `sed`

```bash
# s/old/new/g - Sustituir GLOBAL
sed 's/foo/bar/g' archivo.txt

# s/old/new/3 - Solo la 3ª ocurrencia
sed 's/:/|/3' data.txt  # Cambia el 3er : por |

# Usar diferentes delimitadores (útil con paths)
sed 's|/var/log|/tmp/log|g' config.txt

# Eliminar líneas
sed '/^#/d' script.sh           # Eliminar comentarios
sed '/^$/d' archivo.txt         # Eliminar líneas vacías
sed '1,5d' archivo.txt          # Eliminar líneas 1-5
sed '$d' archivo.txt            # Eliminar última línea

# Extraer líneas específicas
sed -n '10,20p' archivo.txt     # Solo líneas 10-20
sed -n '5p;10p;15p' archivo.txt # Solo líneas 5,10,15
```

Ediciones mas complejas.

```bash
# Añadir texto al inicio
sed 's/^/>> /' archivo.txt       # >> al inicio de cada línea
sed '1i\## HEADER ##' archivo.txt # Insertar en línea 1

# Añadir al final
sed 's/$/ <</' archivo.txt       # << al final
sed '$a\## FOOTER ##' archivo.txt # Añadir al final

# Editar IN PLACE (cuidado!)
sed -i.bak 's/old/new/g' archivo.txt  # Crea backup .bak
sed -i '' 's/old/new/g' archivo.txt   # Sin backup (peligro)

# Multiples operaciones
sed -e 's/foo/bar/g' -e '/test/d' -e '1,5s/^/# /' archivo.txt
```

## BUCLES `for`

```bash
# 1. Lista explícita
for target in 192.168.1.1 192.168.1.2 192.168.1.3; do
    ping -c1 $target && echo "$target está vivo"
done

# 2. Secuencia numérica
for port in {1..1000}; do
    timeout 0.5 bash -c "echo >/dev/tcp/10.0.0.1/$port" 2>/dev/null &&
    echo "Puerto $port abierto"
done

# 3. Con incremento
for i in {0..100..10}; do      # 0, 10, 20, ..., 100
    echo "Progreso: $i%"
done

# 4. Sobre resultados de comandos
for user in $(cat users.txt); do
    echo "Probando user: $user"
    # Comando de fuerza bruta aquí
done

# 5. Sobre archivos
for file in *.log *.txt; do
    [ -f "$file" ] || continue  # Si no es archivo, salta
    echo "Procesando: $file"
    grep -q "ERROR" "$file" && echo "  Tiene errores!"
done
```

## BUCLES `while`

```bash
# 1. Con condición numérica
counter=0
while [ $counter -lt 10 ]; do
    echo "Intento: $((counter+1))"
    ((counter++))
done

# 2. Leer archivo línea por línea (¡IMPORTANTE!)
while IFS= read -r line; do
    # IFS= preserva espacios/tabs
    # -r evita interpretar backslashes
    echo "Procesando: $line"
done < archivo.txt

# 3. Leer output de comando
grep "ERROR" log.txt | while read -r error_line; do
    echo "ALERTA: $error_line"
done

# 4. Hasta que algo exista
while [ ! -f /tmp/flag.txt ]; do
    echo "Esperando flag..."
    sleep 2
done
echo "¡Flag encontrado!"
```

#### **While infinitos útiles:**

```bash
# Monitoreo continuo
while true; do
    clear
    netstat -tulpn | grep -E ":(80|443|22)"
    sleep 5
done

# Hasta que respuesta sea correcta
while ! curl -s http://target.com/login | grep -q "Bienvenido"; do
    echo "Servidor no listo, reintentando..."
    sleep 3
done

# Con timeout
timeout=60
while [ $timeout -gt 0 ] && [ ! -f resultado.txt ]; do
    echo "Quedan $timeout segundos..."
    sleep 5
    ((timeout-=5))
done
```

### `until` - El Hermano de `while`

```bash
# until [ condición ]; do ... done
# Ejecuta MIENTRAS condición sea FALSA

# Esperar servicio
until nc -z localhost 3306; do
    echo "MySQL no responde, esperando..."
    sleep 2
done
echo "¡MySQL listo!"

# Hasta tener resultado
result=""
until [[ $result == *"flag{"* ]]; do
    result=$(curl -s http://ctf.com/challenge)
    echo "Intento: $result"
    sleep 1
done
```

## Tabular datos - `column`

```bash
# Formatear output como tabla
ps aux | head -10 | column -t

# Con delimitador específico
echo "user:pass:role
admin:1234:super
john:abcd:user" | column -s: -t
```

## Combinar líneas - `paste`

```bash
# Juntar archivos lado a lado
paste usuarios.txt passwords.txt

# Con delimitador
paste -d':' usuarios.txt passwords.txt > userpass.txt
```

## Preparar para impresión - `pr`

```bash
# Dividir en columnas
cat lista_larga.txt | pr -3 -t  # 3 columnas
```
