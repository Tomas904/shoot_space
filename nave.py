import pygame
import random
import sys

# Inicializar PyGame
pygame.init()

# Constantes de pantalla
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Inicializar ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Cargar imágenes
nave_img = pygame.Surface((50, 40))
nave_img.fill(AZUL)
enemigo_img = pygame.Surface((40, 30))
enemigo_img.fill(ROJO)
proyectil_img = pygame.Surface((5, 10))
proyectil_img.fill(BLANCO)


#Funcion textos
def mostrar_texto(texto, tamano, x, y):
    fuente = pygame.font.SysFont(None, tamano)
    superficie = fuente.render(texto, True, BLANCO)
    rect = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rect)

#Funcion de muertes enemigas y de la nave
def detectar_colision(rect1, rect2):
    return rect1.colliderect(rect2)


#Clase nave
class Nave:
    def __init__(self):
        self.rect = nave_img.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 5
        self.vidas = 3

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(nave_img, self.rect)

#Clase enemigo
class Enemigo:
    def __init__(self, velocidad):
        self.rect = enemigo_img.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad = velocidad

    def mover(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.__init__(self.velocidad)

    def dibujar(self):
        pantalla.blit(enemigo_img, self.rect)

#Clase proyectil
class Proyectil:
    def __init__(self, x, y):
        self.rect = proyectil_img.get_rect(center=(x, y))
        self.velocidad = -8

    def mover(self):
        self.rect.y += self.velocidad

    def dibujar(self):
        pantalla.blit(proyectil_img, self.rect)


# Menú
opciones_menu = ["Fácil", "Medio", "Difícil", "Progresivo", "Salir"]
opcion_seleccionada = 0
rect_opciones = []

# Variables de juego
velocidad_base = 2
definir_dificultad = False
score = 0

# Lógica del juego
nave = Nave()
enemigos = []
proyectiles = []
menu_activo = True
juego_activo = False
pausado = False
modo_progresivo = False

# Temporizador para agregar enemigos en intervalos
intervalo_agregar_enemigos = 2000  # en milisegundos
ultimo_agregado = pygame.time.get_ticks()


def reiniciar_juego():
    global nave, enemigos, proyectiles, pausado, score, modo_progresivo
    nave = Nave()
    enemigos = []
    proyectiles = []
    pausado = False
    score = 0
    modo_progresivo = False


def mostrar_menu():
    pantalla.fill(NEGRO)
    mostrar_texto("Space Shooter", 60, ANCHO // 2, ALTO // 4)

    global rect_opciones
    rect_opciones = []

    for i, opcion in enumerate(opciones_menu):
        color = BLANCO if i == opcion_seleccionada else (150, 150, 150)
        fuente = pygame.font.SysFont(None, 40)
        superficie = fuente.render(opcion, True, color)
        rect = superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + i * 50))
        rect_opciones.append(rect)  # Guardar los rectángulos para comprobar clics
        pantalla.blit(superficie, rect)

    pygame.display.flip()


def mostrar_pausa():
    pantalla.fill(NEGRO)
    mostrar_texto("Juego en pausa", 50, ANCHO // 2, ALTO // 2 - 40)
    mostrar_texto("Presiona P para continuar", 30, ANCHO // 2, ALTO // 2 + 40)
    mostrar_texto("Presiona M para volver al menú", 30, ANCHO // 2, ALTO // 2 + 80)
    pygame.display.flip()


# Bucle principal
while True:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_activo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones_menu)
                elif evento.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones_menu)
                elif evento.key == pygame.K_RETURN:
                    if opcion_seleccionada == 4:  # Opción "Salir"
                        pygame.quit()
                        sys.exit()
                    else:
                        reiniciar_juego()
                        modo_progresivo = False
                        if opcion_seleccionada == 0:
                            velocidad_base = 2
                        elif opcion_seleccionada == 1:
                            velocidad_base = 5
                        elif opcion_seleccionada == 2:
                            velocidad_base = 10
                        elif opcion_seleccionada == 3:
                            velocidad_base = 2
                            modo_progresivo = True
                        enemigos = [Enemigo(velocidad_base) for _ in range(8)]
                        menu_activo = False
                        juego_activo = True

            # Detectar clic del mouse
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
                mouse_pos = pygame.mouse.get_pos()
                for idx, rect in enumerate(rect_opciones):
                    if rect.collidepoint(mouse_pos):
                        if idx == 4:  # Opción "Salir"
                            pygame.quit()
                            sys.exit()
                        else:
                            reiniciar_juego()
                            modo_progresivo = False
                            if idx == 0:
                                velocidad_base = 2
                            elif idx == 1:
                                velocidad_base = 5
                            elif idx == 2:
                                velocidad_base = 10
                            elif idx == 3:
                                velocidad_base = 2
                                modo_progresivo = True
                            enemigos = [Enemigo(velocidad_base) for _ in range(8)]
                            menu_activo = False
                            juego_activo = True

        if juego_activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                proyectiles.append(Proyectil(nave.rect.centerx, nave.rect.top))
            if evento.key == pygame.K_p:
                pausado = not pausado
            if pausado and evento.key == pygame.K_m:
                # Volver al menú principal si el juego está pausado
                reiniciar_juego()
                menu_activo = True
                juego_activo = False

    teclas = pygame.key.get_pressed()

    if menu_activo:
        mostrar_menu()

    elif juego_activo:
        if pausado:
            mostrar_pausa()
            continue

        pantalla.fill(NEGRO)

        nave.mover(teclas)
        nave.dibujar()

        # Comprobar si ha pasado el intervalo para agregar nuevos enemigos
        if pygame.time.get_ticks() - ultimo_agregado > intervalo_agregar_enemigos:
            enemigos.append(Enemigo(velocidad_base))
            ultimo_agregado = pygame.time.get_ticks()

        for enemigo in enemigos[:]:
            if modo_progresivo:
                enemigo.velocidad = velocidad_base + score // 5
            enemigo.mover()
            enemigo.dibujar()
            if detectar_colision(nave.rect, enemigo.rect):
                nave.vidas -= 1
                enemigos = [Enemigo(velocidad_base) for _ in range(8)]
                if nave.vidas <= 0:
                    mostrar_texto("¡Has perdido!", 50, ANCHO // 2, ALTO // 2)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    reiniciar_juego()
                    menu_activo = True
                    juego_activo = False
                    break

        for proyectil in proyectiles[:]:
            proyectil.mover()
            proyectil.dibujar()
            if proyectil.rect.bottom < 0:
                proyectiles.remove(proyectil)
            else:
                for enemigo in enemigos:
                    if detectar_colision(proyectil.rect, enemigo.rect):
                        enemigos.remove(enemigo)
                        enemigos.append(Enemigo(velocidad_base))  # Reemplazar enemigo
                        if proyectil in proyectiles:
                            proyectiles.remove(proyectil)
                        score += 1
                        break

        mostrar_texto(f"Vidas: {nave.vidas}", 30, 70, 20)
        mostrar_texto(f"Puntuación: {score}", 30, ANCHO - 120, 20)
        pygame.display.flip()
