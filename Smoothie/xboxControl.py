#control your Smoothie powered device with your Xbox controller

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

#check if the triggers or analog sticks are moved
def checkAxes():
    x = 3
    y = 4
    z = 1

    leftTriggerAxis = 2
    rightTriggerAxis = 5

    xPos = controller.get_axis(x)
    yPos = controller.get_axis(y)
    zPos = controller.get_axis(z)
    leftTrigger = controller.get_axis(leftTriggerAxis)
    rightTrigger = controller.get_axis(rightTriggerAxis)

    if xPos != 0:
        setText("X moved")
    elif yPos != 0:
        setText("Y moved")
    elif zPos != 0:
        setText("Z moved")
    elif leftTrigger > 0:
        setText("Left Trigger")
    elif rightTrigger > 0:
        setText("right trigger")
    # else:
    #     setText("let's do this")

#check if buttons are pressed
def checkButtons():
    tenth = 0
    one = 1
    ten = 2
    hundred = 3
    leftBumper = 4
    rightBumper = 5
    back = 6
    select = 7
    leftAnalogClick = 9
    rightAnalogClick = 10
    xboxButton = 8

    if controller.get_button(tenth):
        setText("increment: 0.1")
        increment = 0.1
    elif controller.get_button(one):
        setText("increment: 1")
        increment = 1
    elif controller.get_button(ten):
        setText("increment: 10")
        increment = 10
    elif controller.get_button(hundred):
        setText("increment: 100")
        increment = 100
    elif controller.get_button(leftBumper):
        setText("left bumper")
    elif controller.get_button(rightBumper):
        setText("right bumper")
    elif controller.get_button(back):
        setText("back")
    elif controller.get_button(select):
        setText("select")
    elif controller.get_button(leftAnalogClick):
        setText("right analog stick")
    elif controller.get_button(rightAnalogClick):
        setText("left analog click")
    elif controller.get_button(xboxButton):
        setText("xbox button")
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
print controller.get_numbuttons()

running = True
while running:

    checkAxes()
    checkButtons()

    #continue running until user specifies quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
