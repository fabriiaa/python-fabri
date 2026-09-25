import pygame
import random
import sys

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los Meteoritos 🚀")

# 3. Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
AZUL = (50, 150, 255)

# 4. Configuración del Jugador (Nave)
jugador_ancho = 50
jugador_alto = 50
jugador_x = ANCHO // 2 - jugador_ancho // 2
jugador_y = ALTO - jugador_alto - 20
velocidad_jugador = 8

# 5. Configuración de los Enemigos (Meteoritos)
enemigo_ancho = 40
enemigo_alto = 40
velocidad_enemigo = 6
lista_enemigos = []

# Función para crear un nuevo enemigo en la parte superior
def crear_enemigo():
    x = random.randint(0, ANCHO - enemigo_ancho)
    y = -enemigo_alto
    return pygame.Rect(x, y, enemigo_ancho, enemigo_alto)

# 6. Variables del juego
reloj = pygame.time.Clock()
puntuacion = 0
fuente = pygame.font.SysFont("monospace", 35)
juego_terminado = False

# Frecuencia con la que aparecen los enemigos (en milisegundos)
FRECUENCIA_ENEMIGO = 30
contador_tiempo = 0

# --- BUCLE PRINCIPAL DEL JUEGO ---
while True:
    # Manejo de eventos (Teclado y cerrar ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Reiniciar el juego con la tecla 'R' si perdiste
        if juego_terminado and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                jugador_x = ANCHO // 2 - jugador_ancho // 2
                lista_enemigos.clear()
                velocidad_enemigo = 6
                puntuacion = 0
                juego_terminado = False

    if not juego_terminado:
        # Movimiento del jugador (Mantener presionado)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x > 0:
            jugador_x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_ancho:
            jugador_x += velocidad_jugador

        # Crear rectángulo del jugador actualizado
        rect_jugador = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)

        # Aparición de enemigos de forma progresiva
        contador_tiempo += 1
        if contador_tiempo >= FRECUENCIA_ENEMIGO:
            lista_enemigos.append(crear_enemigo())
            contador_tiempo = 0

        # Mover y actualizar enemigos
        for enemigo in lista_enemigos[:]:
            enemigo.y += velocidad_enemigo
            
            # Si el enemigo sale de la pantalla, el jugador gana puntos
            if enemigo.y > ALTO:
                lista_enemigos.remove(enemigo)
                puntuacion += 1
                # Aumentar la dificultad poco a poco
                if puntuacion % 10 == 0:
                    velocidad_enemigo += 1

            # Detectar colisión entre el jugador y cualquier enemigo
            if rect_jugador.colliderect(enemigo):
                juego_terminado = True

    # --- RENDERIZADO (DIBUJAR EN PANTALLA) ---
    pantalla.fill(NEGRO) # Limpiar pantalla con fondo negro

    if not juego_terminado:
        # Dibujar jugador (Nave azul)
        pygame.draw.rect(pantalla, AZUL, rect_jugador)

        # Dibujar enemigos (Meteoritos rojos)
        for enemigo in lista_enemigos:
            pygame.draw.rect(pantalla, ROJO, enemigo)

        # Mostrar puntuación en vivo
        texto_puntos = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
    else:
        # Pantalla de "Game Over"
        texto_game_over = fuente.render("¡GAME OVER!", True, ROJO)
        texto_reiniciar = fuente.render("Presiona R para reiniciar", True, BLANCO)
        texto_final = fuente.render(f"Puntuación final: {puntuacion}", True, BLANCO)
        
        pantalla.blit(texto_game_over, (ANCHO // 2 - 100, ALTO // 2 - 60))
        pantalla.blit(texto_final, (ANCHO // 2 - 140, ALTO // 2))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - 200, ALTO // 2 + 60))

    # Actualizar los gráficos en la ventana
    pygame.display.update()
    
    # Controlar los FPS (Fotogramas por segundo)
    reloj.tick(60)
