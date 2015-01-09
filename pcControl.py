#control your SmoothieBoard powered device with your keyboard

# todo

hostIP = "192.168.1.120"

import pygame
import socket
import urllib
import urllib2

#make window for dispaying sent command
screenWidth = 400
screenHeight = 150
screen = pygame.display.set_mode((screenWidth, screenHeight))
background_color = (0,0,0)
screen.fill(background_color)
pygame.display.flip()
pygame.display.set_caption("Smoothie PC Control")

#intialize joystick module
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print joysticks

joystick = pygame.joystick.Joystick(0)
joystick.init()
print joystick.get_name()

def sendCommand(command):
    timeout = 15
    socket.setdefaulttimeout(timeout)

    print hostIP

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

setText("let's do this")

running = True
while running:
    #continue running until user specifies quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
