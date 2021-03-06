#control your OctoPrint powered printer with your Xbox controller

# todo

#enter your OctoPrint info here
hostIP = ["192.168.1.122", "prusa.local"]
apiKey = ["25A1AE457F3E4ACF854B80A51BA51776", "156A8AE4000940CFB3C51C9DFD812D8A"]

increment = 1
printerIndex = 0

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

def sendCommand(axis, command):
    timeout = 15
    socket.setdefaulttimeout(timeout)

    url = "http://" + hostIP[printerIndex] + "/api/printer/printhead"
    print printerIndex
    content_type = "application/json"

    body = []

    if command == "home":
        body = ['{"command":"home","axes":%s}' % axis]
    elif command == "jog":
        body = ['{"command":"jog","%s":%s}' % (axis, increment)]
    elif command == "-jog":
        body = ['{"command":"jog","%s":-%s}' % (axis, increment)]

    body = '\r\n'.join(body)

    req = urllib2.Request(url)

    req.add_header('User-agent', 'OctoXbox Control')
    req.add_header('Content-type', content_type)
    req.add_header('Content-length', len(body))
    req.add_header('X-Api-Key', apiKey[printerIndex])
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
        if xPos > 0:
            sendCommand("x", "jog")
        else:
            sendCommand("x", "-jog")
    elif yPos != 0:
        setText("Y moved")
        if yPos > 0:
            sendCommand("y", "-jog")
        else:
            sendCommand("y", "jog")
    elif zPos != 0:
        setText("Z moved")
        if zPos > 0:
            sendCommand("z", "-jog")
        else:
            sendCommand("z", "jog")
    elif leftTrigger > 0:
        setText("Left Trigger")
        #retract
    elif rightTrigger > 0:
        setText("right trigger")
        #extrude
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

    global increment
    global printerIndex

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
        sendCommand('["z"]', "home")
    elif controller.get_button(rightBumper):
        setText("right bumper")
        sendCommand('["x", "y"]', "home")
    elif controller.get_button(back):
        if len(hostIP) > 1:
            if len(hostIP) == len(apiKey):
                if printerIndex > 0:
                    printerIndex -= 1
                    setText(hostIP[printerIndex])
                else:
                    printerIndex = len(hostIP) - 1
    elif controller.get_button(select):
        #cycle through printers
        if len(hostIP) > 1:
            if len(hostIP) == len(apiKey):
                if printerIndex < (len(hostIP)-1):
                    printerIndex += 1
                    setText(hostIP[printerIndex])
                else:
                    printerIndex = 0
    elif controller.get_button(leftAnalogClick):
        setText("right analog stick")
    elif controller.get_button(rightAnalogClick):
        setText("left analog click")
    elif controller.get_button(xboxButton):
        setText("xbox button")
        sys.exit("quit")
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

    pygame.time.wait(100)

    #continue running until user specifies quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
