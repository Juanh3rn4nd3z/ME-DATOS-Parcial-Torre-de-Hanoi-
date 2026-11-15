# ME-DATOS-Parcial-Torre-de-Hanoi-

# 🌸 Torre de Hanoi - Edición Sakura | Parcial ME-DATOS

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ursina Engine](https://img.shields.io/badge/Ursina_Engine-2D%2F2.5D-FF69B4?style=for-the-badge)
![Estructura de Datos](https://img.shields.io/badge/TDA-Pilas_(LIFO)-4CAF50?style=for-the-badge)

Proyecto práctico para la evaluación parcial de **Manejo y Estructura de Datos (ME-DATOS)**. Consiste en una implementación interactiva en **2D / 2.5D** del clásico problema matemático y algorítmico de la **Torre de Hanoi**, desarrollada en **Python** con el motor gráfico **Ursina Engine**.

El proyecto destaca por su **arquitectura 100% procedural y vectorial**: todo el entorno visual (paisaje japonés de atardecer, pagoda, flores de cerezo, mallas geométricas de estrellas, paneles redondeados y discos) se construye mediante algoritmos geométricos en tiempo de ejecución, **sin depender de texturas ni imágenes externas (`.png`/`.jpg`)**, garantizando que el repositorio funcione en cualquier computadora inmediatamente después de clonarlo.

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para clonar y ejecutar el proyecto localmente:

### 1. Clonar este repositorio
```bash
git clone [https://github.com/Juanh3rn4nd3z/ME-DATOS-Parcial-Torre-de-Hanoi-.git](https://github.com/Juanh3rn4nd3z/ME-DATOS-Parcial-Torre-de-Hanoi-.git)
cd ME-DATOS-Parcial-Torre-de-Hanoi-
```

### 2. Crear y activar un entorno virtual (Opcional pero recomendado)
```bash
python -m venv venv
# En Windows (PowerShell / CMD):
venv\Scripts\activate
# En Linux / macOS:
source venv/bin/activate
```

### 3. Instalar la dependencia requerida (`ursina`)
```bash
pip install ursina
```

### 4. Ejecutar la aplicación
```bash
python main.py
```
*(Nota: Si tu archivo principal tiene otro nombre en el repositorio, como `hanoi.py` o `torre_hanoi.py`, reemplaza `main.py` por ese nombre).*

---

## 🗂️ Fundamento en Estructuras de Datos (Enfoque ME-DATOS)

El núcleo lógico del juego modela las tres torres como **Pilas (*Stacks*)** bajo el principio **LIFO (*Last In, First Out* — Último en entrar, primero en salir)**:

1. **Representación en Memoria (`torres = [[], [], []]`):**
   * Cada sublista representa uno de los tres postes (**Torre A** = `torres[0]`, **Torre B** = `torres[1]`, **Torre C** = `torres[2]`).
   * Al iniciar un nivel en `construir_nivel()`, los discos se insertan desde el más grande (`valor = NUM_DISCOS`) hasta el más pequeño (`valor = 1`) en `torres[0]`.
2. **Inspección de la Cima (*Peek* — `torres[idx][-1]`):**
   * En la función `input(key)`, cuando el jugador hace clic izquierdo (`left mouse down`), el algoritmo **solo evalúa colisión con `t[-1]`** (el elemento en el tope de cada pila). Los discos inferiores quedan bloqueados estructuralmente, cumpliendo la regla de que solo se puede mover un disco a la vez y únicamente el que está arriba.
3. **Validación de Regla de Ordenamiento:**
   * Antes de permitir que el disco arrastrado se suelte en la torre destino (`torre_dest`), se verifica:
     ```python
     if len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor:
         movimiento_valido = True
     ```
   * Esto impide colocar un nodo de mayor peso (`valor`) sobre uno de menor peso.
4. **Operaciones *Pop* (Desapilar) y *Push* (Apilar):**
   * Si el movimiento es válido, se ejecuta la transición entre pilas en tiempo constante $O(1)$:
     ```python
     torres[torre_origen_arrastre].pop()              # Desapila de la torre origen
     torres[idx_destino].append(disco_arrastrado)     # Apila en la torre destino
     ```
5. **Complejidad Algorítmica y Sistema de Estrellas ($2^n - 1$):**
   * El número mínimo de movimientos necesarios para trasladar $n$ discos de la Torre A a la Torre C está dado por la recurrencia matemática $T(n) = 2^n - 1$.
   * La función `calcular_estrellas_actuales()` compara en vivo los movimientos del usuario contra `mov_optimos = (2 ** NUM_DISCOS) - 1` para otorgar **3, 2 o 1 estrella**.

---

## ⚙️ Arquitectura del Código (Secciones 1 a 11)

El código fuente está organizado secuencialmente en **11 secciones modulares**:

* **Sección 1 (`Configuración y Paleta`):** Inicializa `Ursina()`, configura una cámara **2D Ortográfica** (`camera.orthographic = True`, `fov = 11.2`) y define la función `c_rgb()` junto con todas las constantes de color.
* **Sección 2 (`Variables Globales y Progreso`):** Define las dificultades (`Fácil`, `Medio`, `Difícil`), la matriz de cantidad de discos por nivel (`config_discos`), el diccionario de récord de estrellas (`estrellas_progreso`) y las pilas de juego (`torres`).
* **Sección 3 (`Componentes Gráficos Vectoriales`):** Construye geometría mediante código:
  * `_crear_malla_estrella()`: Genera un objeto `Mesh` calculando 10 vértices trigonométricos para dibujar estrellas de 5 puntas.
  * `crear_capsula()` y `crear_panel_redondeado()`: Combinan `quad` y `circle` para renderizar botones píldora, discos redondeados y paneles UI con sombras.
* **Sección 4 (`Paisaje de Fondo`):** Crea el escenario Sakura en el plano `z = 10` con cielo degradado, montañas, pagoda de 5 pisos, lago con reflejos y 22 pétalos animados.
* **Secciones 5, 6 y 7 (`Menú Principal`, `Tus Estrellas`, `Cómo Jugar`):** Construyen las interfaces gráficas ancladas a `camera.ui` y el selector circular rápido de los 15 niveles.
* **Sección 8 (`Escenario 2.5D y HUD`):** Genera la base de madera, los 3 postes con iluminación lateral, los hologramas de validación (`hologramas_postes`) y la barra superior de estadísticas (nivel, cronómetro, movimientos, estrellas en vivo y meta óptima).
* **Sección 9 (`Lógica de Juego y Construcción de Nivel`):** Contiene `construir_nivel()`, `verificar_victoria()`, `crear_onda_choque()` y el sistema de partículas `lanzar_fuegos_artificiales()`.
* **Sección 10 (`Navegación y Eventos de Mouse`):** Gestiona el cambio de vistas y la función nativa `input(key)` de Ursina para capturar el clic y liberación del mouse (`left mouse down` / `left mouse up`).
* **Sección 11 (`Bucle Principal update()`):** Ejecuta en cada fotograma (`time.dt`) la caída senoidal de los pétalos, el cronómetro, el posicionamiento de los hologramas verdes/rojos y la **interpolación lineal (`lerp`)** para que los discos se deslicen suavemente hacia su posición objetivo (`target_pos`).

---

## 🛠️ Guía de Modificación Rápida (Para Defensa / Evaluación)

Si durante la presentación o revisión del parcial te piden modificar parámetros del juego en vivo, ubica estas secciones:

| Cambio solicitado | Ubicación en el código | Cómo modificarlo sin errores |
| :--- | :--- | :--- |
| **Cambiar la cantidad de discos de un nivel** | **Sección 2:** Diccionario `config_discos` | Edita los números dentro de las listas, por ejemplo: `"Fácil": [3, 4, 5, 5, 6]`. Usa valores entre `2` y `8`. |
| **Exigir movimientos exactos ($2^n - 1$) para 3 estrellas** | **Sección 9:** Función `calcular_estrellas_actuales()` | Reemplaza la línea de `lim_3` por: `lim_3 = mov_optimos`. Así solo dará 3 estrellas si no comete ningún error. |
| **Cambiar los colores de los discos** | **Sección 1:** Lista `COLORES_DISCOS` | Cambia los valores `c_rgb(r, g, b)` o añade más colores a la lista. |
| **Hacer que los discos caigan más rápido o más lento** | **Sección 11:** Dentro de `update()` | Busca `lerp(d.position, d.target_pos, time.dt * 14)`. Sube `14` a `25` (más rápido) o bájalo a `6` (más lento). |
| **Cambiar la distancia entre las 3 torres** | **Sección 2:** Lista `posiciones_x` | Modifica `[-4.3, 0.0, 4.3]` (ej. `[-5.0, 0.0, 5.0]` para separarlas más). |
| **Empezar con todas las estrellas desbloqueadas (Demo)** | **Sección 2:** Diccionario `estrellas_progreso` | Cambia los `[0, 0, 0, 0, 0]` por `[3, 3, 3, 3, 3]` en cada dificultad. |

---

## ⚠️ Reglas Críticas para Evitar que el Código Colapse (Anti-Crash)

Si necesitas editar la estructura del código, **respeta estrictamente estas 5 reglas técnicas** para evitar cierres inesperados o corrupción gráfica:

### 1. Sincronía obligatoria entre `config_discos` y `estrellas_progreso`
Cada dificultad tiene exactamente **5 niveles** (listas de 5 elementos). 
* **Peligro:** Si agregas o quitas un número en `config_discos["Fácil"]` sin hacer lo mismo en `estrellas_progreso["Fácil"]` y en los bucles `range(1, 6)` / `range(5)` del menú, el juego colapsará con un `IndexError: list index out of range`.
* **Regla:** Mantén siempre 5 elementos por lista en ambos diccionarios.

### 2. Límite visual de discos en el poste (`Máximo recomendado: 8 discos`)
Cada disco tiene una altura de `ALTO_DISCO = 0.44` y cada poste mide `ALTURA_POSTE = 3.85`.
* **Peligro:** Si pones `10` o más discos en `config_discos`, el código no dará error matemático (incluso reciclará los colores automáticamente gracias a `(tam_val - 1) % len(COLORES_DISCOS)`), pero la torre de discos **sobrepasará físicamente la punta del poste** y tapará el HUD superior.
* **Solución si te piden 9 o 10 discos:** Reduce `ALTO_DISCO = 0.32` en la **Sección 2**.

### 3. Liberación de memoria en Ursina (`destroy()` antes de `.clear()`)
En `construir_nivel()` verás este bloque al inicio:
```python
for d in todos_discos:
    destroy(d)
todos_discos.clear()
```
* **Peligro:** Nunca elimines el bucle `for d in todos_discos: destroy(d)`. En Ursina Engine, hacer solo `todos_discos.clear()` vacía la lista de Python, pero **deja los objetos gráficos vivos en el motor de renderizado**, haciendo que los discos del nivel anterior queden congelados en pantalla encima de los nuevos.

### 4. Profundidad Z (`z = 10`) del paisaje vs `camera.ui`
El contenedor `fondo_paisaje` está instanciado en el mundo con `position=(0, 0, 10)` y **NO** tiene `parent=camera.ui`.
* **Peligro:** Si le agregas `parent=camera.ui` al `fondo_paisaje`, Ursina lo dibujará en la capa de interfaz frontal y **ocultará por completo los postes y los discos** del juego.

### 5. Iteración segura con copia superficial `[:]` en `update()`
En el bucle `update()`, las listas de efectos se recorren usando `for onda in ondas_choque[:]:` y `for p in particulas_efecto[:]:`.
* **Peligro:** Nunca borres los corchetes `[:]`. Como dentro del bucle se ejecuta `.remove()` cuando una partícula desaparece, iterar sobre la lista original sin `[:]` muta los índices en plena lectura y puede provocar comportamientos erráticos o bloqueos.

---

## 👨‍💻 Autor

* **Juan René Flores Hernández** — [@Juanh3rn4nd3z](https://github.com/Juanh3rn4nd3z)
* **Asignatura:** Manejo y Estructura de Datos (ME-DATOS)
