import pygame
from pygame import *
import sys

# Inisialisasi
pygame.init()
font.init()

# Ukuran dan window
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")

# Warna
back = (200, 255, 255)
black = (0, 0, 0)
orange = (255, 150, 0)
red = (200, 0, 0)
green = (0, 180, 0)

# Path file gambar
mypath = 'C:/Program Files/Algoritmika/vscode/data/extensions/algoritmika.algopython-20251111.203400.0/temp/'
img_background = mypath + 'backroundskyblue.jpg'
img_racket = mypath + 'racket.png'
img_ball = mypath + 'tennisball.png'

background = transform.scale(image.load(img_background), (win_width, win_height))

# Sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# class Label()

# Objek 
racket1 = Player(img_racket, 30, 200, 10, 50, 150)
racket2 = Player(img_racket, 620, 200, 10, 50, 150)
ball = GameSprite(img_ball, 300, 200, 0, 50, 50)

# Font
# main_font = font.Font(None, 70)
main_font = font.SysFont('courier', 100) 
small_font = font.SysFont("courier", 36)

# Timer and score label
time_limit = 35  
score1 = 0  # scores for 1st player
score2 = 0  # scrores for 2nd player

# Tombol
def draw_button(text, rect, color, text_color=black):
    # import pygame
    # pygame.init()
    pygame.draw.rect(window, color, rect)
    txt = small_font.render(text, True, text_color)
    txt_rect = txt.get_rect(center=rect.center)
    window.blit(txt, txt_rect)

# Loop game
clock = time.Clock()
FPS = 60
game_state = 'start'  
start_ticks = 0

speed_x = 5
speed_y = 5

import random

while True:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            import pygame
            pygame.quit()
            sys.exit()
        if e.type == MOUSEBUTTONDOWN:
            mx, my = e.pos    
            if game_state == 'start':
                if start_btn.collidepoint(mx, my):
                    game_state = 'play'
                    start_ticks = pygame.time.get_ticks()
                    score1 = 0
                    score2 = 0
                    ball.rect.x, ball.rect.y = 300, 200
                    speed_x = random.choice([-5, 5])  
            elif game_state == 'gameover':
                if replay_btn.collidepoint(mx, my):
                    game_state = 'start'

    if game_state == 'start':
        title = main_font.render("PING PONG", True, orange)
        window.blit(title, (110, 30))
        start_btn = pygame.Rect(270, 400, 160, 50)
        draw_button("START", start_btn, green)

    elif game_state == 'play':
        racket1.update_left()
        racket2.update_right()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

       
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        
        if ball.rect.x < 0:
            score2 += 1
            ball.rect.x, ball.rect.y = 400, 200
            speed_x = -5   
            speed_y = -5

        if ball.rect.x > win_width:
            score1 += 1
            ball.rect.x, ball.rect.y = 200, 200
            speed_x = 5 
            speed_y = 5

        # Timer
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        # seconds = int(pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, time_limit - seconds)

        # time is over
        if remaining_time <= 0:
            game_state = 'gameover'

        # Gambar objek
        racket1.reset()
        racket2.reset()
        ball.reset()

        timer_text = small_font.render(f"Time: {remaining_time} s", True, black)
        timer_rect = timer_text.get_rect(center=(win_width // 2, 10 + timer_text.get_height() // 2))
        window.blit(timer_text, timer_rect)

        window.blit(small_font.render(f"P1: {score1}", True, black), (10, 50))
        window.blit(small_font.render(f"P2: {score2}", True, black), (575, 50))

    elif game_state == 'gameover':
        result_text = main_font.render("GAME OVER", True, red)
        window.blit(result_text, (230, 150))
        winner = "DRAW🤣"
        if score1 > score2:
            winner = "PLAYER 1 WINS!😁"
        elif score2 > score1:
            winner = "PLAYER 2 WINS!😉"

        win_text = small_font.render(winner, True, black)
        window.blit(win_text, (250, 220))
        replay_btn = pygame.Rect(270, 300, 160, 50)
        draw_button("REPLAY", replay_btn, orange)

    display.update()
    clock.tick(FPS)