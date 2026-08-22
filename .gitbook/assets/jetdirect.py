#!/usr/bin/env python3

import os
import sys
import socket
import logging
import re
import hashlib
from collections import defaultdict

class PJLServer:
    def __init__(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, port=9100, backlog=100):
        self._server.bind(("0.0.0.0", port))
        self._server.listen(backlog)

        logging.info("listening on port %d" % port)

    def close(self):
        self._server.close()

    def accept(self):
        client, addr = self._server.accept()
        ip = addr[0]
        logging.info("[%s] connected" % ip)

        return PJLClient(client, ip)

class PJLClient:
    def __init__(self, client, address):
        self._client = client
        self._address = address
    
    @property
    def ip(self):
        return self._address

    def get_command(self, chunk_size=1024):
        command = b""
        packet_count = 0

        while True:
            packet = self._client.recv(chunk_size)

            if not packet:
                break

            command += packet
            packet_count += 1

            if b"\r\n" in command:
                break

        logging.info("[%s] received %d bytes (%d packets)" % (self.ip, len(command), packet_count))
        logging.debug("[%s] received command %s" % (self.ip, command))

        return command

    def reply(self, message):
        logging.info("[%s] sending %s" % (self.ip, message))
        self._client.send(message)

    def close(self):
        self._client.close()

class Filesystem:
    # Nombre logico de la carpeta especial dentro del volumen "0:" que
    # esta respaldada por disco real (en vez de estar precargada en
    # memoria de forma estatica como el resto del arbol). Es el "puente"
    # entre la pagina web de escaneo y el filesystem PJL simulado: todo
    # lo que la web deposite en el directorio de disco configurado
    # aparecera aqui EN CALIENTE, sin reiniciar el honeypot.
    SCANS_DIRNAME = "scans"

    def __init__(self, scans_disk_dir=None):
        self._fs = defaultdict(defaultdict)
        # Ruta REAL en el disco del contenedor (ej. /app/prints/scans)
        # que respalda dinamicamente "0:\scans". Se asigna despues de
        # parsear los argumentos de linea de comandos, ver bloque
        # __main__ mas abajo.
        self.scans_disk_dir = scans_disk_dir

    def split_path(self, path):
        return [part for part in re.split(r"(\\|/)", path) if part.strip() not in ["", "/", "\\"]]

    def add_file(self, name, content):
        # ARREGLADO: la version original hacia
        #   cwd[part] = defaultdict(defaultdict)
        # de forma INCONDICIONAL para cada carpeta intermedia, incluso si
        # esa carpeta ya existia de una llamada anterior a add_file(). Eso
        # significa que anadir un segundo fichero bajo "0:\" borraba
        # silenciosamente todo lo que ya hubiera bajo "0:\" (incluidos
        # otros ficheros anadidos antes). Con varias llamadas seguidas a
        # add_file() solo sobrevivia la carpeta de la ULTIMA llamada.
        # Ahora solo se crea un dict nuevo si esa carpeta no existe aun.
        parts = self.split_path(name)
        cwd = self._fs

        for part in parts[:-1]:
            if not isinstance(cwd.get(part), dict):
                cwd[part] = defaultdict(defaultdict)
            cwd = cwd[part]

        cwd[parts[-1]] = content

    def mkdir(self, name):
        """
        NUEVO: crea (o asegura que existe) un directorio VACIO en el
        arbol estatico, sin necesidad de anadir ningun fichero dentro.
        Se usa para que "scans" aparezca como carpeta real en el listado
        de la raiz "0:\", aunque su CONTENIDO real se sirva luego desde
        disco (ver _is_scans_path / _listdir_disk mas abajo).
        """
        parts = self.split_path(name)
        cwd = self._fs

        for part in parts:
            if not isinstance(cwd.get(part), dict):
                cwd[part] = defaultdict(defaultdict)
            cwd = cwd[part]

    def _is_scans_dir(self, parts):
        """True si `parts` apunta exactamente a "0:\\scans" (la carpeta
        respaldada por disco), sin importar mayus/minus."""
        return (
            self.scans_disk_dir is not None
            and len(parts) == 2
            and parts[0].lower() == "0:"
            and parts[1].lower() == self.SCANS_DIRNAME.lower()
        )

    def _is_scans_file(self, parts):
        """True si `parts` apunta a un fichero DENTRO de "0:\\scans"."""
        return (
            self.scans_disk_dir is not None
            and len(parts) == 3
            and parts[0].lower() == "0:"
            and parts[1].lower() == self.SCANS_DIRNAME.lower()
        )

    def _safe_disk_path(self, filename):
        """
        Resuelve `filename` dentro de self.scans_disk_dir e impide salir
        de ese directorio con trucos tipo '..' (path traversal) -> esto
        es exactamente el tipo de vulnerabilidad real documentada en
        HP LaserJet (CVE-2017-2741 y el fallo historico de FSDIRLIST con
        '0:\\..\\..\\..\\'), asi que el honeypot debe resistirlo tambien
        para que el lab sea representativo.
        """
        base = os.path.abspath(self.scans_disk_dir)
        target = os.path.abspath(os.path.join(base, filename))
        if not target.startswith(base + os.sep) and target != base:
            return None
        return target

    def _listdir_disk(self):
        """Genera el listado de '0:\\scans' leyendo el directorio real
        en disco compartido via volumen Docker con la pagina web."""
        directory = [". TYPE=DIR", ".. TYPE=DIR"]

        if self.scans_disk_dir and os.path.isdir(self.scans_disk_dir):
            for entry in sorted(os.listdir(self.scans_disk_dir)):
                full_path = os.path.join(self.scans_disk_dir, entry)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    directory.append("%s TYPE=FILE SIZE=%d" % (entry, size))

        return "\n".join(directory)

    def listdir(self, name=""):
        parts = self.split_path(name)

        # Interceptar "0:\scans" ANTES de consultar el arbol estatico:
        # su contenido se genera dinamicamente desde disco en cada
        # llamada, para reflejar en caliente lo que la web de escaneo
        # vaya guardando.
        if self._is_scans_dir(parts):
            return self._listdir_disk()

        cwd = self._fs

        for part in parts:
            if part not in cwd:
                return "FILEERROR=1"

            cwd = cwd[part]

        if isinstance(cwd, str):
            return "%s TYPE=FILE SIZE=%d" % (parts[-1], len(cwd))

        directory = [
            ". TYPE=DIR",
        ]

        if cwd != self._fs:
            directory.append(".. TYPE=DIR")

        for element in cwd:
            if isinstance(cwd[element], str):
                directory.append("%s TYPE=FILE SIZE=%d" % (element, len(cwd[element])))
            else:
                directory.append("%s TYPE=DIR" % element)

        return "\n".join(directory)

    def read_file(self, name):
        """
        Lee el contenido de un fichero ya existente en el fs simulado.
        Devuelve None si la ruta no existe o es un directorio, para que
        el llamante pueda decidir como reportar el error.

        Si la ruta cae dentro de "0:\\scans\\<fichero>", se lee del
        disco real en vez del arbol estatico en memoria.
        """
        parts = self.split_path(name)

        if self._is_scans_file(parts):
            filename = parts[2]
            disk_path = self._safe_disk_path(filename)
            if disk_path is None or not os.path.isfile(disk_path):
                return None
            try:
                with open(disk_path, "r", encoding="utf-8") as fh:
                    return fh.read()
            except (UnicodeDecodeError, OSError):
                # Contenido binario no representable como texto UTF-8:
                # este honeypot es un protocolo de solo texto (ver nota
                # en el README de printer_webui/), asi que la pagina web
                # se encarga de guardar SIEMPRE contenido en base64 aqui,
                # de modo que este caso no deberia darse en uso normal.
                return None

        cwd = self._fs

        for part in parts:
            if part not in cwd:
                return None
            cwd = cwd[part]

        if isinstance(cwd, str):
            return cwd
        return None  # es un directorio, no un fichero

fs = Filesystem()
fs.add_file("0:\\pcl\\macros\\jobs", "")

# --- Ficheros simulados para el lab de pentesting (precarga estatica) ---
# Se anaden aqui, ANTES de arrancar el servidor, porque FSDOWNLOAD no esta
# implementado en este honeypot (ver diccionario de comandos mas abajo:
# "FSDOWNLOAD": "" es un stub vacio) -> la escritura en caliente via PJL
# no persiste nada, asi que el contenido de prueba se precarga aqui.
fs.add_file("0:\\scan001.pdf", "%PDF-1.4 contenido simulado de un escaneo de prueba")
fs.add_file("0:\\scan002.pdf", "%PDF-1.4 segundo documento escaneado simulado")
fs.add_file("0:\\config\\network.cfg", "WIFI_SSID=TestNet\nWIFI_PASS=fake_password_123")

# "scans" se reserva aqui como carpeta VACIA en el arbol estatico, solo
# para que aparezca listada en la raiz "0:\". Su contenido REAL se sirve
# dinamicamente desde disco (ver Filesystem._is_scans_dir/_listdir_disk)
# una vez que fs.scans_disk_dir se asigne en el bloque __main__ de abajo,
# con la ruta real compartida por volumen Docker con printer_webui/.
fs.mkdir("0:\\scans")

commands = {
    "@PJL": {
        "COMMENT": "",
        "ENTER": {
            "LANGUAGE": {
                "PCL": "E . . . . PCL Job . . . . E",
                "POSTSCRIPT": "%!PS-ADOBE ... PostScript print job ...",
            }
        },
        "JOB": "",
        "EOJ": "",
        "DEFAULT": "",
        "SET": "",
        "INITIALIZE": "",
        "RESET": "",
        "INQUIRE": {
            "RET": "MEDIUM",
            "PAGEPROTECT": "OFF",
            "RESOLUTION": "600",
            "PERSONALITY": "AUTO",
            "TIMEOUT": "15",
            "LPARM:PCL": {
                "PITCH": "10.00",
                "PTSIZE": "12.00",
                "SYMSET": "ROMAN8",
            },
        },
        "DINQUIRE": {
            "RET": "MEDIUM",
            "PAGEPROTECT": "OFF",
            "RESOLUTION": "600",
            "PERSONALITY": "AUTO",
            "TIMEOUT": "15",
            "LPARM:PCL": {
                "PITCH": "10.00",
                "PTSIZE": "12.00",
                "SYMSET": "ROMAN8",
            },
        },
        "ECHO": lambda command: command,
        "INFO": {
            "ID": "HP LASERJET 4ML",
            "CONFIG": "IN TRAYS [3 ENUMERATED]\n\tINTRAY1 MP\n\tINTRAY2 PC\n\tINTRAY3 LC\nENVELOPE TRAY\nOUT TRAYS [1 ENUMERATED]\n\tNORMAL FACEDOWN\nPAPERS [9 ENUMERATED]\n\tLETTER\n\tLEGAL\n\tA4\n\tEXECUTIVE\n\tMONARCH\n\tCOM10\n\tDL\n\tC5\n\tB5\nLANGUAGES [2 ENUMERATED]\n\tPCL\n\tPOSTSCRIPT\nUSTATUS [4 ENUMERATED]\n\tDEVICE\n\tJOB\n\tPAGE\n\tTIMED\nFONT CARTRIDGE SLOTS [1 ENUMERATED]\n\tCARTRIDGE\nMEMORY=2097152\nDISPLAY LINES=1\nDISPLAY CHARACTER SIZE=16",
            "FILESYS": "VOLUME TOTAL SIZE FREE SPACE LOCATION LABEL STATUS\n0:     1755136    1718272    <HT>     <HT>  READ-WRITE",
            "MEMORY": "TOTAL=1494416\nLARGEST=1494176",
            "PAGECOUNT": "PAGECOUNT=183933",
            "STATUS": "CODE=10001\nDISPLAY=\"Non HP supply in use\"\nONLINE=TRUE",
            "VARIABLES": "COPIES=1 [2 RANGE]\n\t1\n\t999\nPAPER=LETTER [3 ENUMERATED]\n\tLETTER\n\tLEGAL\n\tA4\nORIENTATION=PORTRAIT [2 ENUMERATED]\n\tPORTRAIT\n\tLANDSCAPE\nFORMLINES=60 [2 RANGE]\n\t5\n\t128\nMANUALFEED=OFF [2 ENUMERATED]\n\tOFF\n\tON\nRET=MEDIUM [4 ENUMERATED]\n\tOFF\n\tLIGHT\n\tMEDIUM\n\tDARK\nPAGEPROTECT=OFF [4 ENUMERATED]\n\tOFF\n\tLETTER\n\tLEGAL\n\tA4\nRESOLUTION=600 [2 ENUMERATED]\n\t300\n\t600\nPERSONALITY=AUTO [3 ENUMERATED]\n\tAUTO\n\tPCL\n\tPOSTSCRIPT\nTIMEOUT=15 [2 RANGE]\n\t5\n\t300\nMPTRAY=CASSETTE [3 ENUMERATED]\n\tMANUAL\n\tCASSETTE\n\tFIRST\nINTRAY1=UNLOCKED [2 ENUMERATED]\n\tUNLOCKED\n\tLOCKED\nINTRAY2=UNLOCKED [2 ENUMERATED]\n\tUNLOCKED\n\tLOCKED\nINTRAY3=UNLOCKED [2 ENUMERATED]\n\tUNLOCKED\n\tLOCKED\nCLEARABLEWARNINGS=ON [2 ENUMERATED READONLY]\n\tJOB\n\tON\nAUTOCONT=OFF [2 ENUMERATED READONLY]\n\tOFF\n\tON\n\nDENSITY=3 [2 RANGE READONLY]\n\t1\n\t5\nLOWTONER=ON [2 ENUMERATED READONLY]\n\tOFF\n\tON\nINTRAY1SIZE=LETTER [9 ENUMERATED READONLY]\n\tLETTER\n\tLEGAL\n\tA4\n\tEXECUTIVE\n\tCOM10\n\tMONARCH\n\tC5\n\tDL\n\tB5\nINTRAY2SIZE=LETTER [4 ENUMERATED READONLY]\n\tLETTER\n\tLEGAL\n\tA4\n\tEXECUTIVE\nINTRAY3SIZE=LETTER [4 ENUMERATED READONLY]\n\tLETTER\n\tLEGAL\n\tA4\n\tEXECUTIVE\nINTRAY4SIZE=COM10 [5 ENUMERATED READONLY]\n\tCOM10\n\tMONARCH\n\tC5\n\tDL\n\tB5\nLPARM:PCL FONTSOURCE=I [1 ENUMERATED]\n\tI\nLPARM:PCL FONTNUMBER=0 [2 RANGE]\n\t0\n\t50\nLPARM:PCL PITCH=10.00 [2 RANGE]\n\t0.44\n\t99.99\nLPARM:PCL PTSIZE=12.00 [2 RANGE]\n\t4.00\n\t999.75\nLPARM:PCL SYMSET=ROMAN8 [4 ENUMERATED]\n\tROMAN8\n\tISOL1\n\tISOL2\n\tWIN30\nLPARM:POSTSCRIPT PRTPSERRS=OFF [2 ENUMERATED]\n\tOFF\n\tON",
            "USTATUS": "DEVICE=OFF [3 ENUMERATED]\n\tOFF\n\tON\n\tVERBOSE\nJOB=OFF [2 ENUMERATED]\n\tOFF\n\tON\nPAGE=OFF [2 ENUMERATED]\n\tOFF\n\tON\nTIMED=0 [2 RANGE]\n\t5\n\t300",
        },
        "USTATUSOFF": "",
        "USTATUS": {
            "DEVICE": "CODE=10001\nDISPLAY=\"Non HP supply in use\"\nONLINE=TRUE",
            "JOB": "",
            "PAGE": "",
            "TIMED": "CODE=10001\nDISPLAY=\"Non HP supply in use\"\nONLINE=TRUE",
        },
        "RDYMSG": "",
        "OPMSG": "",
        "STMSG": "",
        "FSAPPEND": "",
        "FSDELETE": "",
        "FSDIRLIST": lambda command: fs.listdir(re.findall(r"\"([^\"]+)\"", command)[0]),
        "FSDOWNLOAD": "",
        "FSINIT": "",
        "FSMKDIR": "",
        "FSQUERY": lambda command: fs.listdir(re.findall(r"\"([^\"]+)\"", command)[0]),
        # MODIFICADO: antes era "" (stub vacio, nunca devolvia contenido
        # real). Ahora lee de verdad del filesystem simulado 'fs'. Si el
        # fichero no existe o es un directorio, devuelve FILEERROR=1,
        # igual que hacen FSDIRLIST/FSQUERY en este mismo honeypot.
        "FSUPLOAD": lambda command: (
            fs.read_file(re.findall(r"\"([^\"]+)\"", command)[0]) or "FILEERROR=1"
        ),
    },
}

def log_command(command):
    logging.info("couldn't parse command '%s'" % command)

    return "?"

def find_action(command):
    search_area = commands
    parsed_command = command.strip()

    if not parsed_command:
        return None

    while len(parsed_command) > 0:
        could_parse = False

        if not isinstance(search_area, dict):
            break

        for (subcommand, area) in search_area.items():
            if subcommand == "":
                continue

            if parsed_command.lower().startswith(subcommand.lower()):
                parsed_command = parsed_command[len(subcommand):].strip()
                search_area = area
                could_parse = True
                break

        if not could_parse:
            logging.debug("unknown argument '%s'" % parsed_command)
            return None

    while isinstance(search_area, dict):
        if "" not in search_area.keys():
            return None

        search_area = search_area[""]

    return search_area


def run_command(command):
    command = command.strip()
    logging.debug("parsing '%s'" % command)
    action = find_action(command)

    if action == None:
        return log_command(command)

    if isinstance(action, str):
        logging.debug("found '%s' for '%s'" % (action, command))
        return action

    logging.debug("executing found action for '%s'" % command)
    try:
        result = action(command)
    except Exception as error:
        logging.warning("error in action: %s" % str(error))
        return log_command(command)

    logging.debug("execution result '%s' for '%s'" % (result, command))

    return result

if __name__ == "__main__":
    if not (3 <= len(sys.argv) <= 4):
        print("usage: %s PORT PCL_DIRECTORY [LOGFILE]" % sys.argv[0])
        exit(1)

    port = int(sys.argv[1])
    pcl_directory = sys.argv[2]
    log_handlers = [logging.StreamHandler()]

    if len(sys.argv) == 4:
        logfile = sys.argv[3]
        log_handlers.append(logging.FileHandler(logfile))

    logging.basicConfig(
        level = logging.DEBUG,
        format="%(asctime)s [%(levelname)s]\t%(message)s",
        handlers=log_handlers
    )

    # Conecta "0:\scans" con la carpeta real "<PCL_DIRECTORY>/scans" del
    # contenedor. Esta es la ruta que printer_webui/ debe usar tambien
    # (mapeada al mismo volumen Docker que ya usas para PCL_DIRECTORY, ej.
    # -v `pwd`/prints:/app/prints), de modo que un fichero subido desde la
    # pagina web aparezca en "ls 0:\scans" sin reiniciar el honeypot.
    fs.scans_disk_dir = os.path.join(pcl_directory, Filesystem.SCANS_DIRNAME)
    os.makedirs(fs.scans_disk_dir, exist_ok=True)
    logging.info("volumen '0:\\scans' respaldado por disco en: %s" % fs.scans_disk_dir)

    if not os.path.exists(pcl_directory):
        logging.warning("pcl directory '%s' not found" % pcl_directory)
        exit(2)

    server = PJLServer()
    server.listen(port)

    while True:
        try:
            client = server.accept()
        except KeyboardInterrupt:
            break

        is_pcl_session = False
        pcl_file_bytes = b""

        while True:
            try:
                program = client.get_command()

                if program.startswith(b"\x1bE\x1b&l"):
                    is_pcl_session = True

                if is_pcl_session:
                    if not program:
                        break

                    pcl_file_bytes += program
                    continue

                if len(program) > 0 and program[0] == ord(b"\x1b"):
                    program_start = program.index(b"@")
                    program_delimiter = program[:program_start]
                    program = program[len(program_delimiter):-len(program_delimiter)]

                program = program.decode("utf-8").strip()
            except KeyboardInterrupt:
                break

            if not program:
                break

            replies = []

            for command in program.split("\r\n"):
                command_result = run_command(command)
                result = (command_result + "\n").replace("\n", "\r\n")
                replies.append(result)

            reply = bytes("\r\n".join(replies), "utf-8")
            client.reply(reply)

        if is_pcl_session:
            md5 = hashlib.md5()
            md5.update(pcl_file_bytes)
            file_hash = md5.hexdigest()
            filename = os.path.join(pcl_directory, file_hash)
            logging.info("[%s] received document %s" % (client.ip, filename))

            with open(filename, "wb") as file_handle:
                file_handle.write(pcl_file_bytes)

            is_pcl_session = False
            pcl_file_bytes = b""

        client.close()

    server.close()
