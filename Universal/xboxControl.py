#control your OctoPrint powered printer with your Xbox controller

# TODO
# txt with controls explanation
# user configurable background and text color

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

# choose which printer index you want to be used on start
startPrinterIndex = 0 # should be 0 if you only have one printer

# set the four jogging increments you would like (in mm)
# must be four increments
jogging_increments = [0.1, 1.0, 10.0, 100.0]

# enter your preferred default jogging increment
# must be one of the four you specified above in jogging_increments
default_increment = jogging_increments[1]

# feedrate settings
xy_feedrate = 3000
z_feedrate = 200

# choose one of the following
heat_command = "M109" # safer option - sets extruder temp nd waits for it to reach temp
# heat_command = "M104" # sets extruder temp but does not wait

# extruder temperature (in °C)
extruder_temperature = 210

# enter how often you would like to check for new input (milliseconds)
refresh_rate = 100

# set sensitivity
# enter a percentage without the %
sensitivity = 50
# ---------------------------------------------------------------------------------------------

increment = jogging_increments[1]
if(default_increment == jogging_increments[0] or default_increment == jogging_increments[1] or default_increment == jogging_increments[2] or default_increment == jogging_increments[3]):
    increment = default_increment

printerIndex = startPrinterIndex
joggingIncrement = jogging_increments
maximumJoystickValue = 32768
sensitivityCutoff = maximumJoystickValue*(sensitivity/100)
xyFeedrate = xy_feedrate
zFeedrate = z_feedrate
heatCommand = heat_command
extruderTemperature = extruder_temperature

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

__version__ = "0.2"
pygame.display.set_caption("Universal Xbox Printer Control v" + __version__)

def sendOctoPrintCommand(command):
    timeout = 15
    socket.setdefaulttimeout(timeout)

    url = "http://" + hostIP[printerIndex] + ":" + hostPort[printerIndex] + "/api/printer/command"
    content_type = "application/json"

    body = []
    body =  '{\"command\": \"' + command + '\"}' + '\n\n'

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

def sendJogCommand(jogCommand):
    sendCommand("G91")
    sendCommand(jogCommand)
    sendCommand("G90")

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
    e = 2

    leftTriggerAxis = 2
    rightTriggerAxis = 5

    xPos = controller.get_axis(x)
    yPos = controller.get_axis(y)
    zPos = controller.get_axis(z)
    ePos = controller.get_axis(e)
    leftTrigger = controller.get_axis(leftTriggerAxis)
    rightTrigger = controller.get_axis(rightTriggerAxis)

    if xPos > sensitivityCutoff or xPos < sensitivityCutoff:
        print "Cutoff: %d" % sensitivityCutoff
        setText("X moved")
        if xPos > 0:
            sendJogCommand("G1 X%f F%d" % (increment, xyFeedrate))
        else:
            sendJogCommand("G1 X-%f F%d" % (increment, xyFeedrate))
    elif yPos > sensitivityCutoff or yPos < sensitivityCutoff:
        setText("Y moved")
        if yPos > 0:
            sendJogCommand("G1 Y-%f F%d" % (increment, xyFeedrate))
        else:
            sendJogCommand("G1 Y%f F%d" % (increment, xyFeedrate))
    elif zPos > sensitivityCutoff or zPos < sensitivityCutoff:
        setText("Z moved")
        if zPos > 0:
            sendJogCommand("G1 Z-%f F%d" % (increment, zFeedrate))
        else:
            sendJogCommand("G1 Z%f F%d" % (increment, zFeedrate))
    elif ePos > sensitivityCutoff or ePos < sensitivityCutoff:
        if ePos > 0:
            setText("Extruder heating")
            sendCommand("%s S%d" % (heatCommand, extruderTemperature))
        else:
            setText("Heaters off")
            sendCommand("%s S0" % heatCommand)
    elif leftTrigger > 0:
        setText("Retract %fmm" % increment)
        sendJogCommand("G1 E-%f" % increment)
    elif rightTrigger > 0:
        setText("Extrude %fmm" % increment)
        sendJogCommand("G1 E%f" % increment)
    # else:
    #     setText("Ready")

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
        setText("increment: %f" % joggingIncrement[0])
        increment = joggingIncrement[0]
    elif controller.get_button(one):
        setText("increment: %f" % joggingIncrement[1])
        increment = joggingIncrement[1]
    elif controller.get_button(ten):
        setText("increment: %f" % joggingIncrement[2])
        increment = joggingIncrement[2]
    elif controller.get_button(hundred):
        setText("increment: %f" % joggingIncrement[3])
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
    #else:
        #setText("Ready")


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

setText("Ready")

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
