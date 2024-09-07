import pygame
import random
import sys  
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 1000
screen = pygame.display.set_mode((ANCHO, ALTO)) #tamaño de la pantalla
pygame.display.set_caption("JUEGO") #titulo del juego

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Cargar imágenes
carpeta_juego = os.path.dirname(__file__)
imagenes = os.path.join(carpeta_juego, "img")

fondo_juego = pygame.image.load(os.path.join(imagenes, "fondo_verde.png")).convert()
fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO, ALTO))
nave = pygame.image.load(os.path.join(imagenes, "nave.png")).convert_alpha()
enemigo = pygame.image.load(os.path.join(imagenes, "enemigo.png")).convert_alpha()


# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(nave, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.speed = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemigo, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 1

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)


# Bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

  

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

# Función para mostrar texto
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLANCO)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Función para inicializar/reiniciar el juego
def init_game():
    global all_sprites, enemies, bullets, player, score
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
    score = 0

# Función del menú principal
def show_menu():
    screen.fill(NEGRO)
    draw_text(screen, "Enemigos Espaciales", 64, ANCHO // 2, ALTO // 4)
    draw_text(screen, "Flechas para moverse, \nEspacio para disparar", 30, ANCHO // 2, ALTO // 2)
    draw_text(screen, "Presiona una tecla para comenzar", 22, ANCHO // 2, ALTO * 3 // 4)
    draw_text(screen, "Presiona P para pausar el juego", 30, ANCHO // 2,550)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
#funcion para pausar el juego
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        
        screen.fill(NEGRO)
        draw_text(screen, "PAUSA", 64, ANCHO // 2, ALTO // 2)
        draw_text(screen, "Presiona P para continuar", 22, ANCHO // 2, ALTO // 2 + 50)
        pygame.display.flip()

# Modificar la función game_loop para dibujar el fondo
def game_loop():
    global score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key== pygame.K_p:
                    pause_game()

        all_sprites.update()

        # Colisiones entre balas y enemigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)

        # Colisiones entre jugador y enemigos
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            running = False

        # Dibujar el fondo
        screen.blit(fondo_juego, (0, 0))
        
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, ANCHO // 2, 10)
        pygame.display.flip()

    return score

def main():
    while True:
        show_menu()
        init_game()
        final_score = game_loop()
        if final_score is None:
            break
        screen.fill(NEGRO)
        draw_text(screen, "FIN", 64, ANCHO // 2, ALTO // 4)
        draw_text(screen, f"Puntuación final: {final_score}", 22, ANCHO // 2, ALTO // 2)
        draw_text(screen, "Presiona una tecla para jugar de nuevo", 18, ANCHO // 2, ALTO * 3 // 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

if __name__ == "__main__":
    main()