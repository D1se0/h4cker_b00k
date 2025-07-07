---
icon: power-off
---

# WOL (Wake On Lan) Conf

Si por ejemplo queremos encender nuestro PC desde un movil o desde un microcontrolador, podremos hacerlo mediante un llamado `Paquete Magico` que se le envia al `Router` y mediante la identificacion de la MAC del PC viaja por el cable `Ethernet` hasta el PC activando el mismo.

> NOTA IMPORTANTE

Tenemos que estar en la misma red con el PC y el movil, el PC tiene que estar por cable al mismo `Router` desde donde esta conectado el movil con el `Wifi` del mismo `Router`.

## <mark style="color:purple;">Activar opcion WOL en la BIOS</mark>

Nos meteremos a nuestra BIOS con la tecla correspondiente al equipo (`F2, F11, Supr, etc...`) mientras se esta iniciando el sistema, una vez estando dentro de la BIOS tendremos que irnos a opciones avanzadas u opciones de alimentacion dependiendo de la BIOS que tengamos y en esas opciones deberemos de ver una opcion llamada algo parecido como `Wake On Lan`, `Power Management`, `Network Boot`, etc... Opciones parecidas a las mencionadas y si aparece como `Disable` tendremos que ponerlo en `Enable`.

Una vez echo eso, guardaremos la configuracion y saldremos de la BIOS entrando al S.O.

## <mark style="color:purple;">Configuracion en Windows</mark>

Abrir `Administrador de dispositivos`, nos dirigimos a la seccion llamada `Adaptadores de red` y seleccionamos nuestro adaptador de red (Que me refiero a nuestro cable `Ethernet`), entramos a las propiedades del mismo con click derecho, nos vamos a la pestaña `Administracion de energia` y marcamos las siguientes casillas:

1. Permitir que este dispositivo reactive el equipo
2. Solo permitir un paquete magico para activar el equipo

### Obtener la direccion MAC del equipo

Para obtener la direccion MAC de nuestro equipo abriremos `PowerShell` y pondremos el siguiente comando:

```powershell
ipconfig /all
```

En esta informacion buscaremos nuestro adaptador de red y apuntaremos la direccion MAC (Ej. `A8-CC-L1-F6-55-C1`) del equipo, tambien nos vendra bien saber la direccion IP con la que esta asociada para posteriormente sacar la direccion del `Broadcast` (Ej. `192.168.1.255`)

## <mark style="color:purple;">Script para el movil</mark>

Ahora crearemos un script en `python3` para el movil, para que desde el script de forma automatizada envie el `paquete magico` al `router` y con la direccion `MAC` vaya directo por el cable `Ethernet` hasta que llegue a encender el equipo.

Para ello antes de hacer el script descargaremos en nuestro movil la aplicacion llamada `Pydroid3` y dentro crearemos el script, en mi caso hice algo tal que asi:

```python
import kivy

from [kivy.app](http://kivy.app/) import App

from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label

from kivy.uix.textinput import TextInput

from kivy.core.window import Window

import socket

from kivy.graphics import Color, Rectangle

  

kivy.require('2.0.0')

  

class TerminalLayout(FloatLayout):

    def __init__(self, **kwargs):

        super(TerminalLayout, self).__init__(**kwargs)

  

        # Fondo negro estilo terminal

        with self.canvas.before:

            Color(0, 0, 0, 1)  # Negro para el fondo

            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

  

        # Etiqueta de salida de terminal

        self.output_label = Label(

            text="root@hackpc:~# Bienvenido a la terminal. Escribe 'Power' para encender la PC o 'Exit' para salir.",

            font_size='18sp',

            color=(0, 1, 0, 1),

            halign='left',

            valign='top',

            size_hint=(1, None),  # Ajustar a un ancho completo

            height=200,  # Establecer altura fija para el área de salida

            pos_hint={'x': 0, 'top': 1}  # Posicionar en la parte superior

        )

        self.output_label.bind(size=self._update_output_label)

        self.add_widget(self.output_label)

  

        # Layout para el prompt y el campo de entrada

        self.input_layout = FloatLayout(size_hint_y=None, height=50)

  

        # Etiqueta del prompt (root@hackpc#)

        self.prompt_label = Label(

            text="root@hackpc# ",

            font_size='18sp',

            color=(0, 1, 0, 1),

            size_hint_x=None,

            #width=150  # Un ancho fijo para el prompt

            height=50,  # Establecer una altura fija

     pos_hint={'x': 0.1, 'top': 40}  # Posiciona en la parte superior

        )

        self.input_layout.add_widget(self.prompt_label)

  

        # Entrada de texto para comandos

        self.command_input = TextInput(

            multiline=False,

            font_size='18sp',

            background_color=(0, 0, 0, 1),

            foreground_color=(0, 1, 0, 1),

            cursor_color=(0, 1, 0, 1),

            size_hint_x=1,  # Aseguramos que se ajuste al ancho

            height=50,

            write_tab=False,  # No permitir tabulación

            padding_y=[0, -0.01],  # Padding superior e inferior

            halign='left',

            pos_hint={'x': 0.28, 'y': 39}  # Posicionar en la parte inferior

        )

        self.command_input.bind(on_text_validate=self.on_enter)

        self.input_layout.add_widget(self.command_input)

  

        # Añadir el layout del prompt y entrada

        self.add_widget(self.input_layout)

  

    def _update_rect(self, *args):

        self.rect.pos = self.pos

        self.rect.size = self.size

  

    def _update_output_label(self, instance, value):

        # Asegurarse de que el texto se ajuste al tamaño del label

        self.output_label.text_size = (self.output_label.width, None)

  

    def on_enter(self, instance):

        command = self.command_input.text.strip().lower()

        self.output_label.text += f"\nroot@hackpc# {command}"

        if command == 'power':

            try:

                pc_ip_address = "<IP>"  # Cambia esto por la IP de tu PC

                if self.check_pc_status(pc_ip_address, 80):

                    self.output_label.text += "\n> PC ya está encendida."

                else:

                    mac_address = "<DIRECCION_MAC>"  # Cambia esto por la MAC de tu PC

                    self.send_magic_packet(mac_address)

                    self.output_label.text += "\n> Enviando paquete WoL, PC encendiendo..."

            except Exception as e:

                self.output_label.text += f"\n> Error: {str(e)}"

        elif command == 'exit':

            self.output_label.text += "\n> Saliendo de la terminal..."

            App.get_running_app().stop()  # Cierra la aplicación

        else:

            self.output_label.text += f"\n> Comando '{command}' no reconocido."

  

        # Desplazar el texto hacia arriba si es necesario

        if len(self.output_label.text.splitlines()) > 20:

            self.output_label.text = '\n'.join(self.output_label.text.splitlines()[-20:])

  

        # Limpiar la entrada de texto después de cada comando

        self.command_input.text = ''

  

    def check_pc_status(self, ip_address, port):

        """Verifica si la PC está encendida intentando conectarse a un puerto específico."""

        try:

            sock = socket.create_connection((ip_address, port), timeout=2)

            sock.close()

            return True  # Si la conexión es exitosa, la PC está encendida

        except (socket.timeout, ConnectionRefusedError, OSError):

            return False  # Si no se puede conectar, la PC está apagada o el puerto no está abierto

  

    def send_magic_packet(self, mac_address):

        """Envia un paquete WoL (Wake-on-LAN) para encender la PC."""

        mac_address = mac_address.replace(":", "")

        if len(mac_address) != 12:

            raise ValueError("Dirección MAC inválida")

  

        magic_packet = bytes.fromhex('FF' * 6 + mac_address * 16)

  

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            sock.sendto(magic_packet, ('<DIRECCION_BROADCAST>', 9))

  

class WakeOnLanApp(App):

    def build(self):

        Window.clearcolor = (0, 0, 0, 1)  # Fondo negro completo

        return TerminalLayout()

  

if __name__ == '__main__':

    WakeOnLanApp().run()
```

Le damos a ejecutar, escribimos `Power` y con esto se encenderia el equipo.
