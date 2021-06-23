#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      stanl
#
# Created:     11/01/2021
# Copyright:   (c) stanl 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import scrapy
import re
import json
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.exceptions import CloseSpider
import tkinter
import urllib.parse
from datetime import date
import Utilities


import matplotlib.pyplot as plt
import numpy as np

global p_players
global p_new
p_players=['5t4n1582','pilky980','zonatii','pops risk','loots please']
global p_new
p_new=[]



#global recentlookupdata
#global currentplayer

#recentlookupdata=""
#currentplayer=""

class persondata:
    def __init__(self,Name):
        self.Name=Name
        self.Total=[[],
                    []]

class Graph:
    def __init__(self):
        #print(os.listdir("logs/"))

        self.player_data=[]

        global p_players
        for i in range(len(p_players)):
            self.player_data.append(persondata(p_players[i]))


        for file in os.listdir("logs/"):
            try:
                with open( "logs/"+ file  ,"r") as fd:
                    holder=fd.read()
                    now=Utilities.LineMatrix(holder)

                    for i in range(len(p_players)):
                        for j in range(len(now)):
                            if(now[j]==p_players[i]):
                                #print("here")
                                for k in range(len(self.player_data)):
                                    if(now[j]==self.player_data[k].Name):
                                        self.player_data[k].Total[0].append(file[:len(file)-4])
                                        self.player_data[k].Total[1].append(int(now[j+1]))

            except:
                print ("e")
        for i in range(len(p_players)):
            print(self.player_data[i].Total)
            if(self.player_data[i].Name=='5t4n1582'):
                plt.plot(self.player_data[i].Total[0], self.player_data[i].Total[1], label = self.player_data[i].Name)
            if(self.player_data[i].Name=='pilky980'):
                plt.plot(self.player_data[i].Total[0], self.player_data[i].Total[1], label = self.player_data[i].Name)
        plt.legend()
        plt.show()
class display:
    def __init__(self,players):
        self.players=players
        self.app=tkinter.Tk()
        self.app.title('Game')
        size=str(75+225*len(players))+"x"+"660"
        self.app.geometry(size)

        self.process = CrawlerProcess()
        self.process.crawl(Spider,players)#can have arguments
        self.process.start()
        for i in range(len(self.players)):
            self.players[i].ConstructData()
        self.draw_stats()

    def creategraph(self):
        G=Graph()

    def create(self):
        global p_new
        players=[]
        for i in range(len(p_new)):
            players.append(player(p_new[i]))
        self.process.stop()
        new_window=display(players)



    def addp(self,string):
        global p_new
        for i in range(len(p_new)):
            if(p_new[i]==string):
                p_new.pop(i)
                return
        p_new.append(string)

    def createnew(self):
        global p_players
        global p_new
        self.makeapp=tkinter.Tk()
        self.makeapp.title('options')
        self.makeapp.geometry("150x200")
        self.buttons=[]
        for i in range(len(p_players)):
            x=tkinter.Checkbutton(self.makeapp, text=p_players[i],command=lambda j=i:self.addp(p_players[j]))
            x.pack()
            self.buttons.append(x)
        print(self.buttons)

        go=tkinter.Button(self.makeapp,text="Go",command=lambda:self.create())
        go.pack()



    def logging(self):

        try:
            f = open("Logs/"+str(date.today())+".txt", "a")
            readf = open("Logs/"+str(date.today())+".txt", "r")
        except:
            pass
        readfstring=readf.read()
        thestring=""
        for i in range(len(self.players)):
            if self.players[i].Name not in readfstring:
                thestring=thestring+self.players[i].Name+"\n"
                for k in range(len(self.players[i].Stats)):
                    thestring=thestring+self.players[i].Stats[k]+"\n"
        f.write(thestring)
        f.close()


    def draw_stats(self):

        holder_array=[]

        newhold=[""]
        for i in range(len(self.players)):
            newhold.append(" ")
            newhold.append(self.players[i].Name)
            newhold.append(" ")
        holder_array.append(newhold)

        newhold=[""]
        for i in range(len(self.players)):
            newhold.append("Rank")
            newhold.append("Stats")
            newhold.append("Xp")
        holder_array.append(newhold)

        skill=["Total","Attack","Defence","Strength","Hitpoints","Ranged","Prayer","Magic","Cooking",
        "Woodcutting","Fletching","Fishing","Firemaking","Crafting","Smithing","Mining","Herblore","Agility",
        "Thieving","Slayer","Farming","Runecraft","Hunter","Construction",
        "Clues(all)","Clues(beginner)","Clues(easy)","Clues(medium)",
        "Clues(hard)","Clues(elite)","Clues(master)"]

        for i in range(24):
            newhold=[skill[i]]
            for j in range(len(self.players)):
                newhold.append(self.players[j].Rank[i])

                #--------------------calculating position-----------------
                pos=len(self.players)
                for k in range(len(self.players)):
                    one=self.players[j].Stats[i]
                    two=self.players[k].Stats[i]
                    if(int(one)==int(two)):
                        one1=self.players[j].Xp[i]
                        two1=self.players[k].Xp[i]
                        if(int(one1)>int(two1)):
                            pos=pos-1
                            continue
                    if(int(one)>int(two)):
                        pos=pos-1
                        continue

                #--------------------------------------------------------

                newhold.append(self.players[j].Stats[i]+"("+str(pos)+")")
                newhold.append(self.players[j].Xp[i])
            holder_array.append(newhold)

        newhold=[""]
        for i in range(7):
            newhold=[skill[i+24]]
            for k in range(len(self.players)):

                #--------------------calculating position-----------------
                pos=len(self.players)
                for p in range(len(self.players)):
                    one=self.players[k].Cluesscore[i]
                    two=self.players[p].Cluesscore[i]
                    if(int(one)>int(two)):
                        pos=pos-1

                #--------------------------------------------------------

                newhold.append(self.players[k].Cluesrank[i])
                newhold.append(self.players[k].Cluesscore[i]+"("+str(pos)+")")
                newhold.append("")
            holder_array.append(newhold)

        for i in range(len(holder_array)):
            for j in range(len(holder_array[0])):
                if(j>0):
                    if((j+1)%3==0):
                        hold=holder_array[i][j]
                        if("(1)" in hold):
                            self.e = tkinter.Entry(self.app, width=10,bg='green', fg='black',font=('Arial',10,'bold'))
                            self.e.grid(row=i, column=j)
                            self.e.insert("end", holder_array[i][j])
                            continue
                self.e = tkinter.Entry(self.app, width=10, fg='black',font=('Arial',10,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert("end", holder_array[i][j])
        self.logging()


        self.menubar = tkinter.Menu(self.app)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.createnew)
        self.filemenu.add_command(label="Graph", command=self.creategraph)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.app.config(menu=self.menubar)


class Spider(scrapy.Spider):
    name = "topic1"
    allowed_domains = ['runescape.com']

    def __init__(self,players):
        self.players=players

    def start_requests(self):
        urls=[]
        for i in range(len(self.players)):
            urls.append('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='+self.players[i].Name)
        #urls = ['https://towardsdatascience.com/how-to-extract-online-data-using-python-8d072f522d86']
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)
        #raise CloseSpider('bandwidth_exceeded')

    def parse(self, response):
        pop1=urllib.parse.urlparse(response.url)
        hold0=str(pop1.query)
        hold1=hold0[7:]
        hold2=str(hold1)
        if "%20" in hold2:
            hold3=hold2.replace("%20"," ")
            hold2=hold3
        name=hold2
        links = response.xpath('/html/body').extract()
        for i in range(len(self.players)):
            if(self.players[i].Name==name):
                self.players[i].Data=links[0]


class player:
    def __init__(self,Name):
        self.Name=Name
        self.Rank=[]
        self.Stats=[]
        self.Xp=[]
        self.Data=""
        self.Cluesrank=[]
        self.Cluesscore=[]

    def ConstructData(self):
        holder=self.Data[9:len(self.Data)-8]

        commaindex=[0]
        commas=True
        while(commas):
            commaindex.append(holder.find(",",commaindex[-1]+1,len(holder)))
            if(holder.find(",",commaindex[-1]+1,len(holder))==-1):
                commas=False

        lineindex=[-1]
        lines=True
        while(lines):
            lineindex.append(holder.find("\n",lineindex[-1]+2,len(holder)))
            if(holder.find("\n",lineindex[-1]+2,len(holder))==-1):
                lines=False

        skill_len=24

        for i in range(skill_len):
            self.Rank.append(holder[lineindex[i]+1:commaindex[2*i+1]])
            self.Stats.append(holder[commaindex[2*i+1]+1:commaindex[2*i+2]])
            self.Xp.append(holder[commaindex[2*i+2]+1:lineindex[i+1]])

        clue_len=7

        for i in range(clue_len):
            self.Cluesrank.append(holder[lineindex[i+27]+1:commaindex[i+1+51]])
            self.Cluesscore.append(holder[commaindex[i+1+51]+1:lineindex[i+27+1]])



def main():
    players=[]
    players.append(player('5t4n1582'))
    players.append(player('pilky980'))
    players.append(player('zonatii'))
    players.append(player('pops risk'))
    #players.append(player('loots please'))

    new_window=display(players)

if __name__ == '__main__':
    main()

tkinter.mainloop()