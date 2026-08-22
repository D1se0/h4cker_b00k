#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 PJL-TOOLKIT — Cliente de auditoria para impresoras via Printer Job Language
================================================================================

Autor:      (tu nombre / handle aqui antes de subirlo a GitHub)
Licencia:   MIT (o la que prefieras)
Proposito:  Herramienta educativa y de pentesting para auditar impresoras de
            red (protocolo RAW / JetDirect, puerto TCP 9100) que exponen el
            lenguaje PJL (Printer Job Language). Permite reconocimiento
            pasivo, enumeracion de sistema de ficheros interno, lectura y
            escritura de ficheros, y consulta de variables de entorno.

AVISO LEGAL / SCOPE:
    Esta herramienta debe usarse EXCLUSIVAMENTE sobre dispositivos de tu
    propiedad o sobre los que tengas autorizacion explicita y por escrito
    para realizar pruebas de seguridad. El uso no autorizado de estas
    tecnicas contra sistemas de terceros puede constituir un delito segun
    la legislacion aplicable (en Espana, arts. 197 y 264 del Codigo Penal).

    El autor no se hace responsable del mal uso de este software.

------------------------------------------------------------------------------
QUE ES PJL (para quien llega nuevo al protocolo)
------------------------------------------------------------------------------
PJL (Printer Job Language) es un protocolo de control creado por HP en 1993
que viaja *dentro* del mismo flujo de datos que se envia a una impresora por
el puerto RAW/JetDirect (TCP 9100). No requiere autenticacion en la inmensa
mayoria de configuraciones por defecto: cualquiera que pueda alcanzar ese
puerto por red puede mandar comandos PJL.

Cada sesion PJL se abre y cierra con la secuencia UEL (Universal Exit
Language): el byte ESC (0x1B) seguido de "%-12345X". Esta secuencia le dice
al lenguaje de impresion activo en ese momento (PCL, PostScript...) "sal de
tu modo actual y entra en modo PJL". Por eso veras SIEMPRE este patron:

    UEL + "@PJL COMANDO ...\r\n" + UEL

Este script encapsula esa mecanica para que no tengas que escribirla a mano
cada vez, y ademas actua de "traductor": expones comandos tipo shell (ls,
cat, get, put, rm...) y el script se encarga de generar el PJL real
equivalente, imprimiendolo en pantalla para que aprendas la traduccion.

------------------------------------------------------------------------------
ARQUITECTURA DEL SCRIPT
------------------------------------------------------------------------------
    1. PJLTransport   -> maneja la conexion TCP cruda (socket), envio/recibo,
                          timeouts y reintentos. Es la unica clase que toca
                          la red directamente.
    2. PJLProtocol    -> construye las cadenas PJL correctas (el "diccionario"
                          del protocolo) y parsea las respuestas.
    3. PJLClient      -> API de alto nivel ("traductor"): metodos con nombres
                          humanos (ls, get_file, put_file, whoami...) que
                          internamente llaman a PJLProtocol + PJLTransport.
    4. PJLShell       -> interfaz interactiva tipo shell (REPL) que mapea
                          comandos escritos por el usuario a metodos de
                          PJLClient.
    5. CLI (main)     -> parseo de argumentos para uso no interactivo /
                          scriptable (automatizacion, integracion en otras
                          herramientas, CI de pentesting, etc.)

Cross-platform: unicamente usa la libreria estandar de Python 3 (socket,
argparse, logging, shlex, cmd, dataclasses...). Funciona igual en Windows,
Linux y macOS sin dependencias externas.
"""

from __future__ import annotations

import argparse
import cmd
import logging
import shlex
import socket
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Tuple


# ==============================================================================
# 1. CONFIGURACION Y CONSTANTES DEL PROTOCOLO
# ==============================================================================

# UEL (Universal Exit Language): ESC + "%-12345X"
# Es el "abrir y cerrar puertas" de PJL. Todo comando PJL real va envuelto
# entre dos UEL: el primero saca a la impresora de su lenguaje actual
# (PCL/PostScript) y la mete en modo PJL; el segundo cierra la sesion PJL
# de forma limpia para no dejar la impresora "colgada" esperando mas datos.
UEL = "\x1b%-12345X"

# Terminador de linea que PJL espera en cada comando.
EOL = "\r\n"

# Puerto RAW/JetDirect estandar en el que casi todas las impresoras de red
# (HP, Brother, Xerox, Lexmark, Kyocera...) escuchan PJL sin autenticacion.
DEFAULT_PORT = 9100

# Volumenes de sistema de ficheros habituales dentro del firmware de la
# impresora. "0:" suele ser RAM volatil, "1:" suele ser flash/NVRAM persistente.
# No todos los modelos exponen ambos, ni exponen filesystem en absoluto.
DEFAULT_VOLUME = "0:"

# Timeouts / reintentos configurables por CLI, con valores por defecto
# razonables para red local (LAN).
DEFAULT_TIMEOUT = 5.0
DEFAULT_RETRIES = 2

# Tamano de buffer de lectura por paquete TCP.
RECV_CHUNK = 4096

# Marcador que usamos para partir respuestas multi-linea de PJL, que no
# llevan ningun campo tipo "Content-Length" fiable: el propio protocolo
# es de texto plano sin delimitador estandarizado de fin de mensaje, asi
# que hay que basarse en timeouts cortos y en reconocer el eco del propio
# comando enviado.
PJL_ECHO_PREFIX = "@PJL"


def split_shell_args(arg: str) -> List[str]:
    """
    Divide una linea de argumentos del shell interactivo en tokens,
    preservando barras invertidas literales pero manteniendo el soporte
    de comillas para rutas con espacios.

    POR QUE NO SE USA shlex.split() A SECAS:
    shlex.split() en modo POSIX (el modo por defecto) trata la barra
    invertida '\\' como caracter de ESCAPE, igual que hace bash. Las
    rutas PJL usan '\\' como separador de directorio de forma constante
    (ej. "0:\\config\\network.cfg"), asi que shlex.split() se comia esas
    barras y las rutas llegaban corruptas a la impresora/honeypot
    (p.ej. "0:\\config\\network.cfg" se convertia en "0:confignetwork.cfg").

    Este helper usa shlex.shlex de mas bajo nivel con el atributo
    `escape` vaciado, para desactivar especificamente el tratamiento de
    '\\' como escape, sin perder el resto de comportamiento util de
    shlex (dividir por espacios respetando comillas para rutas con
    espacios en su interior).
    """
    lexer = shlex.shlex(arg, posix=True)
    lexer.whitespace_split = True
    lexer.escape = ""  # desactiva el tratamiento de '\' como caracter de escape
    return list(lexer)


# ==============================================================================
# 2. LOGGING
# ==============================================================================
# Usamos el modulo logging estandar en vez de "print" sueltos para poder:
#   - activar modo verbose/debug con -v en la CLI
#   - separar claramente los mensajes informativos de los datos exfiltrados
#   - redirigir facilmente a fichero si se usa en una campana de auditoria
logger = logging.getLogger("pjl_toolkit")


def setup_logging(verbose: bool = False) -> None:
    """Configura el logger global. Nivel DEBUG si verbose=True."""
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    fmt = "[%(asctime)s] %(levelname)-8s %(message)s"
    handler.setFormatter(logging.Formatter(fmt, datefmt="%H:%M:%S"))
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)


# ==============================================================================
# 3. EXCEPCIONES PROPIAS
# ==============================================================================
# Definir excepciones especificas (en vez de dejar que exploten OSError o
# socket.timeout genericos) hace que el codigo que llama a estas funciones
# pueda reaccionar de forma fina y dar mensajes claros al usuario final.

class PJLError(Exception):
    """Excepcion base de toda la herramienta."""


class PJLConnectionError(PJLError):
    """Fallo al establecer o mantener la conexion TCP con la impresora."""


class PJLTimeoutError(PJLError):
    """La impresora no respondio dentro del timeout configurado."""


class PJLProtocolError(PJLError):
    """La respuesta recibida no tiene el formato esperado por el protocolo."""


# ==============================================================================
# 4. CAPA DE TRANSPORTE (socket TCP puro, sin dependencias externas)
# ==============================================================================

class PJLTransport:
    """
    Maneja la conexion TCP cruda contra el puerto 9100 (o el que se indique).

    Se abre una conexion nueva por cada comando (en vez de mantener un socket
    persistente) porque muchas impresoras cierran la sesion tras cada
    intercambio PJL, y reabrir es mas robusto que gestionar reconexiones
    silenciosas a mitad de un comando.
    """

    def __init__(self, host: str, port: int = DEFAULT_PORT,
                 timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = max(0, retries)

    def send_receive(self, payload: str, expect_binary: bool = False,
                      read_timeout: Optional[float] = None) -> bytes:
        """
        Abre conexion, envia `payload` (ya construido en PJL) y lee la
        respuesta hasta que la impresora deja de mandar datos o se agota
        el timeout de lectura.

        Se reintenta `self.retries` veces ante errores de red transitorios
        (muy tipico en impresoras que tardan en despertar de bajo consumo).
        """
        last_exc: Optional[Exception] = None
        rt = read_timeout if read_timeout is not None else self.timeout

        for attempt in range(1, self.retries + 2):  # +1 intento inicial
            try:
                logger.debug(f"Conectando a {self.host}:{self.port} "
                             f"(intento {attempt}/{self.retries + 1})")
                with socket.create_connection(
                    (self.host, self.port), timeout=self.timeout
                ) as sock:
                    sock.settimeout(self.timeout)
                    # PJL es texto plano en latin-1/ascii extendido; usamos
                    # latin-1 porque preserva byte a byte (necesario cuando
                    # luego leemos binario, p.ej. al descargar un fichero).
                    sock.sendall(payload.encode("latin-1", errors="ignore"))
                    logger.debug(f"Payload enviado ({len(payload)} bytes)")

                    return self._read_response(sock, rt)

            except socket.timeout as exc:
                last_exc = exc
                logger.debug(f"Timeout en intento {attempt}: {exc}")
            except (ConnectionRefusedError, OSError) as exc:
                last_exc = exc
                logger.debug(f"Error de conexion en intento {attempt}: {exc}")

            if attempt <= self.retries:
                time.sleep(0.5)  # pequena espera antes de reintentar

        # Si llegamos aqui, todos los intentos fallaron.
        if isinstance(last_exc, socket.timeout):
            raise PJLTimeoutError(
                f"La impresora {self.host}:{self.port} no respondio a "
                f"tiempo tras {self.retries + 1} intento(s)."
            ) from last_exc
        raise PJLConnectionError(
            f"No se pudo conectar a {self.host}:{self.port} "
            f"tras {self.retries + 1} intento(s): {last_exc}"
        ) from last_exc

    @staticmethod
    def _read_response(sock: socket.socket, read_timeout: float) -> bytes:
        """
        Lee todo lo disponible en el socket hasta que:
          a) el peer cierra la conexion (recv devuelve b""), o
          b) pasa `read_timeout` segundos sin recibir mas datos nuevos.

        PJL no tiene un delimitador de "fin de mensaje" fiable en todas las
        implementaciones, asi que un timeout de silencio es el metodo mas
        portable entre fabricantes.
        """
        sock.settimeout(read_timeout)
        data = b""
        try:
            while True:
                chunk = sock.recv(RECV_CHUNK)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            # Es NORMAL llegar aqui: significa que la impresora ya mando
            # todo lo que tenia y simplemente se quedo en silencio.
            pass
        return data


# ==============================================================================
# 5. CAPA DE PROTOCOLO (construccion y parseo de comandos PJL)
# ==============================================================================

@dataclass
class DirEntry:
    """Representa una entrada devuelta por FSDIRLIST (fichero o directorio)."""
    name: str
    is_dir: bool
    size: Optional[int] = None
    raw_line: str = ""


class PJLProtocol:
    """
    Construye las cadenas PJL exactas para cada operacion y parsea las
    respuestas crudas a estructuras de datos utiles.

    Cada metodo `build_*` documenta en su docstring el comando PJL real
    que genera, para que sirva como referencia de aprendizaje del lenguaje.
    """

    # -- Comandos de identificacion / info -----------------------------------

    @staticmethod
    def build_info_id() -> str:
        """
        PJL real:  @PJL INFO ID

        Devuelve el nombre/modelo tal como lo reporta el firmware.
        Es de solo lectura, no modifica ningun estado -> seguro de ejecutar
        siempre como primer paso de reconocimiento.
        """
        return f'{UEL}@PJL INFO ID{EOL}{UEL}{EOL}'

    @staticmethod
    def build_info_status() -> str:
        """
        PJL real:  @PJL INFO STATUS

        Devuelve el estado operativo actual (idle, imprimiendo, error de
        papel, toner bajo, etc.) junto a un codigo numerico de estado.
        """
        return f'{UEL}@PJL INFO STATUS{EOL}{UEL}{EOL}'

    @staticmethod
    def build_info_variables() -> str:
        """
        PJL real:  @PJL INFO VARIABLES

        Vuelca todas las variables de entorno PJL configurables del
        dispositivo (idioma, bandeja por defecto, timeout de trabajo,
        modo duplex, densidad de tóner...). Es la version "env | sort"
        de una impresora.
        """
        return f'{UEL}@PJL INFO VARIABLES{EOL}{UEL}{EOL}'

    @staticmethod
    def build_info_filesys() -> str:
        """
        PJL real:  @PJL INFO FILESYS

        Pregunta que volumenes de sistema de ficheros expone el firmware
        (tipicamente 0:=RAM, 1:=FLASH/NVRAM, a veces 2:=tarjeta opcional).
        Es el paso previo obligado antes de intentar FSDIRLIST, porque si
        este comando no devuelve volumenes, el modelo probablemente no
        implementa filesystem PJL (muy comun en impresoras domesticas).
        """
        return f'{UEL}@PJL INFO FILESYS{EOL}{UEL}{EOL}'

    @staticmethod
    def build_ustatus_off() -> str:
        """
        PJL real:  @PJL USTATUSOFF

        Desactiva el envio de mensajes de estado asincronos no solicitados
        (unsolicited status). Util para "limpiar" el canal antes de leer
        una respuesta y evitar mezclar datos de distintos eventos.
        """
        return f'{UEL}@PJL USTATUSOFF{EOL}{UEL}{EOL}'

    @staticmethod
    def build_echo(text: str = "PJL-TOOLKIT-PING") -> str:
        """
        PJL real:  @PJL ECHO "texto"

        Pide a la impresora que repita el texto enviado. Sirve como "ping"
        de aplicacion: si el eco vuelve, confirmamos que el interprete PJL
        esta vivo y respondiendo, no solo que el puerto TCP esta abierto.
        """
        safe = text.replace('"', "'")
        return f'{UEL}@PJL ECHO "{safe}"{EOL}{UEL}{EOL}'

    # -- Comandos de sistema de ficheros --------------------------------------

    @staticmethod
    def build_fsdirlist(path: str, entry: int = 1, count: int = 999) -> str:
        """
        PJL real:  @PJL FSDIRLIST NAME="<path>" ENTRY=<n> COUNT=<n>

        Lista el contenido de un directorio del volumen indicado.
        ENTRY es el indice desde el que empezar a listar (para paginar
        directorios muy grandes) y COUNT cuantas entradas devolver como
        maximo por llamada.
        """
        return (f'{UEL}@PJL FSDIRLIST NAME="{path}" ENTRY={entry} '
                f'COUNT={count}{EOL}{UEL}{EOL}')

    @staticmethod
    def build_fsquery(path: str) -> str:
        """
        PJL real:  @PJL FSQUERY NAME="<path>"

        Consulta metadatos de un fichero o directorio concreto (si existe,
        tipo, tamano) sin descargar su contenido. Es el equivalente a un
        `stat` remoto.
        """
        return f'{UEL}@PJL FSQUERY NAME="{path}"{EOL}{UEL}{EOL}'

    @staticmethod
    def build_fsupload(path: str, offset: int = 0, size: int = 1_000_000) -> str:
        """
        PJL real:  @PJL FSUPLOAD NAME="<path>" OFFSET=<n> SIZE=<n>

        OJO CON EL NOMBRE: "UPLOAD" esta desde el punto de vista de la
        IMPRESORA (ella "sube" el fichero hacia nosotros), asi que en la
        practica esto es una DESCARGA para el atacante/auditor.
        OFFSET permite leer por trozos ficheros grandes que no caben en
        un unico recv(); SIZE es el numero maximo de bytes a leer desde
        ese offset.
        """
        return (f'{UEL}@PJL FSUPLOAD NAME="{path}" OFFSET={offset} '
                f'SIZE={size}{EOL}{UEL}{EOL}')

    @staticmethod
    def build_fsdownload(path: str, data: bytes) -> bytes:
        """
        PJL real:  @PJL FSDOWNLOAD FORMAT:BINARY SIZE=<n> NAME="<path>"
                   seguido de <n> bytes binarios crudos del propio fichero.

        Aqui "DOWNLOAD" es tambien desde el punto de vista de la impresora
        (ella "descarga" el fichero que nosotros le enviamos), asi que en
        la practica esto es una SUBIDA/ESCRITURA para el auditor.
        Devuelve bytes (no str) porque el payload final mezcla cabecera de
        texto + contenido binario arbitrario, y no se puede tratar todo
        como texto sin arriesgar corromper datos binarios.
        """
        header = f'{UEL}@PJL FSDOWNLOAD FORMAT:BINARY SIZE={len(data)} ' \
                 f'NAME="{path}"{EOL}'
        footer = f'{EOL}{UEL}{EOL}'
        return header.encode("latin-1") + data + footer.encode("latin-1")

    @staticmethod
    def build_fsdelete(path: str) -> str:
        """
        PJL real:  @PJL FSDELETE NAME="<path>"

        Borra un fichero o directorio (vacio) del volumen indicado.
        DESTRUCTIVO: usar con cuidado, sobre todo en firmware sin
        confirmacion adicional.
        """
        return f'{UEL}@PJL FSDELETE NAME="{path}"{EOL}{UEL}{EOL}'

    @staticmethod
    def build_fsmkdir(path: str) -> str:
        """
        PJL real:  @PJL FSMKDIR NAME="<path>"

        Crea un directorio nuevo en el volumen indicado.
        """
        return f'{UEL}@PJL FSMKDIR NAME="{path}"{EOL}{UEL}{EOL}'

    @staticmethod
    def build_fsinit(volume: str) -> str:
        """
        PJL real:  @PJL FSINIT VOLUME="<vol>"

        Formatea/inicializa un volumen del sistema de ficheros de la
        impresora. EXTREMADAMENTE DESTRUCTIVO (borra todo el volumen).
        Incluido solo con fines educativos; el shell interactivo pide
        confirmacion explicita antes de construir este comando.
        """
        return f'{UEL}@PJL FSINIT VOLUME="{volume}"{EOL}{UEL}{EOL}'

    # -- Variables de entorno / NVRAM -----------------------------------------

    @staticmethod
    def build_dinquire(variable: str) -> str:
        """
        PJL real:  @PJL DINQUIRE <VARIABLE>

        "Default INQUIRE": pregunta el valor por defecto (persistido en
        NVRAM) de una variable concreta, sin necesidad de listarlas todas
        con INFO VARIABLES. Util para sondear variables especificas del
        fabricante que no siempre aparecen en el volcado general.
        """
        return f'{UEL}@PJL DINQUIRE {variable}{EOL}{UEL}{EOL}'

    @staticmethod
    def build_set_variable(variable: str, value: str) -> str:
        """
        PJL real:  @PJL SET <VARIABLE>=<VALOR>

        Modifica una variable de entorno para el TRABAJO ACTUAL (no
        persistente salvo que se combine con DEFAULT, ver mas abajo).
        """
        return f'{UEL}@PJL SET {variable}={value}{EOL}{UEL}{EOL}'

    @staticmethod
    def build_default_variable(variable: str, value: str) -> str:
        """
        PJL real:  @PJL DEFAULT <VARIABLE>=<VALOR>

        Igual que SET, pero PERSISTE el cambio en NVRAM como nuevo valor
        por defecto de fabrica. Esto es lo que usan algunos ataques de
        "printer bricking" para dejar la impresora inutilizable, o para
        alterar configuracion de forma permanente -> tratar con maxima
        precaucion, solo en tu propio equipo y sabiendo revertirlo.
        """
        return f'{UEL}@PJL DEFAULT {variable}={value}{EOL}{UEL}{EOL}'

    @staticmethod
    def build_rdymsg(line1: str, line2: str = "") -> str:
        """
        PJL real:  @PJL RDYMSG DISPLAY="<texto>"

        Cambia el mensaje que se muestra en la pantalla LCD de la
        impresora en estado "ready". Es la clasica demo visual e
        inofensiva para confirmar en persona que tus comandos realmente
        estan llegando al dispositivo (low-risk, alta confirmacion visual).
        """
        text = (line1 + (" " + line2 if line2 else "")).replace('"', "'")
        return f'{UEL}@PJL RDYMSG DISPLAY="{text}"{EOL}{UEL}{EOL}'

    # -- Parsing de respuestas --------------------------------------------------

    @staticmethod
    def parse_dirlist(raw: str) -> List[DirEntry]:
        """
        Parsea la salida de texto de FSDIRLIST a una lista de DirEntry.

        IMPORTANTE: el formato de cada linea NO esta estandarizado entre
        implementaciones. Se han observado en la practica (y por tanto se
        soportan aqui) dos variantes:

          Variante A ("tipo primero", HP LaserJet clasicas, PRET, etc.):
              TYPE=DIR NAME=temp
              TYPE=FILE SIZE=1024 NAME=scan001.pdf

          Variante B ("nombre primero", vista p.ej. en el honeypot
          pjl-honeypot de michaelneu/pjl-honeypot):
              . TYPE=DIR
              .. TYPE=DIR
              scan001.pdf TYPE=FILE SIZE=1024

        Un parser que solo reconociera la variante A descartaria en
        silencio TODAS las entradas de un dispositivo que hable la
        variante B, haciendo parecer que el directorio esta vacio cuando
        en realidad no lo esta -> por eso se comprueban ambas.
        """
        entries: List[DirEntry] = []
        for raw_line in raw.splitlines():
            line = raw_line.strip()
            if not line or "TYPE=" not in line:
                continue

            is_dir = "TYPE=DIR" in line
            is_file = "TYPE=FILE" in line
            if not (is_dir or is_file):
                continue  # linea sin TYPE reconocible (cabecera/ruido)

            size = None
            if "SIZE=" in line:
                try:
                    size_str = line.split("SIZE=", 1)[1].split()[0]
                    size = int(size_str)
                except (ValueError, IndexError):
                    size = None

            if "NAME=" in line:
                # Variante A: el nombre viene en un campo NAME= explicito.
                name = line.split("NAME=", 1)[1].strip()
            else:
                # Variante B: el nombre es el primer token de la linea,
                # todo lo que precede a " TYPE=".
                name = line.split(" TYPE=", 1)[0].strip()

            entries.append(DirEntry(name=name, is_dir=is_dir, size=size,
                                     raw_line=line))
        return entries

    @staticmethod
    def extract_fsupload_payload(raw: bytes) -> bytes:
        """
        Extrae el contenido binario real de una respuesta FSUPLOAD,
        eliminando la linea de cabecera PJL que el firmware antepone
        (del tipo '@PJL FSUPLOAD NAME="..." OFFSET=0 SIZE=1234\r\n')
        y cualquier UEL final de cierre de sesion.
        """
        data = raw
        # Elimina UEL de cierre si esta presente al final.
        uel_bytes = UEL.encode("latin-1")
        if data.endswith(uel_bytes + EOL.encode("latin-1")):
            data = data[: -len(uel_bytes + EOL.encode("latin-1"))]
        # Busca el primer salto de linea tras la cabecera "@PJL FSUPLOAD..."
        marker = b"@PJL FSUPLOAD"
        idx = data.find(marker)
        if idx != -1:
            nl = data.find(b"\n", idx)
            if nl != -1:
                data = data[nl + 1:]
        return data


# ==============================================================================
# 6. CLIENTE DE ALTO NIVEL ("TRADUCTOR" shell -> PJL)
# ==============================================================================

class PJLClient:
    """
    API de alto nivel pensada para uso humano o programatico.

    Cada metodo publico:
      1. Construye el comando PJL correspondiente via PJLProtocol.
      2. Lo muestra por logger.debug/info para fines de aprendizaje
         (asi ves EXACTAMENTE que se manda "por detras").
      3. Lo envia via PJLTransport.
      4. Parsea/devuelve el resultado en una forma comoda de usar.
    """

    def __init__(self, host: str, port: int = DEFAULT_PORT,
                 timeout: float = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES,
                 show_wire: bool = True):
        self.host = host
        self.port = port
        self.transport = PJLTransport(host, port, timeout, retries)
        self.show_wire = show_wire  # si True, imprime el PJL crudo enviado

    # -- utilidades internas --------------------------------------------------

    def _log_wire(self, pjl_cmd: str) -> None:
        """Muestra al usuario el comando PJL real que se va a enviar."""
        if self.show_wire:
            # Sustituimos caracteres de control por su representacion
            # legible para que el log no rompa la terminal.
            visible = (pjl_cmd
                       .replace(UEL, "<UEL>")
                       .replace("\r\n", "\\r\\n"))
            logger.info(f"  \u21b3 PJL enviado: {visible}")

    def _send(self, pjl_cmd: str, read_timeout: Optional[float] = None) -> str:
        self._log_wire(pjl_cmd)
        raw = self.transport.send_receive(pjl_cmd, read_timeout=read_timeout)
        return raw.decode("latin-1", errors="replace")

    def _send_binary(self, pjl_bytes: bytes,
                      read_timeout: Optional[float] = None) -> bytes:
        if self.show_wire:
            logger.info(f"  \u21b3 PJL enviado: <payload binario, "
                        f"{len(pjl_bytes)} bytes>")
        # send_receive espera str en la firma publica por comodidad general,
        # pero para binarios usamos el socket directamente para no arriesgar
        # perdida de bytes al reencodear.
        return self.transport.send_receive(
            pjl_bytes.decode("latin-1"), read_timeout=read_timeout
        )

    # -- comandos de alto nivel -------------------------------------------------

    def send_raw(self, pjl_command: str, read_timeout: Optional[float] = None) -> str:
        """
        Modo --original / raw: envia `pjl_command` TAL CUAL como cuerpo
        del comando PJL, SIN ninguna capa de traduccion shell -> PJL de
        por medio (a diferencia de todos los demas metodos de esta
        clase, que construyen la sintaxis PJL por ti a partir de un
        comando amigable tipo 'ls' o 'get').

        Lo UNICO que este metodo anade por ti es el envoltorio UEL
        (Universal Exit Language, ESC%-12345X) al principio y al final,
        porque eso es un requisito de TRANSPORTE del protocolo (le dice
        a la impresora "entra en modo PJL" / "sal de modo PJL"), no una
        traduccion de comandos: sin UEL, la inmensa mayoria de firmwares
        ni siquiera reconocerian que les estas hablando en PJL. El
        contenido real del comando -- la sintaxis @PJL que escribas -- se
        envia sin tocar ni interpretar absolutamente nada.

        Ejemplo de uso (equivalente RAW de 'ls 0:\\'):
            client.send_raw('@PJL FSDIRLIST NAME="0:\\\\" ENTRY=1 COUNT=999')
        """
        wrapped = f'{UEL}{pjl_command}{EOL}{UEL}{EOL}'
        return self._send(wrapped, read_timeout=read_timeout)

    def ping(self) -> bool:
        """
        Traduccion: comando de usuario 'ping'  ->  @PJL ECHO "..."

        Comprueba que la impresora responde a nivel de aplicacion PJL
        (no solo TCP). Devuelve True/False.
        """
        token = "PJL-TOOLKIT-PING"
        cmd = PJLProtocol.build_echo(token)
        try:
            resp = self._send(cmd)
        except PJLError as exc:
            logger.error(f"ping fallido: {exc}")
            return False
        ok = token in resp
        logger.debug(f"Respuesta cruda de ECHO: {resp!r}")
        return ok

    def whoami(self) -> str:
        """
        Traduccion: comando de usuario 'id' / 'whoami'  ->  @PJL INFO ID

        Devuelve la cadena de identificacion del dispositivo (marca/modelo).
        """
        cmd = PJLProtocol.build_info_id()
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def status(self) -> str:
        """
        Traduccion: comando de usuario 'status'  ->  @PJL INFO STATUS
        """
        cmd = PJLProtocol.build_info_status()
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def variables(self) -> str:
        """
        Traduccion: comando de usuario 'env'  ->  @PJL INFO VARIABLES
        """
        cmd = PJLProtocol.build_info_variables()
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def filesystems(self) -> str:
        """
        Traduccion: comando de usuario 'df' / 'volumes'  ->  @PJL INFO FILESYS
        """
        cmd = PJLProtocol.build_info_filesys()
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def ls(self, path: str = DEFAULT_VOLUME) -> List[DirEntry]:
        """
        Traduccion: comando de usuario 'ls <ruta>'
                    ->  @PJL FSDIRLIST NAME="<ruta>" ENTRY=1 COUNT=999
        """
        cmd = PJLProtocol.build_fsdirlist(path)
        resp = self._send(cmd)
        entries = PJLProtocol.parse_dirlist(resp)
        if not entries:
            logger.warning(
                "FSDIRLIST no devolvio entradas. Posibles causas: "
                "(a) el directorio esta vacio, (b) la ruta no existe, "
                "(c) este modelo no implementa filesystem PJL. "
                "Prueba antes con 'volumes' para confirmar (c)."
            )
        return entries

    def stat(self, path: str) -> str:
        """
        Traduccion: comando de usuario 'stat <ruta>'
                    ->  @PJL FSQUERY NAME="<ruta>"
        """
        cmd = PJLProtocol.build_fsquery(path)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def get_file(self, remote_path: str, local_path: Optional[str] = None,
                 max_size: int = 5_000_000) -> Path:
        """
        Traduccion: comando de usuario 'get <remoto> [local]'
                    ->  @PJL FSUPLOAD NAME="<remoto>" OFFSET=0 SIZE=<max_size>

        Descarga un fichero del volumen de la impresora a disco local.
        Devuelve la ruta local escrita.
        """
        cmd = PJLProtocol.build_fsupload(remote_path, offset=0, size=max_size)
        self._log_wire(cmd)
        raw = self.transport.send_receive(cmd, read_timeout=None)
        payload = PJLProtocol.extract_fsupload_payload(raw)

        if not payload:
            raise PJLProtocolError(
                f"FSUPLOAD no devolvio datos para '{remote_path}'. "
                f"Comprueba con 'stat {remote_path}' que el fichero existe."
            )

        dest = Path(local_path) if local_path else Path(Path(remote_path).name)
        dest.write_bytes(payload)
        logger.info(f"Fichero remoto '{remote_path}' guardado en "
                    f"'{dest.resolve()}' ({len(payload)} bytes)")
        return dest

    def put_file(self, local_path: str, remote_path: str) -> None:
        """
        Traduccion: comando de usuario 'put <local> <remoto>'
                    ->  @PJL FSDOWNLOAD FORMAT:BINARY SIZE=<n> NAME="<remoto>"
                        + contenido binario del fichero

        Sube un fichero local al volumen de la impresora. DESTRUCTIVO si
        sobrescribe algo existente: usar con conocimiento de causa.
        """
        src = Path(local_path)
        if not src.is_file():
            raise FileNotFoundError(f"No existe el fichero local: {local_path}")
        data = src.read_bytes()
        payload = PJLProtocol.build_fsdownload(remote_path, data)
        self._send_binary(payload)
        logger.info(f"Fichero local '{local_path}' enviado como "
                    f"'{remote_path}' ({len(data)} bytes)")

    def rm(self, remote_path: str) -> str:
        """
        Traduccion: comando de usuario 'rm <ruta>'
                    ->  @PJL FSDELETE NAME="<ruta>"

        DESTRUCTIVO. El shell interactivo pide confirmacion antes de llamar
        a este metodo.
        """
        cmd = PJLProtocol.build_fsdelete(remote_path)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def mkdir(self, remote_path: str) -> str:
        """
        Traduccion: comando de usuario 'mkdir <ruta>'
                    ->  @PJL FSMKDIR NAME="<ruta>"
        """
        cmd = PJLProtocol.build_fsmkdir(remote_path)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def dinquire(self, variable: str) -> str:
        """
        Traduccion: comando de usuario 'dinquire <VARIABLE>'
                    ->  @PJL DINQUIRE <VARIABLE>

        Consulta el valor PERSISTIDO en NVRAM de una variable. A diferencia
        de 'env' (que vuelca TODO de golpe), esto pregunta por una variable
        concreta y es la forma correcta de comprobar el estado real antes
        y despues de modificarla con 'set'/'default'.
        """
        cmd = PJLProtocol.build_dinquire(variable)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def set_variable(self, variable: str, value: str) -> str:
        """
        Traduccion: comando de usuario 'set <VARIABLE> <VALOR>'
                    ->  @PJL SET <VARIABLE>=<VALOR>

        Modifica una variable de entorno SOLO para el trabajo/sesion
        actual. NO persiste en NVRAM: si apagas y enciendes la impresora
        (o simplemente empieza un trabajo de impresion normal desde otro
        equipo), el valor vuelve al que tuviera por defecto. Es la forma
        de bajo riesgo de probar el efecto de una variable antes de
        hacerla persistente con 'default'.
        """
        cmd = PJLProtocol.build_set_variable(variable, value)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def set_default_variable(self, variable: str, value: str) -> str:
        """
        Traduccion: comando de usuario 'default <VARIABLE> <VALOR>'
                    ->  @PJL DEFAULT <VARIABLE>=<VALOR>

        Modifica una variable de entorno y la PERSISTE en NVRAM como
        nuevo valor de fabrica. Esto sobrevive a reinicios de la
        impresora. Es el comando que usan los ataques reales de
        "printer lockout" (p.ej. estableciendo PASSWORD a un valor
        desconocido para el propietario legitimo) o de alteracion
        permanente de configuracion (bandejas bloqueadas, calidad de
        impresion, etc.).

        USAR SOLO EN TU PROPIO EQUIPO Y SABIENDO COMO REVERTIRLO.
        El shell interactivo pide confirmacion explicita antes de
        llamar a este metodo; en modo scriptable/CLI eres tu quien debe
        asegurarse de anotar el valor original con 'dinquire' antes de
        cambiarlo.
        """
        cmd = PJLProtocol.build_default_variable(variable, value)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    def set_display_message(self, line1: str, line2: str = "") -> str:
        """
        Traduccion: comando de usuario 'display <texto>'
                    ->  @PJL RDYMSG DISPLAY="<texto>"

        Cambia el texto de la pantalla LCD. Comando de bajo riesgo, ideal
        para hacer una demo visual/fisica de que el ataque funciona.
        """
        cmd = PJLProtocol.build_rdymsg(line1, line2)
        resp = self._send(cmd)
        return self._clean_info_response(resp)

    # -- helpers de formato -----------------------------------------------------

    @staticmethod
    def _clean_info_response(raw: str) -> str:
        """
        Limpia la respuesta cruda quitando el eco del propio comando (la
        primera linea suele repetir '@PJL INFO ...') para dejar solo el
        contenido util de cara al usuario.
        """
        lines = [l for l in raw.splitlines() if l.strip()]
        return "\n".join(lines) if lines else "(sin respuesta / vacio)"


# ==============================================================================
# 7. SHELL INTERACTIVO (REPL tipo consola de pentesting)
# ==============================================================================

class PJLShell(cmd.Cmd):
    """
    Interfaz interactiva estilo shell, construida sobre el modulo estandar
    `cmd`. Cada metodo `do_<comando>` implementa un comando que el usuario
    puede escribir directamente en el prompt, traduciendolo a la llamada
    correspondiente de PJLClient (y por tanto, al PJL real por debajo).

    Escribe 'help' dentro del shell para ver todos los comandos disponibles,
    o 'help <comando>' para ayuda especifica.
    """

    intro = (
        "\n=== PJL-Toolkit :: shell interactivo ===\n"
        "Escribe 'help' para ver comandos disponibles, 'exit' para salir.\n"
    )

    def __init__(self, client: PJLClient):
        super().__init__()
        self.client = client
        self.prompt = f"pjl@{client.host}:{client.port}> "

    # -- wrapper generico de manejo de errores para todos los do_* -----------

    def _safe(self, func, *args, **kwargs):
        """Ejecuta func(*args) capturando y mostrando errores PJL de forma
        homogenea, sin que el shell se caiga por una excepcion."""
        try:
            return func(*args, **kwargs)
        except PJLTimeoutError as exc:
            logger.error(f"TIMEOUT: {exc}")
        except PJLConnectionError as exc:
            logger.error(f"CONEXION: {exc}")
        except PJLProtocolError as exc:
            logger.error(f"PROTOCOLO: {exc}")
        except FileNotFoundError as exc:
            logger.error(f"FICHERO: {exc}")
        except Exception as exc:  # salvaguarda final, nunca crashear el REPL
            logger.error(f"ERROR INESPERADO: {exc!r}")
        return None

    # -- comandos de reconocimiento -------------------------------------------

    def do_ping(self, arg):
        "ping                 -> comprueba si el interprete PJL responde (@PJL ECHO)"
        ok = self._safe(self.client.ping)
        print("✅ La impresora responde a PJL." if ok
              else "❌ Sin respuesta PJL (revisa IP/puerto/firewall).")

    def do_id(self, arg):
        "id                   -> identifica marca/modelo (@PJL INFO ID)"
        r = self._safe(self.client.whoami)
        if r is not None:
            print(r)

    def do_status(self, arg):
        "status               -> estado operativo actual (@PJL INFO STATUS)"
        r = self._safe(self.client.status)
        if r is not None:
            print(r)

    def do_env(self, arg):
        "env                  -> vuelca variables de entorno (@PJL INFO VARIABLES)"
        r = self._safe(self.client.variables)
        if r is not None:
            print(r)

    def do_volumes(self, arg):
        "volumes              -> lista volumenes de filesystem (@PJL INFO FILESYS)"
        r = self._safe(self.client.filesystems)
        if r is not None:
            print(r)

    def do_dinquire(self, arg):
        "dinquire <VARIABLE>  -> consulta variable NVRAM concreta (@PJL DINQUIRE)"
        if not arg.strip():
            print("Uso: dinquire <NOMBRE_VARIABLE>  (ej: dinquire PASSWORD)")
            return
        r = self._safe(self.client.dinquire, arg.strip())
        if r is not None:
            print(r)

    def do_set(self, arg):
        "set <VARIABLE> <VALOR>      -> cambia variable SOLO para la sesion actual (@PJL SET) [riesgo bajo, no persiste]"
        parts = split_shell_args(arg)
        if len(parts) < 2:
            print("Uso: set <VARIABLE> <VALOR>  (ej: set DENSITY 3)")
            print("Nota: el valor puede llevar espacios si la variable los necesita, "
                  "ej: set 'LPARM:PCL SYMSET' PC8")
            return
        variable, value = parts[0], " ".join(parts[1:])
        r = self._safe(self.client.set_variable, variable, value)
        if r is not None:
            print(r)
        print("ℹ️  Cambio aplicado SOLO a la sesion/trabajo actual (no persiste "
              "en NVRAM). Para hacerlo permanente usarias 'default'.")

    def do_default(self, arg):
        "default <VARIABLE> <VALOR>  -> cambia variable de forma PERMANENTE en NVRAM (@PJL DEFAULT) [DESTRUCTIVO / ALTO RIESGO]"
        parts = split_shell_args(arg)
        if len(parts) < 2:
            print("Uso: default <VARIABLE> <VALOR>  (ej: default PASSWORD 0)")
            return
        variable, value = parts[0], " ".join(parts[1:])

        # Recomendamos SIEMPRE consultar el valor actual antes de tocarlo,
        # para poder revertir el cambio despues.
        print(f"Valor NVRAM actual de '{variable}' (via dinquire):")
        current = self._safe(self.client.dinquire, variable)
        if current is not None:
            print(f"  {current}")

        warning = (
            f"Vas a modificar PERMANENTEMENTE la variable '{variable}' a "
            f"'{value}' en la NVRAM de la impresora. Esto persiste tras "
            f"reiniciar el dispositivo. Anota el valor actual mostrado "
            f"arriba para poder revertirlo. ¿Continuar?"
        )
        if not self._confirm(warning):
            print("Cancelado. No se ha modificado nada.")
            return

        r = self._safe(self.client.set_default_variable, variable, value)
        if r is not None:
            print(r)
        print(f"✅ Aplicado. Para revertir: default {variable} "
              f"<valor_original_anotado_arriba>")

    # -- comandos de sistema de ficheros ---------------------------------------

    def do_ls(self, arg):
        "ls [ruta]            -> lista directorio (@PJL FSDIRLIST), por defecto 0:\\"
        path = arg.strip() or DEFAULT_VOLUME
        entries = self._safe(self.client.ls, path)
        if not entries:
            return
        print(f"{'TIPO':<6}{'TAMANO':>10}  NOMBRE")
        for e in entries:
            size_str = str(e.size) if e.size is not None else "-"
            tipo = "DIR" if e.is_dir else "FILE"
            print(f"{tipo:<6}{size_str:>10}  {e.name}")

    def do_stat(self, arg):
        "stat <ruta>          -> metadatos de un fichero/dir (@PJL FSQUERY)"
        if not arg.strip():
            print("Uso: stat <ruta_remota>")
            return
        r = self._safe(self.client.stat, arg.strip())
        if r is not None:
            print(r)

    def do_get(self, arg):
        "get <remoto> [local] -> descarga fichero (@PJL FSUPLOAD, nombre visto desde la impresora)"
        parts = split_shell_args(arg)
        if not parts:
            print("Uso: get <ruta_remota> [ruta_local_opcional]")
            return
        remote = parts[0]
        local = parts[1] if len(parts) > 1 else None
        self._safe(self.client.get_file, remote, local)

    def do_put(self, arg):
        "put <local> <remoto> -> sube fichero (@PJL FSDOWNLOAD) [DESTRUCTIVO]"
        parts = split_shell_args(arg)
        if len(parts) != 2:
            print("Uso: put <ruta_local> <ruta_remota>")
            return
        local, remote = parts
        if not self._confirm(f"Vas a escribir '{remote}' en la impresora. "
                              f"¿Continuar?"):
            return
        self._safe(self.client.put_file, local, remote)

    def do_rm(self, arg):
        "rm <ruta>            -> borra fichero/dir remoto (@PJL FSDELETE) [DESTRUCTIVO]"
        if not arg.strip():
            print("Uso: rm <ruta_remota>")
            return
        if not self._confirm(f"Vas a BORRAR '{arg.strip()}' de la impresora. "
                              f"¿Continuar?"):
            return
        r = self._safe(self.client.rm, arg.strip())
        if r is not None:
            print(r)

    def do_mkdir(self, arg):
        "mkdir <ruta>         -> crea directorio remoto (@PJL FSMKDIR)"
        if not arg.strip():
            print("Uso: mkdir <ruta_remota>")
            return
        r = self._safe(self.client.mkdir, arg.strip())
        if r is not None:
            print(r)

    def do_display(self, arg):
        "display <texto>      -> cambia mensaje del LCD (@PJL RDYMSG) [demo visual]"
        if not arg.strip():
            print("Uso: display <texto a mostrar en la pantalla de la impresora>")
            return
        r = self._safe(self.client.set_display_message, arg.strip())
        if r is not None:
            print(r)
            print("Revisa fisicamente la pantalla LCD de la impresora.")

    # -- utilidades del propio shell -------------------------------------------

    @staticmethod
    def _confirm(message: str) -> bool:
        resp = input(f"⚠️  {message} (escribe 'si' para confirmar): ").strip().lower()
        return resp in ("si", "s", "yes", "y")

    def do_verbose(self, arg):
        "verbose [on|off]     -> activa/desactiva el volcado de PJL crudo enviado"
        arg = arg.strip().lower()
        if arg in ("on", "1", "true"):
            self.client.show_wire = True
            logging.getLogger("pjl_toolkit").setLevel(logging.DEBUG)
            print("Modo verbose: ON")
        elif arg in ("off", "0", "false"):
            self.client.show_wire = False
            logging.getLogger("pjl_toolkit").setLevel(logging.INFO)
            print("Modo verbose: OFF")
        else:
            print(f"Estado actual: {'ON' if self.client.show_wire else 'OFF'}")

    def do_exit(self, arg):
        "exit / quit          -> cierra el shell"
        print("Cerrando sesion PJL. Hasta la proxima.")
        return True

    do_quit = do_exit

    def do_EOF(self, arg):
        "Ctrl+D               -> equivalente a exit"
        print()
        return self.do_exit(arg)

    def emptyline(self):
        # Evita que pulsar Enter repita el ultimo comando (comportamiento
        # por defecto de cmd.Cmd que suele confundir en demos).
        pass


# ==============================================================================
# 7bis. SHELL "RAW" / --original — sin capa de traduccion shell -> PJL
# ==============================================================================

class PJLRawShell(cmd.Cmd):
    """
    Shell interactivo en modo CRUDO, activado con el flag global
    --original de la CLI.

    A diferencia de PJLShell (que ofrece comandos amigables como 'ls',
    'get', 'id'... y los traduce por ti a la sintaxis PJL real), aqui NO
    existe esa capa de traduccion: cada linea que escribas se envia TAL
    CUAL como el cuerpo de un comando PJL. Tienes que conocer y escribir
    tu mismo la sintaxis real del protocolo, por ejemplo:

        pjl-raw@192.168.1.20:9100> @PJL INFO ID
        pjl-raw@192.168.1.20:9100> @PJL FSDIRLIST NAME="0:\\" ENTRY=1 COUNT=999
        pjl-raw@192.168.1.20:9100> @PJL FSUPLOAD NAME="0:\\scan001.pdf" OFFSET=0 SIZE=5000000
        pjl-raw@192.168.1.20:9100> @PJL DINQUIRE PASSWORD
        pjl-raw@192.168.1.20:9100> @PJL DEFAULT PASSWORD=0

    Este modo esta pensado para cuando ya conoces PJL y quieres mandar
    comandos exactos sin que la herramienta interprete nada por ti (por
    ejemplo, para probar variantes de sintaxis, comandos no cubiertos por
    PJLShell, o simplemente para practicar el lenguaje de memoria tal
    como lo harias con `nc <ip> 9100` a pelo, pero con la comodidad de
    que la herramienta sigue gestionando por ti el envoltorio UEL, los
    timeouts, reintentos y el manejo de errores de red).

    Se implementa sobrescribiendo `default()` de cmd.Cmd: cualquier linea
    que no coincida con un comando interno de gestion del shell (exit,
    help, verbose...) se interpreta automaticamente como PJL crudo y se
    envia sin mas -> no hace falta ningun prefijo especial para "modo
    comando PJL", basta con escribir el propio "@PJL ...".
    """

    intro = (
        "\n=== PJL-Toolkit :: modo RAW (--original) ===\n"
        "Aqui NO hay traduccion de comandos: escribe la sintaxis PJL real,\n"
        "tal cual la mandarias por cable. Ejemplo: @PJL INFO ID\n"
        "Escribe 'exit' para salir, 'help' para los comandos de gestion del shell.\n"
    )

    def __init__(self, client: PJLClient):
        super().__init__()
        self.client = client
        self.prompt = f"pjl-raw@{client.host}:{client.port}> "

    def default(self, line: str):
        """
        Se ejecuta para CUALQUIER entrada que no coincida con un comando
        interno definido mas abajo (do_exit, do_verbose...). Aqui es
        donde ocurre la ausencia total de traduccion: `line` se envia
        exactamente como el usuario la escribio, como cuerpo de un
        comando PJL, sin parsear su sintaxis ni comprobar que sea valida
        -- si te equivocas al escribir el PJL, el error te lo devuelve
        la propia impresora/honeypot, no la herramienta.
        """
        line = line.strip()
        if not line:
            return
        try:
            resp = self.client.send_raw(line)
        except PJLTimeoutError as exc:
            logger.error(f"TIMEOUT: {exc}")
            return
        except PJLConnectionError as exc:
            logger.error(f"CONEXION: {exc}")
            return
        except Exception as exc:  # salvaguarda final, nunca crashear el REPL
            logger.error(f"ERROR INESPERADO: {exc!r}")
            return
        print(resp if resp.strip() else "(sin respuesta / vacio)")

    def do_verbose(self, arg):
        "verbose [on|off]     -> activa/desactiva el volcado de PJL crudo enviado"
        arg = arg.strip().lower()
        if arg in ("on", "1", "true"):
            self.client.show_wire = True
            logging.getLogger("pjl_toolkit").setLevel(logging.DEBUG)
            print("Modo verbose: ON")
        elif arg in ("off", "0", "false"):
            self.client.show_wire = False
            logging.getLogger("pjl_toolkit").setLevel(logging.INFO)
            print("Modo verbose: OFF")
        else:
            print(f"Estado actual: {'ON' if self.client.show_wire else 'OFF'}")

    def do_exit(self, arg):
        "exit / quit          -> cierra el shell"
        print("Cerrando sesion PJL (modo raw). Hasta la proxima.")
        return True

    do_quit = do_exit

    def do_EOF(self, arg):
        "Ctrl+D               -> equivalente a exit"
        print()
        return self.do_exit(arg)

    def emptyline(self):
        pass


# ==============================================================================
# 8. RECONOCIMIENTO DE RED PREVIO (descubrimiento de hosts con 9100 abierto)
# ==============================================================================
# Implementado en Python puro (sin invocar nmap como subproceso) para que
# la herramienta sea autocontenida y no dependa de tener nmap instalado.
# Es deliberadamente simple: para reconocimiento serio de red segueramente
# preferiras nmap, pero esto sirve como modulo de descubrimiento rapido
# integrado, pensado solo para redes locales pequenas (/24 o menores).

def discover_hosts(subnet_base: str, port: int = DEFAULT_PORT,
                    timeout: float = 0.4, max_workers: int = 64) -> List[str]:
    """
    Escanea todas las IPs de una subred /24 (ej. '192.168.1') en busca de
    hosts con el puerto indicado abierto, usando conexiones TCP concurrentes
    con ThreadPoolExecutor para que sea rapido incluso en Python puro.

    subnet_base: los tres primeros octetos, ej. '192.168.1' (SIN el ".0/24").
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _check(ip: str) -> Optional[str]:
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return ip
        except OSError:
            return None

    targets = [f"{subnet_base}.{i}" for i in range(1, 255)]
    found: List[str] = []

    logger.info(f"Escaneando {subnet_base}.0/24 en puerto {port} "
                f"({len(targets)} hosts, timeout={timeout}s)...")

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_check, ip): ip for ip in targets}
        for fut in as_completed(futures):
            result = fut.result()
            if result:
                logger.info(f"  ✅ Host activo con puerto {port} abierto: {result}")
                found.append(result)

    return sorted(found, key=lambda ip: int(ip.split(".")[-1]))


# ==============================================================================
# 9. CLI (argparse) — uso no interactivo / scripting / automatizacion
# ==============================================================================

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pjl_toolkit.py",
        description=(
            "PJL-Toolkit: herramienta propia de auditoria PJL para impresoras "
            "de red (puerto 9100/JetDirect). Uso exclusivo en dispositivos "
            "propios o con autorizacion explicita."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python pjl_toolkit.py --host 192.168.1.20 shell\n"
            "  python pjl_toolkit.py --host 192.168.1.20 id\n"
            "  python pjl_toolkit.py --host 192.168.1.20 ls --path '0:\\'\n"
            "  python pjl_toolkit.py --host 192.168.1.20 get --remote scan.pdf\n"
            "  python pjl_toolkit.py --host 192.168.1.20 dinquire --var PASSWORD\n"
            "  python pjl_toolkit.py --host 192.168.1.20 set --var DENSITY --value 3\n"
            "  python pjl_toolkit.py --host 192.168.1.20 default --var PASSWORD --value 0\n"
            "  python pjl_toolkit.py --host 192.168.1.20 --original shell\n"
            "  python pjl_toolkit.py discover --subnet 192.168.1\n"
        ),
    )
    parser.add_argument("--host", help="IP o hostname de la impresora objetivo")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                         help=f"Puerto TCP (por defecto {DEFAULT_PORT})")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                         help=f"Timeout en segundos (por defecto {DEFAULT_TIMEOUT})")
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES,
                         help=f"Reintentos ante fallo de red (por defecto {DEFAULT_RETRIES})")
    parser.add_argument("-v", "--verbose", action="store_true",
                         help="Muestra el PJL crudo enviado y logs de depuracion")
    parser.add_argument("-q", "--quiet", action="store_true",
                         help="Silencia el volcado de comandos PJL crudos")
    parser.add_argument("--original", action="store_true",
                         help=(
                             "Modo RAW/crudo: solo aplica al subcomando 'shell'. "
                             "Desactiva la traduccion de comandos amigables (ls, "
                             "get, id...) -> en su lugar, cada linea que escribas "
                             "en el shell se envia TAL CUAL como comando PJL real "
                             "(ej: '@PJL INFO ID'). Pensado para quien ya conoce "
                             "PJL y quiere mandar comandos exactos sin traduccion."
                         ))

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("shell", help="Abre el shell interactivo (recomendado)")
    sub.add_parser("ping", help="Comprueba respuesta PJL (@PJL ECHO)")
    sub.add_parser("id", help="Identifica el dispositivo (@PJL INFO ID)")
    sub.add_parser("status", help="Estado operativo (@PJL INFO STATUS)")
    sub.add_parser("env", help="Variables de entorno (@PJL INFO VARIABLES)")
    sub.add_parser("volumes", help="Volumenes de filesystem (@PJL INFO FILESYS)")

    p_ls = sub.add_parser("ls", help="Lista un directorio (@PJL FSDIRLIST)")
    p_ls.add_argument("--path", default=DEFAULT_VOLUME)

    p_get = sub.add_parser("get", help="Descarga un fichero (@PJL FSUPLOAD)")
    p_get.add_argument("--remote", required=True)
    p_get.add_argument("--local", default=None)

    p_put = sub.add_parser("put", help="Sube un fichero (@PJL FSDOWNLOAD) [DESTRUCTIVO]")
    p_put.add_argument("--local", required=True)
    p_put.add_argument("--remote", required=True)
    p_put.add_argument("--yes", action="store_true",
                        help="Omite la confirmacion interactiva")

    p_dinq = sub.add_parser("dinquire",
                             help="Consulta una variable NVRAM concreta (@PJL DINQUIRE)")
    p_dinq.add_argument("--var", required=True, help='Ej: PASSWORD, DENSITY, "LPARM:PCL SYMSET"')

    p_set = sub.add_parser("set",
                            help="Cambia variable SOLO para la sesion actual (@PJL SET)")
    p_set.add_argument("--var", required=True)
    p_set.add_argument("--value", required=True)

    p_default = sub.add_parser("default",
                                help="Cambia variable de forma PERMANENTE en NVRAM "
                                     "(@PJL DEFAULT) [DESTRUCTIVO]")
    p_default.add_argument("--var", required=True)
    p_default.add_argument("--value", required=True)
    p_default.add_argument("--yes", action="store_true",
                            help="Omite la confirmacion interactiva")

    p_disc = sub.add_parser("discover",
                             help="Escanea una subred /24 buscando puerto 9100 abierto")
    p_disc.add_argument("--subnet", required=True,
                         help="Tres primeros octetos, ej. 192.168.1")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    setup_logging(verbose=args.verbose)

    # --- comando de descubrimiento: no requiere --host ------------------------
    if args.command == "discover":
        hosts = discover_hosts(args.subnet, port=args.port)
        if hosts:
            print("\nHosts con puerto {} abierto:".format(args.port))
            for h in hosts:
                print(f"  - {h}")
        else:
            print("No se encontro ningun host con ese puerto abierto.")
        return 0

    # --- todos los demas comandos requieren --host -----------------------------
    if not args.host:
        parser.error("--host es obligatorio para este comando")

    if args.original and args.command != "shell":
        logger.warning(
            "--original solo tiene efecto en el subcomando 'shell'; se ignora "
            "para '%s' (los subcomandos sueltos como 'id'/'ls'/'get' ya son "
            "en si mismos la capa traducida, no tiene sentido combinarlos "
            "con el modo crudo)." % args.command
        )

    client = PJLClient(
        host=args.host, port=args.port, timeout=args.timeout,
        retries=args.retries, show_wire=not args.quiet,
    )

    try:
        if args.command == "shell":
            if args.original:
                PJLRawShell(client).cmdloop()
            else:
                PJLShell(client).cmdloop()

        elif args.command == "ping":
            ok = client.ping()
            print("✅ Responde a PJL" if ok else "❌ Sin respuesta")
            return 0 if ok else 1

        elif args.command == "id":
            print(client.whoami())

        elif args.command == "status":
            print(client.status())

        elif args.command == "env":
            print(client.variables())

        elif args.command == "volumes":
            print(client.filesystems())

        elif args.command == "ls":
            entries = client.ls(args.path)
            for e in entries:
                tipo = "DIR " if e.is_dir else "FILE"
                size = e.size if e.size is not None else "-"
                print(f"{tipo}  {size:>10}  {e.name}")

        elif args.command == "get":
            client.get_file(args.remote, args.local)

        elif args.command == "put":
            if not args.yes:
                resp = input(f"Vas a escribir '{args.remote}' en la impresora. "
                              f"Escribe 'si' para confirmar: ").strip().lower()
                if resp not in ("si", "s", "yes", "y"):
                    print("Cancelado.")
                    return 1
            client.put_file(args.local, args.remote)

        elif args.command == "dinquire":
            print(client.dinquire(args.var))

        elif args.command == "set":
            print(client.set_variable(args.var, args.value))
            print("ℹ️  Cambio aplicado solo a la sesion actual (no persiste en NVRAM).")

        elif args.command == "default":
            current = client.dinquire(args.var)
            print(f"Valor NVRAM actual de '{args.var}':\n  {current}")
            if not args.yes:
                resp = input(
                    f"Vas a modificar PERMANENTEMENTE '{args.var}' a "
                    f"'{args.value}' en NVRAM. Escribe 'si' para confirmar: "
                ).strip().lower()
                if resp not in ("si", "s", "yes", "y"):
                    print("Cancelado.")
                    return 1
            print(client.set_default_variable(args.var, args.value))
            print(f"✅ Aplicado. Para revertir: default --var {args.var} "
                  f"--value <valor_original_anotado_arriba>")

    except PJLError as exc:
        logger.error(str(exc))
        return 1
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
