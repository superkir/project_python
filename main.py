import pygame
from random import randint

pygame.init()

FPS = 70
clock = pygame.time.Clock()
#створи вікно гри

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption("Game")

#завантаження музики
pygame.mixer.music.load("1.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

#задай фон сцени
background = pygame.image.load("3.png")
background = pygame.transform.scale(background, (wind_w, wind_h))

background1 = pygame.image.load("2.png")
background1 = pygame.transform.scale(background1, (wind_w, wind_h))
try:
    with open("record.txt", "r", encoding="Utf-8") as file:
        record = int(file.read())
except:
    record = 0
    print(record)

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, a, d):
        keys = pygame.key.get_pressed()
        if keys[a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[d]:
            if self.rect.right < wind_w:
                self.rect.x += self.speed

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        global lost_lb, lost
        self.rect.y += self.speed
        if self.rect.y >= wind_h:
            self.rect.x = randint(0, wind_w-self.rect.w)
            self.rect.y = randint(-250, -50)
            lost += 1
            lost_lb = font_stat.render(f"не торкнулося: {lost}", True, (255, 255, 255))
            
player = Player(0, 400, 50, 50, pygame.image.load("5.png"), 15)

enemy_img = pygame.image.load("7.png")
enemies = []

for i in range(20):
    enemies.append(Enemy(randint(0, wind_w-70), randint(-250, -50), 70, 50, enemy_img, 6))

font = pygame.font.SysFont("Arial", 80)
lose = font.render("You Lose!", True, (255, 0, 0))

points = 0
lost = 0
font = pygame.font.SysFont("Arial", 80)
font_stat = pygame.font.SysFont("Arial", 30)
points_lb = font_stat.render(f"торкнулося: {points}", True,(255, 255, 255))
lost_lb = font_stat.render(f"не торкнулося: {lost}", True, (255, 255, 255))

but_img = pygame.image.load("start.png")
button = Sprite(200, 200, 200, 50, but_img)
but_img1 = pygame.image.load("restart.png")
button1 = Sprite(200, 250, 200, 50, but_img1)
but_img2 = pygame.image.load("exit.png")
button2 = Sprite(200, 300, 200, 50, but_img2)


def new_record(record, score):
    if record < score:
        with open("record.txt", "w", encoding="Utf-8") as file:
            file.write(str(score))
        window.blit(font_stat.render(f"Новий рекорд {score}", True, (255, 255, 255)), (200, 0))

finish = False
game = True
menu = True

while game:
    if menu:
        window.blit(background1, (0, 0))
        button.draw()
        button1.draw()
        button2.draw()

    pygame.display.update()
    clock.tick(FPS)
    if not finish and not menu:
        window.blit(background, (0, 0))
        window.blit(points_lb, (0, 0))
        window.blit(lost_lb, (0, 50))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menu = True
        
        if lost == 10000000000000000:
            finish = True
            new_record(record, points)

        if points == 20:
            window.blit(lose, (215, 120))
            finish = True


        for enemy in enemies:
            enemy.draw()
            enemy.move()
            
            if enemy.rect.colliderect(player.rect):
                enemy.rect.x = randint(0, wind_w-enemy.rect.w)
                enemy.rect.y = randint(-250, -50)
                points += 1
                points_lb = font_stat.render(f"торкнулося: {points}", True,(255, 255, 255))
                    
        player.draw()
        player.move(pygame.K_a, pygame.K_d)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player = Player(0, 400, 50, 50, pygame.image.load("5.png"), 15)
            finish = False
            points = 0
            lost = 0
            enemies.clear()
            for i in range(20):
                enemies.append(Enemy(randint(0, wind_w-70), randint(-250, -50), 70, 50, enemy_img, 6))
            points_lb = font_stat.render(f"торкнулося: {points}", True,(255, 255, 255))
            lost_lb = font_stat.render(f"не торкнулося: {lost}", True, (255, 255, 255))
        
        if menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y, = event.pos 
            if button.rect.collidepoint(x, y):
                menu = False
            if button1.rect.collidepoint(x, y):
                player = Player(0, 400, 50, 50, pygame.image.load("5.png"), 15)
                menu = False
                game = True
                points = 0
                lost = 0
                enemies.clear()
                for i in range(20):
                    enemies.append(Enemy(randint(0, wind_w-70), randint(-250, -50), 70, 50, enemy_img, 6))
                points_lb = font_stat.render(f"торкнулося: {points}", True,(255, 255, 255))
                lost_lb = font_stat.render(f"не торкнулося: {lost}", True, (255, 255, 255))
            if button2.rect.collidepoint(x, y):
                game = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("6.mp3")
                pygame.mixer.music.play(-1)

    
    clock.tick(FPS)