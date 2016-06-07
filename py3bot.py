#!/usr/bin/env python3

#irc python 3 bot for windows

import sys
import socket
import string
from threading import Timer
import random
import datetime
import os

#fill in the gaps :D
#---

HOST = "irc.freenode.net"
PORT = 6667

NICK = #botNick
IDENT = #password
REALNAME = #botNick
MASTER = #botOwnerNick
CHANNEL = #channel
LOGS = "irc_bot_logs" #Linux users check this

#CHANNEL = "#PBSIdeaChannel"
CHANNEL = "#botTesting"


#---

readbuffer = ""

s=socket.socket( )
s.connect((HOST, PORT))

s.send(bytes("NICK "+ NICK + "\r\n", "UTF-8"));
s.send(bytes("USER "+ IDENT + " " + HOST + " " + REALNAME + ":This is a bot thingy \r\n", "UTF-8"));
s.send(bytes("JOIN "+ CHANNEL + "\r\n", "UTF-8"));

s.send(bytes("PRIVMSG " + MASTER + " :Hi Princess!\r\n", "UTF-8"))

try:
    os.makedirs(LOGS)
except OSError:
    if not os.path.isdir(LOGS):
        raise

def tell(sender,recipient,message):
    s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " sent you a message: " + message + "\r\n", "UTF-8"))

def msgSelf(sender,message):
    s.send(bytes("PRIVMSG "+ sender + " :" + message + "\r\n", "UTF-8"))

while 1:    
    readbuffer = readbuffer+s.recv(512).decode("UTF-8")
    #be sure to check your log dir if using linux
    with open(LOGS + "\\" + str(datetime.date.today())+".dat","a+") as f:
        f.write(str(datetime.datetime.now()) + " "+ readbuffer)
    temp = str.split(readbuffer, "\n")
    
    readbuffer=temp.pop( )
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            s.send(bytes("PONG " + line[1] + "\r\n", "UTF-8"))

        if(line[1] == "PRIVMSG"):
        
            sender = line[0][1:line[0].find('!')]
            
            if(line[3] == ":!msgMe" and len(line) >= 4):
                message = "OH HAI!"
                if(len(line) > 4):
                    message = ''
                    j = 4
                    while j < len(line):
                        message += line[j]
                        message += ' '
                        j += 1
                msgSelf(sender,message)
            elif(line [3] == ":!quitNao" and len(line) == 4):
                if(sender == MASTER or sender == MASTER2):
                    s.send(bytes("QUIT\r\n", "UTF-8"))
                    sys.exit()
            elif(line [3] == ":!poke" and len(line) == 4):
                s.send(bytes("PRIVMSG "+ CHANNEL + " : \r\n", "UTF-8"))
            elif(line [3] == ":!roll20" and len(line) == 4):
                s.send(bytes("PRIVMSG "+ CHANNEL + " :" + str(random.randrange(1,20))+ "\r\n", "UTF-8"))
            elif(line [3] == ":!say" and len(line) >= 4):
                message = ''
                j = 4
                while j < len(line):
                    message += line[j]
                    message += ' '
                    j += 1
                s.send(bytes("PRIVMSG "+ CHANNEL + " :" + message + "\r\n", "UTF-8"))
            elif(line [3] == ":!gauss100" and len(line) == 4):
                j = 0
                mean = 0.0
                rand = []
                while j < 10000:
                    rand.append(random.randrange(1,100))
                    mean += rand[j]
                    j += 1
                mean = mean / float(len(rand))
                stdDev = 0.0
                for eachN in rand:
                    stdDev += (float(eachN) - mean)**2
                stdDev = (stdDev / float(len(rand)))**(1/2)
                s.send(bytes("PRIVMSG "+ CHANNEL + " : Number: " + str(rand[50]) + " ArraySize: " + str(len(rand)) + " Mean: " + str(mean) + ". StdDev: " + str(stdDev) + "\r\n", "UTF-8"))
            elif(line [3] == ":!flip" and len(line) == 4):
                s.send(bytes("PRIVMSG "+ CHANNEL + " : (╯°□°)╯︵ ┻━┻\r\n", "UTF-8"))
            elif(line [3] == ":!ping" and len(line) == 4):
                s.send(bytes("PRIVMSG "+ CHANNEL + " :PONG!!! ┬─┬°o(^_^o)\r\n", "UTF-8"))
            elif(line[3] == ":!tell" and len(line) >= 7):
                recipient = line[4]
                delaySec = line[5]
                message = ''
                j = 6
                while j < len(line):
                    message += line[j]
                    message += ' '
                    j += 1
                try:
                    delaySec = float(delaySec)
                    t = Timer(delaySec, tell,[sender,recipient,message])
                    t.start();
                except ValueError:
                    s.send(bytes("PRIVMSG "+ CHANNEL + " :syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n", "UTF-8"))
                except IndexError:
                    s.send(bytes("PRIVMSG "+ CHANNEL + " :syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n", "UTF-8"))
        for index, i in enumerate(line):
            print(line[index],index,len(line))
            
