#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
import re
import urllib

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

#CHANNEL = "#PBSIdeaChannel"
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
        self.s.send(bytes("NICK "+ self.nick1 + "\r\n"));
        self.s.send(bytes("USER "+ self.ident1 + " " + self.host1 + " " + self.realname1 + ":This is a bot thingy \r\n"))
        self.s.send(bytes("JOIN "+ self.channel1 + "\r\n"))
        self.s.send(bytes("PRIVMSG " + self.master1 + " :Hi Princess!\r\n"))
        
    def logFolder(self):
        try:
            os.makedirs(self.logs1)
        except OSError:
            if not os.path.isdir(self.logs1):
                raise
    
    def regCmd(self,command):
        self.commands.append(command)
        
    def tryCmd(command, line):
        if command.predicate(line):
            return command.success(line)
        else:
            return False

    def checkCmd(self, command):
        for command2 in this.command1:
            if this.tryCmd(command) != False:
                self.msg(command.success(line))
    
    def tell(self,sender,recipient,message,time):
        self.s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " sent you a message at " + time + ": " + message + "\r\n"))
        print("\n" + recipient + " - " + sender + " - " + time +" seconds from now: " + message + "\r")

    def msg(self,sender,recipient,message):
        self.s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " says: " + message + "\r\n"))
        print("\n" + recipient + " - " + sender + ": " + message + "\r")
        
    def msgCmd(self,sender,recipient,message):
        self.s.send(bytes("PRIVMSG "+ recipient + " :" + sender + " says: " + message + "\r\n"))

    def fruitLoops(self):
        while 1:
            self.readbuffer = self.readbuffer+self.s.recv(512).decode("UTF-8")
            #be sure to check your log dir if using linux
            with open(self.logs1 + "\\" + str(datetime.date.today())+".dat","a+") as f:
                f.write(str(datetime.datetime.now()) + " "+ self.readbuffer)
            fullLine = self.readbuffer
            
            msgText = fullLine.split(":")
            
            if(len(msgText) >= 3):
                msgText = msgText[2]

            temp = self.readbuffer.split("\n")
            self.readbuffer=temp.pop( )
                        
            for line in temp:
            
                line = line.rstrip()
                line = line.split()

                if(line[0] == "PING"):
                    self.s.send(bytes("PONG " + line[1] + "\r\n"))
                    print("\nSERVER PONG\r")
                
                if(line[1] == "PRIVMSG"):
                
                    line[3] = line[3][1:]
                    
                    for url in line:
                        if url.startswith("http") or url.startswith("www"):
                        
                            sock = urllib.urlopen(url)
                            urlSource = sock.read()
                            sock.close()
                            
                            if url.startswith("https://www.youtube.com/"):
                                urlContent = re.search("<title>(.*?)</title>",urlSource,re.IGNORECASE)
                                
                                if urlContent:
                                    print(urlContent.group(1)+"\r\n")
                                    self.s.send(bytes("PRIVMSG "+ self.channel1 + " :" + urlContent.group(1) + "\r\n"))
                                    
                            elif url.startswith("https://youtu.be/"):
                                urlContent = re.search("<title>(.*?)</title>",urlSource,re.IGNORECASE)
                                
                                if urlContent:
                                    print(urlContent.group(1)+"\r\n")
                                    self.s.send(bytes("PRIVMSG "+ self.channel1 + " :" + urlContent.group(1) + "\r\n"))
                                
                            else:
                            
                                urlContent = re.search("<meta name=\"keywords\" content=\"(.*?)\">",urlSource,re.IGNORECASE)
                                
                                if type(urlContent) == None:
                                    urlContent = re.search("<meta content=\"(.*?)\">",urlSource,re.IGNORECASE)
                                
                                if urlContent:
                                    print(urlContent.group(1)+"\r\n")
                                    self.s.send(bytes("PRIVMSG "+ self.channel1 + " :" + urlContent.group(1) + "\r\n"))

                    if(line[3].startswith('!')):
                    
                        sender = line[0][1:line[0].find('!')]
                                
                        if(line[3] == "!msgMe" and len(line) >= 4):
                            message = "OH HAI!"
                            if(len(line) > 4):
                                message = ''
                                j = 4
                                while j < len(line):
                                    message += line[j]
                                    message += ' '
                                    j += 1
                            self.msg(sender,sender,message)
                            
                        elif(line[3] == "!msg" and len(line) > 4):
                            message = ''
                            recipient = line[4]
                            j = 5
                            while j < len(line):
                                message += line[j]
                                message += ' '
                                j += 1
                            self.msg(sender,recipient,message)
                            
                        elif(line [3] == "!quitNao" and len(line) == 4):
                            if(sender == self.master1 or sender == self.mastah1):
                                self.s.send(bytes("QUIT\r\n"))
                                sys.exit()
                                
                        elif(line [3] == "!poke" and len(line) == 4):
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " : \r\n"))
                            
                        elif(line [3] == "!roll20" and len(line) == 4):
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " :" + str(random.randrange(1,20))+ "\r\n"))
                        
                        elif(line [3] == "!say" and len(line) >= 4):
                            message = ''
                            j = 4
                            while j < len(line):
                                message += line[j]
                                message += ' '
                                j += 1
                            
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " :" + message + "\r\n"))
                        
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
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " : Number: " + str(rand[50]) + " ArraySize: " + str(len(rand)) + " Mean: " + str(mean) + ". StdDev: " + str(stdDev) + "\r\n"))
                        
                        elif(line [3] == "!flip" and len(line) == 4):
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " : (╯°□°)╯︵ ┻━┻\r\n"))
                        
                        elif(line[3] == "!ping" and len(line) == 4):
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " : PONG!!! ┬─┬°o(^_^o)\r\n"))
                        
                        elif(line[3] == "!tell" and len(line) >= 7):
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
                                t = Timer(delaySec, self.tell,[sender,recipient,message,time])
                                t.start();
                            except ValueError:
                                self.s.send(bytes("PRIVMSG "+ self.channel1 + " : Syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n"))
                            except IndexError:
                                self.s.send(bytes("PRIVMSG "+ self.channel1 + " : Syntax -> !tell Nick delay(seconds) message1 message2 etc\r\n"))                    
                        
                        else:
                            self.s.send(bytes("PRIVMSG "+ self.channel1 + " : Command not recognized\r\n"))
                            
                print("\n")
                print(str(msgText) + "\r")
                for index, i in enumerate(line):
                    print(str(line[index]) +" "+ str(index) +" "+ str(len(line)) +" "+ "\r")
                    
            
bot = IRCbot()
bot.setBot(HOST,PORT,NICK,IDENT,REALNAME,MASTER,MASTAH,LOGS,CHANNEL)
bot.connect()
bot.fruitLoops()
