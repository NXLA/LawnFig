#control your SmoothieBoard powered device with your keyboard

# todo

hostIP = "192.168.1.120"
increment = 1

import pygame
import sys
import socket
import urllib
import urllib2

pygame.init()

#make window for dispaying sent command
screenWidth = 400
screenHeight = 150
screen = pygame.display.set_mode((screenWidth, screenHeight))
background_color = (0,0,0)
screen.fill(background_color)
pygame.display.flip()
pygame.display.set_caption("Smoothie Xbox Control")

def sendCommand(command):
    timeout = 15
    socket.setdefaulttimeout(timeout)

    url = "http://" + hostIP + "/command_silent"

    content_type = "application/x-www-form-urlencoded; charset=UTF-8"

    body = []
    body = [command]

    body = '\r\n'.join(body)

    req = urllib2.Request(url)

    req.add_header('User-agent', 'Smoothie PC Control')
    req.add_header('Content-type', content_type)
    req.add_header('Content-length', len(body))
    req.add_data(body)

    print urllib2.urlopen(req).read()

#function for clearing and setting screen text
def setText(message):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    messageText = font.render(message, 1,(0,255,0))
    screen.fill(background_color)
    screen.blit(messageText, ((screenWidth/2) - messageText.get_width() // 2, (screenHeight/2) - messageText.get_height() // 2))
    pygame.display.flip()

def checkAxes():
    x = 3
    y = 4
    z = 1

    xPos = controller.get_axis(x)
    yPos = controller.get_axis(y)
    zPos = controller.get_axis(z)

    if xPos != 0:
        setText("X moved")
    elif yPos != 0:
        setText("Y moved")
    elif zPos != 0:
        setText("Z moved")
    else:
        setText("let's do this")

#intialize joystick module
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print len(joysticks)

#quit if no controller detected
if(len(joysticks) < 1):
    sys.exit("Controller not connected")

controller = pygame.joystick.Joystick(0)
controller.init()
print controller.get_name()

setText("let's do this")

print controller.get_numaxes()

running = True
while running:

    checkAxes()

    #continue running until user specifies quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
