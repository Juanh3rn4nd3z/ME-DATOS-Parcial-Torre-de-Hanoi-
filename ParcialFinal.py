from ursina import *
import random
import math

# =====================================================================
# 1. CONFIGURACIÓN INICIAL Y PALETA DE COLORES DE LA IMAGEN
# =====================================================================

app = Ursina()

window.title = "Torre de Hanoi - Edición Sakura"
window.borderless = False
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False

def c_rgb(r, g, b, a=255):
    return color.rgba(r / 255.0, g / 255.0, b / 255.0, a / 255.0)

# Cámara 2D Ortográfica amplia
camera.orthographic = True
camera.fov = 11.2
camera.position = (0, 0, -20)
camera.rotation = (0, 0, 0)
camera.ui.enabled = True

# --- PALETA EXTRAÍDA DE LAS IMÁGENES DE REFERENCIA ---
CIELO_ALTO       = c_rgb(62, 82, 148)
CIELO_MEDIO      = c_rgb(122, 136, 198)
CIELO_HORIZONTE  = c_rgb(218, 178, 205)
SOL_BRILLO       = c_rgb(255, 232, 185, 110)

MONTANA_LEJANA   = c_rgb(95, 102, 162)
MONTANA_MEDIA    = c_rgb(68, 76, 134)
PAGODA_SILUETA   = c_rgb(56, 64, 118)
COLINA_CERCANA   = c_rgb(38, 48, 92)

LAGO_SUPERIOR    = c_rgb(58, 86, 152)
LAGO_PROFUNDO    = c_rgb(34, 52, 108)
LAGO_REFLEJO     = c_rgb(185, 205, 245, 95)

SAKURA_RAMA      = c_rgb(58, 34, 52)
SAKURA_ROSA      = c_rgb(255, 168, 202)
SAKURA_CLARO     = c_rgb(255, 218, 235)
SAKURA_CENTRO    = c_rgb(235, 95, 145)
HOJA_VERDE       = c_rgb(52, 112, 88)

# Contenedores y Paneles Oscuros Translúcidos
BANNER_AZUL      = c_rgb(32, 43, 82, 242)
BANNER_BORDE     = c_rgb(68, 86, 142)
PANEL_OSCURO     = c_rgb(25, 33, 64, 238)
PANEL_INTERNO    = c_rgb(35, 45, 82, 245)
SOMBRA_UI        = c_rgb(12, 16, 36, 210)

# Colores de los 5 Botones del Menú Izquierdo
BTN_AMARILLO     = c_rgb(255, 198, 52)
BTN_AMARILLO_S   = c_rgb(198, 134, 18)
TEXTO_CAFE       = c_rgb(78, 42, 10)

BTN_MORADO       = c_rgb(84, 62, 168)
BTN_MORADO_S     = c_rgb(50, 34, 112)

BTN_VERDE        = c_rgb(122, 214, 108)
BTN_VERDE_S      = c_rgb(74, 156, 62)
TEXTO_VERDE_OSC  = c_rgb(24, 64, 24)

BTN_AZUL         = c_rgb(102, 162, 232)
BTN_AZUL_S       = c_rgb(58, 108, 174)
TEXTO_AZUL_OSC   = c_rgb(20, 42, 78)

BTN_ROJO         = c_rgb(232, 82, 74)
BTN_ROJO_S       = c_rgb(164, 42, 36)
TEXTO_ROJO_OSC   = c_rgb(68, 14, 14)

# Colores de Cabeceras de Dificultad
HDR_FACIL        = c_rgb(68, 168, 92)
HDR_FACIL_S      = c_rgb(44, 118, 62)

HDR_MEDIO        = c_rgb(58, 124, 198)
HDR_MEDIO_S      = c_rgb(36, 84, 142)

HDR_DIFICIL      = c_rgb(124, 68, 184)
HDR_DIFICIL_S    = c_rgb(82, 40, 128)

# Cinta Dorada y Estrellas
ORO_BRILLO       = c_rgb(255, 238, 128)
ORO_VIVO         = c_rgb(255, 202, 42)
ORO_SOMBRA       = c_rgb(198, 132, 16)
CINTA_ORO        = c_rgb(244, 186, 58)
CINTA_PLIEGUE    = c_rgb(208, 132, 28)
ESTRELLA_VACIA   = c_rgb(72, 84, 126)
ESTRELLA_VACIA_N = c_rgb(55, 66, 104)

# Madera y Discos
MADERA_CLARA     = c_rgb(212, 138, 72)
MADERA_OSCURA    = c_rgb(148, 86, 36)
MADERA_LUZ       = c_rgb(238, 176, 108)
MADERA_SOMBRA    = c_rgb(112, 62, 24)
ORO_TOPE_POSTE   = c_rgb(226, 204, 112)
ORO_PLACA        = c_rgb(236, 190, 52)
ORO_PLACA_S      = c_rgb(190, 128, 16)

COLORES_DISCOS = [
    c_rgb(235, 64, 64),
    c_rgb(252, 198, 42),
    c_rgb(48, 148, 238),
    c_rgb(76, 204, 108),
    c_rgb(245, 124, 42),
    c_rgb(168, 92, 235),
    c_rgb(238, 108, 178),
    c_rgb(64, 210, 210)
]

window.color = CIELO_ALTO


# =====================================================================
# 2. VARIABLES GLOBALES Y PROGRESO DE ESTRELLAS
# =====================================================================

dificultades = ["Fácil", "Medio", "Difícil"]
colores_hdr_dif = [HDR_FACIL, HDR_MEDIO, HDR_DIFICIL]
sombras_hdr_dif = [HDR_FACIL_S, HDR_MEDIO_S, HDR_DIFICIL_S]

indice_dificultad = 0
nivel_actual = 1

config_discos = {
    "Fácil":   [3, 3, 4, 4, 5],
    "Medio":   [4, 5, 5, 6, 6],
    "Difícil": [5, 6, 7, 7, 8]
}

MAX_ESTRELLAS_NIVEL = 3
MAX_ESTRELLAS_DIF   = 15
MAX_ESTRELLAS_TOTAL = 45

estrellas_progreso = {
    "Fácil":   [0, 0, 0, 0, 0],
    "Medio":   [0, 0, 0, 0, 0],
    "Difícil": [0, 0, 0, 0, 0]
}

NUM_DISCOS = 3
posiciones_x = [-4.3, 0.0, 4.3]
BASE_DISCOS_Y = -1.25
ALTO_DISCO = 0.44

torres = [[], [], []]
todos_discos = []
anillos_base = []
hologramas_postes = []

disco_arrastrado = None
torre_origen_arrastre = None
offset_x = 0.0
offset_y = 0.0

petalos_sakura = []
particulas_efecto = []
ondas_choque = []
estrellas_hud_vivo = []

movimientos = 0
tiempo = 0.0
cronometro_activo = False
juego_terminado = False


# =====================================================================
# 3. COMPONENTES GRÁFICOS VECTORIALES
# =====================================================================

def _crear_malla_estrella(R=0.5, r=0.2):
    verts = [Vec3(0, -0.0477, 0)]
    for i in range(10):
        ang = math.radians(90 + 36 * i)
        rad = R if i % 2 == 0 else r
        verts.append(Vec3(rad * math.cos(ang), rad * math.sin(ang) - 0.0477, 0))
    tris = [(0, i, i + 1) for i in range(1, 10)] + [(0, 10, 1)]
    return Mesh(vertices=verts, triangles=tris, mode='triangle')


MALLA_ESTRELLA = _crear_malla_estrella()


def crear_capsula(padre, x, y, z, ancho, alto, col):
    raiz = Entity(parent=padre, position=(x, y, z))
    w_rect = max(0.002, ancho - alto)
    q = Entity(parent=raiz, model='quad', scale=(w_rect, alto), color=col)
    c1 = Entity(parent=raiz, model='circle', position=(-w_rect / 2, 0, 0), scale=(alto, alto), color=col)
    c2 = Entity(parent=raiz, model='circle', position=(w_rect / 2, 0, 0), scale=(alto, alto), color=col)
    raiz.partes = [q, c1, c2]

    def set_col(nuevo_c):
        for p in raiz.partes:
            p.color = nuevo_c

    raiz.set_color = set_col
    return raiz


def crear_panel_redondeado(padre, x, y, z, ancho, alto, col_fondo, col_borde=None, radio=0.045):
    raiz = Entity(parent=padre, position=(x, y, z))

    if col_borde:
        crear_panel_redondeado(raiz, 0, 0, 0.015, ancho + 0.010, alto + 0.010, col_borde, None, radio + 0.005)

    w_in = max(0.01, ancho - radio * 2)
    h_in = max(0.01, alto - radio * 2)

    Entity(parent=raiz, model='quad', scale=(w_in + radio * 2, h_in), color=col_fondo)
    Entity(parent=raiz, model='quad', scale=(w_in, h_in + radio * 2), color=col_fondo)

    for dx in (-w_in / 2, w_in / 2):
        for dy in (-h_in / 2, h_in / 2):
            Entity(parent=raiz, model='circle', position=(dx, dy, 0), scale=(radio * 2, radio * 2), color=col_fondo)
    return raiz


def crear_boton_pildora_menu(padre, texto, pos, escala, col_prin, col_som, col_txt, escala_txt=1.18, offset_txt_x=0.025, accion=None):
    x, y, z = pos
    w, h = escala

    sombra_ent = crear_capsula(padre, x, y - 0.008, z + 0.02, w, h, col_som)
    cuerpo = crear_capsula(padre, x, y, z + 0.01, w, h, col_prin)
    brillo_ent = crear_capsula(padre, x, y + h * 0.25, z, w - h * 0.55, h * 0.18, color.rgba(1, 1, 1, 0.22))

    btn = Button(
        parent=padre,
        text=texto,
        position=(x, y, z - 0.01),
        scale=(w, h),
        color=color.clear,
        highlight_color=color.rgba(1, 1, 1, 0.08),
        pressed_color=color.rgba(0, 0, 0, 0.12),
        text_color=col_txt
    )

    if btn.text_entity:
        btn.text_entity.scale *= escala_txt
        btn.text_entity.position = (offset_txt_x, 0, -0.02)

    btn.cuerpo_vis = cuerpo
    btn.sombra_vis = sombra_ent
    btn.brillo_vis = brillo_ent

    def mostrar_ocultar(estado):
        btn.enabled = estado
        cuerpo.enabled = estado
        sombra_ent.enabled = estado
        brillo_ent.enabled = estado

    btn.set_visible_completo = mostrar_ocultar

    if accion:
        btn.on_click = accion
    return btn


def crear_icono_chevron(padre, x, y, z, direccion=-1, col=color.white):
    raiz = Entity(parent=padre, position=(x, y, z))
    ang_sup = -40 if direccion == -1 else 40
    ang_inf = 40 if direccion == -1 else -40
    Entity(parent=raiz, model='quad', position=(0, 0.007, 0), scale=(0.022, 0.0055), rotation_z=ang_sup, color=col)
    Entity(parent=raiz, model='quad', position=(0, -0.007, 0), scale=(0.022, 0.0055), rotation_z=ang_inf, color=col)
    return raiz


def crear_estrella_5p(padre, pos=(0, 0, 0), tam=0.024, encendido=True, con_sombra=True):
    raiz = Entity(parent=padre, position=pos)
    c_uso = ORO_VIVO if encendido else ESTRELLA_VACIA

    sombra = None
    if con_sombra:
        sombra = Entity(
            parent=raiz, model=MALLA_ESTRELLA,
            position=(0, -tam * 0.07, 0.015),
            scale=(tam * 1.14, tam * 1.14, 1),
            color=ORO_SOMBRA if encendido else SOMBRA_UI,
            double_sided=True
        )

    cuerpo = Entity(
        parent=raiz, model=MALLA_ESTRELLA,
        scale=(tam, tam, 1),
        color=c_uso,
        double_sided=True
    )
    brillo = Entity(
        parent=raiz, model=MALLA_ESTRELLA,
        position=(0, tam * 0.02, -0.005),
        scale=(tam * 0.50, tam * 0.50, 1),
        color=ORO_BRILLO if encendido else ESTRELLA_VACIA_N,
        double_sided=True
    )

    def set_estado(activo):
        cuerpo.color = ORO_VIVO if activo else ESTRELLA_VACIA
        brillo.color = ORO_BRILLO if activo else ESTRELLA_VACIA_N
        if sombra:
            sombra.color = ORO_SOMBRA if activo else SOMBRA_UI

    raiz.set_encendido = set_estado
    return raiz


def crear_flor_sakura(padre, x, y, z, tam=0.028):
    f = Entity(parent=padre, position=(x, y, z))
    for ang in range(0, 360, 72):
        rad = math.radians(ang)
        px = math.cos(rad) * (tam * 0.42)
        py = math.sin(rad) * (tam * 0.42)
        Entity(parent=f, model='circle', position=(px, py, 0), scale=(tam * 0.58, tam * 0.58), color=SAKURA_ROSA)
    Entity(parent=f, model='circle', position=(0, 0, -0.005), scale=(tam * 0.32, tam * 0.32), color=SAKURA_CLARO)
    Entity(parent=f, model='circle', position=(0, 0, -0.01), scale=(tam * 0.14, tam * 0.14), color=SAKURA_CENTRO)
    return f


# =====================================================================
# 4. PAISAJE DE FONDO
# =====================================================================

# CORRECCIÓN: el fondo se coloca detrás de las torres.
# No usar camera.ui aquí, porque puede tapar los postes y discos.
fondo_paisaje = Entity(position=(0, 0, 10), scale=(10, 10, 1))

# Capas del cielo de atardecer
Entity(parent=fondo_paisaje, model='quad', position=(0, 0.25, 0.10), scale=(2.2, 0.65), color=CIELO_ALTO)
Entity(parent=fondo_paisaje, model='quad', position=(0, -0.02, 0.09), scale=(2.2, 0.42), color=CIELO_MEDIO)
Entity(parent=fondo_paisaje, model='quad', position=(0, -0.18, 0.08), scale=(2.2, 0.28), color=CIELO_HORIZONTE)
Entity(parent=fondo_paisaje, model='circle', position=(0.05, -0.05, 0.075), scale=(0.65, 0.45), color=SOL_BRILLO)

# Montañas lejanas
for mx, my, mw, mh in [(-0.65, -0.16, 0.75, 0.35), (-0.15, -0.18, 0.65, 0.28), (0.42, -0.15, 0.85, 0.38), (0.82, -0.16, 0.55, 0.30)]:
    Entity(parent=fondo_paisaje, model='circle', position=(mx, my, 0.07), scale=(mw, mh), color=MONTANA_LEJANA)

for mx, my, mw, mh in [(-0.78, -0.22, 0.65, 0.28), (0.28, -0.20, 0.58, 0.25), (0.68, -0.19, 0.62, 0.30)]:
    Entity(parent=fondo_paisaje, model='circle', position=(mx, my, 0.06), scale=(mw, mh), color=MONTANA_MEDIA)

# Silueta de la pagoda
pagoda_x = 0.06
pagoda_base_y = -0.12

for piso in range(5):
    py = pagoda_base_y + piso * 0.042
    ancho_piso = 0.15 - piso * 0.020
    Entity(parent=fondo_paisaje, model='quad', position=(pagoda_x, py, 0.055), scale=(ancho_piso * 0.68, 0.028), color=PAGODA_SILUETA)
    crear_capsula(fondo_paisaje, pagoda_x, py + 0.014, 0.054, ancho_piso, 0.012, PAGODA_SILUETA)

Entity(parent=fondo_paisaje, model='quad', position=(pagoda_x, pagoda_base_y + 0.22, 0.055), scale=(0.008, 0.045), color=PAGODA_SILUETA)

# Lago y reflejos
Entity(parent=fondo_paisaje, model='quad', position=(0, -0.36, 0.05), scale=(2.2, 0.32), color=LAGO_SUPERIOR)
Entity(parent=fondo_paisaje, model='quad', position=(0, -0.46, 0.045), scale=(2.2, 0.16), color=LAGO_PROFUNDO)

for rx, ry, rw in [(-0.45, -0.34, 0.18), (-0.12, -0.39, 0.24), (0.22, -0.36, 0.16), (0.05, -0.44, 0.28), (-0.55, -0.46, 0.14)]:
    crear_capsula(fondo_paisaje, rx, ry, 0.04, rw, 0.006, LAGO_REFLEJO)

# Colinas y vegetación
Entity(parent=fondo_paisaje, model='circle', position=(-0.82, -0.28, 0.035), scale=(0.55, 0.22), color=COLINA_CERCANA)
Entity(parent=fondo_paisaje, model='circle', position=(0.84, -0.30, 0.035), scale=(0.50, 0.20), color=COLINA_CERCANA)

for ax, ay, tam_a in [(-0.78, -0.14, 0.12), (-0.70, -0.17, 0.10), (-0.85, -0.16, 0.11), (0.76, -0.18, 0.11)]:
    Entity(parent=fondo_paisaje, model='circle', position=(ax, ay, 0.03), scale=(tam_a, tam_a * 0.75), color=HOJA_VERDE)

# Ramas y flores Sakura
Entity(parent=fondo_paisaje, model='quad', position=(-0.74, 0.42, 0.025), scale=(0.32, 0.016), rotation_z=-18, color=SAKURA_RAMA)
Entity(parent=fondo_paisaje, model='quad', position=(-0.62, 0.44, 0.025), scale=(0.18, 0.012), rotation_z=12, color=SAKURA_RAMA)
Entity(parent=fondo_paisaje, model='quad', position=(0.74, 0.42, 0.025), scale=(0.30, 0.015), rotation_z=16, color=SAKURA_RAMA)

pos_flores = [
    (-0.84, 0.45, 0.042), (-0.77, 0.47, 0.035), (-0.71, 0.42, 0.038), (-0.64, 0.46, 0.032),
    (-0.56, 0.43, 0.028), (-0.80, 0.38, 0.030), (0.83, 0.45, 0.040), (0.75, 0.46, 0.034),
    (0.67, 0.42, 0.032), (0.80, 0.38, 0.028)
]

for fx, fy, ft in pos_flores:
    crear_flor_sakura(fondo_paisaje, fx, fy, 0.02, tam=ft)

# Pétalos animados
random.seed(10)

for _ in range(22):
    pet = Entity(
        parent=fondo_paisaje,
        model='circle',
        position=(random.uniform(-0.88, 0.88), random.uniform(-0.48, 0.48), 0.015),
        scale=(random.uniform(0.008, 0.015), random.uniform(0.005, 0.010)),
        rotation_z=random.uniform(0, 360),
        color=random.choice([SAKURA_ROSA, SAKURA_CLARO])
    )
    pet.vel_y = random.uniform(0.025, 0.055)
    pet.vel_x = random.uniform(-0.020, 0.020)
    pet.fase = random.uniform(0, 6.28)
    petalos_sakura.append(pet)


# Contenedores de las vistas
menu_principal_ui = Entity(parent=camera.ui, enabled=True)
menu_estrellas_ui = Entity(parent=camera.ui, enabled=False)
menu_ayuda_ui = Entity(parent=camera.ui, enabled=False)
juego_ui = Entity(parent=camera.ui, enabled=False)
mundo_juego_2d = Entity(enabled=False)


# =====================================================================
# 5. PANTALLA 1: MENÚ PRINCIPAL
# =====================================================================

crear_panel_redondeado(menu_principal_ui, 0, 0.34, 0.12, 0.92, 0.21, SOMBRA_UI, None, radio=0.05)
crear_panel_redondeado(menu_principal_ui, 0, 0.35, 0.10, 0.91, 0.20, BANNER_AZUL, BANNER_BORDE, radio=0.05)

# Miniatura de las torres
crear_capsula(menu_principal_ui, -0.31, 0.285, 0.05, 0.21, 0.022, MADERA_OSCURA)
crear_capsula(menu_principal_ui, -0.31, 0.292, 0.04, 0.20, 0.018, MADERA_CLARA)

for px_t in [-0.38, -0.31, -0.24]:
    Entity(parent=menu_principal_ui, model='quad', position=(px_t, 0.348, 0.045), scale=(0.013, 0.105), color=MADERA_CLARA)
    Entity(parent=menu_principal_ui, model='circle', position=(px_t, 0.400, 0.042), scale=(0.013, 0.013), color=MADERA_CLARA)

crear_capsula(menu_principal_ui, -0.31, 0.312, 0.03, 0.095, 0.024, COLORES_DISCOS[2])
crear_capsula(menu_principal_ui, -0.31, 0.336, 0.02, 0.072, 0.022, COLORES_DISCOS[1])
crear_capsula(menu_principal_ui, -0.31, 0.358, 0.01, 0.050, 0.020, COLORES_DISCOS[0])

Text(parent=menu_principal_ui, text="Torre de Hanoi", position=(0.083, 0.372, -0.02), origin=(0, 0), scale=2.65, color=SOMBRA_UI)
Text(parent=menu_principal_ui, text="Torre de Hanoi", position=(0.080, 0.378, -0.04), origin=(0, 0), scale=2.65, color=color.white)
Text(parent=menu_principal_ui, text="Ordena los discos, alcanza la cima", position=(0.080, 0.295, -0.04), origin=(0, 0), scale=1.02, color=c_rgb(220, 228, 250))

# Botones del menú
X_COL_IZQ = -0.21

btn_iniciar = crear_boton_pildora_menu(
    menu_principal_ui, "Iniciar Juego",
    pos=(X_COL_IZQ, 0.135, 0.02), escala=(0.43, 0.092),
    col_prin=BTN_AMARILLO, col_som=BTN_AMARILLO_S, col_txt=TEXTO_CAFE,
    escala_txt=1.22, offset_txt_x=0.03
)

Entity(parent=menu_principal_ui, model='quad', position=(X_COL_IZQ - 0.135, 0.135, -0.03), scale=(0.028, 0.028), rotation_z=45, color=TEXTO_CAFE)
Entity(parent=menu_principal_ui, model='quad', position=(X_COL_IZQ - 0.147, 0.135, -0.025), scale=(0.022, 0.044), color=BTN_AMARILLO)

btn_dif_pildora = crear_boton_pildora_menu(
    menu_principal_ui, "",
    pos=(X_COL_IZQ, 0.012, 0.02), escala=(0.43, 0.096),
    col_prin=BTN_MORADO, col_som=BTN_MORADO_S, col_txt=color.white
)

eng_x, eng_y = X_COL_IZQ - 0.105, 0.028
Entity(parent=menu_principal_ui, model='quad', position=(eng_x, eng_y, -0.03), scale=(0.024, 0.024), color=color.white)
Entity(parent=menu_principal_ui, model='quad', position=(eng_x, eng_y, -0.03), scale=(0.024, 0.024), rotation_z=45, color=color.white)
Entity(parent=menu_principal_ui, model='circle', position=(eng_x, eng_y, -0.04), scale=(0.011, 0.011), color=BTN_MORADO)

Text(parent=menu_principal_ui, text="Dificultad", position=(X_COL_IZQ + 0.025, 0.030, -0.04), origin=(0, 0), scale=1.18, color=color.white)
crear_estrella_5p(menu_principal_ui, pos=(X_COL_IZQ - 0.025, -0.012, -0.04), tam=0.018, encendido=True, con_sombra=False)
lbl_dif_sub = Text(parent=menu_principal_ui, text="Fácil", position=(X_COL_IZQ + 0.022, -0.012, -0.04), origin=(0, 0), scale=0.92, color=ORO_VIVO)

crear_icono_chevron(menu_principal_ui, X_COL_IZQ - 0.175, 0.012, -0.04, direccion=-1, col=color.white)

btn_dif_izq = Button(
    parent=menu_principal_ui, text="",
    position=(X_COL_IZQ - 0.175, 0.012, -0.05), scale=(0.055, 0.080),
    color=color.clear, highlight_color=color.rgba(1, 1, 1, 0.12)
)

crear_icono_chevron(menu_principal_ui, X_COL_IZQ + 0.175, 0.012, -0.04, direccion=1, col=color.white)

btn_dif_der = Button(
    parent=menu_principal_ui, text="",
    position=(X_COL_IZQ + 0.175, 0.012, -0.05), scale=(0.055, 0.080),
    color=color.clear, highlight_color=color.rgba(1, 1, 1, 0.12)
)

btn_estrellas = crear_boton_pildora_menu(
    menu_principal_ui, "Mis Estrellas",
    pos=(X_COL_IZQ, -0.108, 0.02), escala=(0.43, 0.088),
    col_prin=BTN_VERDE, col_som=BTN_VERDE_S, col_txt=TEXTO_VERDE_OSC,
    escala_txt=1.16, offset_txt_x=0.032
)

tx_i, ty_i = X_COL_IZQ - 0.125, -0.108
Entity(parent=menu_principal_ui, model='quad', position=(tx_i, ty_i + 0.008, -0.03), scale=(0.026, 0.022), color=TEXTO_VERDE_OSC)
Entity(parent=menu_principal_ui, model='circle', position=(tx_i, ty_i + 0.002, -0.03), scale=(0.026, 0.018), color=TEXTO_VERDE_OSC)
Entity(parent=menu_principal_ui, model='quad', position=(tx_i, ty_i - 0.010, -0.03), scale=(0.007, 0.014), color=TEXTO_VERDE_OSC)
Entity(parent=menu_principal_ui, model='quad', position=(tx_i, ty_i - 0.018, -0.03), scale=(0.022, 0.006), color=TEXTO_VERDE_OSC)

btn_como_jugar = crear_boton_pildora_menu(
    menu_principal_ui, "Cómo Jugar",
    pos=(X_COL_IZQ, -0.222, 0.02), escala=(0.38, 0.084),
    col_prin=BTN_AZUL, col_som=BTN_AZUL_S, col_txt=TEXTO_AZUL_OSC,
    escala_txt=1.14, offset_txt_x=0.028
)

Entity(parent=menu_principal_ui, model='circle', position=(X_COL_IZQ - 0.115, -0.222, -0.03), scale=(0.038, 0.038), color=TEXTO_AZUL_OSC)
Text(parent=menu_principal_ui, text="i", position=(X_COL_IZQ - 0.115, -0.222, -0.05), origin=(0, 0), scale=1.1, color=color.white)

btn_salir = crear_boton_pildora_menu(
    menu_principal_ui, "Salir",
    pos=(X_COL_IZQ, -0.332, 0.02), escala=(0.28, 0.080),
    col_prin=BTN_ROJO, col_som=BTN_ROJO_S, col_txt=TEXTO_ROJO_OSC,
    escala_txt=1.16, offset_txt_x=0.022,
    accion=application.quit
)

sx_i, sy_i = X_COL_IZQ - 0.068, -0.332
Entity(parent=menu_principal_ui, model='quad', position=(sx_i, sy_i, -0.03), scale=(0.026, 0.028), color=TEXTO_ROJO_OSC)
Entity(parent=menu_principal_ui, model='quad', position=(sx_i + 0.008, sy_i, -0.04), scale=(0.016, 0.007), color=BTN_ROJO)

# Panel derecho
X_PANEL_DER = 0.25

crear_panel_redondeado(menu_principal_ui, X_PANEL_DER, -0.10, 0.08, 0.34, 0.54, SOMBRA_UI, None, radio=0.04)
crear_panel_redondeado(menu_principal_ui, X_PANEL_DER, -0.095, 0.06, 0.33, 0.53, PANEL_OSCURO, BANNER_BORDE, radio=0.04)

botones_circulares_menu = {}

for idx_d, nom_dif in enumerate(dificultades):
    y_sec = 0.095 - idx_d * 0.165

    Text(parent=menu_principal_ui, text=nom_dif, position=(X_PANEL_DER, y_sec + 0.042, -0.03), origin=(0, 0), scale=1.08, color=color.white)
    Text(parent=menu_principal_ui, text="(5 niveles)", position=(X_PANEL_DER, y_sec + 0.015, -0.03), origin=(0, 0), scale=0.75, color=c_rgb(190, 202, 235))

    if idx_d < 2:
        Entity(parent=menu_principal_ui, model='quad', position=(X_PANEL_DER, y_sec - 0.072, 0.01), scale=(0.27, 0.002), color=BANNER_BORDE)

    botones_circulares_menu[nom_dif] = []

    for n in range(1, 6):
        cx = (X_PANEL_DER - 0.112) + (n - 1) * 0.056
        cy = y_sec - 0.028

        borde_c = Entity(parent=menu_principal_ui, model='circle', position=(cx, cy, 0.02), scale=(0.046, 0.046), color=BANNER_BORDE)
        relleno_c = Entity(parent=menu_principal_ui, model='circle', position=(cx, cy, 0.01), scale=(0.040, 0.040), color=PANEL_INTERNO)

        b_circ = Button(
            parent=menu_principal_ui,
            text=str(n),
            position=(cx, cy, -0.01),
            scale=(0.042, 0.042),
            color=color.clear,
            highlight_color=color.rgba(1, 1, 1, 0.15),
            text_color=color.white
        )

        if b_circ.text_entity:
            b_circ.text_entity.scale *= 0.88

        b_circ.borde_c = borde_c
        b_circ.relleno_c = relleno_c

        def seleccionar_nivel_circular(d_i=idx_d, niv=n):
            global indice_dificultad, nivel_actual
            indice_dificultad = d_i
            nivel_actual = niv
            actualizar_selector_menu()

        b_circ.on_click = seleccionar_nivel_circular
        botones_circulares_menu[nom_dif].append(b_circ)


def actualizar_selector_menu():
    dif_actual = dificultades[indice_dificultad]
    lbl_dif_sub.text = dif_actual
    btn_dif_pildora.on_click = Func(cambiar_dificultad, 1)

    for nom_dif, lista_btns in botones_circulares_menu.items():
        for i, b_c in enumerate(lista_btns):
            pts = estrellas_progreso[nom_dif][i]
            es_activo = (nom_dif == dif_actual and (i + 1) == nivel_actual)

            if es_activo:
                b_c.relleno_c.color = BTN_AMARILLO
                b_c.borde_c.color = ORO_BRILLO
                b_c.text_color = TEXTO_CAFE
            elif pts > 0:
                b_c.relleno_c.color = c_rgb(52, 72, 132)
                b_c.borde_c.color = ORO_VIVO
                b_c.text_color = ORO_BRILLO
            else:
                b_c.relleno_c.color = PANEL_INTERNO
                b_c.borde_c.color = BANNER_BORDE
                b_c.text_color = color.white


def cambiar_dificultad(delta):
    global indice_dificultad
    indice_dificultad = (indice_dificultad + delta) % len(dificultades)
    actualizar_selector_menu()


btn_dif_izq.on_click = Func(cambiar_dificultad, -1)
btn_dif_der.on_click = Func(cambiar_dificultad, 1)


# =====================================================================
# 6. PANTALLA 2: TUS ESTRELLAS
# =====================================================================

crear_panel_redondeado(menu_estrellas_ui, 0, -0.02, 0.12, 0.96, 0.84, SOMBRA_UI, None, radio=0.055)
crear_panel_redondeado(menu_estrellas_ui, 0, -0.01, 0.10, 0.95, 0.83, PANEL_OSCURO, BANNER_BORDE, radio=0.055)

Entity(parent=menu_estrellas_ui, model='circle', position=(0, 0.39, 0.06), scale=(0.24, 0.18), color=SOL_BRILLO)
estrella_top_grande = crear_estrella_5p(menu_estrellas_ui, pos=(0, 0.39, -0.02), tam=0.115, encendido=True)

Entity(parent=menu_estrellas_ui, model='quad', position=(-0.27, 0.275, 0.05), scale=(0.08, 0.062), rotation_z=8, color=CINTA_PLIEGUE)
Entity(parent=menu_estrellas_ui, model='quad', position=(0.27, 0.275, 0.05), scale=(0.08, 0.062), rotation_z=-8, color=CINTA_PLIEGUE)

crear_capsula(menu_estrellas_ui, 0, 0.285, 0.04, 0.50, 0.076, ORO_SOMBRA)
crear_capsula(menu_estrellas_ui, 0, 0.292, 0.03, 0.50, 0.074, CINTA_ORO)

Text(parent=menu_estrellas_ui, text="Tus Estrellas", position=(0, 0.292, -0.04), origin=(0, 0), scale=1.95, color=TEXTO_CAFE)

crear_estrella_5p(menu_estrellas_ui, pos=(-0.115, 0.195, -0.03), tam=0.056, encendido=True)

lbl_total_estrellas = Text(
    parent=menu_estrellas_ui,
    text="0 / 45",
    position=(0.035, 0.195, -0.04),
    origin=(0, 0),
    scale=2.25,
    color=color.white
)

Text(
    parent=menu_estrellas_ui,
    text="¡Sigue jugando para obtener más estrellas!",
    position=(0, 0.132, -0.04),
    origin=(0, 0),
    scale=0.92,
    color=c_rgb(215, 225, 250)
)

ui_columnas_estrellas = {}

for idx_c, nom_dif in enumerate(dificultades):
    cx_col = -0.285 + idx_c * 0.285
    cy_col = -0.085
    col_hdr = colores_hdr_dif[idx_c]

    crear_panel_redondeado(menu_estrellas_ui, cx_col, cy_col, 0.06, 0.255, 0.365, PANEL_INTERNO, col_hdr, radio=0.03)
    crear_panel_redondeado(menu_estrellas_ui, cx_col, cy_col + 0.145, 0.04, 0.250, 0.072, col_hdr, None, radio=0.025)

    Text(parent=menu_estrellas_ui, text=nom_dif, position=(cx_col, cy_col + 0.150, -0.03), origin=(0, 0), scale=1.18, color=color.white)

    crear_estrella_5p(menu_estrellas_ui, pos=(cx_col - 0.045, cy_col + 0.082, -0.03), tam=0.030, encendido=True)

    lbl_sub_col = Text(parent=menu_estrellas_ui, text="0 / 15", position=(cx_col + 0.022, cy_col + 0.082, -0.03), origin=(0, 0), scale=1.05, color=color.white)

    Entity(parent=menu_estrellas_ui, model='quad', position=(cx_col, cy_col + 0.048, 0.02), scale=(0.22, 0.002), color=BANNER_BORDE)

    filas_estrellas_col = []

    for n_fila in range(5):
        fy = (cy_col + 0.018) - n_fila * 0.042

        Entity(parent=menu_estrellas_ui, model='circle', position=(cx_col - 0.082, fy, 0.01), scale=(0.030, 0.030), color=col_hdr)
        Entity(parent=menu_estrellas_ui, model='circle', position=(cx_col - 0.082, fy, 0.00), scale=(0.025, 0.025), color=PANEL_OSCURO)

        Text(parent=menu_estrellas_ui, text=str(n_fila + 1), position=(cx_col - 0.082, fy, -0.03), origin=(0, 0), scale=0.78, color=color.white)

        estrellas_nivel_ui = []

        for s_idx in range(MAX_ESTRELLAS_NIVEL):
            sx_e = (cx_col - 0.022) + s_idx * 0.044
            est_item = crear_estrella_5p(menu_estrellas_ui, pos=(sx_e, fy, -0.02), tam=0.030, encendido=False, con_sombra=False)
            estrellas_nivel_ui.append(est_item)

        filas_estrellas_col.append(estrellas_nivel_ui)

    ui_columnas_estrellas[nom_dif] = (lbl_sub_col, filas_estrellas_col)


def actualizar_vista_estrellas():
    suma_total = 0

    for nom_dif in dificultades:
        pts_lista = estrellas_progreso[nom_dif]
        sub_suma = sum(pts_lista)
        suma_total += sub_suma

        lbl_sub_col, filas_estrellas_col = ui_columnas_estrellas[nom_dif]
        lbl_sub_col.text = f"{sub_suma} / {MAX_ESTRELLAS_DIF}"

        for idx_niv, tri_estrellas in enumerate(filas_estrellas_col):
            ganadas = pts_lista[idx_niv]

            for s_i, est_ent in enumerate(tri_estrellas):
                est_ent.set_encendido(s_i < ganadas)

    lbl_total_estrellas.text = f"{suma_total} / {MAX_ESTRELLAS_TOTAL}"


btn_volver_estrellas = crear_boton_pildora_menu(
    menu_estrellas_ui, "Volver al Menú",
    pos=(0, -0.345, 0.02), escala=(0.42, 0.084),
    col_prin=BTN_MORADO, col_som=BTN_MORADO_S, col_txt=color.white,
    escala_txt=1.15, offset_txt_x=0.028
)

hx, hy = -0.125, -0.345
Entity(parent=menu_estrellas_ui, model='quad', position=(hx, hy - 0.006, -0.03), scale=(0.024, 0.020), color=color.white)
Entity(parent=menu_estrellas_ui, model='quad', position=(hx, hy + 0.006, -0.03), scale=(0.022, 0.022), rotation_z=45, color=color.white)
Entity(parent=menu_estrellas_ui, model='quad', position=(hx, hy - 0.010, -0.04), scale=(0.008, 0.012), color=BTN_MORADO)


# =====================================================================
# 7. PANTALLA 3: CÓMO JUGAR
# =====================================================================

crear_panel_redondeado(menu_ayuda_ui, 0, 0, 0.10, 0.88, 0.74, PANEL_OSCURO, BANNER_BORDE, radio=0.05)
crear_capsula(menu_ayuda_ui, 0, 0.27, 0.03, 0.44, 0.072, CINTA_ORO)

Text(parent=menu_ayuda_ui, text="Cómo Jugar", position=(0, 0.27, -0.04), origin=(0, 0), scale=1.85, color=TEXTO_CAFE)

Text(
    parent=menu_ayuda_ui,
    text=(
        "1. Haz CLIC IZQUIERDO sobre el disco superior de cualquier torre\n"
        "   y mantén presionado para levantarlo.\n\n"
        "2. ARRASTRA el disco hacia otra torre: verás una silueta luminosa\n"
        "   indicando si el movimiento es válido (Verde) o inválido (Rojo).\n\n"
        "3. Regla de oro: Nunca coloques un disco más grande sobre uno pequeño.\n\n"
        "4. Lleva todos los discos a la Torre C en la menor cantidad de movimientos\n"
        "   para conseguir las 3 estrellas de cada nivel (45 estrellas en total)."
    ),
    position=(0, 0.01, -0.04),
    origin=(0, 0),
    scale=1.02,
    color=color.white
)

btn_volver_ayuda = crear_boton_pildora_menu(
    menu_ayuda_ui, "Volver al Menú",
    pos=(0, -0.265, 0.02), escala=(0.40, 0.082),
    col_prin=BTN_MORADO, col_som=BTN_MORADO_S, col_txt=color.white,
    escala_txt=1.15, offset_txt_x=0.0
)


# =====================================================================
# 8. ESCENARIO DE JUEGO 2.5D Y HUD
# =====================================================================

crear_capsula(mundo_juego_2d, 0, -2.16, 0.93, 13.5, 1.00, MADERA_SOMBRA)
crear_capsula(mundo_juego_2d, 0, -2.10, 0.90, 13.3, 0.88, MADERA_OSCURA)
crear_capsula(mundo_juego_2d, 0, -2.06, 0.86, 13.1, 0.78, MADERA_CLARA)
crear_capsula(mundo_juego_2d, 0, -1.84, 0.85, 12.6, 0.14, MADERA_LUZ)

etiquetas_torres = ["Torre A", "Torre B", "Torre C"]

ALTURA_POSTE = 3.85
ANCHO_POSTE = 0.54

for i, x in enumerate(posiciones_x):

    placa = crear_capsula(mundo_juego_2d, x, -2.08, 0.74, 2.1, 0.46, MADERA_SOMBRA)

    Text(
        parent=placa,
        text=etiquetas_torres[i],
        position=(0, 0.02, -0.1),
        origin=(0, 0),
        scale=14,
        color=ORO_TOPE_POSTE
    )

    crear_capsula(mundo_juego_2d, x, -1.52, 0.76, 2.3, 0.26, ORO_PLACA_S)

    anillo = crear_capsula(mundo_juego_2d, x, -1.47, 0.70, 2.2, 0.24, ORO_PLACA)
    anillos_base.append(anillo)

    Y_CENTRO = -1.48 + (ALTURA_POSTE / 2)
    Y_TOPE = -1.48 + ALTURA_POSTE

    # Poste de madera
    Entity(parent=mundo_juego_2d, model="quad", position=(x, Y_CENTRO, 0.66), scale=(ANCHO_POSTE, ALTURA_POSTE), color=MADERA_CLARA)
    Entity(parent=mundo_juego_2d, model="quad", position=(x - 0.17, Y_CENTRO, 0.65), scale=(0.15, ALTURA_POSTE), color=MADERA_LUZ)
    Entity(parent=mundo_juego_2d, model="quad", position=(x + 0.17, Y_CENTRO, 0.65), scale=(0.18, ALTURA_POSTE), color=MADERA_OSCURA)

    crear_capsula(mundo_juego_2d, x, Y_TOPE + 0.01, 0.64, ANCHO_POSTE + 0.12, 0.20, ORO_TOPE_POSTE)

    ghost = Entity(
        parent=mundo_juego_2d,
        model="quad",
        position=(x, BASE_DISCOS_Y, 0.25),
        scale=(2.2, ALTO_DISCO - 0.04),
        color=c_rgb(100, 235, 120, 120),
        enabled=False
    )

    hologramas_postes.append(ghost)


# HUD superior
crear_panel_redondeado(juego_ui, 0, 0.43, 0.08, 1.62, 0.10, BANNER_AZUL, BANNER_BORDE, radio=0.035)

nivel_text = Text(parent=juego_ui, text="Fácil - Nivel 1", position=(-0.62, 0.43, -0.04), origin=(0, 0), scale=1.18, color=ORO_VIVO)
temporizador = Text(parent=juego_ui, text="Tiempo: 00:00", position=(-0.22, 0.43, -0.04), origin=(0, 0), scale=1.15, color=color.white)
contador = Text(parent=juego_ui, text="Movs: 0", position=(0.14, 0.43, -0.04), origin=(0, 0), scale=1.15, color=BTN_VERDE)

for s_i in range(3):
    est_h = crear_estrella_5p(juego_ui, pos=(0.35 + s_i * 0.042, 0.43, -0.04), tam=0.034, encendido=True, con_sombra=True)
    estrellas_hud_vivo.append(est_h)

discos_text = Text(parent=juego_ui, text="Meta: 7 movs", position=(0.62, 0.43, -0.04), origin=(0, 0), scale=1.08, color=c_rgb(200, 225, 255))

crear_panel_redondeado(juego_ui, 0, 0.31, 0.08, 0.92, 0.068, PANEL_OSCURO, BANNER_BORDE, radio=0.028)

mensaje = Text(
    parent=juego_ui,
    text="Arrastra los discos hacia la Torre C",
    position=(0, 0.31, -0.04),
    origin=(0, 0),
    scale=1.10,
    color=color.white
)

boton_menu_juego = crear_boton_pildora_menu(
    juego_ui, "Menú",
    pos=(-0.64, -0.43, 0.02), escala=(0.24, 0.076),
    col_prin=BTN_MORADO, col_som=BTN_MORADO_S, col_txt=color.white,
    escala_txt=1.10, offset_txt_x=0.0
)

boton_reiniciar = crear_boton_pildora_menu(
    juego_ui, "Reiniciar",
    pos=(0.64, -0.43, 0.02), escala=(0.24, 0.076),
    col_prin=BTN_ROJO, col_som=BTN_ROJO_S, col_txt=TEXTO_ROJO_OSC,
    escala_txt=1.10, offset_txt_x=0.0
)

boton_siguiente = crear_boton_pildora_menu(
    juego_ui, "Siguiente Nivel »",
    pos=(0, -0.43, 0.02), escala=(0.38, 0.080),
    col_prin=BTN_AMARILLO, col_som=BTN_AMARILLO_S, col_txt=TEXTO_CAFE,
    escala_txt=1.15, offset_txt_x=0.0
)

boton_siguiente.set_visible_completo(False)


# =====================================================================
# 9. LÓGICA DE JUEGO, DISCOS Y ARRASTRAR Y SOLTAR
# =====================================================================

def calcular_estrellas_actuales():
    mov_optimos = (2 ** NUM_DISCOS) - 1
    lim_3 = max(mov_optimos + 3, int(mov_optimos * 1.40))
    lim_2 = max(mov_optimos + 10, int(mov_optimos * 2.25))

    if movimientos <= lim_3:
        return 3
    elif movimientos <= lim_2:
        return 2

    return 1


def actualizar_estrellas_hud():
    est_act = calcular_estrellas_actuales()

    for i, e_ui in enumerate(estrellas_hud_vivo):
        e_ui.set_encendido(i < est_act)


def obtener_mouse_mundo():
    # CORRECCIÓN: mouse.x ya viene escalado por el aspect ratio,
    # por eso no hay que multiplicarlo otra vez.
    return mouse.x * camera.fov, mouse.y * camera.fov


def calcular_y_disco(indice_en_torre):
    return BASE_DISCOS_Y + indice_en_torre * ALTO_DISCO


def crear_onda_choque(x, y, col_disco):
    onda = Entity(
        parent=mundo_juego_2d,
        model="circle",
        position=(x, y, 0.3),
        scale=(0.5, 0.16),
        color=c_rgb(int(col_disco.r * 255), int(col_disco.g * 255), int(col_disco.b * 255), 165)
    )

    ondas_choque.append(onda)


def lanzar_fuegos_artificiales():
    for cx in posiciones_x:
        for _ in range(18):
            ang = random.uniform(0, math.pi * 2)
            vel = random.uniform(2.0, 5.8)

            p = Entity(
                parent=mundo_juego_2d,
                model=MALLA_ESTRELLA,
                position=(cx, 0.6, -0.2),
                scale=(0.3, 0.3, 1),
                color=random.choice(COLORES_DISCOS),
                double_sided=True
            )

            tam_p = random.uniform(0.25, 0.5)
            p.scale = (tam_p, tam_p, 1)
            p.vx = math.cos(ang) * vel
            p.vy = math.sin(ang) * vel + 1.8
            p.vida = random.uniform(0.9, 1.5)

            particulas_efecto.append(p)


def construir_nivel():
    global NUM_DISCOS, movimientos, tiempo, cronometro_activo, juego_terminado
    global disco_arrastrado, torre_origen_arrastre

    for d in todos_discos:
        destroy(d)

    todos_discos.clear()

    for t in torres:
        t.clear()

    for g in hologramas_postes:
        g.enabled = False

    disco_arrastrado = None
    torre_origen_arrastre = None

    dif_nombre = dificultades[indice_dificultad]
    NUM_DISCOS = config_discos[dif_nombre][nivel_actual - 1]

    mov_optimos = (2 ** NUM_DISCOS) - 1

    movimientos = 0
    tiempo = 0.0
    cronometro_activo = False
    juego_terminado = False

    nivel_text.text = f"{dif_nombre} - Nivel {nivel_actual}"
    temporizador.text = "Tiempo: 00:00"
    contador.text = "Movs: 0"
    discos_text.text = f"Discos: {NUM_DISCOS} (Meta: {mov_optimos})"
    mensaje.text = "Arrastra los discos de la Torre A hacia la Torre C"
    mensaje.color = color.white

    actualizar_estrellas_hud()
    boton_siguiente.set_visible_completo(False)

    ancho_max = 3.35
    ancho_min = 1.25
    paso = (ancho_max - ancho_min) / max(1, NUM_DISCOS - 1)

    for i in range(NUM_DISCOS):
        tam_val = NUM_DISCOS - i
        ancho_d = ancho_min + (tam_val - 1) * paso
        col_d = COLORES_DISCOS[(tam_val - 1) % len(COLORES_DISCOS)]
        y_pos = calcular_y_disco(i)

        disco = Entity(
            parent=mundo_juego_2d,
            model="quad",
            position=(posiciones_x[0], y_pos, 0.1 - i * 0.01),
            scale=(ancho_d, ALTO_DISCO - 0.04),
            color=col_d
        )

        disco.valor = tam_val
        disco.ancho_propio = ancho_d
        disco.color_base = col_d
        disco.target_pos = Vec3(posiciones_x[0], y_pos, 0.1 - i * 0.01)

        r_cap = (ALTO_DISCO - 0.04) / ancho_d

        Entity(parent=disco, model="circle", position=(-0.5, 0, 0.01), scale=(r_cap, 1.0), color=col_d)
        Entity(parent=disco, model="circle", position=(0.5, 0, 0.01), scale=(r_cap, 1.0), color=col_d)

        # Brillo superior y sombra inferior.
        # IMPORTANTE: los discos no llevan números.
        Entity(parent=disco, model="quad", position=(0, 0.26, -0.01), scale=(0.90, 0.20), color=color.rgba(1, 1, 1, 0.30))
        Entity(parent=disco, model="quad", position=(0, -0.32, -0.01), scale=(0.96, 0.22), color=color.rgba(0, 0, 0, 0.22))

        torres[0].append(disco)
        todos_discos.append(disco)


def verificar_victoria():
    global juego_terminado, cronometro_activo

    if len(torres[2]) == NUM_DISCOS:
        juego_terminado = True
        cronometro_activo = False

        est_ganadas = calcular_estrellas_actuales()
        dif_nom = dificultades[indice_dificultad]

        if est_ganadas > estrellas_progreso[dif_nom][nivel_actual - 1]:
            estrellas_progreso[dif_nom][nivel_actual - 1] = est_ganadas

        actualizar_selector_menu()
        actualizar_vista_estrellas()
        lanzar_fuegos_artificiales()

        mensaje.text = f"¡Nivel Completado! Obtuviste {est_ganadas} / 3 Estrellas"
        mensaje.color = ORO_VIVO

        boton_siguiente.set_visible_completo(True)


# =====================================================================
# 10. NAVEGACIÓN ENTRE PANTALLAS Y CONTROL DEL MOUSE
# =====================================================================

def mostrar_menu_principal():
    menu_principal_ui.enabled = True
    menu_estrellas_ui.enabled = False
    menu_ayuda_ui.enabled = False
    juego_ui.enabled = False
    mundo_juego_2d.enabled = False

    actualizar_selector_menu()


def mostrar_tus_estrellas():
    menu_principal_ui.enabled = False
    menu_estrellas_ui.enabled = True
    menu_ayuda_ui.enabled = False
    juego_ui.enabled = False
    mundo_juego_2d.enabled = False

    actualizar_vista_estrellas()


def mostrar_como_jugar():
    menu_principal_ui.enabled = False
    menu_estrellas_ui.enabled = False
    menu_ayuda_ui.enabled = True
    juego_ui.enabled = False
    mundo_juego_2d.enabled = False


def iniciar_partida():
    menu_principal_ui.enabled = False
    menu_estrellas_ui.enabled = False
    menu_ayuda_ui.enabled = False
    juego_ui.enabled = True
    mundo_juego_2d.enabled = True

    construir_nivel()


def avanzar_siguiente_nivel():
    global nivel_actual, indice_dificultad

    if nivel_actual < 5:
        nivel_actual += 1
    else:
        nivel_actual = 1
        indice_dificultad = (indice_dificultad + 1) % len(dificultades)

    construir_nivel()


btn_iniciar.on_click = iniciar_partida
btn_estrellas.on_click = mostrar_tus_estrellas
btn_como_jugar.on_click = mostrar_como_jugar
btn_volver_estrellas.on_click = mostrar_menu_principal
btn_volver_ayuda.on_click = mostrar_menu_principal

boton_menu_juego.on_click = mostrar_menu_principal
boton_reiniciar.on_click = construir_nivel
boton_siguiente.on_click = avanzar_siguiente_nivel


def obtener_torre_cercana(mx):
    distancias = [abs(mx - px) for px in posiciones_x]
    idx_min = distancias.index(min(distancias))

    if distancias[idx_min] < 2.35:
        return idx_min

    return None


def input(key):
    global disco_arrastrado, torre_origen_arrastre, offset_x, offset_y
    global movimientos, cronometro_activo

    if not mundo_juego_2d.enabled or juego_terminado:
        return

    mx, my = obtener_mouse_mundo()

    if key == "left mouse down":

        for idx_t, t in enumerate(torres):
            if len(t) > 0:
                disco_sup = t[-1]

                mitad_w = disco_sup.ancho_propio / 2 + 0.25
                mitad_h = ALTO_DISCO / 2 + 0.18

                if abs(mx - disco_sup.x) <= mitad_w and abs(my - disco_sup.y) <= mitad_h:
                    disco_arrastrado = disco_sup
                    torre_origen_arrastre = idx_t

                    offset_x = disco_sup.x - mx
                    offset_y = disco_sup.y - my

                    disco_arrastrado.z = -0.5

                    if not cronometro_activo:
                        cronometro_activo = True

                    break

    elif key == "left mouse up" and disco_arrastrado is not None:

        idx_destino = obtener_torre_cercana(disco_arrastrado.x)
        movimiento_valido = False

        if idx_destino is not None and idx_destino != torre_origen_arrastre:
            torre_dest = torres[idx_destino]

            if len(torre_dest) == 0 or torre_dest[-1].valor > disco_arrastrado.valor:
                movimiento_valido = True

        if movimiento_valido:
            torres[torre_origen_arrastre].pop()
            torres[idx_destino].append(disco_arrastrado)

            nueva_y = calcular_y_disco(len(torres[idx_destino]) - 1)

            disco_arrastrado.target_pos = Vec3(
                posiciones_x[idx_destino],
                nueva_y,
                0.1 - len(torres[idx_destino]) * 0.01
            )

            movimientos += 1
            contador.text = f"Movs: {movimientos}"

            actualizar_estrellas_hud()

            crear_onda_choque(
                posiciones_x[idx_destino],
                nueva_y,
                disco_arrastrado.color_base
            )

            mensaje.text = f"Disco colocado en {etiquetas_torres[idx_destino]}"
            mensaje.color = BTN_VERDE

            verificar_victoria()

        else:
            y_orig = calcular_y_disco(len(torres[torre_origen_arrastre]) - 1)

            disco_arrastrado.target_pos = Vec3(
                posiciones_x[torre_origen_arrastre],
                y_orig,
                0.1 - len(torres[torre_origen_arrastre]) * 0.01
            )

            if idx_destino is not None and idx_destino != torre_origen_arrastre:
                mensaje.text = "¡Movimiento inválido! No pongas un disco grande sobre uno pequeño"
                mensaje.color = BTN_ROJO

        for g in hologramas_postes:
            g.enabled = False

        disco_arrastrado = None
        torre_origen_arrastre = None


# =====================================================================
# 11. BUCLE PRINCIPAL DE ANIMACIÓN
# =====================================================================

def update():
    global tiempo

    for pet in petalos_sakura:
        pet.y -= pet.vel_y * time.dt
        pet.x += (pet.vel_x + math.sin(time.time() * 1.8 + pet.fase) * 0.015) * time.dt
        pet.rotation_z += 35 * time.dt

        if pet.y < -0.52:
            pet.y = 0.52
            pet.x = random.uniform(-0.88, 0.88)

    if menu_estrellas_ui.enabled:
        pulso = 1.0 + math.sin(time.time() * 3.2) * 0.05
        estrella_top_grande.scale = (pulso, pulso, 1)

    if not mundo_juego_2d.enabled:
        return

    if cronometro_activo and not juego_terminado:
        tiempo += time.dt

        mins = int(tiempo) // 60
        segs = int(tiempo) % 60

        temporizador.text = f"Tiempo: {mins:02d}:{segs:02d}"

    if disco_arrastrado is not None:

        mx, my = obtener_mouse_mundo()

        disco_arrastrado.x = mx + offset_x
        disco_arrastrado.y = my + offset_y

        idx_cercano = obtener_torre_cercana(disco_arrastrado.x)

        for i, g in enumerate(hologramas_postes):

            if i == idx_cercano:
                g.enabled = True
                g.scale_x = disco_arrastrado.ancho_propio

                t_dest = torres[i]

                es_valido = (
                    len(t_dest) == 0
                    or t_dest[-1].valor > disco_arrastrado.valor
                    or i == torre_origen_arrastre
                )

                y_ghost = calcular_y_disco(
                    len(t_dest) - (1 if i == torre_origen_arrastre else 0)
                )

                g.y = y_ghost

                g.color = (
                    c_rgb(100, 240, 120, 130)
                    if es_valido
                    else c_rgb(245, 80, 80, 140)
                )

            else:
                g.enabled = False

    for d in todos_discos:
        if d is not disco_arrastrado:
            d.position = lerp(d.position, d.target_pos, time.dt * 14)

    for onda in ondas_choque[:]:
        onda.scale_x += time.dt * 4.8
        onda.scale_y += time.dt * 1.6
        onda.alpha -= time.dt * 1.9

        if onda.alpha <= 0.05:
            ondas_choque.remove(onda)
            destroy(onda)

    for p in particulas_efecto[:]:
        p.x += p.vx * time.dt
        p.y += p.vy * time.dt
        p.vy -= 4.8 * time.dt
        p.vida -= time.dt
        p.rotation_z += 120 * time.dt

        if p.vida <= 0:
            particulas_efecto.remove(p)
            destroy(p)


actualizar_selector_menu()
actualizar_vista_estrellas()

app.run()