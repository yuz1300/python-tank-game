import pygame
import sys
import random

padWidth = 480
padHeight = 640

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, background, tank, missile, enemyTank, font
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("Tank shooter")
    
    background = pygame.image.load(r"background.jpg")
    
    tank = pygame.image.load(r"tankmain.png")
    tank = pygame.transform.scale(tank, (80, 80))
    
    missile = pygame.image.load(r"tankmissile.png")
    missile = pygame.transform.scale(missile, (50, 50))
    
    enemyTank = pygame.image.load(r"tankenemy.png")
    enemyTank = pygame.transform.scale(enemyTank, (80, 80))
    enemyTank = pygame.transform.flip(enemyTank, False, True)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 25)

def runGame():
    global gamePad, clock, background, tank, missile, enemyTank, font

    tankWidth, tankHeight = tank.get_rect().size
    missileWidth, missileHeight = missile.get_rect().size
    enemyWidth, enemyHeight = enemyTank.get_rect().size

    x = padWidth * 0.43
    y = padHeight * 0.85
    tank_x = 0
    missileXY = []
    enemies = []
    enemy_spawn_delay = 96
    enemy_speed = 3
    frame_count = 0
    canShoot = True
    lives = 3
    score = 0
    combo = 0
    running = True


    level = 1
    kills = 0
    kills_per_level = 10
    level_display_duration = 2000
    level_start_time = pygame.time.get_ticks()
    show_level_text = True
    win = False


    extra_life_awarded = False

    while running:
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_x = -7
                elif event.key == pygame.K_RIGHT:
                    tank_x = 7
                elif event.key == pygame.K_SPACE and canShoot:
                    missile_x = x + (tankWidth / 2) - (missileWidth / 2)
                    missile_y = y - missileHeight
                    missileXY.append([missile_x, missile_y])
                    canShoot = False
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and tank_x < 0:
                    tank_x = 0
                elif event.key == pygame.K_RIGHT and tank_x > 0:
                    tank_x = 0

        x += tank_x
        if x < 0:
            x = 0
        elif x > padWidth - tankWidth:
            x = padWidth - tankWidth

        if frame_count % enemy_spawn_delay == 0:
            enemy_x = random.randint(0, padWidth - enemyWidth)
            enemy_y = -enemyHeight
            enemies.append([enemy_x, enemy_y])

        for e in enemies[:]:
            e[1] += enemy_speed
            if e[1] > padHeight:
                enemies.remove(e)
                lives -= 1
                combo = 0
                enemy_speed -= 1
                if enemy_speed < 2:
                    enemy_speed = 2
                if lives <= 0:
                    running = False

        for m in missileXY[:]:
            m[1] -= 10
            for e in enemies[:]:
                if (m[0] + missileWidth > e[0] and m[0] < e[0] + enemyWidth and
                    m[1] + missileHeight > e[1] and m[1] < e[1] + enemyHeight):

                    hitPos = (m[0] + missileWidth/2) - e[0]
                    third = enemyWidth / 3

                    if third <= hitPos <= 2*third:
                        enemy_speed += 3
                    elif 0.33*enemyWidth <= hitPos <= 0.66*enemyWidth:
                        enemy_speed += 2
                    else:
                        enemy_speed += 1

                    if enemy_speed > 8:
                        enemy_speed = 8

                    missileXY.remove(m)
                    enemies.remove(e)
                    score += 5
                    combo += 1
                    kills += 1


                    if kills >= kills_per_level:
                        level += 1
                        kills = 0
                        show_level_text = True
                        level_start_time = pygame.time.get_ticks()

                        if level >= 5:
                            win = True
                            running = False

                    if combo == 3:
                        score += 30
                        combo = 0

                        if not extra_life_awarded:
                            lives += 1
                            extra_life_awarded = True
                    canShoot = True
                    break
            else:
                if m[1] < 0:
                    missileXY.remove(m)
                    canShoot = True

        drawObject(background, 0, 0)
        drawObject(tank, x, y)

        for bx, by in missileXY:
            drawObject(missile, bx, by)

        for ex, ey in enemies:
            drawObject(enemyTank, ex, ey)

        score_text = font.render(f"Score: {score}", True, (255,255,255))
        lives_text = font.render(f"Lives: {lives}", True, (255,255,255))
        combo_text = font.render(f"Combo: {combo}", True, (255,255,0))
        gamePad.blit(score_text, (padWidth - 120, 10))
        gamePad.blit(lives_text, (padWidth - 120, 40))
        gamePad.blit(combo_text, (padWidth - 120, 70))

        if show_level_text:
            now = pygame.time.get_ticks()
            if now - level_start_time <= level_display_duration:
                large_font = pygame.font.SysFont("Arial", 40)
                level_text = large_font.render(f"Level {level} - Start", True, (255,255,255))
                gamePad.blit(level_text, (padWidth/2 - level_text.get_width()/2, padHeight/2 - level_text.get_height()/2))
            else:
                show_level_text = False

        pygame.display.update()
        clock.tick(60)

    gamePad.fill((0,0,0))
    if win:
        over_text = font.render(f"YOU WIN!", True, (0,255,0))
    else:
        over_text = font.render(f"GAME OVER", True, (255,0,0))
    final_score = font.render(f"Final Score: {score}", True, (255,255,255))
    gamePad.blit(over_text, (padWidth/2 - over_text.get_width()/2, padHeight/2 - 30))
    gamePad.blit(final_score, (padWidth/2 - final_score.get_width()/2, padHeight/2 + 10))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

initGame()
runGame()

