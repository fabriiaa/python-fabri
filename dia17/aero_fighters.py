import pygame
import random
import sys

# Inicialización
pygame.init()

# Pantalla en formato arcade vertical (480x640)
ANCHO = 480
ALTO = 640
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aero Fighters - Python Edition")

# Colores Arcade
NEGRO = (15, 15, 25)
AZUL_AVION = (41, 128, 185)
AMARILLO_DISPARO = (241, 196, 15)
ROJO_ENEMIGO = (231, 76, 60)
VERDE_POWERUP = (46, 204, 113)
BLANCO = (236, 240, 241)
ORANGE_BOMBA = (230, 126, 34)

reloj = pygame.time.Clock()
FPS = 60
fuente = pygame.font.SysFont("Arial", 20, bold=True)

# ----------------- CLASES -----------------

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Dibujar silueta de jet
        pygame.draw.polygon(self.image, AZUL_AVION, [(20, 0), (0, 35), (10, 40), (20, 30), (30, 40), (40, 35)])
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.velocidad = 7
        self.nivel_disparo = 1
        self.vidas = 3
        self.bombas = 2
        self.cadencia = 150 # milisegundos entre disparos
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self):
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

        if teclas[pygame.K_SPACE]:
            self.disparar()

    def disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia:
            self.ultimo_disparo = ahora
            if self.nivel_disparo == 1:
                bala = Bala(self.rect.centerx, self.rect.top)
                todos_sprites.add(bala)
                balas.add(bala)
            elif self.nivel_disparo == 2:
                b1 = Bala(self.rect.left + 5, self.rect.top)
                b2 = Bala(self.rect.right - 5, self.rect.top)
                todos_sprites.add(b1, b2)
                balas.add(b1, b2)
            elif self.nivel_disparo >= 3:
                b1 = Bala(self.rect.centerx, self.rect.top)
                b2 = Bala(self.rect.left, self.rect.top + 10, -2)
                b3 = Bala(self.rect.right, self.rect.top + 10, 2)
                todos_sprites.add(b1, b2, b3)
                balas.add(b1, b2, b3)


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, velocidad_base):
        super().__init__()
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        # Dibujar silueta de avión enemigo
        pygame.draw.polygon(self.image, ROJO_ENEMIGO, [(20, 35), (0, 10), (10, 0), (20, 10), (30, 0), (40, 10)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.vy = random.randint(3, 3 + velocidad_base)
        self.vx = random.choice([-1, 0, 1])

    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, vx=0):
        super().__init__()
        self.image = pygame.Surface((6, 15))
        self.image.fill(AMARILLO_DISPARO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vy = -12
        self.vx = vx

    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(VERDE_POWERUP)
        # Dibujar una "P"
        letra = fuente.render("P", True, NEGRO)
        self.image.blit(letra, (4, -2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vy = 2

    def update(self):
        self.rect.y += self.vy
        if self.rect.top > ALTO:
            self.kill()

# ----------------- CONFIGURACIÓN DE GRUPOS -----------------

todos_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
powerups = pygame.sprite.Group()

jugador = Jugador()
todos_sprites.add(jugador)

velocidad_dificultad = 1
puntuacion = 0

def generar_enemigos(cantidad):
    for _ in range(cantidad):
        e = Enemigo(velocidad_dificultad)
        todos_sprites.add(e)
        enemigos.add(e)

generar_enemigos(6)

# ----------------- BUCLE PRINCIPAL -----------------

ejecutando = True
while ejecutando:
    reloj.tick(FPS)

    # 1. Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            # Activar Bomba con Tecla X
            if evento.key == pygame.K_x and jugador.bombas > 0:
                jugador.bombas -= 1
                # Limpiar todos los enemigos
                for enemigo in enemigos:
                    puntuacion += 15
                    enemigo.kill()
                # Efecto visual de Bomba
                pantalla.fill(ORANGE_BOMBA)
                pygame.display.flip()
                pygame.time.delay(100)
                # Re-generar ola de enemigos
                generar_enemigos(6)

    # 2. Actualizar Sprites
    todos_sprites.update()

    # 3. Colisiones: Balas -> Enemigos
    impactos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for e in impactos:
        puntuacion += 20
        # Aumentar dificultad paulatinamente
        if puntuacion % 200 == 0:
            velocidad_dificultad += 1
        
        # Chance del 15% de soltar PowerUp
        if random.random() < 0.15:
            pu = PowerUp(e.rect.centerx, e.rect.centery)
            todos_sprites.add(pu)
            powerups.add(pu)

        # Reponer enemigo
        nuevo_e = Enemigo(velocidad_dificultad)
        todos_sprites.add(nuevo_e)
        enemigos.add(nuevo_e)

    # 4. Colisiones: Jugador -> Powerups
    powerup_obtenido = pygame.sprite.spritecollide(jugador, powerups, True)
    for pu in powerup_obtenido:
        if jugador.nivel_disparo < 3:
            jugador.nivel_disparo += 1

    # 5. Colisiones: Jugador -> Enemigos
    golpes = pygame.sprite.spritecollide(jugador, enemigos, True)
    if golpes:
        jugador.vidas -= 1
        jugador.nivel_disparo = max(1, jugador.nivel_disparo - 1) # Reduce poder al perder vida
        
        # Reponer enemigo destruido en la colisión
        nuevo_e = Enemigo(velocidad_dificultad)
        todos_sprites.add(nuevo_e)
        enemigos.add(nuevo_e)

        if jugador.vidas <= 0:
            ejecutando = False # Fin del juego

    # 6. Renderizado / Dibujo
    pantalla.fill(NEGRO)
    
    # Efecto de estrellas de fondo (simulación de velocidad)
    for _ in range(3):
        rx = random.randint(0, ANCHO)
        ry = random.randint(0, ALTO)
        pygame.draw.circle(pantalla, BLANCO, (rx, ry), 1)

    todos_sprites.draw(pantalla)

    # Dibujar HUD (Interfaz)
    txt_puntos = fuente.render(f"PUNTOS: {puntuacion}", True, BLANCO)
    txt_vidas = fuente.render(f"VIDAS: {jugador.vidas}", True, AZUL_AVION)
    txt_bombas = fuente.render(f"BOMBAS [X]: {jugador.bombas}", True, ORANGE_BOMBA)
    txt_power = fuente.render(f"NIVEL ARMA: {jugador.nivel_disparo}", True, VERDE_POWERUP)

    pantalla.blit(txt_puntos, (10, 10))
    pantalla.blit(txt_vidas, (10, 35))
    pantalla.blit(txt_bombas, (ANCHO - 150, 10))
    pantalla.blit(txt_power, (ANCHO - 150, 35))

    pygame.display.flip()

# ----------------- GAME OVER -----------------
pantalla.fill(NEGRO)
txt_game_over = fuente.render("¡GAME OVER!", True, ROJO_ENEMIGO)
txt_final = fuente.render(f"Puntuación Final: {puntuacion}", True, BLANCO)
pantalla.blit(txt_game_over, (ANCHO // 2 - 60, ALTO // 2 - 20))
pantalla.blit(txt_final, (ANCHO // 2 - 90, ALTO // 2 + 20))
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
sys.exit()