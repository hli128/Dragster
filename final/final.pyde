'''
Control:
press R to start the game or back to title when on the result scree

press J for accelerator
press E to start move when progress bar indicates enginer is ready to start
press W to up, and S to down.


Rules:
5s countdown - Countdown timer. Moving during countdown will result in false start (however, player can accelerate (J) without starting move (E))
Progress bar - indicate enginer state. The green line means ready to start
False start - press E when enginer is not ready will result in false start
blast - enginer will blast if progress bar is full
Incoming cars - dodging objects. Hiting on any of those cars will end the game
'''

gameState = 0
TITLE_STATE = 0
PLAY_STATE = 1
GAME_OVER_STATE = 2

startTime = 0
stoppedTimes = []
MAX_TIMES = 10

lastRoundTime = 0
acc = 0

# prograss bar
progress = 0

def setup():
    size(960, 640)
    textSize(32)
    
def draw():
    global lastRoundTime
    background(0)
    
    if gameState == TITLE_STATE:
        drawTitleScreen()
    elif gameState == PLAY_STATE:
        drawPlayScreen()
    elif gameState == GAME_OVER_STATE:
        drawGameOverScreen()
        
def drawTitleScreen():
    global moving, posX, falseStart, startTime, countdown, checkPoint, acc, hit, carPosY, ballPosX, ballPosY, progress, blast
    textAlign(CENTER)
    text("Dragster", width/2, height/2)
    textAlign(LEFT)
    text("Press J to accelerate", 20, 40)
    text("Press R to start a new game", 20, 80)
    
    posX = 5000 # final line
    carPosY = height/2
    startTime = 0
    checkPoint = 1 # trigger to record lastRoundTime
    acc = 0

    moving = 0
    progress = 0
    blast = 0
    falseStart = 0
    
    ballPosX = []
    ballPosY = []
    
    # create ball list with len of 3
    for i in range(3):
        ballPosX.append(1000)
        ballPosY.append(random(0,640))
    hit = 0
    
def drawPlayScreen():
    global posX, startTime, travelTime, gameState, falseStart, lastRoundTime, checkPoint, acc, hit, carPosY, millisString, ballPosX, ballPosY, progress, blast
    textAlign(RIGHT)
    
    if checkPoint:
        lastRoundTime = millis()
        checkPoint = 0
    
    countdown = (1 - ((millis() - lastRoundTime) / 1000)) ### count down
    # prepare stage: during which pressing the accelerator will result in a false start
    if countdown > 0:
        text(countdown, width/2, height/4)
        text("0:0:0", 850, 50)
        # false start
        if moving == 1:
            falseStart = 1
            gameState = GAME_OVER_STATE
    # ready to start stage
    elif countdown == 0:
        text("Go!", width/2, height/4)
        startTime = millis()
        text("Start!", 850, 50)
    # moving stage
    else:
        offsetTime = millis() - startTime
        text(str(offsetTime), width/2, height/4)
    
        millisString = str(offsetTime / 1000) + ":" + str((offsetTime / 100) - (offsetTime / 1000) * 10) + ":" + nf(offsetTime % 100, 2)
        text(millisString, 850, 50)
    
    
    # finish line move, not the car
    if moving == 1:
        posX -= (2 + acc)
    
    car = loadImage("assets/car.png")
    image(car, 20, carPosY,100, 50)
    # finish line
    fill(255, 0, 0)
    rect(posX, height/4, 2, 400)
    fill(255, 255, 255)
    if posX <= 20:
        travelTime = millisString
        gameState = GAME_OVER_STATE
    
    # incoming cars  
    for i in range(len(ballPosX)):
        if i < len(ballPosX):
            if moving == 1:
                ballPosX[i] -= (random(0,10) + acc/2)
        # off-screen
        if ballPosX[i] < 50:
            ballPosX[i] = 1000
            ballPosY[i] = random(0, 640)
        # hit
        if ballPosX[i] <= 120: # car position is fixed
            if ballPosY[i] > carPosY-20:
                if ballPosY[i] < carPosY+20:
                    travelTime = millisString
                    hit = 1
                    gameState = GAME_OVER_STATE
    
    ball1 = loadImage("assets/ball1.png")
    ball2 = loadImage("assets/ball2.png")
    ball3 = loadImage("assets/ball3.png")
    ball = [ball1, ball2, ball3]
    for i in range(len(ballPosX)):
        image(ball[i], ballPosX[i], ballPosY[i], 100, 50)
    
    if progress > 0:
        progress -= 3
    
    if progress > 600:
        blast = 1
        gameState = GAME_OVER_STATE
    # prograss bar
    stroke(0, 0, 0)
    
    fill(255)
    rect(10, 10, 600, 30)
    
    fill(255, 0, 0)
    rect(10, 10, progress, 30)
    
    fill(0, 255, 0)
    rect(400, 10, 5, 30)
    
def drawGameOverScreen():
    global falseStart, bestTime, blast
    textAlign(CENTER)
    fill(255, 0, 0)
    if falseStart:
        text("False Start!", width/2, height/2)
    elif blast:
        text("Blast!", width/2, height/2)
    elif hit:
        text("Hit!", width/2, height/2)
    else:
        text("Travel Time: " + travelTime, width/2, height/2)
    for time in stoppedTimes:
        time.render()
        
    fill(255)
    textAlign(LEFT)
    text("Press R to start a new game", 20, 80)
    
def keyPressed():
    global gameState, startTime, stoppedTimes, speed, posX, moving, acc, carPosY, millisString, progress, falseStart
    if key == "r" or key == "R":
        if gameState == TITLE_STATE:
            gameState = PLAY_STATE
        elif gameState == PLAY_STATE:
            pressTime = millis() - startTime
            millisString = str(pressTime / 1000) + ":" + str((pressTime / 100) - (pressTime / 1000) * 10) + ":" + nf(pressTime % 100, 2)
            tempPos = PVector(width - 10, 30 * len(stoppedTimes) + 30)
            stoppedTimes.append(StoppedTimes(tempPos, millisString))
            if len(stoppedTimes) >= MAX_TIMES:
                gameState = GAME_OVER_STATE
        elif gameState == GAME_OVER_STATE:
            gameState = TITLE_STATE
            stoppedTimes = []
        
    if key == "j" or key == "J":
        if gameState == PLAY_STATE:
            if moving == 1:
                acc += 0.5
                progress += 30
            else:
                progress += 30
                print(progress)

    # restart the game
    if key == "r" or key == "R":
        if gameState == GAME_OVER_STATE:
            gameState = TITLE_STATE
            
    # Y move
    if key == "w" or key == "W":
        if gameState == PLAY_STATE:
            if moving == 1:
                carPosY -= 10
    if key == "s" or key == "S":
        if gameState == PLAY_STATE:
            if moving == 1:
                carPosY += 10 
                
    if key == "e" or key == "E":
        if gameState == PLAY_STATE:
            if progress >= 400: # ready to start
                moving = 1
            else:
                falseStart = 1
                gameState = GAME_OVER_STATE       

def keyReleased():
    global moving, gameState, acc, progress
    if key == "j" or key == "J":
        if gameState == PLAY_STATE and acc >= 0:
            acc -= 1
    

class StoppedTimes():
    def __init__(self, tempPos, tempString):
        self.pos = tempPos
        self.string = tempString
        
    def render(self):
        textAlign(RIGHT)
        text(self.string, self.pos.x, self.pos.y)
