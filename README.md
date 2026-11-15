
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

## 🧠 ¿En qué consiste el código y cómo funciona? (Explicación por Secciones)

El código está organizado en **11 bloques principales** identificados con comentarios dentro del script:

### 1. Configuración Inicial y Paleta de Colores (`# 1. CONFIGURACIÓN INICIAL...`)
Prepara la ventana del juego y define todos los colores antes de renderizar la escena.
* **`app = Ursina()`:** Inicia el motor gráfico y configura el título de la ventana (`"Torre de Hanoi - Edición Sakura"`), ocultando los contadores de depuración (FPS, entidades y colisionadores).
* **Cámara 2D Ortográfica (`camera.orthographic = True`):** Desactiva la deformación de perspectiva 3D para trabajar en un plano 2D exacto con un campo de visión amplio (`camera.fov = 11.2`).
* **Función `c_rgb(r, g, b, a)`:** Convierte valores de color RGB estándar (`0` a `255`) a la escala decimal (`0.0` a `1.0`) que utiliza Ursina internamente.
* **Constantes de Paleta:** Define todas las variables de color para el paisaje, botones, madera y la lista `COLORES_DISCOS` con los 8 colores distintos para los discos.

### 2. Variables Globales y Progreso de Estrellas (`# 2. VARIABLES GLOBALES...`)
Actúa como la memoria central del juego y define la **Estructura de Datos** principal.
* **`config_discos`:** Diccionario que establece cuántos discos tiene cada uno de los 5 niveles en las 3 dificultades (`"Fácil": [3, 3, 4, 4, 5]`, `"Medio": [4, 5, 5, 6, 6]`, `"Difícil": [5, 6, 7, 7, 8]`).
* **`estrellas_progreso`:** Diccionario que almacena las estrellas ganadas (de 0 a 3) en cada uno de los 15 niveles (máximo **45 estrellas**).
* **`torres = [[], [], []]` (Estructura de Datos de Pilas / LIFO):** Representa las 3 torres (A, B y C) mediante 3 listas que operan bajo el principio **LIFO (*Last In, First Out* — Último en entrar, primero en salir)**. Los discos solo pueden extraerse o insertarse desde el tope de cada lista.
* **Variables de control:** Guardan el disco sujetado actualmente por el mouse (`disco_arrastrado`), su torre de origen (`torre_origen_arrastre`), el contador de `movimientos` y el `tiempo` del cronómetro.

### 3. Componentes Gráficos Vectoriales (`# 3. COMPONENTES GRÁFICOS...`)
Contiene las funciones que construyen las figuras geométricas de la interfaz sin usar imágenes externas:
* **`_crear_malla_estrella()`:** Usa funciones trigonométricas (`math.cos` y `math.sin`) para calcular 10 vértices alternando el radio exterior e interior, generando la malla poligonal (`Mesh`) de una estrella de 5 puntas.
* **`crear_capsula()`:** Une un rectángulo central (`quad`) con dos círculos (`circle`) en los extremos para formar figuras con bordes redondeados (usadas en la base de madera, botones y discos).
* **`crear_panel_redondeado()` y `crear_boton_pildora_menu()`:** Generan los paneles oscuros translúcidos y los botones interactivos con sombra, brillo superior y detección de clic (`on_click`).

### 4. Paisaje de Fondo (`# 4. PAISAJE DE FONDO`)
Dibuja el escenario japonés detrás del área de juego.
* **`fondo_paisaje`:** Se ubica al fondo en el eje Z (`position=(0, 0, 10)`) para no tapar nunca los postes ni los discos. Superpone capas de cielo de atardecer, sol, montañas lejanas/medias, una pagoda de 5 pisos, un lago con reflejos, colinas y ramas de cerezo (`crear_flor_sakura`).
* **`petalos_sakura`:** Instancia 22 pétalos con tamaños, velocidades (`vel_x`, `vel_y`) y fases aleatorias para animar su caída constante.
* **Contenedores de Vistas (`menu_principal_ui`, `menu_estrellas_ui`, `menu_ayuda_ui`, `juego_ui`, `mundo_juego_2d`):** Agrupan los elementos de cada pantalla. Para cambiar de vista, simplemente se activa `.enabled = True` en la pantalla deseada y `.enabled = False` en las demás.

### 5. Pantalla 1: Menú Principal (`# 5. PANTALLA 1: MENÚ PRINCIPAL`)
Construye la portada del juego:
* **Banner superior:** Muestra el título `"Torre de Hanoi"` acompañado de una miniatura decorativa de las torres.
* **Columna izquierda:** Contiene los 5 botones principales (*Iniciar Juego, selector de Dificultad con flechas laterales, Mis Estrellas, Cómo Jugar y Salir*).
* **Panel derecho (`botones_circulares_menu`):** Genera una cuadrícula con los 15 niveles (5 por dificultad). La función `actualizar_selector_menu()` resalta en amarillo el nivel activo y en dorado los niveles que ya tienen estrellas ganadas.

### 6. Pantalla 2: Tus Estrellas (`# 6. PANTALLA 2: TUS ESTRELLAS`)
Muestra el historial de calificaciones del jugador:
* Presenta un contador global (`0 / 45`) y 3 columnas correspondientes a *Fácil, Medio y Difícil*.
* **`actualizar_vista_estrellas()`:** Recorre el diccionario `estrellas_progreso`, suma el puntaje de cada dificultad (`0 / 15`) y enciende en color dorado las estrellas obtenidas en cada nivel.

### 7. Pantalla 3: Cómo Jugar (`# 7. PANTALLA 3: CÓMO JUGAR`)
Despliega un panel informativo con las 4 instrucciones clave (cómo levantar discos con clic izquierdo, el significado del holograma verde/rojo, la regla de oro de no poner un disco grande sobre uno pequeño y cómo obtener las 3 estrellas).

### 8. Escenario de Juego 2.5D y HUD (`# 8. ESCENARIO DE JUEGO 2.5D Y HUD`)
Construye el tablero interactivo donde se desarrolla la partida:
* **Base y Postes:** Dibuja la plataforma de madera y coloca los 3 postes en las posiciones `posiciones_x = [-4.3, 0.0, 4.3]` con sus etiquetas (`Torre A`, `Torre B`, `Torre C`).
* **Hologramas (`hologramas_postes`):** Crea una silueta translúcida en cada poste que permanece oculta hasta que el jugador arrastra un disco sobre esa torre.
* **HUD Superior e Inferior:** Muestra en tiempo real la dificultad y nivel actual, el `temporizador` (`00:00`), el contador de `movimientos`, las 3 estrellas encendidas/apagadas según el rendimiento, la meta óptima de movimientos y los botones de *Menú*, *Reiniciar* y *Siguiente Nivel*.

### 9. Lógica de Juego, Discos y Arrastrar y Soltar (`# 9. LÓGICA DE JUEGO...`)
Contiene los algoritmos centrales del problema de la Torre de Hanoi:
* **`calcular_estrellas_actuales()`:** Calcula el mínimo matemático de movimientos mediante la fórmula **`mov_optimos = (2 ** NUM_DISCOS) - 1`**. Otorga **3 estrellas** si el jugador resuelve el nivel dentro de un margen cercano al óptimo (`lim_3`), **2 estrellas** dentro del límite intermedio (`lim_2`) y **1 estrella** si realiza más movimientos.
* **`construir_nivel()`:**
  1. Destruye las entidades gráficas del nivel previo (`destroy(d)`) y vacía las 3 pilas (`t.clear()`).
  2. Obtiene la cantidad de discos del nivel actual (`NUM_DISCOS`) y reinicia movimientos y reloj a cero.
  3. Mediante un ciclo `for`, instancia los discos de mayor a menor tamaño (`disco.valor`), les asigna su color y los apila inicialmente en la **Torre A** (`torres[0].append(disco)`).
* **`verificar_victoria()`:** Comprueba si la **Torre C** ya contiene todos los discos del nivel (`if len(torres[2]) == NUM_DISCOS:`). Al cumplirse, detiene el cronómetro, guarda el récord de estrellas, ejecuta `lanzar_fuegos_artificiales()` y habilita el botón *Siguiente Nivel*.

### 10. Navegación entre Pantallas y Control del Mouse (`# 10. NAVEGACIÓN...`)
Gestiona el cambio de menús y las operaciones de las pilas con el mouse:
* **`obtener_torre_cercana(mx)`:** Calcula la distancia horizontal entre el disco arrastrado y las 3 torres para detectar sobre cuál poste se encuentra el cursor.
* **`input(key)`:**
  * **Al presionar clic izquierdo (`"left mouse down"`):** Inspecciona **únicamente el último elemento de cada pila (`disco_sup = t[-1]`)**. Si el clic cae dentro del área de ese disco superior, permite levantarlo e inicia el cronómetro. (Esto garantiza la regla LIFO: nunca se puede tomar un disco que tenga otros encima).
  * **Al soltar el clic izquierdo (`"left mouse up"`):** Evalúa si la torre destino cumple la regla de Hanoi:
    ```python
    if len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor:
    ```
    * **Movimiento válido:** Desapila el disco de la torre de origen con `torres[torre_origen_arrastre].pop()`, lo apila en la torre destino con `torres[idx_destino].append(disco_arrastrado)`, incrementa `movimientos += 1`, genera una onda de choque (`crear_onda_choque`) y llama a `verificar_victoria()`.
    * **Movimiento inválido:** Regresa suavemente el disco a su torre de origen y muestra una alerta en rojo.

### 11. Bucle Principal de Animación (`# 11. BUCLE PRINCIPAL DE ANIMACIÓN`)
La función **`update()`** se ejecuta automáticamente en cada fotograma (`time.dt`):
1. **Animación de Sakura:** Desplaza los pétalos hacia abajo y aplica una onda senoidal (`math.sin`) en X para simular el balanceo del viento; cuando un pétalo sale por abajo (`y < -0.52`), reaparece arriba.
2. **Cronómetro en vivo:** Suma `time.dt` a la variable `tiempo` mientras la partida está activa y actualiza el texto en formato `MM:SS`.
3. **Seguimiento del Mouse y Hologramas:** Actualiza la posición `(x, y)` del disco arrastrado y proyecta en la torre más cercana el holograma en color **verde** (si `es_valido` es verdadero) o **rojo** (si es inválido).
4. **Interpolación Lineal (`lerp`):** Desliza suavemente todos los discos hacia su coordenada objetivo (`d.position = lerp(d.position, d.target_pos, time.dt * 14)`).
5. **Limpieza de Partículas:** Expande y desvanece las ondas de choque y aplica gravedad a las estrellas de los fuegos artificiales, destruyendo las entidades (`destroy()`) cuando termina su tiempo de vida.

---

## 🔧 ¿Qué modificar en caso de que lo pidan? (Guía de Cambios Rápidos)

Si durante una revisión o defensa te piden cambiar el comportamiento del juego, busca estas líneas exactas:

| ¿Qué te piden cambiar? | Dónde está en el código | Qué valor debes modificar |
| :--- | :--- | :--- |
| **Cantidad de discos en los niveles** | Diccionario `config_discos` *(Sección 2)* | Cambia los números dentro de las listas `[3, 3, 4, 4, 5]`. Se recomienda usar valores entre `2` y `8`. |
| **Colores de los discos** | Lista `COLORES_DISCOS` *(Sección 1)* | Edita los números dentro de `c_rgb(R, G, B)` o agrega más colores a la lista. |
| **Exigir movimientos exactos ($2^n - 1$) para 3 estrellas** | Función `calcular_estrellas_actuales()` *(Sección 9)* | Cambia `lim_3 = max(...)` por `lim_3 = mov_optimos`. Así solo dará 3 estrellas si no se comete ningún error. |
| **Cambiar la torre ganadora (ej. ganar en la Torre B)** | Función `verificar_victoria()` *(Sección 9)* | Cambia `if len(torres[2]) == NUM_DISCOS:` por `if len(torres[1]) == NUM_DISCOS:` (`0` = Torre A, `1` = Torre B, `2` = Torre C). |
| **Velocidad con la que se acomodan los discos** | Función `update()` *(Sección 11)* | En `lerp(d.position, d.target_pos, time.dt * 14)`, sube `14` a `25` para que sea más rápido, o bájalo a `6` para que sea lento. |
| **Cantidad o velocidad de los pétalos Sakura** | Bucle `for _ in range(22):` *(Sección 4)* | Cambia `22` por la cantidad de pétalos deseada, o sube los valores de `pet.vel_y` para que caigan más rápido. |

---

## ⚠️ Cómo evitar que el código colapse al modificarlo (Reglas de Seguridad)

Para asegurarte de que el programa **nunca se cierre con errores (`Crash` / `IndexError`)** ni se dañe visualmente al editarlo, respeta siempre estas 5 reglas:

1. **Sincronía entre `config_discos` y `estrellas_progreso`:**
   Cada dificultad en `config_discos` tiene **5 niveles** (5 números) y en `estrellas_progreso` tiene **5 ceros** (`[0, 0, 0, 0, 0]`). Si agregas o quitas un nivel en uno, debes hacer exactamente lo mismo en el otro; de lo contrario, el programa colapsará con un `IndexError: list index out of range`.
2. **Límite visual de discos por poste (`Máximo recomendado: 8`):**
   El grosor de cada disco es `ALTO_DISCO = 0.44` y la altura del poste es `ALTURA_POSTE = 3.85`. Si configuras un nivel con 10 o más discos, la pila rebasará el tope del poste y se meterá dentro del marcador superior. Si te piden poner 10 discos, reduce también `ALTO_DISCO = 0.32`.
3. **Nunca pongas `fondo_paisaje` dentro de `camera.ui`:**
   El paisaje de fondo (`fondo_paisaje`) está en el mundo 2D con profundidad `z = 10` (detrás de las torres). Si le agregas `parent=camera.ui`, pasará a la capa frontal de interfaz y tapará por completo los postes y los discos.
4. **No borrar el bucle `destroy(d)` en `construir_nivel()`:**
   Antes de hacer `todos_discos.clear()`, el código ejecuta `for d in todos_discos: destroy(d)`. Si borras el `destroy(d)`, los discos viejos no se eliminarán de la tarjeta gráfica y quedarán congelados en pantalla encimándose con los discos nuevos.
5. **Mantener siempre los corchetes `[:]` en los bucles de partículas:**
   En `update()`, las ondas y fuegos artificiales se recorren con `for onda in ondas_choque[:]:` y `for p in particulas_efecto[:]:`. El `[:]` crea una copia temporal de la lista para poder borrar elementos con `.remove()` de forma segura mientras el ciclo está corriendo.

---

## 👤 Autor

* **Juan René Flores Hernández** ([@Juanh3rn4nd3z](https://github.com/Juanh3rn4nd3z))
* **Carrera:** Ingeniería en Desarrollo de Software — Universidad de Oriente (UNIVO)

