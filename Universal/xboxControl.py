#control your OctoPrint powered printer with your Xbox controller

# TODO
# sensitivity setting
# txt with controls explanation

# ---------------------------------------------------------------------------------------------
# USER CONFIGURABLE INFO

# list the IPs of your smoothie or octoprint printers
hostIP = ["pb.local", "192.168.1.122", "prusa.local"]

# port
# must be the same number of ports as IPs
hostPort = ["80", "80", "80"]

# enter your OctoPrint apikeys here - they must match the index of the list of IPs above
# if it is smoothie the value should be "smoothie"
apiKey = ["25A1AE457F3E4ACF854B80A51BA51776", "smoothie", "156A8AE4000940CFB3C51C9DFD812D8A"]

# set the four jogging increments you would like (in mm)
# must be four increments
jogging_increments = [0.1, 1, 10, 100]

# enter your preferred default jogging increment
# must be one of the four you specified above in jogging_increments
default_increment = jogging_increments[1]

# choose which printer index you want to be used on start
startPrinterIndex = 0 # should be 0 if you only have one printer

# enter how often you would like to check for new input (milliseconds)
refresh_rate = 150

#feedrate settings
xyFeedrate = 3000
zFeedrate = 200
# ---------------------------------------------------------------------------------------------

if(default_increment == jogging_increments[0] or default_increment == jogging_increments[1] or default_increment == jogging_increments[2] or default_increment == jogging_increments[3]):
    increment = default_increment
else:
    increment = jogging_increments[1]

printerIndex = startPrinterIndex
joggingIncrement = joggingIncrements

import pygame
import sys
import socket
import urllib
import urllib2

pygame.init()

#make window for dispaying sent commands
screenWidth = 400
screenHeight = 150
screen = pygame.display.set_mode((screenWidth, screenHeight))
background_color = (0,0,0)
screen.fill(background_color)
pygame.display.flip()

__version__ = "0.1"
pygame.display.set_caption("Universal Xbox Printer Control v" + __version__)

def sendOctoPrintCommand(command):
    timeout = 15
    socket.setdefaulttimeout(timeout)

    url = "http://" + hostIP[printerIndex] + ":" + hostPort[printerIndex] + "/api/printer/command"
    print printerIndex
    content_type = "application/json"

    body = []
    body =  '{\"command\": \"' + command + '\"}' + '\r\n'

    req = urllib2.Request(url)

    req.add_header('User-agent', 'Xbox Printer Controller')
    req.add_header('Content-type', content_type)
    req.add_header('Content-length', len(body))
    req.add_header('X-Api-Key', apiKey[printerIndex])
    req.add_data(body)

    print urllib2.urlopen(req).read()

def sendSmoothieCommand(command):
        timeout = 15
        socket.setdefaulttimeout(timeout)

        url = "http://" + hostIP[printerIndex] + ":" + hostPort[printerIndex] + "/command"
        print printerIndex
        content_type = "application/x-www-form-urlencoded"

        body = []
        body =  command + "\n:"

        req = urllib2.Request(url)

        req.add_header('User-agent', 'Xbox Printer Controller')
        req.add_header('Content-type', content_type)
        req.add_header('Content-length', len(body))
        req.add_data(body)

        print urllib2.urlopen(req).read()

def sendCommand(command):
    if(apiKey[printerIndex] == "smoothie"):
        sendSmoothieCommand(command)
    else:
        sendOctoPrintCommand(command)

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
            sendCommand("G91 G0 X" + increment + " F" + xyFeedrate + " G90")
        else:
            sendCommand("G91 G0 X-" + increment + " F" + xyFeedrate + " G90")
    elif yPos != 0:
        setText("Y moved")
        if yPos > 0:
            sendCommand("G91 G0 Y-" + increment + " F" + xyFeedrate + " G90")
        else:
            sendCommand("G91 G0 Y" + increment + " F" + xyFeedrate + " G90")
    elif zPos != 0:
        setText("Z moved")
        if zPos > 0:
            sendCommand("G91 G0 Z-" + increment + " F" + zFeedrate + " G90")
        else:
            sendCommand("G91 G0 Z" + increment + " F" + zFeedrate + " G90")
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
        setText("increment: " + joggingIncrement[0])
        increment = joggingIncrement[0]
    elif controller.get_button(one):
        setText("increment: " + joggingIncrement[1])
        increment = joggingIncrement[1]
    elif controller.get_button(ten):
        setText("increment: " + joggingIncrement[2])
        increment = joggingIncrement[2]
    elif controller.get_button(hundred):
        setText("increment: " + joggingIncrement[3])
        increment = joggingIncrement[3]
    elif controller.get_button(leftBumper):
        setText("left bumper")
        sendCommand("G28 Z")
    elif controller.get_button(rightBumper):
        setText("right bumper")
        sendCommand("G28 XY")
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
    sys.exit("Controller not connected (or detected)")

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

    pygame.time.wait(refresh_rate)

    #continue running until user specifies quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
