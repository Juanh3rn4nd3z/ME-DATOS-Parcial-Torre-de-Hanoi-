# ME-DATOS-Parcial-Torre-de-Hanoi-

# 🌸 Torre de Hanoi - Edición Sakura

Una implementación interactiva en **2D / 2.5D** del clásico rompecabezas matemático y algorítmico **Torre de Hanoi**, desarrollada en **Python** utilizando **Ursina Engine**. 

Destaca por contar con un **motor gráfico 100% procedural y vectorial**: absolutamente todo el paisaje japonés (montañas, pagoda, lago, flores de cerezo), los menús, las estrellas de 5 puntas y los discos se generan mediante código y mallas geométricas en tiempo de ejecución, **sin depender de imágenes (`.png`/`.jpg`) ni archivos externos** que puedan perderse al clonar el repositorio.

---

## ✨ Características Principales

* **Arte Procedural Dinámico:** Paisaje de atardecer con caída animada de pétalos de Sakura, ondas de choque al soltar discos y fuegos artificiales al ganar.
* **Sistema de Progreso y Dificultad:** 3 niveles de dificultad (*Fácil, Medio, Difícil*) con 5 niveles cada uno (15 niveles en total y hasta 45 estrellas coleccionables).
* **Mecánica Drag & Drop con Validación en Vivo:** Arrastra discos con el mouse con previsualización holográfica en cada poste (**Verde** = movimiento válido, **Rojo** = movimiento inválido).
* **Cálculo Algorítmico de Eficiencia:** Evaluación en tiempo real basada en la fórmula matemática óptima de Hanoi ($2^n - 1$ movimientos).
* **Interfaz Completa Integrada:** Menú principal interactivo, selector rápido de niveles, galería de estrellas ("Tus Estrellas"), pantalla de instrucciones ("Cómo Jugar") y HUD en partida con cronómetro y contador de movimientos.

---

## 🛠️ Requisitos e Instalación

Para ejecutar este proyecto no necesitas descargar texturas ni recursos adicionales; solo necesitas **Python 3.8 o superior** y la librería `ursina`.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO
```

### 2. Crear un entorno virtual (Opcional pero recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install ursina
```

### 4. Ejecutar el juego
```bash
python main.py
```
*(Reemplaza `main.py` por el nombre exacto de tu archivo `.py`).*

---

## 🧠 ¿En qué consiste el código y cómo funciona?

El proyecto está diseñado en un único script modular dividido en **11 bloques lógicos**:

### 1. Configuración y Cámara Ortográfica (Secciones 1 y 2)
* Configura la ventana de Ursina y establece una cámara **2D Ortográfica** (`camera.orthographic = True`, `camera.fov = 11.2`). Esto evita la distorsión de perspectiva 3D y permite manejar coordenadas cartesianas limpias.
* Define la función auxiliar `c_rgb(r, g, b, a)` para convertir valores RGB estándar (0–255) al formato normalizado (0.0–1.0) que exige Ursina.

### 2. Motor de Gráficos Vectoriales (Secciones 3 y 4)
* **`_crear_malla_estrella()`:** Construye una malla poligonal (`Mesh`) personalizada calculando vértices con trigonometría ($\sin$ y $\cos$) para alternar entre el radio exterior e interior de una estrella de 5 puntas.
* **Primitivas compuestas (`crear_capsula`, `crear_panel_redondeado`):** Combina rectángulos (`quad`) y círculos (`circle`) en los extremos para crear botones tipo píldora, paneles con bordes redondeados y discos biselados sin usar imágenes.

### 3. Sistema de Vistas y UI (Secciones 5, 6, 7 y 8)
* Utiliza contenedores padre (`Entity(parent=camera.ui)`) para separar cada pantalla (`menu_principal_ui`, `menu_estrellas_ui`, `menu_ayuda_ui`, `juego_ui`). Cambiar de pantalla consiste simplemente en alternar la propiedad `.enabled = True/False` de cada contenedor.

### 4. Estructuras de Datos y Lógica de Hanoi (Secciones 9 y 10)
* **Pilas (LIFO - *Last In, First Out*):** Las 3 torres se representan mediante la lista de listas `torres = [[], [], []]`.
  * El disco superior de una torre siempre es `torres[i][-1]`.
  * Al levantar y mover un disco válido, se extrae de la torre origen con `.pop()` y se apila en la torre destino con `.append()`.
* **Regla de validación:** Cada entidad disco almacena el atributo `disco.valor` (donde 1 es el más pequeño y $N$ el más grande). Un movimiento hacia `torre_dest` solo se aprueba si:
  ```python
  len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor
  ```
* **Sistema de Estrellas:** Se calcula el mínimo teórico de movimientos con `mov_optimos = (2 ** NUM_DISCOS) - 1`. Si el jugador termina dentro del margen del 40% extra obtiene **3 estrellas**; dentro del 125% extra obtiene **2 estrellas**; si supera ese límite obtiene **1 estrella**.

### 5. Bucle Principal y Físicas Suaves (`update()` - Sección 11)
* Se ejecuta en cada fotograma (`time.dt`):
  * Mueve y rota los pétalos de Sakura mediante funciones senoidales (`math.sin`).
  * Actualiza el cronómetro de la partida.
  * Aplica **interpolación lineal (`lerp`)** a la posición de los discos (`d.position = lerp(d.position, d.target_pos, time.dt * 14)`), logrando que los discos se deslicen suavemente hacia su poste al soltarlos en lugar de teletransportarse bruscamente.

---

## 🔧 Guía de Modificación Rápida (Qué cambiar si te lo piden)

Si durante una revisión o defensa del proyecto te piden hacer cambios en vivo, aquí tienes exactamente qué tocar:

| ¿Qué te piden cambiar? | Variable / Función a buscar | Cómo modificarlo de forma segura |
| :--- | :--- | :--- |
| **Cantidad de discos por nivel** | Diccionario `config_discos` *(Sección 2)* | Cambia los números dentro de las listas `[3, 3, 4, 4, 5]`. Mantén valores entre `2` y `8`. |
| **Colores de los discos** | Lista `COLORES_DISCOS` *(Sección 1)* | Modifica los valores `c_rgb(R, G, B)` o agrega más colores a la lista. |
| **Exigencia para ganar 3 estrellas** | Función `calcular_estrellas_actuales()` *(Sección 9)* | Para exigir perfección absoluta en 3 estrellas, cambia `lim_3` a: `lim_3 = mov_optimos`. |
| **Velocidad al soltar los discos** | Función `update()` *(Sección 11)* | Busca `lerp(d.position, d.target_pos, time.dt * 14)`. Sube `14` a `25` para que sea más rápido, o bájalo a `6` para cámara lenta. |
| **Velocidad de caída de los pétalos** | Bucle `for _ in range(22):` *(Sección 4)* | Ajusta `pet.vel_y = random.uniform(0.025, 0.055)` a valores más altos si quieres viento fuerte. |
| **Posición o separación de postes** | Lista `posiciones_x = [-4.3, 0.0, 4.3]` *(Sección 2)* | Modifica las coordenadas X de la Torre A, B y C. |

---

## ⚠️ Reglas de Seguridad (Cómo evitar que el código colapse)

Para garantizar que el juego nunca sufra cierres inesperados (*crashes*) ni bugs visuales al editarlo, respeta estas 5 reglas críticas de arquitectura:

1. **Sincronía entre `config_discos` y `estrellas_progreso`:**
   Cada dificultad en `config_discos` tiene una lista de **exactamente 5 elementos** (5 niveles). Si agregas un 6.º nivel a `config_discos`, **DEBES** agregar un sexto `0` en `estrellas_progreso` y ajustar los bucles `range(1, 6)` y `range(5)` de la interfaz, o el programa lanzará un `IndexError: list index out of range`.
2. **Límite físico de discos (`Máximo recomendado: 8`):**
   El alto de cada disco es `ALTO_DISCO = 0.44` y la altura del poste es `ALTURA_POSTE = 3.85`. Si configuras un nivel con 10 o más discos sin reducir `ALTO_DISCO`, la torre de discos rebasará la punta del poste y se superpondrá con el HUD superior. *(Nota: si pones más de 8 discos, el código NO colapsará por falta de colores gracias al operador módulo `% len(COLORES_DISCOS)`, que recicla la paleta automáticamente).*
3. **NUNCA pongas `fondo_paisaje` como hijo de `camera.ui`:**
   El paisaje de fondo (`fondo_paisaje`) vive en el espacio del mundo con profundidad `z = 10` (detrás de las torres que están entre `z = 0.93` y `z = 0.1`). Si lo asignas a `parent=camera.ui`, pasará a la capa superficial de interfaz y tapará por completo los postes y los discos.
4. **Destrucción de entidades en Ursina (`destroy()` vs `.clear()`):**
   En `construir_nivel()`, primero se ejecuta `for d in todos_discos: destroy(d)` y luego `todos_discos.clear()`. **Nunca borres el bucle `destroy(d)`**: vaciar solo la lista de Python con `.clear()` deja las entidades gráficas fantasma renderizándose en pantalla para siempre y satura la memoria.
5. **Eliminación segura en listas de partículas (`[:]`):**
   En `update()`, las ondas de choque y fuegos artificiales se recorren usando una copia superficial de la lista (`for onda in ondas_choque[:]:`). No quites los corchetes `[:]`, ya que eliminar elementos de una lista mientras la estás iterando en Python altera los índices y provoca saltos o errores en tiempo de ejecución.
