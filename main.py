import pygame, random
from pygame.locals import *
from bird import *
from pipe import *

pygame.init()

clock = pygame.time.Clock()

screen_width = 764
screen_height = 736

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Icy Bird')

font = pygame.font.SysFont('malgungothic', 60)

ground_scroll = 0
scroll_speed = 13
flying = False
game_over = False
pipe_gap = 220
pipe_frequency = 1000 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
bg = pygame.image.load('assets/pics/bg.png')
ground_img = pygame.image.load('assets/pics/ground.png')
button_img = pygame.image.load('assets/pics/restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height // 2
    score = 0
    return score

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # check if mouse is on button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, screen_height // 2)

bird_group.add(flappy)

# make restart button
button = Button(screen_width//2 - 50, screen_height//2 - 100, button_img)

while True:
    clock.tick(75)
    #draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 768))

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        # decrease pipe gap (increase difficulty) every 10 points
        if pipe_gap > 180 and score % 10 == 0:           
            pipe_gap -= 10


    draw_text(str(score), font, (0, 128, 255), int(screen_width / 2), 20)

    # check for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False


    if not game_over and flying:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35: ground_scroll = 0

        pipe_group.update(scroll_speed)

    # check for game over and stop
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if not flying and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                flying = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == K_UP:
                    flying = True

    pygame.display.update()