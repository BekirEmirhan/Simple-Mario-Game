import pygame
import random
import os
import ctypes


so_file = ".so file"
cfile = ctypes.CDLL(so_file)
cfile.move.argtypes = [ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)]
pygame.init()
screen = pygame.display.set_mode((1000,500))

bckMenu =  pygame.image.load(r"image path/menuBackground.png")
bckStage1 = pygame.image.load(r"image path/Stage-1.png")
bckStage2 = pygame.image.load(r"image path/Stage-2.png")
bckStage3 = pygame.image.load(r"image path/Stage-3.png")


player1 = pygame.image.load(r"image path/MPlayer.png")
player2 = pygame.image.load(r"image path/MPlayer-2.png")
player3 = pygame.image.load(r"image path/MPlayer-3.png")

car1 = pygame.image.load(r"image path/Car-1.png")
car2 = pygame.image.load(r"image path/Car-2.png")

monster1 = pygame.image.load(r"image path/monster-1.png")

bullet1 = pygame.image.load(r"image path/bullet-1.png")

coin100 = pygame.image.load(r"image path/coin100.png")
coin50 = pygame.image.load(r"image path/coin50.png")

pos = (0,0)

selection = player1

playerX = 300
playerY = ctypes.c_int(331) 
limit = 331
playerX_change=0
playerY_change = 0
backX =ctypes.c_int(0)
backY=0

car1X = 850
car1Y = 300
car1X_movement = 2

monster1X = 400
monster1Y = 320
monster1X_movement = 3

bulletX = 540
bullet_init = bulletX
bulletY = 360
bulletSpeed = 5
tempB = 0


gravity = 1

lives = 333
score = 0



blue = (0,0,128)
grey = (170,170,170)
dark_grey = (100,100,100)




IsMenu = True
Stage1 = False
Stage2 = False
Stage3 = False

isSpace = False #It cheks if player jumped
jump = False #It checks if jumped to platform
access1 = False #It checks Stage-1 platform-1 gravity situations
access2 = False #It checks Stage-1 enemy-1 gravity situations
limChecker = False #It checks player reached ground limit
isplatform=False
isHole = False

temper1 =True

Shop = False
selected = True

txt = pygame.font.Font('freesansbold.ttf', 20)

def start():
    global isSpace,jump,access1,access2,car1X,car1Y,car1X_movement,limChecker,limit,backX, playerX_change,playerY_change,playerY,lives
    isSpace = False #It cheks if player jumped
    jump = False #It checks if jumped to platform
    access1 = False #It checks Stage-1 platform-1 gravity situations
    access2 = False #It checks Stage-1 enemy-1 gravity situations
    limChecker = False #It checks player reached ground limit
    if Stage1:      
        limit = 331
        playerY.value = 331
    elif Stage2:
        limit = 318  
        car1X = 850
        car1Y = 300
        playerY.value = 318
        car1X_movement = 2
    backX.value=0
    playerX_change=0
    playerY_change = 0
    lives -=1

def hole(x1,y1,h,inital,deadLine):
    global backX,playerY,limit,isSpace,limChecker,isHole
    isHole=True
    pygame.time.delay(1)
    if backX.value<=x1 and backX.value>=y1 and playerY.value>inital:
        limit = h
        isSpace = True
        if limChecker and playerY.value >=deadLine:
            i = 0
            while i <100000:
                i +=1
            if i == 100000:
                start()
    
    #elif backX.value<y1+1:
        #isSpace = False

def platform(x1,x2,y1,y2,h,lim,realLim,downMove=False):
    global limChecker,limit,playerY,backX,isSpace,jump,playerX_change,isplatform
    pygame.time.delay(1)
    if backX.value <= x1 and backX.value >=y2:
        limit = lim
        if playerY.value<=h:
            jump = True
        if backX.value <= x1 and backX.value >=x2 and jump==False:
            backX.value = x1+1
            playerX_change = 0
        elif backX.value <= y1 and backX.value >=y2 and jump==False:
            backX.value = y2-3
            playerX_change = 0
        else:
            jump = False
        if backX.value <= y2+5:
            isplatform = True
            return True
        else:
            isplatform = False
            return False
    elif backX.value<= x1-6 and backX.value>= x1-1:
        isplatform =True
    elif isplatform:
        isplatform = False
        limit=realLim
        isSpace = True

def woodTrap(x1,y1,h,deadLine):
    global backX,limit,isSpace,limChecker
    if backX.value<=x1 and backX.value>=y1:
        limit = h
        isSpace = True
        if playerY.value >=deadLine:
            i = 0
            while i <10000:
                i +=1
            if i == 10000:
                 start()

def car(x1,width,height,limit1):
    global backX,playerY,playerX
    if playerX<=x1+3*width and playerX>= x1-width and playerY.value>=limit1-height:
        i = 0
        while i <10000:
            i +=1
        if i == 10000:
            #start()
            pass
    
def machine_gun(x1,y1,bulletImage,bulletSpeed):
    global limChecker,limit,playerY,backX,isSpace,jump,playerX_change,isplatform,bulletX,bulletY,tempB,temper1,bullet_init
    i=0
    if backX.value<=x1 and backX.value>=y1:
        if bulletX<=0:
            bullet_init -= tempB-backX.value
            bulletX = bullet_init
            bulletY = 360
            temper1 =True
        if temper1:
            tempB = backX.value
            temper1=False
        bulletX+=-5
        if playerX >=bulletX-3 and playerX <=bulletX+3 and bulletY-50<=playerY.value:
            while i <10000:
                i +=1
                if i == 10000:
                    start()
            
class Coin:
    def __init__(self,x1,x2,y1,type,y2 = limit,collected=False):
        self.collected = collected
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.type = type
    def collect(self):
        global score
        self.collected = True
        score +=self.type
    def collectCheck(self):
        global backX,playerY
        if backX.value <= self.x1 and backX.value>=self.x2 and playerY.value >= self.y1 and playerY.value<=self.y2 and self.collected ==False:
            self.collect()
    def coinTex(self,x,y,tex):
        if self.collected == False:  
            screen.blit(tex,(x,y))

def keyboard():
    global pos,running,playerX_change,isSpace,playerY_change,IsMenu,Shop,Stage1,Stage2,Stage3,backX,limit,playerY,bulletSpeed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IsMenu = False
            Shop = False
            Stage1 = False
            Stage2 = False
            Stage3 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change=3
                bulletSpeed = 10
            if event.key == pygame.K_LEFT:
                playerX_change=-3
            if event.key == pygame.K_SPACE:
                if playerY_change == 0:
                    playerY_change = -15
                isSpace = True
            if event.key == pygame.K_w:
                if Stage1:
                    Stage1=False
                    Stage2 = True
                    backX.value = 0
                    limit = 318
                    playerY.value = 318
                elif Stage2:
                    Stage2=False
                    Stage3 = True
                    backX.value = 0
                    limit = 296
                    playerY.value = 296
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change =0  
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

def carTex(x,y,tex):
    screen.blit(tex,(x,y))
    return screen.blit(tex,(x,y))
def background(x,y,back):
    screen.blit(back,(x,y))
    return screen.blit(back,(x,y))
def playerM(x,y,tex):
    screen.blit(tex, (x,y))
def livCount(x,y):
    txtLives = txt.render("Lives: "+str(lives),True,blue)
    screen.blit(txtLives, (x,y))
def scoreTable(x,y):
    txtScore = txt.render("Score: "+str(score),True,blue)
    screen.blit(txtScore, (x,y))
def texter(x,y,text):
    txter = txt.render(text,True,blue)
    screen.blit(txter, (x,y))

def texture(x,y,tex):
    screen.blit(tex, (x,y))

def play():
    global IsMenu,Stage1
    IsMenu = False
    Stage1 = True
def shop():
    global Shop,pos,dark_grey,grey,selection
    keyboard()
    screen.fill((0,0,0))
    background(backX.value,backY,bckMenu)
    mouse = pygame.mouse.get_pos()


    playerM(300,150,player1)
    playerM(400,150,player2)
    playerM(500,150,player3)

    if(mouse[0]<= 930 and mouse[0]>=800 and mouse[1]>=20 and mouse[1]<=40):
        pygame.draw.rect(screen,dark_grey,(800,20,130,25))
        texter(848,23,"Back")
    else:
        pygame.draw.rect(screen,grey,(800,20,130,25))
        texter(848,23,"Back")
    if(pos[0]<= 930 and pos[0]>=800 and pos[1]>=20 and pos[1]<=40):
        Shop = False
        pos = (0,0)
    if(pos[0]<= 930 and pos[0]>=800 and pos[1]>=20 and pos[1]<=40):
        Shop = False
        pos = (0,0)

    if(mouse[0]<= 400 and mouse[0]>=300 and mouse[1]>=230 and mouse[1]<=250):
        pygame.draw.rect(screen,dark_grey,(260,230,100,25))
        if selected and selection == player1:   
            texter(263,233,"Selected")
        else:
            texter(263,233,"Select")
    else:
        if selected and selection == player1:
            pygame.draw.rect(screen,dark_grey,(260,230,100,25))  
            texter(263,233,"Selected")
        else:
            pygame.draw.rect(screen,grey,(260,230,100,25))
            texter(263,233,"Select")
    if(pos[0]<= 400 and pos[0]>=300 and pos[1]>=230 and pos[1]<=250 and selection !=player1):
        selection = player1
    


    if(mouse[0]<= 480 and mouse[0]>=380 and mouse[1]>=230 and mouse[1]<=250):
        pygame.draw.rect(screen,dark_grey,(380,230,100,25))
        if selected and selection == player2:   
            texter(383,233,"Selected")
        else:
            texter(383,233,"Select")
    else:
        if selected and selection == player2:
            pygame.draw.rect(screen,dark_grey,(380,230,100,25))  
            texter(383,233,"Selected")
        else:
            pygame.draw.rect(screen,grey,(380,230,100,25))
            texter(383,233,"Select")
    if(pos[0]<= 480 and pos[0]>=380 and pos[1]>=230 and pos[1]<=250 and selection !=player2):
        selection = player2

    if(mouse[0]<= 580 and mouse[0]>=485 and mouse[1]>=230 and mouse[1]<=250):
        pygame.draw.rect(screen,dark_grey,(485,230,100,25))
        if selected and selection == player3:   
            texter(483,233,"Selected")
        else:
            texter(483,233,"Select")
    else:
        if selected and selection == player3:
            pygame.draw.rect(screen,dark_grey,(485,230,100,25))  
            texter(483,233,"Selected")
        else:
            pygame.draw.rect(screen,grey,(485,230,100,25))
            texter(483,233,"Select")
    if(pos[0]<= 580 and pos[0]>=485 and pos[1]>=230 and pos[1]<=250 and selection !=player3):
        selection = player3
    pygame.display.update()






while IsMenu:
    keyboard()
    screen.fill((0,0,0))
    background(backX.value,backY,bckMenu)
    mouse = pygame.mouse.get_pos()
    if(mouse[0]<= 530 and mouse[0]>=400 and mouse[1]>=170 and mouse[1]<=190):
        pygame.draw.rect(screen,dark_grey,(400,170,130,25))
        texter(448,173,"Play")
    else:
        pygame.draw.rect(screen,grey,(400,170,130,25))
        texter(448,173,"Play")
    if(pos[0]<= 530 and pos[0]>=400 and pos[1]>=170 and pos[1]<=190):
        play()

    if(mouse[0]<= 530 and mouse[0]>=400 and mouse[1]>=220 and mouse[1]<=240):
        pygame.draw.rect(screen,dark_grey,(400,220,130,25))
        texter(448,223,"Shop")
    else:
        pygame.draw.rect(screen,grey,(400,220,130,25))
        texter(448,223,"Shop")
    if(pos[0]<= 530 and pos[0]>=400 and pos[1]>=220 and pos[1]<=240):
        Shop = True
        pos = (0,0)
        while Shop:
            shop()

    if(mouse[0]<= 530 and mouse[0]>=400 and mouse[1]>=270 and mouse[1]<=290):
        pygame.draw.rect(screen,dark_grey,(400,270,130,25))
        texter(448,273,"QUIT")
    else:
        pygame.draw.rect(screen,grey,(400,270,130,25))
        texter(448,273,"QUIT")
    if(pos[0]<= 530 and pos[0]>=400 and pos[1]>=270 and pos[1]<=290):
        IsMenu = False
        Stage1 = False
        Stage2 = False
        Stage3 = False
    pygame.display.update()
    pygame.time.delay(250)







while Stage1:
    #pygame.time.wait(20)
    keyboard()

    #It is code of Stage-passing
    if backX.value <=-4250:
        Stage1=False
        Stage2 = True
        backX.value = 0
        limit = 318
        playerY.value = 318
        break
    #It is code of ground test
    if playerY.value > limit and isSpace:
        pygame.time.delay(1)
        playerY_change = 0
        playerY.value = limit
        isSpace = False
        limChecker = True
        

    #It checks player in the air
    if isSpace:
        playerY_change += gravity
    #It is code of the first platform
    platform(-1326,-1399,-1400,-1447,325,280,331)
    #It is code of the second platform
    platform(-1870,-1910,-1920,-1956,325,280,331)
    #It is code of the third platform
    platform(-1988,-2020,-2025,-2075,237,237,331)
    #It is code of the fourth platform
    platform(-2145,-2070,-2175,-2225,175,175,331)
    #It is code of the fiveth platform
    platform(-2754,-2800,-2801,-2838,325,325,331)
    #It is code of the sixth platform
    platform(-2904,-2945,-2946,-2988,325,325,331)
    #It is code of the seventh platform
    platform(-3075,-3115,-3120,-3160,325,325,331)
    #It is code of the eighth platform
    platform(-3205,-3245,-3250,-3285,325,325,331)
    #It is code of the nineth platform
    platform(-3600,-3639,-3640,-3680,260,260,331)
 

    #It is code of the first hole
    if backX.value <= -1510 and backX.value >=-1630:
        hole(-1510,-1630,400,330,380)
    #It is code of the second hole
    elif backX.value <= -2418 and backX.value >=-2500:
        hole(-2418,-2500,400,330,380)
    #It is code of the third hole
    elif backX.value <= -2658 and backX.value >=-3310:
        hole(-2658,-3310,400,330,380)
    else:
        if isHole:
            if Stage1:
                playerY.value = 331
                limit = 331
            if Stage2:
                playerY.value = 318
                limit = 318
            isHole=False

    #It is code of the first trap
    if backX.value <= -1956 and backX.value >=-2364 and playerY.value>=300:
        woodTrap(-1956,-2364,330,300)
    #It is code of the second trap
    if backX.value <= -3560 and backX.value >=-3735 and playerY.value>=300:
        woodTrap(-3560,-3735,330,300)

    #If lives == 0 terminates the game
    if lives == 0:
        Stage1 = False

    print(backX.value)
    #It is algorithm of movements 
    #playerY.value += playerY_change
    #backX.value +=-3*playerX_change
    cfile.move(backX,playerY,playerX_change,playerY_change)
    #It is code of background    
    screen.fill((0,0,0))
    background(backX.value,backY,bckStage1)

    #It is code of player image
    playerM(playerX,playerY.value,selection)

    #It is text of live
    livCount(900,50)
    scoreTable(900,100)
    
    # 1st 100 coin check
    if 'c1' not in globals():
        c1 = Coin(-180,-235,300,100,collected=False)
    c1.coinTex(backX.value+500,345,coin100)
    c1.collectCheck()
    # 2nd 100 coin check
    if 'c2' not in globals():
        c2 = Coin(-378,-432,300,100,collected=False)
    c2.coinTex(backX.value+700,345,coin100)
    c2.collectCheck()    
    # 1st 50 coin check
    if 'c3' not in globals():
        c3 = Coin(-662,-735,300,50,collected=False)
    c3.coinTex(backX.value+1000,335,coin50)
    c3.collectCheck() 
    # 3rd 100 coin check
    if 'c4' not in globals():
        c4 = Coin(-1320,-1386,250,100,collected=False)
    c4.coinTex(backX.value+1650,270,coin100)
    c4.collectCheck() 
    # 4th 50 coin check
    if 'c5' not in globals():
        c5 = Coin(-1580,-1630,220,50,y2=235,collected=False)
    c5.coinTex(backX.value+1900,220,coin50)
    c5.collectCheck() 
        # 4th 50 coin check
    if 'c6' not in globals():
        c6 = Coin(-1780,-1830,310,100,y2=340,collected=False)
    c6.coinTex(backX.value+2100,310,coin100)
    c6.collectCheck() 
    pygame.time.wait(1)



    texture(backX.value+1950,200,coin50)
    #texture(backX.value+1900,220,coin50)
    #texture(backX.value+1800,220,coin50)

    
    pygame.display.update()









    
while Stage2:
    pygame.time.wait(20)
    keyboard()
    pygame.time.wait(1)
    if backX.value <=-4300:
        Stage2=False
        Stage3 = True
        backX.value = 0
        limit = 296
        playerY.value = 296
        break
    #It is code of background    
    screen.fill((0,0,0))
    background(backX.value,backY,bckStage2)
    #It is code of Stage-passing

    #It is code of ground test
    if playerY.value > limit and isSpace:
        playerY_change = 0
        playerY.value = limit
        isSpace = False
        limChecker = True

    #It is code of first platform
    platform(-300,-349,-350,-405,270,270,318)
    #It is code of second platform
    platform(-430,-480,-481,-535,270,270,318)
    #It is code of third platform
    platform(-555,-599,-600,-650,270,270,318)
    #It is code of forth platform
    platform(-1720,-1765,-1770,-1815,229,229,318)
    #It is code of fifth platform
    platform(-1850,-1900,-1901,-1930,149,149,318)
    #It is code of sixth platform
    platform(-2038,-2080,-2081,-2120,224,224,318)
    
    #It is code of the first hole
    if backX.value <= -410 and backX.value >=-429:
        hole(-410,-429,318,270,318)
    #It is code of the second hole
    elif backX.value <= -536 and backX.value >=-554:
        hole(-536,-554,318,270,318)
    #It is code of the third hole
    elif backX.value <= -1374 and backX.value >=-1390:
        hole(-1374,-1392,400,270,400)
    #It is code of the forth hole
    elif backX.value <= -1425 and backX.value >=-1439:
        hole(-1425,-1439,400,270,400)
    #It is code of the fiveth hole
    elif backX.value <= -1374 and backX.value >=-1390:
        hole(-1374,-1390,400,270,400)
    #It is code of the seventh hole
    elif backX.value <= -1470 and backX.value >=-1488:
        hole(-1470,-1488,400,270,400)
    #It is code of the eigth hole
    elif backX.value <= -1516 and backX.value >=-1537:
        hole(-1516,-1537,400,270,400)
    #It is code of the nineth hole
    elif backX.value <= -1561 and backX.value >=-1584:
        hole(-1561,-1584,400,270,400)
    #It is code of the tenth hole
    elif backX.value <= -2904 and backX.value >=-2925:
        hole(-2904,-2925,400,270,400)
    #It is code of the eleventh hole
    elif backX.value <= -2950 and backX.value >=-2975:
        hole(-2950,-2975,400,270,400)
    #It is code of the twelth hole
    elif backX.value <= -3000 and backX.value >=-3023:
        hole(-3000,-3023,400,270,400)
    #It is code of the thirth hole
    elif backX.value <= -3047 and backX.value >=-3069:
        hole(-3047,-3069,400,270,400)
    #It is code of the fourteenth hole
    elif backX.value <= -3091 and backX.value >=-3114:
        hole(-3091,-3114,400,270,400)
    #It is code of the fifteenth hole
    elif backX.value <= -3145 and backX.value >=-3168:
        hole(-3145,-3168,400,270,400)
    #It is code of the sixteenth hole
    elif backX.value <= -3194 and backX.value >=-3216:
        hole(-3194,-3216,400,270,400)
    #It is code of the seventh hole
    elif backX.value <= -3240 and backX.value >=-3264:
        hole(-3240,-3264,400,270,400)
    #It is code of the eighteenth hole
    elif backX.value <= -3288 and backX.value >=-3312:
        hole(-3288,-3312,400,270,400)
    #It is code of the nineteenth hole
    elif backX.value <= -3336 and backX.value >=-3355:
        hole(-3336,-3355,400,270,400)
    #It is code of the twenty hole
    elif backX.value <= -3390 and backX.value >=-3414:
        hole(-3390,-3414,400,270,400)
    #It is code of the twenth-one hole
    elif backX.value <= -3438 and backX.value >=-3462:
        hole(-3438,-3462,400,270,400)
    #It is code of the twenty-two hole
    elif backX.value <= -3486 and backX.value >=-3510:
        hole(-3486,-3510,400,270,400)
    #It is code of the twenth-three hole
    elif backX.value <= -3535 and backX.value >=-3558:
        hole(-3535,-3558,400,270,400)
    #It is code of the twenty-four hole
    elif backX.value <= -3582 and backX.value >=-3603:
        hole(-3582,-3603,400,270,400)
    else:
        if isHole==False:
            if Stage1:
                playerY.value = 331
                limit = 331
            if Stage2:
                playerY.value = 318
                limit = 318
            isHole=True



    #It is code of first car
    if backX.value<=-500 and backX.value>=-1300:
        carTex(car1X,car1Y,car1)
        car(car1X,30,30,318)
        car1X += car1X_movement+-5*playerX_change
        if car1X<=100:
            car1X_movement = -car1X_movement 
        elif car1X>=1000:
            car1X_movement = -car1X_movement 
    #It is code of second car
    elif backX.value<=-1700 and backX.value>=-2300:
        carTex(car1X,car1Y,car1)
        car(car1X,30,30,318)
        car1X += car1X_movement+-5*playerX_change
        if car1X<=100:
            car1X_movement = -car1X_movement 
        elif car1X>=1000:
            car1X_movement = -car1X_movement 
    else:
        car1X = 850
        car1Y = 300



    if backX.value<=-2200 and backX.value>=-2800:
        machine_gun(-2200,-2800,bullet1,-1)
        screen.blit(bullet1, (bulletX,bulletY))

    #It checks player in the air
    if isSpace:
        playerY_change += gravity
    #If lives == 0 terminates the game
    if lives == 0:
        break

    print(backX.value)
    #It is algorithm of movements 
    #playerY.value += playerY_change
    #backX.value +=-3*playerX_change
    cfile.move(backX,playerY,playerX_change,playerY_change)

    #It is code of player image
    playerM(playerX,playerY.value,selection)

    #It is text of live
    livCount(900,50)
    scoreTable(900,100)
    pygame.display.update()








monster1Set = 700

while Stage3:
    keyboard()
    #It is code of background    
    screen.fill((0,0,0))
    background(backX.value,backY,bckStage3)
     #It checks player in the air
    if isSpace:
        playerY_change += gravity

    #It is code of ground test
    if playerY.value > limit and isSpace:
        playerY_change = 0
        playerY.value = limit
        isSpace = False
        limChecker = True
    
    #It is code of first car
    if backX.value<=-720 and backX.value>=-1150:
        carTex(monster1X,monster1Y,monster1)
        car(monster1X,30,30,296)
        monster1X += monster1X_movement+-5*playerX_change
        if monster1X<=0:
            monster1X_movement = -monster1X_movement 
        elif monster1X>=monster1Set:
            monster1X_movement = -monster1X_movement 
    elif  backX.value<=-1150:
        monster1Set -= backX.value+720 
    else:
        monster1X = 400
        monster1Y = 320
    #If lives == 0 terminates the game
    if lives == 0:
        break

    #print(backX.value)
    print("lim: ",monster1Set)
    #It is algorithm of movements 
    #playerY.value += playerY_change
    #backX.value +=-3*playerX_change
    cfile.move(backX,playerY,playerX_change,playerY_change)
    if backX.value<=-720 and backX.value>=-1150:
        monster1Set -= 3*playerX_change
    else:
        monster1Set = 700


    #It is code of player image
    playerM(playerX,playerY.value,selection)

    #It is text of live
    livCount(900,50)
    scoreTable(900,100)
    pygame.display.update()

