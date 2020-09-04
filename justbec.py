import pygame, random, math, sys
from pygame import mixer
pygame.init()
pygame.display.set_caption("Flapyopussylikethis")
screen = pygame.display.set_mode((800, 600))

PlayerImg = pygame.image.load('yo.png')
PlayerX = 370
PlayerY = 480
Playerxchange = 0

background = pygame.image.load('background.png').convert()

EnemyImg = []
EnemyX = []
EnemyY = []
Enemyxchange = []
Enemyychange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('alien.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    Enemyxchange.append(0.4)
    Enemyychange.append(40)

BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
Bulletxchange = 0
Bulletychange = 1
Bullet_state = "ready"

score_value = 0

font = pygame.font.Font('freesansbold.ttf', 32)
game_over = pygame.font.Font('freesansbold.ttf', 64)


textX = 10
textY = 10

mixer.music.load('background.wav')
mixer.music.play(-1)


def show_score(x,y):
    score = font.render("Score:" + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

def show_game_over():
    screen.blit(game_over.render("GAME OVER", True, (255,255,255)), (200, 250))

def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def is_collision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + math.pow(EnemyY - BulletY, 2))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                Playerxchange -= 0.4
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                Playerxchange += 0.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Playerxchange = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    yo = pygame.mixer.Sound('laser.wav')
                    yo.play()
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)


    if PlayerX >= 736:
        PlayerX = 736
    if PlayerX <= 0:
        PlayerX = 0
    if PlayerY <= 50:
        PlayerY = 50
    if PlayerY >= 550:
        PlayerY = 550
    for i in range(num_of_enemies):
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            show_game_over()
            break
        EnemyX[i] += Enemyxchange[i]
        if EnemyX[i] >= 736:
            Enemyxchange[i] = -0.2
            EnemyY[i] += Enemyychange[i]
        if EnemyX[i] <= 0:
            Enemyxchange[i] = 0.2
            EnemyY[i] += Enemyychange[i]
        collision = is_collision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            lol = pygame.mixer.Sound('sound/nut.wav')
            lol.play()
            BulletY = 480
            Bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)
        enemy(EnemyX[i], EnemyY[i], i)


    if Bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= Bulletychange

    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"




    show_score(textX,textY)
    PlayerX += Playerxchange
    player(PlayerX, PlayerY)

    pygame.display.update()
