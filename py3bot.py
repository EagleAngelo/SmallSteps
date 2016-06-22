#!/usr/bin/env python3

#irc python 3 bot for windows
#2016-06-13, 6PM

import sys
import socket
import string
from threading import Timer
import random
import datetime
import os
import time

#fill in the gaps :D
#---

HOST = "irc.freenode.net"
PORT = 6667

NICK = #botNick
IDENT = #password
REALNAME = #botNick
MASTER = #botOwnerNick
MASTAH = #botOwnerNick2
CHANNEL = #channel
LOGS = "C:\irc_bot_logs" #Linux users correct this

CHANNEL = "#botTesting"

#---

class IRCbot():
    def __init__(self):
        self.command1 = []
        self.readbuffer = ""
        self.s = None
        self.host1 = ""
        self.port1 = 0
        self.nick1 = ""
        self.ident1 = ""
        self.realname1 = ""
        self.master1 = ""
        self.mastah1 = ""
        self.logs1 = ""
        self.channel1 = ""
        
    def setBot(self,P_HOST,P_PORT,P_NICK,P_IDENT,P_REALNAME,P_MASTER,P_MASTAH,P_LOGS,P_CHANNEL):
        self.host1 = P_HOST
        self.port1 = P_PORT
        self.nick1 = P_NICK
        self.ident1 = P_IDENT
        self.realname1 = P_REALNAME
        self.master1 = P_MASTER
        self.mastah1 = P_MASTAH
        self.logs1 = P_LOGS
        self.channel1 = P_CHANNEL
        
    def connect(self):
        self.s=socket.socket( )
        self.s.connect((self.host1,self.port1))
        self.s.send(bytes("NICK "+ self.nick1 + "\r\n", "UTF-8"));
        self.s.send(bytes("USER "+ self.ident1 + " " + self.host1 + " " + self.realname1 + ":This is a bot thingy \r\n", "UTF-8"));
        self.s.send(bytes("JOIN "+ self.channel1 + "\r\n", "UTF-8"))
        self.s.send(bytes("PRIVMSG " + self.master1 + " :Hi Princess!\r\n", "UTF-8"))
        
    def logFolder(self):
        try:
            os.makedirs(self.logs1)
        exce``pt OSError:
            if not os.path.isdir(self.logs1):
                raise
        
    def reg_command(self,command):
        self.commands.append(command)
    
    def commandCheck(self, command):
        for command2 in this.command1:
            if(command == command2):
                return
                
    
    def tell(self,sender,recipient,message,time):
        self.s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " sent you a message at " + time + ": " + message + "\r\n", "UTF-8"))

    def msg(self,sender,recipient,message):
        self.s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " says: " + message + "\r\n", "UTF-8"))

bot = IRCbot()
bot.setBot(HOST,PORT,NICK,IDENT,REALNAME,MASTER,MASTAH,LOGS,CHANNEL)
bot.connect()
bot.logFolder()

while 1:
    bot.readbuffer = bot.readbuffer+bot.s.recv(512).decode("UTF-8")
    #be sure to check your log dir if using linux
    with open(bot.logs1 + "\\" + str(datetime.date.today())+".dat","a+") as f:
        f.write(str(datetime.datetime.now()) + " "+ bot.readbuffer)
    temp = str.split(bot.readbuffer, "\n")
    
    bot.readbuffer=temp.pop( )
    
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            bot.s.send(bytes("PONG " + line[1] + "\r\n", "UTF-8"))

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
                bot.msg(sender,sender,message)
            if(line[3] == ":!msg" and len(line) > 4):
                message = ''
                recipient = line[4]
                j = 5
                while j < len(line):
                    message += line[j]
                    message += ' '
                    j += 1
                bot.msg(sender,recipient,message)
            elif(line [3] == ":!quitNao" and len(line) == 4):
                if(sender == bot.master1 or sender == bot.mastah1):
                    bot.s.send(bytes("QUIT\r\n", "UTF-8"))
                    sys.exit()
            elif(line [3] == ":!poke" and len(line) == 4):
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " : \r\n", "UTF-8"))
            elif(line [3] == ":!roll20" and len(line) == 4):
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :" + str(random.randrange(1,20))+ "\r\n", "UTF-8"))
            elif(line [3] == ":!say" and len(line) >= 4):
                message = ''
                j = 4
                while j < len(line):
                    message += line[j]
                    message += ' '
                    j += 1
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :" + message + "\r\n", "UTF-8"))
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
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " : Number: " + str(rand[50]) + " ArraySize: " + str(len(rand)) + " Mean: " + str(mean) + ". StdDev: " + str(stdDev) + "\r\n", "UTF-8"))
            elif(line [3] == ":!flip" and len(line) == 4):
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " : (╯°□°)╯︵ ┻━┻\r\n", "UTF-8"))
            elif(line [3] == ":!ping" and len(line) == 4):
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :PONG!!! ┬─┬°o(^_^o)\r\n", "UTF-8"))
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
                    time = time.strftime("%c")
                    t = Timer(delaySec, bot.tell,[sender,recipient,message,time])
                    t.start();
                except ValueError:
                    bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n", "UTF-8"))
                except IndexError:
                    bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n", "UTF-8"))
            else:
                bot.s.send(bytes("PRIVMSG "+ bot.channel1 + " :command not recognized\r\n", "UTF-8"))
        for index, i in enumerate(line):
            print(line[index],index,len(line))
            
