import pygame
import random
import math

pygame.init()

# --- Configuración de Pantalla ---
ANCHO, ALTO = 750, 650  # Un poco más de altura para dar espacio cómodo al HUD
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("NEON HIGHWAY - Cyberpunk Edition")
reloj = pygame.time.Clock()

# --- Paleta Neon / Cyberpunk ---
COLOR_FONDO = (8, 6, 16)
COLOR_GRID = (22, 18, 40)
COLOR_META = (0, 255, 170)
COLOR_JUGADOR = (0, 210, 255)

COLORES_CARROS = [
    (255, 0, 110),   # Neon Pink
    (255, 190, 11),  # Amber Gold
    (131, 56, 236),  # Ultra Violet
    (255, 87, 51),   # Flame Orange
]

# --- Fuentes Elegantes ---
try:
    fuente_hud = pygame.font.SysFont("Trebuchet MS", 16, bold=True)
    fuente_meta = pygame.font.SysFont("Trebuchet MS", 18, bold=True)
    fuente_big = pygame.font.SysFont("Impact", 48)
    fuente_sub = pygame.font.SysFont("Consolas", 18)
except:
    fuente_hud = fuente_meta = fuente_sub = pygame.font.Font(None, 24)
    fuente_big = pygame.font.Font(None, 60)

# --- Renderizado de Texto con Glow y Sombra ---
def dibujar_texto_pro(superficie, texto, fuente, color_texto, pos, sombra=True, glow=False, color_glow=None, centrado=False):
    x, y = pos
    if glow and color_glow:
        for offset in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
            surf_g = fuente.render(texto, True, color_glow)
            r_g = surf_g.get_rect(center=(x + offset[0], y + offset[1])) if centrado else surf_g.get_rect(topleft=(x + offset[0], y + offset[1]))
            superficie.blit(surf_g, r_g)
            
    if sombra:
        surf_s = fuente.render(texto, True, (0, 0, 0))
        r_s = surf_s.get_rect(center=(x + 2, y + 2)) if centrado else surf_s.get_rect(topleft=(x + 2, y + 2))
        superficie.blit(surf_s, r_s)

    surf_t = fuente.render(texto, True, color_texto)
    r_t = surf_t.get_rect(center=(x, y)) if centrado else surf_t.get_rect(topleft=(x, y))
    superficie.blit(surf_t, r_t)

# --- Generación de Sonidos Sintetizados ---
def generar_sonido(freq, duracion_ms, tipo="sine"):
    sample_rate = 44100
    n_samples = int(sample_rate * (duracion_ms / 1000.0))
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        if tipo == "sine":
            val = int(127 + 127 * math.sin(2 * math.pi * freq * t))
        elif tipo == "square":
            val = 220 if math.sin(2 * math.pi * freq * t) > 0 else 35
        elif tipo == "noise":
            val = random.randint(0, 255)
        buf.append(max(0, min(255, val)))
    return pygame.mixer.Sound(buffer=bytes(buf))

try:
    pygame.mixer.init(frequency=44100, size=-8, channels=1)
    snd_meta = generar_sonido(650, 120, "sine")
    snd_muerte = generar_sonido(100, 250, "noise")
    snd_powerup = generar_sonido(880, 150, "square")
    snd_dash = generar_sonido(300, 80, "sine")
except:
    snd_meta = snd_muerte = snd_powerup = snd_dash = None

# --- Clases del Juego ---
class Jugador:
    def __init__(self, alto_hud):
        self.radio = 14
        self.alto_hud = alto_hud
        self.reset_pos()
        self.speed = 4.5
        self.dash_cooldown = 0
        self.escudo_activo = False
        self.multiplicador = 1

    def reset_pos(self):
        self.x = ANCHO // 2
        # Posición inicial holgada por encima del HUD inferior
        self.y = ALTO - self.alto_hud - self.radio - 15

    def actualizar(self, teclas):
        dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
        dy = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        if teclas[pygame.K_SPACE] and self.dash_cooldown == 0 and (dx != 0 or dy != 0):
            self.x += dx * 45
            self.y += dy * 45
            self.dash_cooldown = 45
            if snd_dash: snd_dash.play()
        else:
            self.x += dx * self.speed
            self.y += dy * self.speed

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # Restricción: No se oculta debajo del HUD (límite inferior ajustado)
        self.x = max(self.radio + 5, min(ANCHO - self.radio - 5, self.x))
        self.y = max(50 + self.radio, min(ALTO - self.alto_hud - self.radio - 2, self.y))

    def dibujar(self, superficie, tick):
        glow_radius = self.radio + int(math.sin(tick * 0.2) * 3) + 3
        if self.escudo_activo:
            pygame.draw.circle(superficie, (0, 255, 255), (int(self.x), int(self.y)), glow_radius + 6, 2)
        
        pygame.draw.circle(superficie, (0, 100, 200), (int(self.x), int(self.y)), glow_radius)
        pygame.draw.circle(superficie, COLOR_JUGADOR, (int(self.x), int(self.y)), self.radio)
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.x), int(self.y)), self.radio - 4)


class Vehiculo:
    def __init__(self, y, vel, ancho):
        self.y = y
        self.ancho = ancho
        self.alto = 18
        self.vel = vel
        self.color = random.choice(COLORES_CARROS)
        self.x = random.randint(-ANCHO, 0) if vel > 0 else random.randint(ANCHO, ANCHO * 2)

    def actualizar(self):
        self.x += self.vel
        if self.vel > 0 and self.x > ANCHO + 60:
            self.x = -self.ancho - random.randint(30, 120)
        elif self.vel < 0 and self.x < -self.ancho - 60:
            self.x = ANCHO + random.randint(30, 120)

    def dibujar(self, sup):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(sup, self.color, rect, border_radius=5)
        pygame.draw.rect(sup, (255, 255, 255), rect, width=1, border_radius=5)
        
        faro_col = (255, 255, 200)
        if self.vel > 0:
            pygame.draw.circle(sup, faro_col, (int(self.x + self.ancho - 2), int(self.y + 4)), 2)
            pygame.draw.circle(sup, faro_col, (int(self.x + self.ancho - 2), int(self.y + 14)), 2)
        else:
            pygame.draw.circle(sup, faro_col, (int(self.x + 2), int(self.y + 4)), 2)
            pygame.draw.circle(sup, faro_col, (int(self.x + 2), int(self.y + 14)), 2)


class ItemPowerUp:
    def __init__(self, x, y, tipo):
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.tipo = tipo

    def dibujar(self, sup, tick):
        offset = math.sin(tick * 0.1) * 3
        pos_y = self.rect.y + offset
        
        if self.tipo == 'escudo':
            pygame.draw.polygon(sup, (0, 230, 255), [
                (self.rect.centerx, pos_y),
                (self.rect.right, pos_y + 8),
                (self.rect.centerx, pos_y + 18),
                (self.rect.left, pos_y + 8)
            ])
        elif self.tipo == 'moneda':
            pygame.draw.circle(sup, (255, 215, 0), (self.rect.centerx, int(pos_y + 10)), 8)
        elif self.tipo == 'x2':
            pygame.draw.rect(sup, (255, 0, 128), (self.rect.x, int(pos_y), 20, 20), border_radius=4)


class Particula:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.life = random.randint(15, 30)
        self.color = color

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1


def cargar_nivel(num_nivel, alto_hud):
    vehiculos = []
    num_carriles = min(6 + (num_nivel // 2), 10)
    y_inicio = 80
    # Espaciado de carriles respetando la barra inferior HUD
    paso_y = (ALTO - alto_hud - 140) // num_carriles

    for i in range(num_carriles):
        y_pos = y_inicio + i * paso_y
        dir = 1 if i % 2 == 0 else -1
        vel = (random.uniform(3.0, 4.5) + (num_nivel * 0.35)) * dir
        
        for j in range(random.randint(2, 3)):
            v = Vehiculo(y_pos, vel, random.randint(50, 80))
            v.x += j * (ANCHO // 2.2)
            vehiculos.append(v)

    powerups = []
    for _ in range(random.randint(1, 3)):
        px = random.randint(50, ANCHO - 50)
        py = random.randint(100, ALTO - alto_hud - 80)
        tipo = random.choice(['moneda', 'moneda', 'escudo', 'x2'])
        powerups.append(ItemPowerUp(px, py, tipo))

    return vehiculos, powerups


# --- Instancias Iniciales ---
ALTO_HUD = 45
jugador = Jugador(ALTO_HUD)
nivel = 1
puntos = 0
vidas = 3
particulas = []
vehiculos, powerups = cargar_nivel(nivel, ALTO_HUD)

meta_rect = pygame.Rect(0, 0, ANCHO, 50)
correr = True
game_over = False
tick = 0

# --- Bucle Principal ---
while correr:
    tick += 1
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            correr = False
        if evento.type == pygame.KEYDOWN and game_over:
            if evento.key == pygame.K_SPACE:
                nivel, puntos, vidas = 1, 0, 3
                jugador.reset_pos()
                jugador.escudo_activo = False
                vehiculos, powerups = cargar_nivel(nivel, ALTO_HUD)
                game_over = False

    if not game_over:
        teclas = pygame.key.get_pressed()
        jugador.actualizar(teclas)

        for v in vehiculos:
            v.actualizar()

            cx = max(v.x, min(jugador.x, v.x + v.ancho))
            cy = max(v.y, min(jugador.y, v.y + v.alto))
            dist = math.hypot(jugador.x - cx, jugador.y - cy)

            if dist < jugador.radio:
                if jugador.escudo_activo:
                    jugador.escudo_activo = False
                    v.x = -200
                    if snd_powerup: snd_powerup.play()
                else:
                    if snd_muerte: snd_muerte.play()
                    for _ in range(25):
                        particulas.append(Particula(jugador.x, jugador.y, COLOR_JUGADOR))
                    
                    vidas -= 1
                    jugador.reset_pos()
                    if vidas <= 0:
                        game_over = True

        for p in powerups[:]:
            if p.rect.collidepoint(jugador.x, jugador.y):
                if snd_powerup: snd_powerup.play()
                if p.tipo == 'escudo': jugador.escudo_activo = True
                elif p.tipo == 'moneda': puntos += 150 * jugador.multiplicador
                elif p.tipo == 'x2': jugador.multiplicador = 2
                powerups.remove(p)

        if jugador.y - jugador.radio <= meta_rect.bottom:
            if snd_meta: snd_meta.play()
            puntos += (200 * nivel) * jugador.multiplicador
            nivel += 1
            jugador.multiplicador = 1
            jugador.reset_pos()
            vehiculos, powerups = cargar_nivel(nivel, ALTO_HUD)

    for p in particulas[:]:
        p.actualizar()
        if p.life <= 0:
            particulas.remove(p)

    # --- RENDERIZADO ---
    ventana.fill(COLOR_FONDO)

    # Grid Cyberpunk
    for gx in range(0, ANCHO, 35):
        pygame.draw.line(ventana, COLOR_GRID, (gx, 50), (gx, ALTO - ALTO_HUD), 1)
    for gy in range(50, ALTO - ALTO_HUD, 35):
        pygame.draw.line(ventana, COLOR_GRID, (0, gy), (ANCHO, gy), 1)

    # Zona Meta
    pygame.draw.rect(ventana, COLOR_META, meta_rect)
    pygame.draw.rect(ventana, (255, 255, 255), meta_rect, 2)
    dibujar_texto_pro(ventana, "OVERDRIVE GOAL", fuente_meta, (10, 30, 20), (ANCHO // 2, 25), sombra=False, glow=True, color_glow=(150, 255, 200), centrado=True)

    # Objetos y Entidades
    for p in powerups: p.dibujar(ventana, tick)
    for v in vehiculos: v.dibujar(ventana)
    for p in particulas: pygame.draw.circle(ventana, p.color, (int(p.x), int(p.y)), max(1, p.life // 6))
    
    # Dibujar Jugador (Aseguramos que siempre esté por encima)
    if not game_over: 
        jugador.dibujar(ventana, tick)

    # --- BARRA HUD SUPERIOR Y INFERIOR ESTILIZADA ---
    hud_bg = pygame.Rect(0, ALTO - ALTO_HUD, ANCHO, ALTO_HUD)
    pygame.draw.rect(ventana, (12, 10, 22), hud_bg)
    pygame.draw.line(ventana, COLOR_JUGADOR, (0, ALTO - ALTO_HUD), (ANCHO, ALTO - ALTO_HUD), 2)

    # Textos Estilizados HUD
    dibujar_texto_pro(ventana, f"NIVEL  {nivel}", fuente_hud, (0, 210, 255), (20, ALTO - 30), glow=True, color_glow=(0, 100, 150))
    dibujar_texto_pro(ventana, f"PUNTOS  {puntos}", fuente_hud, (255, 215, 0), (160, ALTO - 30), glow=True, color_glow=(150, 120, 0))
    dibujar_texto_pro(ventana, f"VIDAS  {'♥ ' * vidas}", fuente_hud, (255, 0, 110), (320, ALTO - 30), glow=True, color_glow=(150, 0, 60))

    # Indicador de Dash
    if jugador.dash_cooldown == 0:
        dibujar_texto_pro(ventana, "DASH: LISTO [ESPACIO]", fuente_hud, (0, 255, 170), (ANCHO - 220, ALTO - 30), glow=True, color_glow=(0, 120, 80))
    else:
        dibujar_texto_pro(ventana, "DASH: CARGANDO...", fuente_hud, (120, 120, 140), (ANCHO - 220, ALTO - 30), sombra=False)

    # Pantalla Game Over
    if game_over:
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((5, 4, 12, 220))
        ventana.blit(overlay, (0, 0))

        dibujar_texto_pro(ventana, "SYSTEM FAILURE", fuente_big, (255, 0, 110), (ANCHO // 2, ALTO // 2 - 60), glow=True, color_glow=(180, 0, 80), centrado=True)
        dibujar_texto_pro(ventana, f"Puntuación Final: {puntos}", fuente_sub, (240, 240, 255), (ANCHO // 2, ALTO // 2 + 10), centrado=True)
        dibujar_texto_pro(ventana, "[ PRESIONA ESPACIO PARA REINICIAR ]", fuente_sub, (0, 255, 170), (ANCHO // 2, ALTO // 2 + 60), glow=True, color_glow=(0, 100, 70), centrado=True)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()