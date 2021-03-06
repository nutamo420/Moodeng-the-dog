import pygame
from pygame import image
from pygame.locals import *
from random import randint, choice
from pygame.sprite import spritecollide

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player1 = pygame.image.load("cm1.png").convert_alpha()
        player2 = pygame.image.load("cm2.png").convert_alpha()
        player11 = pygame.transform.scale(player1, (100, 120))
        player22 = pygame.transform.scale(player2, (100, 120))
        self.player_walk = [player11, player22]
        self.player_index = 0
        playerj = pygame.image.load("cmj.png").convert_alpha()
        self.playerjj = pygame.transform.scale(playerj, (100, 120))

        fire = pygame.image.load("cmf.png").convert_alpha()
        self.fire1 = pygame.transform.scale(fire, (120, 140))

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(bottomleft=(posX, posY))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio_jump.mp3')
        self.jump_sound.set_volume(3)
    
    def restart(self):
        if score == 0:
            self.rect.bottomleft = (posX, posY)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= posY:
            self.gravity = -30
            self.jump_sound.play()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= 15
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.right += 15

    def apply_gravity(self):
            self.gravity += 2.5
            self.rect.bottom += self.gravity
            if self.rect.bottom >= posY:
                self.rect.bottom = posY

    def animation(self):
        global supermoodeng
        if supermoodeng == True:
            self.image = self.fire1
        else:
            if self.rect.bottom < posY:
                self.image = self.playerjj
            else:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk):
                    self.player_index = 0
                self.image = self.player_walk[int(player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
        self.restart()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, thing):
        super().__init__()

        if thing == 'bone':
            bone1 = pygame.image.load("bone1.PNG").convert_alpha()
            bone2 = pygame.image.load("bone2.PNG").convert_alpha()
            bone11 = pygame.transform.scale(bone1, (70, 85))
            bone22 = pygame.transform.scale(bone2, (70, 85))
            self.frame = [bone11, bone22]
        else:
            ghost1 = pygame.image.load("pp1.PNG").convert_alpha()
            ghost2 = pygame.image.load("pp2.PNG").convert_alpha()
            ghost11 = pygame.transform.scale(ghost1, (75, 90))
            ghost22 = pygame.transform.scale(ghost2, (75, 90))
            self.frame = [ghost11, ghost22]

        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), 490))

        self.hit_sound = pygame.mixer.Sound('small hit (2).wav')
        self.hit_sound.set_volume(10)
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= move
        self.destroy()
    def destroy(self):
        global life
        if self.rect.x <= -100:
            self.kill()
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) and supermoodeng == False:
            self.kill()
            life -=1
            self.hit_sound.play()


class heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly1 = pygame.image.load("h1.PNG").convert_alpha()
        fly2 = pygame.image.load("h2.PNG").convert_alpha()
        fly11 = pygame.transform.scale(fly1, (45, 45))
        fly22 = pygame.transform.scale(fly2, (45, 45))
        self.frame = [fly11, fly22]
        posY = 430
        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), 360))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= move
        self.destroy()
    def destroy(self):
        global hearto, supermoodeng
        if pygame.sprite.spritecollide(player.sprite, heart_group, False) and supermoodeng== False:
            hearto += 1
            self.kill()
        if self.rect.x <= -100:
            self.kill()

def display_score():
    global move, supermoodeng
    score_count = (pygame.time.get_ticks() //1000) - start_time
    score_sur = text_fontsmol.render(f'score : {score_count}', False, "Black")
    score_rec = score_sur.get_rect(topright = (780, 30) )
    screen.blit(score_sur, score_rec)
    return score_count

def display_heart():
    global hearto, supermoodeng
    heartshow = int(hearto // 1)
    heart_sur = text_fontsmol.render(f'= {heartshow}', False, "Black")
    heart_rec = heart_sur.get_rect(topright = (450, 30))
    if heartshow == 2: supermoodeng = True
    if supermoodeng: hearto -= 0.003
    if heartshow == 0: supermoodeng = False
    screen.blit(heart_sur, heart_rec)

def display_life():
    life_text = text_fontsmol.render(f'Life = {life}', False, "Black")
    life_rec = life_text.get_rect(topleft = (50, 30))
    screen.blit(life_text, life_rec)

def player_animation():
    global player_surf, player_index
    if supermoodeng == True:
        player_surf = fire1
    else:
        if player_rec.bottom < posY:
            player_surf = playerjj
        else:
            player_index += 0.1
            if player_index >= len(player_move):
                player_index = 0
            player_surf = player_move[int(player_index)]

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Moodeng the dog! - Christmas")
icon = pygame.image.load("pop.png").convert_alpha()
pygame.display.set_icon(icon)

game_active = False

bg = pygame.image.load("snow.jpg").convert_alpha()
bg1 = pygame.transform.scale(bg, (1600, 600))

posX = 80
posY = 490

life = 3

player = pygame.sprite.GroupSingle()
player.add(Player())
player1 = pygame.image.load("cm1.png").convert_alpha()
player2 = pygame.image.load("cm2.png").convert_alpha()
player11 = pygame.transform.scale(player1, (100, 120))
player22 = pygame.transform.scale(player2, (100, 120))
player_move = [player11, player22]
player_index = 0
playerj = pygame.image.load("cmj.png").convert_alpha()
playerjj = pygame.transform.scale(playerj, (100, 120))
player_surf = player_move[player_index]
player_rec = player_surf.get_rect(bottomleft=(posX, posY))

fire = pygame.image.load("cmf.png").convert_alpha()
fire1 = pygame.transform.scale(fire, (120, 140))

obstacle_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

move = 7
scroll = 0 #scroll bg
speed = 0

text_font = pygame.font.Font("byteoff.otf", 40)

luv = pygame.image.load("h1.PNG").convert_alpha()
luv1 = pygame.transform.scale(luv, (45, 45))
luv_rect = luv1.get_rect(topright = (380, 27))
hearto = 0
supermoodeng = False

start_time = 0
score = 0
bg_music = pygame.mixer.Sound('cm somg.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

text_font = pygame.font.Font("byteoff.otf", 50)
text_fontsmol = pygame.font.Font("byteoff.otf", 40)
text_fontsmol2 = pygame.font.Font("byteoff.otf", 38) 
game_name = text_font.render("Moodeng The Dog", False, "white")
game_name_rec = game_name.get_rect(center = (400, 90))
text_start1 = text_fontsmol.render("Hold Tab to see How to Play", False, "white")
text_start2 = text_fontsmol.render("or Press Space to start!", False, "white")
text_start_rec1 = text_start1.get_rect(center=(400, 470))
text_start_rec2 = text_start2.get_rect(center=(400, 540))

bg_gameover = pygame.image.load("cm open.jpg").convert_alpha()
bg_gameover1 = pygame.transform.scale(bg_gameover, (800, 600))
text_gameover = text_font.render("GAME OVER", False, "white")
text_gameover_rec = text_gameover.get_rect(center=(400, 60))
text_score = text_font.render(f'Score: {score}', False, "white")
text_score_rec = text_score.get_rect(center=(400, 120))
text_restart = text_font.render("Press Space to restart!", False, "white")
text_restart_rec = text_restart.get_rect(center=(400, 520))

player_go = pygame.image.load("cmj.png").convert_alpha()
player_go1 = pygame.transform.scale(player_go, (250, 300))
player_go_rec = player_go1.get_rect(center=(400, 320))
player_start_rec = player_go1.get_rect(center=(400, 280))

text_howto = text_font.render('How to play!', False, "white")
text_howto_rec = text_howto.get_rect(center=(400, 90))
text_howto1 = text_fontsmol2.render('Use arrow keys to control Moodeng', False, "white")
text_howto_rec1 = text_howto1.get_rect(center=(400, 200))
text_howto2 = text_fontsmol2.render('and keep away from the ghosts', False, "white")
text_howto_rec2 = text_howto2.get_rect(center=(400, 250))
text_howto22 = text_fontsmol2.render('and skeletons!', False, "white")
text_howto_rec22 = text_howto22.get_rect(center=(400, 300))
text_howto3 = text_fontsmol2.render('Also collect 2 hearts to active', False, "white")
text_howto_rec3 = text_howto3.get_rect(center=(400, 430))
text_howto4 = text_fontsmol2.render('Super Moodeng Mode!', False, "white")
text_howto_rec4 = text_howto4.get_rect(center=(400, 480))

obstacle_timer = pygame.USEREVENT + 5
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    if supermoodeng == False:
        pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if game_active:
            if event.type == obstacle_timer:
                thing = choice(['fly', 'fly', 'bone', 'ghost','bone', 'ghost'])
                if thing == 'fly':
                    heart_group.add(heart())
                else:
                    obstacle_group.add(Obstacle(thing))

    if game_active:
        screen.fill((0,0,0))
        screen.blit(bg1, (scroll, 0))

        rel_x = scroll % bg1.get_rect().width
        screen.blit(bg1, (rel_x - bg1.get_rect().width, 0))
        if rel_x < 800:
            screen.blit(bg1, (rel_x, 0))

        if supermoodeng == False and score < 100:
            move += 0.01
            speed += 0.01
        
        if life <= 0:
            obstacle_group.empty()
            game_active =  False

        score = display_score()
        display_heart()
        display_life()
        screen.blit(luv1, luv_rect)

        scroll -= speed+1
        player_animation()
        player.draw(screen)
        player.update()
        # if supermoodeng == False:
        obstacle_group.draw(screen)
        obstacle_group.update()
        heart_group.draw(screen)
        heart_group.update()

    else:
        screen.blit(bg_gameover1, (0, 0))
        text_score = text_font.render(f'Score: {score}', False, "white")
        text_score_rec = text_score.get_rect(center=(400, 120))
        keys = pygame.key.get_pressed()
        
        if score == 0:
            screen.blit(player_go1, player_start_rec)
            screen.blit(game_name, game_name_rec)
            screen.blit(text_start1, text_start_rec1)
            screen.blit(text_start2, text_start_rec2)
        else:
            screen.blit(player_go1, player_go_rec)
            screen.blit(text_score, text_score_rec)
            screen.blit(text_gameover, text_gameover_rec)
            screen.blit(text_restart, text_restart_rec)

        if keys[pygame.K_TAB]:
            screen.blit(bg_gameover1, (0, 0))
            screen.blit(text_howto, text_howto_rec)
            screen.blit(text_howto1, text_howto_rec1)
            screen.blit(text_howto2, text_howto_rec2)
            screen.blit(text_howto22, text_howto_rec22)
            screen.blit(text_howto3, text_howto_rec3)
            screen.blit(text_howto4, text_howto_rec4)
            
        if keys[pygame.K_SPACE]:
            game_active = True
            move = 7
            scroll = 0
            speed = 0
            hearto = 0
            life = 3
            start_time = int(pygame.time.get_ticks()//1000)

    pygame.display.update()