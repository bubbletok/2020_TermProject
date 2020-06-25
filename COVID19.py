import pygame as pg
import random

WHITE =(255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
green = (0,200,0)
bright_green = (0,255,0)

pad_width = 1024
pad_height = 512
player_width = 48
player_height = 48
background_width = 1024
grid_width = 48
grid_height = 48
block_width = 48
block_height = 48
chances = 3
day = 1
age = 10
over = False
simul = False
begin = False
age_selected = False
infected = False
infection = 0
boring = 10
hungry = 10

def print_text(string, x, y, color):
    font=pg.font.SysFont("NanumSquareRoundR", 32)
    text = font.render(string, True, color)
    text_rect = text.get_rect( )
    text_rect.centerx = x
    text_rect.y = y
    gamepad.blit(text, text_rect)

def drawObject(obj,x,y):
    global gamepad
    gamepad.blit(obj,(x,y))


def retryGame():
    global gamepad, chances
    print_text("Your infection has increased",pad_width/2,180,RED)
    print_text("You have " + str(chances) + " chances",pad_width/2,250,BLUE)
    pg.display.update()
    pg.time.wait(1400)
    runGame()
    
def runGame(): # Start side-view Game
    global stage_progress, map_level, blocks, blcoks2, chances, day, player_height, infection
    global begin, over, infected
    
    x = pad_width * 0.05
    y = pad_height * 0.8
    
    background1_x = 0
    background2_x = background_width
    
    block_get_pos = False
    
    x_change = 0
    y_change = 0
    cur_x = x
    cur_y = y
    gravity = 7
    
    remaining_object = 10
    
    grid_xy = []
    
    block_x = 48
    block_y = 0    
    block2_x = pad_width
    block2_y = pad_height * 0.8
    random.shuffle(blocks)
    random.shuffle(blocks2)
    block = blocks[0]
    block2 = blocks2[0]
    
    if map_level == 1:
        remaining_object = 10
    elif map_level == 2:
        reamining_object = 15
    elif map_level == 3 or map_level == 4:
        remaining_object = 20
    elif map_level == 5:
        remaining_object = 25
    
    crashed = False
    jumping = False
    clear = False

    while not crashed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True
                over = True
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_UP or event.key == pg.K_SPACE) and y_change == 0:
                    cur_y = y
                    jumping = True
                elif event.key == pg.K_RIGHT:
                    x_change = 7
                elif event.key == pg.K_LEFT:
                    x_change = -7
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    x_change = 0
        
        if jumping:
            y_change = -9
            if cur_y - y >100:
                jumping = False
        else:
            y_change = gravity
            if y>pad_height-player_height-grid_height:
                y = pad_height-player_height-grid_height+1
                y_change = 0
            
        y += y_change
        x += x_change

        if x <= 0:
            x = 0;
        if x+player_width >= pad_width:
            x = pad_width - player_width
        
        if block == None:
            block_y += 10
        else:
            if map_level == 1:
                block_y += 6
            elif map_level == 2 or map_level == 3:
                block_y += 8
            elif map_level == 4:
                block_y += 12
            elif map_level == 5:
                block_y += 14
        
        if block2 == None:
            block2_x -= 30
        else:
            if map_level == 1:
                block2_x -= 5
            elif map_level == 2 or map_level == 3:
                block2_x -= 7
            elif map_level == 4:
                block2_x -= 11 
            elif map_level == 5:
                block2_x -= 13
            
        if block_y >= pad_height:
            if block != None:
                remaining_object -= 1
            block_y = 0
            random.shuffle(blocks)
            block = blocks[0]
            block_get_pos = False
        
        if block2_x <= 0:
            if block2 != None:
                remaining_object -= 1
            block2_x = pad_width
            random.shuffle(blocks2)
            block2 = blocks2[0]
           
        background1_x -= 2
        background2_x -= 2
        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width
        
        gamepad.fill(WHITE)
        
        drawObject(background1,background1_x,0)
        drawObject(background2,background2_x,0)
        
        drawObject(player,x,y) 
        
        if not block_get_pos:
            block_x = 48 +(48*random.randint(0,10))
            block_get_pos = True
        if block != None:
            drawObject(block, block_x, block_y)
        if block2 != None:
            drawObject(block2 ,block2_x, block2_y)
        
        for i in range((int)(pad_width/grid_width)+1):
                drawObject(grid,grid_width*i,pad_height-grid_height)
            
        if block != None:
            if (block_x+block_width >= x >= block_x) or (block_x+block_width >= x+player_width >= block_x):
                if (block_y+block_height >= y >= block_y) or(block_y+block_height >= y+player_height >= block_y):
                    chances -= 1
                    if age == 10:
                        infection += 5
                    else:
                        infection += 15
                    if(chances > 0):
                        retryGame()
                        return 0
                    else:
                        crashed = True
        if block2 != None:
            if (block2_x+block_width >= x >= block2_x) or (block2_x+block_width >= x+player_width >= block2_x):
                if (block2_y+block_height >= y >= block2_y) or(block2_y+block_height >= y+player_height >= block2_y):
                    chances -= 1
                    if age == 10:
                        infection += 5
                    else:
                        infection += 15
                    if(chances > 0):
                        retryGame()
                        return 0
                    else:
                        crashed = True
        
        print_text("Remaining Object",pad_width/2,0,BLACK)
        print_text(str(remaining_object),pad_width/2,30,RED)
        
        if remaining_object <= 0:
            remaining_object = 0
            crashed = True
            clear = True
        
        pg.display.set_caption("pygame_level_" + (str)(map_level))
        pg.display.update()
        clock.tick(60)
        
    if clear == True:
        if map_level == 5:
            infected = False
            infection = 0
        day += 1
        gamepad.fill(WHITE)
        print_text("You safely arrived!",pad_width/2,256,BLUE)
        pg.display.update()
        pg.time.wait(1500)
        if map_level == 5:
            gamepad.fill(WHITE)
            print_text("You've been cured!",pad_width/2,256,BLUE)
            pg.display.update()
            pg.time.wait(1500)

        pg.display.update()
        runGame_simul()
    elif chances < 1:
        if map_level == 5:
            gamepad.fill(WHITE)
            print_text("You died by COVID-19",pad_width/2,250, RED)
            pg.display.update()
            over = True
            infected = False
            pg.time.wait(1500)
        else:
            print_text("You are infected",pad_width/2,250, RED)
            pg.display.update()
            pg.time.wait(1500)
            infected = True
        runGame_simul()
    
    return 0

def initGame(): #Set side-view Game
    global gamepad, clock, player, sliding, grid, background1, background2, blocks, blocks2
    
    blocks = []
    blocks2 = []
    
    gamepad = pg.display.set_mode((pad_width,pad_height))
    pg.display.set_caption("pygame_level_" + (str)(map_level))
    
    player = pg.image.load("images/player.png")
    grid = pg.image.load("images/grid.png")
    background1 = pg.image.load("images/background.png")
    background2 = background1.copy()
    blocks.append(pg.image.load("images/block.png"))
    blocks2.append(pg.image.load("images/block2.png"))
    blocks2.append(pg.image.load("images/block3.png"))
    
    for i in range(3):
        blocks2.append(None)
    
    clock = pg.time.Clock()
    runGame()
    
    return 0


def startGame():
    pg.init()
    initGame_simul()

def endGame():
    pg.quit()
    
def drawStatus():
    print_text("Day :" + str(day),pad_width/2,0,BLACK)
    print_text("Infection",850,5,BLACK)
    pg.draw.rect(gamepad,WHITE,(900,5,100,25))
    pg.draw.rect(gamepad,BLACK,(900,5,infection,25))
    print_text("Boring",850,40,BLACK)
    pg.draw.rect(gamepad,WHITE,(900,40,100,25))
    pg.draw.rect(gamepad,BLACK,(900,40,boring,25))
    print_text("Hungry",850,75,BLACK)
    pg.draw.rect(gamepad,WHITE,(900,75,100,25))
    pg.draw.rect(gamepad,BLACK,(900,75,hungry,25))
    
def button(msg,ic,ac,x,y,w,h,number,action = None,): #draw button
    global getSelected, moveSelected, restSelected, cookSelected
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(gamepad,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
            if number == 0:
                getSelected = True
            elif number == 1:
                moveSelected = True
            elif number == 2:
                restSelected = True
            elif number == 3:
                cookSelected = True
            return 0
    else:
        pg.draw.rect(gamepad,ic,(x,y,w,h))

    font=pg.font.SysFont("NanumSquareRoundR", 24)
    text = font.render(msg, True, BLACK)
    textRect = text.get_rect( )
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gamepad.blit(text, textRect)

def region():
    global boring, day, map_level, chances
    chances = 3
    
    gamepad.fill(WHITE)
    destinations = ["Gyeongbuk","Gyeonggi","Gwangju","Daegu","Busan","Seoul"]
    random.shuffle(destinations)
    destination = destinations[0]
    print_text("This time, the destination is " + destination , pad_width/2,pad_height/2 - 48,BLACK)
    if destination == "Daegu":
        map_level = 3
    elif destination == "Gyeongbuk" or destination == "Seoul":
        map_level = 2
    else:
        map_level = 1
    boring -= 30
    pg.display.update()
    pg.time.wait(1500)
    initGame()
    day+=1
    return 0
def club():
    global boring, age, infection, day, map_level, chances
    chances = 3
    if age >= 40:
        gamepad.fill(WHITE)
        print_text("Sorry, but the guard is blocking you!",pad_width/2,pad_height/2,BLACK)
        pg.display.update()
        pg.time.wait(1500)
        runGame_simul()
    else:
        map_level = 4
        boring -= 50
        if infection < 100:
            infection += 30
        else:
            infection = 100
        initGame()
    day += 1
    return 0

def game():
    global boring, day
    gamepad.fill(WHITE)
    print_text("LOL!",pad_width/2,50,BLACK)
    drawObject(lol_image, pad_width/2 - 384/2, pad_height/2 - 216/2)
    boring -= 10
    pg.display.update()
    pg.time.wait(2000)
    day +=1
    runGame_simul()
    return 0
def youtube():
    global boring, day
    gamepad.fill(WHITE)
    print_text("Youtube!",pad_width/2,100,BLACK)
    drawObject(socialDistancing, pad_width/2 - 255/2, pad_height/2 - 190/2)
    pg.display.update()
    pg.time.wait(2000)
    boring -= 10
    day +=1
    runGame_simul()
    return 0

def ramen():
    global hungry, day, cook_available
    gamepad.fill(WHITE)
    print_text("RAMEN!",pad_width/2,100,BLACK)
    drawObject(eat_ramen, pad_width/2 - 132/2, pad_height/2 - 99/2)
    pg.display.update()
    pg.time.wait(2000)
    if hungry > 0:
        hungry -= 20
    else:
        hungry = 0
    day +=1
    runGame_simul()
    return 0
def spam():
    global hungry, day, cook_available
    gamepad.fill(WHITE)
    print_text("SPAM!",pad_width/2,50,BLACK)
    drawObject(spams_image, pad_width/2 - 200/2, pad_height/2 - 200/2)
    pg.display.update()
    pg.time.wait(2000)
    if hungry > 0:
        hungry -= 20
    else:
        hungry = 0
    day +=1
    runGame_simul()
    return 0

def moveSelect(): #move 선택시
    global moveSelected
    moveSelected = True
    moveString = ['Other region','Club']
    moveAction = [region,club]
    drawObject(move_background,0,0)
    drawStatus()
    print_text("boring - 30",405, 246 - 130/2,RED)
    drawObject(region_image,405 - 130/2, 280 - 130/2)
    print_text("boring - 50",605, 216 - 130/2,RED)
    print_text("infection + 30",605, 246 - 130/2,RED)
    drawObject(club_image,605 - 141/2, 280 - 79/2)
    for i in range(2):
        button(moveString[i],WHITE,bright_green,350+(i*200),356,100,50,1,moveAction[i])
    return 0
def restSelect():
    global restSelected
    gamepad.fill(WHITE)
    restSelected = True
    restString = ['Game','Youtube']
    restAction = [game,youtube]
    drawObject(rest_background,0,0)
    drawStatus()
    print_text("Let's play the game!",200, 246 - 130/2,BLACK)
    drawObject(play_game,200 - 130/2, 280 - 130/2)
    print_text("boring - 10",405, 246 - 130/2,RED)
    drawObject(game_image,405 - 130/2, 280 - 130/2)
    print_text("Just watch the Youtube!",850, 246 - 130/2,BLACK)
    drawObject(watch_youtube,850 - 130/2, 280 - 130/2)
    print_text("boring - 10",605, 246 - 130/2,RED)
    drawObject(youtube_image,605 - 130/2, 280 - 130/2)
    for i in range(2):
        button(restString[i],WHITE,bright_green,350+(i*200),356,100,50,2,restAction[i])
    return 0
def cookSelect():
    global cookSelected, cook_background
    
    cookSelected = True
    cookString = ['Ramen','Span fried rice']
    cookAction = [ramen,spam]
    drawObject(cook_background,0,0)
    drawStatus()
    print_text("hungry - 20",405, 256 - 99/2,RED)
    drawObject(ramen_image,405 - 132/2, 290 - 99/2)
    print_text("hungry - 30",605, 256 - 99/2,RED)
    drawObject(spam_image,605 - 136/2, 290 - 102/2)
    for i in range(2):
            button(cookString[i],WHITE,bright_green,350+(i*200),356,100,50,3,cookAction[i])

    return 0

def teenager():
    global age
    age = 10
def youth():
    global age
    age = 20
def middle():
    global age
    age = 50
def elderly():
    global age
    age = 80
        
def runGame_simul(): #Start Simulation Game
    global gamepad, day, map_level, background_simul, age, boring, hungry, infection
    global over, begin, description, simul, getSelected, moveSelected, restSelected, cookSelected, infected
    global effect_sound
    
    map_level = 1
    order = 1
    description = False
    getSelected = False
    moveSelected = False
    restSelected = False
    cookSelected = False
    ramenSelected = False

    fileMatrix = []
    checks = []
    for a in range(infection):
        checks.append(1)
    for b in range(100-infection):
        checks.append(None)
    random.shuffle(checks)
    check = checks[0]
    if check == 1:
        infected == True
    
    
    if age == 10:
        boring += 10
        hungry += 5
    elif age == 20:
        boring += 5
        hungry += 10
    elif age == 50:
        boring += 5
        hungry += 5
    elif age == 80:
        boring += 10
        hungry += 3

    if boring <= 0:
        boring = 0
    if hungry <= 0:
        hungry = 0
        
    string = ['move', 'rest', 'cook']
    action = [moveSelect,restSelect,cookSelect]
    ages = ['10','20','50','80']
    ageGroup =[teenager,youth,middle,elderly]
    
    pg.mixer.music.load("sounds/main_sound.mp3")
    pg.mixer.music.play(-1)

    with open('begin_text.txt', 'r') as file:
        for lineContent in file:
            fileMatrix.append(lineContent.strip('\n'))
    while not begin:
        gamepad.fill(WHITE)
        drawObject(begin_background,0,0)
        print_text("COVID-19 Game", pad_width/2,50,WHITE)
        for i in range(len(fileMatrix)):
            print_text(fileMatrix[i],pad_width/2,100+(i*24),WHITE)
        print_text("Select your age group", pad_width/2,200, WHITE)
        for i in range(4):
            button(ages[i],WHITE,bright_green,50+(i*250),250,100,50,3,ageGroup[i])
        print_text("Your age group is " + str(age), pad_width/2,350, WHITE)
        print_text("Press space bar to start", pad_width/2,400, WHITE)
        pg.display.set_caption("simul")
        pg.display.update()
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    begin = True
                    simul= False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        begin = True
                        description = True
    while description:
        gamepad.fill(WHITE)
        if order == 1:
            drawObject(descriptions[0],0,0)
            pg.display.update()
        elif order == 2:
            drawObject(descriptions[1],0,0)
            pg.display.update()
        elif order == 3:
            drawObject(descriptions[2],0,0)
            pg.display.update()
        else:
            description = False
            simul = True
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    begin = True
                    simul= False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        order += 1
    
    while simul:
        if boring >= 100 or hungry >= 100:
            if boring >= 100:
                gamepad.fill(WHITE)
                print_text("Life is so boring",pad_width/2,pad_height/2,BLUE)
                print_text("\"boring\" figure is exceeded more than 100%",pad_width/2-12,pad_height/2+36,BLUE)
                pg.display.update()
                pg.time.wait(2000)
            elif hungry >= 100:
                gamepad.fill(WHITE)
                print_text("You are so starving",pad_width/2,pad_height/2,BLUE)
                print_text("\"hungry\" figure is exceeded more than 100%",pad_width/2-12,pad_height/2+36,BLUE)
                pg.display.update()
                pg.time.wait(2000)
            over = True
        gamepad.fill(WHITE)
        drawObject(background_simul,0,0)
        print_text("Current COVID-19",144,0,BLACK)
        drawObject(graph[day-1],10,26)
        drawStatus()
        if infection >= 50:
            pg.mixer.Sound.play(effect_sound)
            print_text("You are dangerous!",pad_width/2,100,RED)
            print_text("Please Keep Social-Distancing!",pad_width/2-10,130,RED)
        if not getSelected: 
            print_text("Choose your action",pad_width/2,200,WHITE)
            for i in range(3):
                button(string[i],WHITE,bright_green,250+(i*200),256,100,50,0,action[i])
        elif moveSelected:
            moveSelect()
        elif restSelected:
            restSelect()
        elif cookSelected:
            cookSelect()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                simul = False
                
        if infected == True:
            map_level = 5
            gamepad.fill(WHITE)
            print_text("You are infected by COVID-19",pad_width/2,pad_height/2,RED)
            print_text("You should go to the hospital",pad_width/2,pad_height/2+30,RED)
            pg.display.update()
            pg.time.wait(2000)
            initGame()
        elif over == True:
            gamepad.fill(WHITE)
            print_text("GAME OVER",pad_width/2,256,RED)
            pg.display.update()
            simul = False
            pg.time.wait(1500)
            return 0
        elif day == 31:
            gamepad.fill(WHITE)
            print_text("Game Clear!",pad_width/2,256,BLACK)
            print_text("Congratulation!",pad_width/2,300,BLUE)
            simul = False
            pg.display.update()
            pg.time.wait(2000)
            return 0
        pg.display.update()
    
    pg.mixer.music.stop()
    endGame()
    return 0

def initGame_simul(): #Set Simulation Game
    global gamepad, background_simul,begin_background, move_background, cook_background, rest_background, graph
    global ramen_image, spam_image, spams_image, region_image, game_image, youtube_image, socialDistancing, lol_image, club_image, eat_ramen, play_game, watch_youtube, descriptions
    global effect_sound
    
    descriptions = []
    
    gamepad = pg.display.set_mode((pad_width,pad_height))
    background_simul = pg.image.load("images/simul/background.png")
    begin_background = pg.image.load("images/simul/begin_background.jpg")
    move_background = pg.image.load("images/simul/move_background.jpg")
    cook_background = pg.image.load("images/simul/cook_background.png")
    rest_background = pg.image.load("images/simul/rest_background.png")
    region_image = pg.image.load("images/simul/region.png")
    eat_ramen = pg.image.load("images/simul/eat_ramen.png")
    ramen_image = pg.image.load("images/simul/ramen.png")
    spam_image = pg.image.load("images/simul/spam.png")
    spams_image = pg.image.load("images/simul/spams.png")
    game_image = pg.image.load("images/simul/game.jpg")
    play_game = pg.image.load("images/simul/play_game.png")
    youtube_image = pg.image.load("images/simul/youtube.png")
    watch_youtube = pg.image.load("images/simul/watch_youtube.png")
    socialDistancing = pg.image.load("images/simul/SocialDistancing.png")
    lol_image = pg.image.load("images/simul/lol.png")
    club_image = pg.image.load("images/simul/club.png")
    
    for j in range(1,4):
        descriptions.append(pg.image.load("images/description{0}.png".format(j)))

    graph = []
    for i in range(1,31):
        graph.append(pg.image.load("images/simul/graph/graph{0}.png".format(i)))
        
    effect_sound = pg.mixer.Sound("sounds/effect_sound.wav")
    
    pg.display.set_caption("simul")
    
    runGame_simul()
    return 0

startGame()


