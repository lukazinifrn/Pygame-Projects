import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_frame1 = pygame.image.load("graphics/Player/player_walk_1.png")
        player_frame2 = pygame.image.load("graphics/Player/player_walk_2.png")
        self.frames = [player_frame1, player_frame2]
        self.index = 0
        self.image = self.frames[self.index]
        self.ypos = 300
        self.rect = self.image.get_rect(midbottom = (100, self.ypos))
        self.gravity = 0
        self.speed = 5
        self.jump = 0

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.jump == 0:
            self.gravity -= 20
            self.jump = 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

    def apply_gravity(self):
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= self.ypos:
                self.rect.bottom = self.ypos
                self.jump = 0
                self.gravity = 0

    def out_window(self):
        if self.rect.left > w_width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = w_width
    
    def animation(self):
        if self.rect.bottom < self.ypos:
            self.image = pygame.image.load("graphics/Player/jump.png")

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.index += 0.2
                self.image = self.frames[int(self.index%2)]
            else:
                self.index = 0
                self.image = self.frames[self.index]
    def update(self):
        if game_Running:
            self.player_move()
            self.apply_gravity()
            self.out_window()
            self.animation()
        else:
            self.rect.midbottom = (100, self.ypos)
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obs):
        super().__init__()
        if obs == "snail":
            self.speed = snail_speed
            self.frames = [pygame.image.load("graphics/snail/snail1.png"), pygame.image.load("graphics/snail/snail2.png")]
            self.ypos = 300
        
        if obs == "fly":
            self.speed = fly_speed
            self.frames = [pygame.image.load("graphics/Fly/Fly1.png"), pygame.image.load("graphics/Fly/Fly2.png")]
            self.ypos = 150

        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.ypos))

    def animation(self):
        self.index += 0.066
        self.image = self.frames[int(self.index%2)]

    def out_window(self):
        if self.rect.x <= -50:
            self.kill()
 
    def update(self):
        self.animation()
        self.out_window()
        self.rect.x -= self.speed

def display_score():
    score_surf = font.render(f"Score: {score}", False, "black")
    score_rect = score_surf.get_rect(center = (w_width/2, 50))
    screen.blit(score_surf, score_rect)

def collision():
    if pygame.sprite.spritecollide(player.sprite, obs, False):
        obs.empty()
        return False
    else:
        return True
    
def show_score():
    score_text = font.render(f"Score: {score}", False, (13, 61, 71))
    score_text_rect = score_text.get_rect(center = (w_width/2, w_height - 90))
    high_text = font.render(f"Highscore: {high_score}", False, (13, 61, 71))
    high_text_rect = high_text.get_rect(center = (w_width/2, w_height - 45))
    screen.blit(score_text, score_text_rect)
    screen.blit(high_text, high_text_rect)

pygame.init()
w_width = 800
w_height = 400
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Pixel Runner")
font = pygame.font.Font("font/Pixeltype.ttf", 50)
clock = pygame.time.Clock()

# player group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obs group
obs = pygame.sprite.Group()

## Player Stand
player_stand = pygame.image.load("graphics/Player/player_stand.png")
player_stand = pygame.transform.scale_by(player_stand, 2)
player_stand_rect = player_stand.get_rect(center = (w_width/2, w_height/2))

## Texts
game_title = font.render("Pixel Runner", False, (13, 61, 71))
game_title_rect = game_title.get_rect(center = (w_width/2, 50))

click_title = font.render("CLICK TO START", False, (13, 61, 71))
click_title_rect = click_title.get_rect(center = (w_width/2, w_height - 90))

## Ground
ground_ypos = 300
ground = pygame.image.load("graphics/ground.png")
ground_rect = ground.get_rect(topleft = (0, ground_ypos))

## Sky
sky = pygame.image.load("graphics/Sky.png")
sky_rect = sky.get_rect(topleft = (0, 0))

# Score
score_event = pygame.USEREVENT + 1
pygame.time.set_timer(score_event, 1000)
high_score = 0
score_multi = 1
score = 0
sec = 0

# Obstacle Timer
OBSTACLE_TIMER = pygame.USEREVENT + 2
obs_time = 1500
pygame.time.set_timer(OBSTACLE_TIMER, obs_time)

# Dif event
DIF_TIMER = pygame.USEREVENT + 3
pygame.time.set_timer(DIF_TIMER, 5000)

# Operational Variables
game_Running = False
snail_speed = 5
fly_speed = 7

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_Running:
            if event.type == score_event:
                score += score_multi
                sec += 1
                five_multi = score_multi*5
                if int(sec/score_multi)*score_multi >= five_multi:
                    score_multi += 1
                
                if high_score < score:
                    high_score = score

            if event.type == OBSTACLE_TIMER:
                obstacle_obs = choice(["snail", "fly"])
                obs.add(Obstacle(obstacle_obs))
            
            if event.type == DIF_TIMER:
                pygame.time.set_timer(OBSTACLE_TIMER, obs_time)
                if obs_time > 700:
                   obs_time -= 10
                snail_speed += 0.3
                fly_speed += 0.4

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                score_multi = 1
                score = 0
                sec = 0
                game_Running = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_Running = True
                score_multi = 1
                score = 0
                sec = 0
                

    if game_Running:
        screen.blit(sky, sky_rect)
        screen.blit(ground, ground_rect)
        player.draw(screen)
        player.update()
        obs.draw(screen)
        obs.update()
        display_score()

        game_Running = collision()
    else:
        screen.fill((44, 137, 158))
        pygame.time.set_timer(score_event, 1000)
        obs_time = 1500
        pygame.time.set_timer(OBSTACLE_TIMER, obs_time)
        pygame.time.set_timer(DIF_TIMER, 5000)
        player.update()
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_title, game_title_rect)
        if score == 0:
            screen.blit(click_title, click_title_rect)
        else:
            show_score()
        snail_speed = 5
        fly_speed = 7
    
    pygame.display.update()
    clock.tick(60)