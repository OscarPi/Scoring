import pygame, pylirc, sys, copy

players = []
notDone = True
i = 1
while notDone:
    name = raw_input('Enter player %i name: '%i)
    if name == '':
        confirm = raw_input('Please confirm (y/n) ')
        if confirm == 'y':
            notDone = False
    else:
        player = {'name':name, 'score':0}
        players.append(player)
        i = i + 1
roundd = 1

sockid = pylirc.init('any')
pygame.init()

displayInfo = pygame.display.Info()

width = displayInfo.current_w
height = displayInfo.current_h

buttonDelay = 0.01

screen = pygame.display.set_mode([width,height], pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
screen.fill([255, 255, 255])
pygame.display.flip()
font = pygame.font.Font(None, 100)
scoreFont = pygame.font.Font(None, 50)

def waitForOk():
    notDone = True
    while notDone:
        codes = pylirc.nextcode()
        if codes:
            code = codes[0]
            if code == 'ok':
                notDone = False
        time.sleep(buttonDelay)

def getInput(messageLineOne, messageLineTwo=None, codes=[]):
    codes = copy.copy(codes)
    msg1TxtWidth = font.size(messageLineOne)[0]
    if messageLineTwo:
        msg2TxtWidth = font.size(messageLineTwo)[0]
        titleLine2 = font.render(messageLineTwo, 1, [0,0,0])
    msgTxtHeight = font.size(messageLineOne)[1]
    titleLine1 = font.render(messageLineOne, 1, [0,0,0])
    if messageLineTwo:
        screen.blit(titleLine1, [int((width/2)-(msg1TxtWidth/2)),int((height/4)-(msgTxtHeight))])
        screen.blit(titleLine2, [int((width/2)-(msg2TxtWidth/2)),int((height/4))])
    else:
        screen.blit(titleLine1, [int((width/2)-(msg1TxtWidth/2)),int((height/4))])
    selectionText = ''.join(codes)
    selectionTxtWidth = font.size(selectionText)[0]
    txt = font.render(selectionText, 1, [255,0,0])
    screen.blit(txt, [int((width/2)-(selectionTxtWidth/2)),int(height/3*2)])

    pygame.display.flip()
    notDone = True
    while notDone:
        remoteCodes = pylirc.nextcode()
        if remoteCodes:
            time.sleep(buttonDelay)
            code = remoteCodes[0]
            screen.fill([255, 255, 255])

            if messageLineTwo:
                screen.blit(titleLine1, [int((width/2)-(msg1TxtWidth/2)),int((height/4)-(msgTxtHeight))])
                screen.blit(titleLine2, [int((width/2)-(msg2TxtWidth/2)),int((height/4))])
            else:
                screen.blit(titleLine1, [int((width/2)-(msg1TxtWidth/2)),int((height/4))])


            if code == 'power':
                screen.fill([255,255,255])
                sys.exit()
            elif code == 'left':
                if len(codes) > 0:
                    codes.pop()
            elif code == 'ok':
                message = ''.join(codes)
                screen.fill([255,255,255])
                pygame.display.flip()
                return message
            elif code == 'volumeup':
                if len(codes) > 0:
                    if codes[0] == '-':
                        del codes[0]
            elif code == 'volumedown':
                if len(codes) > 0:
                    if codes[0] != '-':
                        codes.insert(0, '-')
                else:
                    codes.append('-')
            else:
                codes.append(code)
            selectionText = ''.join(codes)
            selectionTxtWidth = font.size(selectionText)[0]
            txt = font.render(selectionText, 1, [255,0,0])
            screen.blit(txt, [int((width/2)-(selectionTxtWidth/2)),int(height/3*2)])
            pygame.display.flip()

def displayScores(playersFalse, topMsg):
    players = copy.copy(playersFalse)
    screen.fill([255,255,255])
    scores = []
    for player in players:
        scores.append(player['score'])
    curWidth = 0
    curHeight = 0
    maxWidth = 0

    nextHeight = curHeight + scoreFont.size(topMsg)[1]
    txtWidth = scoreFont.size(topMsg)[0]
    text = scoreFont.render(topMsg, 1, [255,0,0])
    screen.blit(text, [curWidth, curHeight])
    curHeight = nextHeight + height/50
    maxWidth = txtWidth

    scores = sorted(scores)
    for score in scores:
        for player in players:
            if player['score'] == score:
                name = player['name']
                string = name+': '+str(score)
                nextHeight = curHeight + scoreFont.size(string)[1]
                txtWidth = scoreFont.size(string)[0]
                if nextHeight > height:
                    curWidth = curWidth + (height/10) + maxWidth
                    curHeight = 0
                    nextHeight = curHeight + scoreFont.size(string)[1]
                    maxWidth = 0
                if (txtWidth + curWidth) > width:
                    break
                text = scoreFont.render(string, 1, [0,0,0])
                screen.blit(text, [curWidth, curHeight])
                curHeight = nextHeight + height/50
                if txtWidth > maxWidth:
                    maxWidth = txtWidth
                players.remove(player)

    ok = True
    string = 'Press OK to continue'
    nextHeight = curHeight + scoreFont.size(string)[1]
    txtWidth = scoreFont.size(string)[0]
    if nextHeight > height:
        curWidth = curWidth + (height/10) + maxWidth
        curHeight = 0
    if (txtWidth + curWidth) > width:
        ok = False
    if ok:
        text = scoreFont.render(string, 1, [255,0,0])
        screen.blit(text, [curWidth, curHeight])
        curHeight = nextHeight + height/50

    pygame.display.flip()
    waitForOk()
    screen.fill([255,255,255])

screen.fill([255,255,255])

for i in range(0, 10):
    scoringNotDone = True
    for player in players:
        player['tmpScore'] = None
    while scoringNotDone:
        for player in players:
            roundd = i + 1
            notDone = True
            notErrors = True
            while notDone:
                try:
                    if notErrors:
                        if player['tmpScore']:
                            od = int(getInput('Round %i'%roundd, 'What did %s score? '%player.get('name'), list(str(player['tmpScore']))))
                        else:
                            od = int(getInput('Round %i'%roundd, 'What did %s score? '%player.get('name')))
                    else:
                        if player['tmpScore']:
                            od = int(getInput('!!!!Error!!!!', 'What did %s score? '%player.get('name'), list(str(player['tmpScore']))))
                        else:
                            od = int(getInput('!!!!Error!!!!', 'What did %s score? '%player.get('name')))
                
                    notDone = False
                except:
                    notErrors = False
                    continue
            player['tmpScore'] = od

        message = 'Please confirm scores'
        text = font.render(message, 1, [255,0,0])
        txtWidth = font.size(message)[0]
        txtHeight = font.size(message)[1]
        screen.blit(text, [(width/2)-(txtWidth/2), (height/2)-(txtHeight/2)])
        pygame.display.flip()

        notDone = True
        while notDone:
            codes = pylirc.nextcode()
            if codes:
                code = codes[0]
                if code == 'ok':
                    screen.fill([255,255,255])
                    scoringNotDone = False
                    notDone = False
                elif code == 'left':
                    screen.fill([255,255,255])
                    notDone = False

            time.sleep(buttonDelay)

    for player in players:
        score = player['score'] + player['tmpScore']
        player.update({"round%i"%roundd:score})
        player['score'] = score

    if i != 9:
        displayScores(players, 'Scores for Round %i'%roundd)

suspenseMessage = 'And the winner is...'
text = font.render(suspenseMessage, 1, [255,0,0])
txtWidth = font.size(suspenseMessage)[0]
txtHeight = font.size(suspenseMessage)[1]
screen.blit(text, [(width/2)-(txtWidth/2), (height/2)-(txtHeight/2)])
pygame.display.flip()
waitForOk()
screen.fill([255,255,255])

scores = []
for player in players:
    scores.append(player['score'])
scores = sorted(scores)
winningScore = scores[-1]
winningPlayers = []
for player in players:
    if player['score'] == winningScore:
        winningPlayers.append(player['name'])
winners = ' and '.join(winningPlayers)

    
if len(winningPlayers) > 1:
    titleText = 'The winning players are:'
else:
    titleText = 'The winning player is:'

titleHeight = font.size(titleText)[1]
titleWidth = font.size(titleText)[0]
title = font.render(titleText, 1, [0,0,0])
screen.blit(title, [(width/2)-(titleWidth/2), (height/4)-(titleHeight/2)])

winnerHeight = font.size(winners)[1]
winnerWidth = font.size(winners)[0]
winnerText = font.render(winners, 1, [255,0,0])
screen.blit(winnerText, [(width/2)-(winnerWidth/2), (height/2)-(winnerHeight/2)])

pygame.display.flip()
waitForOk()
displayScores(players, 'Final Scores')

pylirc.exit()

