# 🌸 ME-DATOS - Parcial: Torre de Hanoi (Edición Sakura)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Ursina Engine](https://img.shields.io/badge/Engine-Ursina%202.5D-ff69b4)
![Estructura de Datos](https://img.shields.io/badge/Estructura-Pilas%20(LIFO)-success)
![Estado](https://img.shields.io/badge/Proyecto-Evaluaci%C3%B3n%20Parcial-amber)

Implementación interactiva en **2D / 2.5D** del clásico rompecabezas matemático y algorítmico **Torre de Hanoi**, desarrollada en **Python** con **Ursina Engine** para la cátedra de **Estructuras de Datos**.

El proyecto cuenta con un **motor gráfico 100% procedural y vectorial**: el paisaje japonés (cielo, montañas, pagoda, lago, flores de cerezo), los menús, las estrellas de 5 puntas y los discos se dibujan mediante código y geometría matemática en tiempo de ejecución, **sin depender de imágenes externas (`.png`/`.jpg`)**.

---

## 🛠️ Requisitos e Instalación

Para que el proyecto funcione en cualquier computadora solo necesitas **Python 3.8 o superior** y la librería `ursina`.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Juanh3rn4nd3z/ME-DATOS-Parcial-Torre-de-Hanoi-.git](https://github.com/Juanh3rn4nd3z/ME-DATOS-Parcial-Torre-de-Hanoi-.git)
cd ME-DATOS-Parcial-Torre-de-Hanoi-
```

### 2. Instalar la dependencia necesaria
```bash
pip install ursina
```

### 3. Ejecutar el juego
```bash
python main.py
```
*(Si tu archivo `.py` tiene otro nombre, reemplaza `main.py` por el nombre correspondiente).*

---

## 🧠 Explicación Detallada por Secciones y Cómo Modificar Cada Apartado

El código está dividido en **11 secciones comentadas**. A continuación se explica qué hace cada una y **cómo modificarla en vivo si lo solicitan durante la evaluación** sin que el código colapse:

---

### 1. Configuración Inicial y Paleta de Colores (`# 1. CONFIGURACIÓN INICIAL...`)
**¿En qué consiste?**
* Inicia el motor con `app = Ursina()`, asigna el título de la ventana y oculta los contadores técnicos (`fps_counter`, `entity_counter`).
* Activa la **Cámara 2D Ortográfica** (`camera.orthographic = True`, `camera.fov = 11.2`) para trabajar en un plano 2D exacto sin deformación de perspectiva.
* Define `c_rgb(r, g, b, a)` para convertir colores RGB tradicionales (`0-255`) al formato decimal de Ursina (`0.0-1.0`), y declara toda la paleta de colores del paisaje, botones y la lista `COLORES_DISCOS`.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar el título de la ventana o activar los FPS:**
  ```python
  window.title = "Torre de Hanoi - Mi Versión"
  window.fps_counter.enabled = True  # Cambiar False a True si piden ver los FPS
  ```
* **Hacer zoom in / zoom out a todo el escenario de juego:**
  Modifica `camera.fov = 11.2`. Si pones un número mayor (ej. `14.0`) la cámara se aleja; si pones uno menor (ej. `9.0`) se acerca.
* **Cambiar los colores de los discos:**
  Edita los valores RGB dentro de la lista `COLORES_DISCOS`:
  ```python
  COLORES_DISCOS = [
      c_rgb(255, 0, 0),    # Disco 1 (Rojo puro)
      c_rgb(0, 255, 0),    # Disco 2 (Verde puro)
      # ... puedes cambiar cualquiera o agregar más líneas c_rgb(R, G, B)
  ]
  ```
* **⚠️ Qué NO tocar para evitar colapsos:** No borres la función `c_rgb()`, ya que todas las variables de color del script dependen de ella.

---

### 2. Variables Globales y Progreso de Estrellas (`# 2. VARIABLES GLOBALES...`)
**¿En qué consiste?**
* Es la memoria del programa y donde se define la **Estructura de Datos principal**: `torres = [[], [], []]`, que representa las 3 torres como **Pilas (Stacks LIFO)**.
* Define `config_discos` (cuántos discos tiene cada nivel por dificultad), `estrellas_progreso` (estrellas ganadas por nivel) y las medidas físicas como `posiciones_x = [-4.3, 0.0, 4.3]` y `ALTO_DISCO = 0.44`.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar la cantidad de discos de un nivel específico:**
  Busca el diccionario `config_discos` y cambia los números de la lista (cada posición es un nivel del 1 al 5):
  ```python
  config_discos = {
      "Fácil":   [2, 3, 4, 5, 6], # Ejemplo: hacer que el Nivel 1 de Fácil empiece con 2 discos
      "Medio":   [4, 5, 5, 6, 6],
      "Difícil": [5, 6, 7, 7, 8]
  }
  ```
* **Empezar el juego con todas las estrellas desbloqueadas (para pruebas):**
  Cambia los `0` por `3` en `estrellas_progreso`:
  ```python
  estrellas_progreso = {
      "Fácil":   [3, 3, 3, 3, 3],
      "Medio":   [3, 3, 3, 3, 3],
      "Difícil": [3, 3, 3, 3, 3]
  }
  ```
* **Separar o juntar más las 3 torres:**
  Cambia `posiciones_x = [-4.3, 0.0, 4.3]` por `[-5.0, 0.0, 5.0]` (más separadas) o `[-3.5, 0.0, 3.5]` (más juntas).
* **⚠️ Qué NO tocar para evitar colapsos:** `config_discos` y `estrellas_progreso` deben tener **siempre 5 elementos por lista**. Si borras o agregas un elemento en una sola lista sin actualizar la otra, provocará un `IndexError`. Si pones más de `8` discos en un nivel, baja `ALTO_DISCO = 0.30` para que no se salgan del poste.

---

### 3. Componentes Gráficos Vectoriales (`# 3. COMPONENTES GRÁFICOS...`)
**¿En qué consiste?**
* Son las funciones constructoras que dibujan el arte sin imágenes: `_crear_malla_estrella()` genera el modelo geométrico de las estrellas con trigonometría (`sin`/`cos`), `crear_capsula()` une un rectángulo y dos círculos para hacer bordes curvos, `crear_panel_redondeado()` arma las cajas de la interfaz y `crear_boton_pildora_menu()` crea los botones con sombra e interacción.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Hacer las estrellas más puntiagudas o más rellenas:**
  En `def _crear_malla_estrella(R=0.5, r=0.2):`, `R` es la punta exterior y `r` el centro interior. Si cambias `r=0.12`, las estrellas se verán mucho más afiladas; si pones `r=0.35`, se verán más gorditas.
* **Hacer los paneles más cuadrados o más redondos:**
  En `def crear_panel_redondeado(..., radio=0.045):`, disminuye `radio=0.015` para esquinas casi cuadradas.
* **⚠️ Qué NO tocar para evitar colapsos:** En `_crear_malla_estrella()`, no modifiques el `range(10)` ni la lista `tris`, ya que la malla triangular (`Mesh`) requiere exactamente 10 vértices perimetrales cerrados para no corromper el renderizado de OpenGL.

---

### 4. Paisaje de Fondo (`# 4. PAISAJE DE FONDO`)
**¿En qué consiste?**
* Dibuja en el fondo (`z = 10`) el cielo, el sol, las montañas, la pagoda de 5 pisos, el lago con reflejos y las ramas de cerezo.
* Crea la lista `petalos_sakura` con 22 pétalos animados y declara los 5 contenedores de pantallas (`menu_principal_ui`, `menu_estrellas_ui`, `menu_ayuda_ui`, `juego_ui`, `mundo_juego_2d`).

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Aumentar o disminuir la cantidad de pétalos cayendo:**
  Busca `for _ in range(22):` y cambia `22` por `50` (lluvia intensa de pétalos) o `5` (pocos pétalos).
* **Hacer que los pétalos caigan más rápido:**
  Dentro de ese mismo ciclo, modifica `pet.vel_y = random.uniform(0.025, 0.055)` a valores mayores como `random.uniform(0.08, 0.15)`.
* **Cambiar la cantidad de pisos de la pagoda del fondo:**
  Busca `for piso in range(5):` y cámbialo a `range(3)` o `range(7)`.
* **⚠️ Qué NO tocar para evitar colapsos:** **Nunca** agregues `parent=camera.ui` a `fondo_paisaje`. Debe quedarse en el mundo general con `position=(0, 0, 10)` para mantenerse detrás de las torres.

---

### 5. Pantalla 1: Menú Principal (`# 5. PANTALLA 1: MENÚ PRINCIPAL`)
**¿En qué consiste?**
* Construye la pantalla inicial: el banner superior con el título y la miniatura de Hanoi, los 5 botones izquierdos (*Iniciar Juego, Dificultad, Mis Estrellas, Cómo Jugar, Salir*) y el panel derecho con los 15 botones circulares para elegir nivel directamente.
* Incluye `actualizar_selector_menu()` y `cambiar_dificultad(delta)`.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar el título o subtítulo del menú:**
  Busca las líneas `Text(parent=menu_principal_ui, text="Torre de Hanoi"...` y `text="Ordena los discos, alcanza la cima"` y edita el string `text="..."`.
* **Cambiar el texto o color de un botón del menú:**
  En `btn_iniciar = crear_boton_pildora_menu(...)`, puedes cambiar `"Iniciar Juego"` por `"Jugar Ahora"` o cambiar `col_prin=BTN_AMARILLO` por `BTN_VERDE`.
* **⚠️ Qué NO tocar para evitar colapsos:** En la función `seleccionar_nivel_circular(d_i=idx_d, niv=n):`, no borres los parámetros por defecto `d_i=idx_d, niv=n`, ya que en Python son necesarios para capturar el valor correcto dentro de un ciclo `for` (*late binding closure*).

---

### 6. Pantalla 2: Tus Estrellas (`# 6. PANTALLA 2: TUS ESTRELLAS`)
**¿En qué consiste?**
* Dibuja la galería de trofeos donde se ven las 3 columnas (*Fácil, Medio, Difícil*), el puntaje acumulado por dificultad (`0 / 15`) y el total general (`0 / 45`).
* La función `actualizar_vista_estrellas()` suma los puntos de `estrellas_progreso` y enciende las estrellas doradas correspondientes.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar los textos o encabezados de la pantalla de estrellas:**
  Edita el texto en `Text(parent=menu_estrellas_ui, text="Tus Estrellas"...` o el mensaje motivacional `"¡Sigue jugando para obtener más estrellas!"`.
* **⚠️ Qué NO tocar para evitar colapsos:** No modifiques la estructura de la tupla `ui_columnas_estrellas[nom_dif] = (lbl_sub_col, filas_estrellas_col)`, porque `actualizar_vista_estrellas()` la desempaqueta directamente al ganar cada partida.

---

### 7. Pantalla 3: Cómo Jugar (`# 7. PANTALLA 3: CÓMO JUGAR`)
**¿En qué consiste?**
* Crea la ventana de instrucciones con las 4 reglas del juego y el botón `"Volver al Menú"`.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Agregar tu nombre de autor, carnet o una regla nueva en pantalla:**
  Solo edita el bloque de texto dentro de `Text(parent=menu_ayuda_ui, text=(...))` agregando una línea nueva con `\n` al final.

---

### 8. Escenario de Juego 2.5D y HUD (`# 8. ESCENARIO DE JUEGO 2.5D Y HUD`)
**¿En qué consiste?**
* Construye la mesa de madera, genera con un ciclo `for` los 3 postes (`Torre A`, `Torre B`, `Torre C`), crea los `hologramas_postes` (indicadores verde/rojo) y arma la barra superior (HUD) con el nivel, cronómetro, movimientos, estrellas en vivo y meta.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar el nombre de las torres (ej. "Origen", "Auxiliar", "Destino"):**
  Busca la lista `etiquetas_torres` y cámbiala:
  ```python
  etiquetas_torres = ["Origen", "Auxiliar", "Destino"]
  ```
* **Hacer los postes más altos o más gruesos:**
  Modifica `ALTURA_POSTE = 3.85` o `ANCHO_POSTE = 0.54`.
* **⚠️ Qué NO tocar para evitar colapsos:** No elimines `hologramas_postes.append(ghost)` dentro del ciclo `for`, ya que el sistema de arrastrar y soltar busca exactamente 3 hologramas (índices 0, 1 y 2).

---

### 9. Lógica de Juego, Discos y Arrastrar y Soltar (`# 9. LÓGICA DE JUEGO...`)
**¿En qué consiste?**
* Es el corazón matemático y algorítmico del juego:
  * `calcular_estrellas_actuales()`: Usa la fórmula óptima **`(2 ** NUM_DISCOS) - 1`** para decidir si mereces 3, 2 o 1 estrella según tus movimientos.
  * `construir_nivel()`: Destruye los discos anteriores, crea los nuevos de mayor a menor y los apila en `torres[0]` (Torre A).
  * `verificar_victoria()`: Revisa si todos los discos llegaron a la Torre C (`len(torres[2]) == NUM_DISCOS`).

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Hacer que solo den 3 estrellas si el jugador hace el mínimo exacto de movimientos (0 errores):**
  En `calcular_estrellas_actuales()`, cambia `lim_3`:
  ```python
  def calcular_estrellas_actuales():
      mov_optimos = (2 ** NUM_DISCOS) - 1
      lim_3 = mov_optimos       # Antes daba margen extra; así exige perfección absoluta
      lim_2 = mov_optimos + 5   # 2 estrellas si se pasa por máximo 5 movimientos
  ```
* **Cambiar la torre donde se gana el juego (ej. ganar en la Torre B en vez de la Torre C):**
  En `verificar_victoria()`, cambia el índice `2` por `1`:
  ```python
  if len(torres[1]) == NUM_DISCOS:  # 0 = Torre A, 1 = Torre B, 2 = Torre C
  ```
* **Hacer que los discos empiecen en otra torre (ej. empezar en la Torre B):**
  En `construir_nivel()`, cambia `posiciones_x[0]` por `posiciones_x[1]` y `torres[0].append(disco)` por `torres[1].append(disco)`.
* **Mostrar el número de tamaño encima de cada disco:**
  Dentro del ciclo `for i in range(NUM_DISCOS):` de `construir_nivel()`, puedes agregar al final:
  ```python
  Text(parent=disco, text=str(tam_val), position=(0, 0, -0.05), origin=(0, 0), scale=8, color=color.white)
  ```
* **⚠️ Qué NO tocar para evitar colapsos:** En `construir_nivel()`, **jamás borres** el ciclo `for d in todos_discos: destroy(d)`. Si solo haces `todos_discos.clear()` sin `destroy(d)`, los discos del nivel anterior se quedarán dibujados en pantalla para siempre.

---

### 10. Navegación entre Pantallas y Control del Mouse (`# 10. NAVEGACIÓN...`)
**¿En qué consiste?**
* Conecta los botones con las funciones de cambio de pantalla y gestiona el evento `input(key)` del mouse:
  * Con `"left mouse down"`: toma únicamente el disco en la cima de la pila (`t[-1]`).
  * Con `"left mouse up"`: verifica la **Regla de Oro de Hanoi** (`len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor`). Si se cumple, hace `.pop()` en la torre origen y `.append()` en la torre destino.

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Permitir una "trampa" de prueba (poder poner discos grandes sobre pequeños):**
  Si el profesor te pide demostrar qué pasa si se desactiva la regla de Hanoi, en `input(key)` busca:
  ```python
  if len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor:
  ```
  Y cámbialo temporalmente por:
  ```python
  if True:  # Acepta cualquier disco sin importar el tamaño
  ```
* **Agregar una tecla rápida en el teclado (ej. presionar `"r"` para reiniciar el nivel):**
  Al inicio de `def input(key):`, puedes agregar:
  ```python
  if key == "r" and mundo_juego_2d.enabled:
      construir_nivel()
  ```
* **⚠️ Qué NO tocar para evitar colapsos:** Nunca quites la validación `if len(t) > 0:` antes de consultar `disco_sup = t[-1]`. Intentar leer `t[-1]` en una torre vacía detendrá el programa inmediatamente con un `IndexError`.

---

### 11. Bucle Principal de Animación (`# 11. BUCLE PRINCIPAL DE ANIMACIÓN`)
**¿En qué consiste?**
* La función `update()` se ejecuta cada fotograma (~60 veces por segundo). Mueve los pétalos de Sakura, suma segundos al cronómetro, actualiza la posición del holograma verde/rojo mientras arrastras un disco, suaviza el movimiento de los discos con `lerp()` y anima las partículas (ondas de choque y fuegos artificiales).

**🔧 ¿Cómo modificar este apartado si lo piden?**
* **Cambiar la velocidad con la que los discos se deslizan hacia el poste al soltarlos:**
  Busca la línea:
  ```python
  d.position = lerp(d.position, d.target_pos, time.dt * 14)
  ```
  Cambia `14` por `30` para que se acomoden casi instantáneamente, o por `5` para un efecto en cámara lenta.
* **Poner un límite de tiempo (ej. perder o reiniciar si pasa de 60 segundos):**
  Dentro de `if cronometro_activo and not juego_terminado:`, después de `tiempo += time.dt`, puedes agregar:
  ```python
  if tiempo >= 60.0:
      mensaje.text = "¡Se acabó el tiempo! Reiniciando..."
      construir_nivel()
  ```
* **⚠️ Qué NO tocar para evitar colapsos:** En los ciclos `for onda in ondas_choque[:]:` y `for p in particulas_efecto[:]:`, **nunca borres los corchetes `[:]`**. Esos corchetes crean una copia de la lista para poder eliminar partículas con `.remove()` sin corromper el ciclo `for` en plena ejecución. Tampoco borres `app.run()` al final del archivo.

---

#
