# RP2040 MacroPad StreamDeck

MacroPad / StreamDeck casero basado en RP2040 usando CircuitPython.

## Incluye

* 9 botones programables
* Pantalla OLED SSD1306
* Encoder EC11
* Control multimedia
* Macros para programación
* Macros Git y SQL
* Compatible con Windows, Linux y macOS

---

# 📁 Estructura del proyecto

```txt
/
├── code.py
├── lib/
├── stl/
└── README.md
```

## 📂 Carpeta `stl`

La carpeta `stl` contiene todos los archivos `.STL` listos para impresión 3D.

### Incluye

* Base del MacroPad
* Tapa superior
* Perilla del encoder
* Soporte OLED
* Piezas adicionales

---

# 🔧 Componentes necesarios

## Electrónica

* 1x RP2040 Zero o Raspberry Pi Pico
* 1x Pantalla OLED SSD1306 128x64 I2C
* 1x Encoder rotatorio EC11
* 9x Pulsadores mecánicos
* 9x Keycaps
* Cable USB
* Cables Dupont
* Estaño y cautín

---

# 💾 Instalación de CircuitPython

## 1. Descargar CircuitPython

Ir a:

```txt
https://circuitpython.org/downloads
```

Buscar tu placa RP2040 y descargar el archivo `.uf2`.

---

## 2. Entrar en modo BOOTSEL

1. Mantener presionado el botón `BOOT`
2. Conectar el USB
3. Soltar el botón

Aparecerá una unidad llamada:

```txt
RPI-RP2
```

---

## 3. Instalar

Arrastrar el archivo `.uf2` descargado dentro de `RPI-RP2`.

La placa se reiniciará automáticamente.

Luego aparecerá:

```txt
CIRCUITPY
```

---

# 📚 Instalar librerías

Dentro de `CIRCUITPY` crear una carpeta llamada:

```txt
lib
```

Copiar dentro:

* `adafruit_hid`
* `adafruit_ssd1306`

Descargar desde:

```txt
https://circuitpython.org/libraries
```

---

# 📄 Instalar el código

Copiar:

```txt
code.py
```

Dentro de `CIRCUITPY`.

CircuitPython ejecutará automáticamente el archivo.

---

# 🔌 Conexiones

# 🖥 OLED SSD1306

| OLED | RP2040 |
| ---- | ------ |
| VCC  | 3.3V   |
| GND  | GND    |
| SDA  | GP0    |
| SCL  | GP1    |

---

# 🎛 Encoder EC11

| Pin EC11   | RP2040 |
| ---------- | ------ |
| CLK        | GP18   |
| DT         | GP19   |
| SW / CLICK | GP11   |
| GND        | GND    |
| GND        | GND    |

---

# ⌨ Conexión de botones

Todos los botones usan:

* 1 GPIO
* 1 conexión a GND

Todos comparten el mismo GND.

---

# 🔥 Soldar botones uno por uno

## Botón 1 → GP2

* Una pata → GP2
* Otra pata → GND

---

## Botón 2 → GP3

* Una pata → GP3
* Otra pata → GND

---

## Botón 3 → GP4

* Una pata → GP4
* Otra pata → GND

---

## Botón 4 → GP5

* Una pata → GP5
* Otra pata → GND

---

## Botón 5 → GP6

* Una pata → GP6
* Otra pata → GND

---

## Botón 6 → GP7

* Una pata → GP7
* Otra pata → GND

---

## Botón 7 → GP8

* Una pata → GP8
* Otra pata → GND

---

## Botón 8 → GP9

* Una pata → GP9
* Otra pata → GND

---

## Botón 9 → GP10

* Una pata → GP10
* Otra pata → GND

---

# ⚡ Importante

El código usa:

```python
Pull.UP
```

Eso significa:

* El botón normalmente está en HIGH
* Cuando se presiona:

  * Se conecta a GND
  * Cambia a LOW

Por eso todos los botones deben ir a GND.

---

# 📺 Páginas incluidas

## MULTIMEDIA

* Volumen
* Play/Pause
* Next
* Previous
* Mute

---

## MEDIA WEB

Atajos para:

* YouTube
* Spotify Web
* Twitch

---

## CODE

Macros para programación:

* Save
* Undo
* Redo
* Copy/Paste
* Command Palette

---

## BROWSER

* Nueva pestaña
* Cerrar pestaña
* Cambiar tabs
* Incógnito

---

## WINDOWS

* Desktop
* Task View
* Ejecutar
* Snipping Tool
* Task Manager

---

## STREAM

Macros pensadas para OBS o streaming.

---

## GIT

Macros rápidas:

```bash
git add .
git commit -m ""
git push
git pull
```

---

## SQL

Macros SQL:

```sql
SELECT
UPDATE
DELETE
ROLLBACK
```

---

# 🖨 Configuración recomendada para impresión 3D

## Material

```txt
PLA
```

## Altura de capa

```txt
0.2mm
```

## Infill

```txt
15% - 20%
```

---

# 🚀 Personalización

Puedes modificar:

```python
pages = [
]
```

Para agregar:

* Nuevos atajos
* Macros
* Comandos
* Texto automático
* Controles multimedia

---

# 🛠 Posibles mejoras

* RGB LEDs
* Más botones
* Integración Home Assistant
* WiFi con ESP32
* Animaciones OLED
* Integración OBS

---

# 📌 Solución de problemas

## OLED no funciona

Revisar:

* Dirección I2C (`0x3C`)
* SDA/SCL
* Alimentación 3.3V

---

## Botón queda presionado

Revisar:

* Soldaduras
* Cortos
* Conexión correcta a GND

---

# ✅ Final

Al conectar el MacroPad al PC:

* Se detecta como teclado USB HID
* No necesita drivers

## Compatible con

* Windows
* Linux
* macOS
  
---

---

# ❤️ Créditos

Parte de la inspiración del proyecto, ideas base y algunos archivos STL fueron tomados y adaptados desde el proyecto original de Jason Giroux:

- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}

Muchas gracias al proyecto original por compartir el diseño y la idea con la comunidad maker.  
