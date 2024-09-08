import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_POWER = -7
PIPE_SPEED = 5

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images
bird_image = pygame.image.load(r'E:\python\flappy bird\pics\bird.png')
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

background_image = pygame.image.load(r'E:\python\flappy bird\pics\background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pipe_top_image = pygame.image.load(r'E:\python\flappy bird\pics\downside.png')
pipe_bottom_image = pygame.image.load(r'E:\python\flappy bird\pics\upsode.png')

# Load sounds
flap_sound = pygame.mixer.Sound(r'E:\python\flappy bird\sounds\flap.mp3')
hit_sound = pygame.mixer.Sound(r'E:\python\flappy bird\sounds\hit.mp3')
score_sound = pygame.mixer.Sound(r'E:\python\flappy bird\sounds\score.wav')
background_music = pygame.mixer.music.load(r'E:\python\flappy bird\sounds\bgmusic.mp3')

# Set volume for sounds
flap_sound.set_volume(0.5)
hit_sound.set_volume(0.5)
score_sound.set_volume(0.5)

# Play background music with lower volume
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def flap(self):
        self.velocity = FLAP_POWER
        flap_sound.play()

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 400)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw top pipe
        top_image = pygame.transform.scale(pipe_top_image, (PIPE_WIDTH, self.height))
        screen.blit(top_image, (self.x, 0))
        
        # Draw bottom pipe
        bottom_image = pygame.transform.scale(pipe_bottom_image, (PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP)))
        screen.blit(bottom_image, (self.x, self.height + PIPE_GAP))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100), Pipe(SCREEN_WIDTH + 300)]
    score = 0
    game_over = False
    start = False

    def draw_start_screen():
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        font = pygame.font.SysFont(None, 72)
        draw_text('Flappy Bird', font, BLUE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        pygame.draw.rect(screen, GREEN, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50])
        font = pygame.font.SysFont(None, 48)
        draw_text('Start', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25)
        pygame.display.flip()

    def draw_game_over_screen():
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        font = pygame.font.SysFont(None, 72)
        draw_text('Game Over', font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        font = pygame.font.SysFont(None, 48)
        draw_text(f'Score: {score}', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, GREEN, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50])
        draw_text('Restart', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75)
        pygame.display.flip()

    while not start:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 50:
                    start = True

    while start:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        if not game_over:
            # Update bird
            bird.update()
            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                hit_sound.play()
                game_over = True

            # Update pipes
            for pipe in pipes:
                pipe.update()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    pipes.append(Pipe(SCREEN_WIDTH))
                    score += 1
                    score_sound.play()

            # Collision detection
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    hit_sound.play()
                    game_over = True

            # Draw bird
            bird.draw()

            # Draw pipes
            for pipe in pipes:
                pipe.draw()

            # Draw score
            font = pygame.font.SysFont(None, 48)
            draw_text(f'Score: {score}', font, BLACK, screen, 50, 30)
        else:
            draw_game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 + 50 <= mouse_y <= SCREEN_HEIGHT // 2 + 100:
                        game_over = False
                        bird = Bird()
                        pipes = [Pipe(SCREEN_WIDTH + 100), Pipe(SCREEN_WIDTH + 300)]
                        score = 0
                        start = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
