from asyncio.windows_events import NULL
import mysql.connector
import requests
import os
import psutil as psu
from pyinjector import inject
import time
import subprocess
from urllib import request as rq
from discord_webhook import DiscordWebhook, DiscordEmbed
import zipfile
import socket




allowedServers = ['metin2007.bin', 'metin2007.exe', 'test3']
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
hardwareid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
hostname = socket.gethostname()

def animka(tekstm,ile):

    bar = [
        "[|]",
        "[/]",
        "[-]",
        "[\]",
        "[|]"
    ]
    i = 0

    while i < ile:
        print(bar[i % len(bar)], tekstm,end="\r")
        time.sleep(.2)
        i += 1
    clearConsole()

def Login():
    global u,p
    os.system('color 3')
    # animka('Connecting to Server', 55)
    u = input("Login : ")
    p = input("Password : ")
    if(checkLogin(u, p)):
        clearConsole()
        # animka("Logging In", 20)
        downloadDepedencies('maindll', NULL)
        logDiscord('login_webhook', 'Uzytkownik - ' + u + 'pomyslnie sie zalogowal \nHWID : ' + hardwareid)
        injectMenu()
    else:
        print('[-] Wrong Username or Password')
        Login()

def logDiscord(_type, _data):
    global u,p
    if(_type == 'login_success'):
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/964869128735314010/-MixBIFYEZuktOfhrHQNzv6eUcBNmaTdOGAKmNxDUdxsTg-aqJmrj1xmWX92FIS52NJw", username="New Webhook Username")

        embed = DiscordEmbed(
            color='03b2f8'
        )
        embed.set_author(
            name="M2BOT.net - Login Logs",
            url="https://m2bot.net",
            icon_url="https://imgur.com/8JcdnbS.png",
        )
        embed.set_footer(text="Made by neuh#2321")
        embed.set_timestamp()
        embed.add_embed_field(name="Username", value=u)
        embed.add_embed_field(name="Password", value=p)
        embed.add_embed_field(name="HWID", value=hardwareid, inline=False)
        embed.add_embed_field(name="Hostname", value=hostname, inline=False)

        webhook.add_embed(embed)
        response = webhook.execute()    

def downloadDepedencies(_type, _path):
    if(_type == 'maindll'):
        downloadDLL('https://megawrzuta.pl/files/aa75b3131caf2bf3e5cccebf0ce5f14a.dll', NULL, 'neuh.dll')
    if(_type == 'dmg'):
        downloadDLL('https://megawrzuta.pl/files/a6e06a831d3a881738c29523d806e14f.zip', NULL, 'dmg.zip')
        with zipfile.ZipFile('dmg.zip', 'r') as zip_ref:
           zip_ref.extractall(_path)
        downloadDLL("https://megawrzuta.pl/files/aae784599a330622c9634bf4160b4428.zip", NULL, 'a.zip')
        with zipfile.ZipFile('a.zip', 'r') as zip_ref:
            zip_ref.extractall(_path + r'\lib')
        os.remove('dmg.zip')
        os.remove('a.zip')



def injectMenu():
    pathMT2 = input('Path to MT2 : ')
    downloadDepedencies('dmg', pathMT2)
    proccessName = input("Proccess Name : ")
    if(proccessName != NULL):
        if(isAllowed(proccessName)):
            if(getPID(proccessName)):
                animka('Injecting', 30)
                injectPID(getPID(proccessName))
                os.remove(pathMT2 + r'\lib\mini2.py')
            else:
                quit()
        

def injectPID(pid):
    inject(pid, 'neuh.dll') 
    closeEXE()

def closeEXE():
    for x in range(5):
        print('[+] Successfully Injected, closing in', x)
        time.sleep(1)
        if(x == 5):
            quit()


def getPID(pname):
    for proc in psu.process_iter():
        if(pname in proc.name()):
            return proc.pid


def isAllowed(name):
    for x in allowedServers:
        if(name == x):
            return 1

def downloadDLL(dlink, _path, name):
    downloaded_obj = requests.get(dlink)
    with open(name, "wb") as file:
      file.write(downloaded_obj.content)
    if(_path != NULL):
        subprocess.call("MOVE /-Y %s %s" % (name, _path), shell=True)


def checkLogin(uname, passwd):
    if(uname and passwd != NULL):

        currDB = mysql.connector.connect(
        host = "DATABASE_IP",
        user = "DATABASE_USERNAME",
        password = "DATABASE_PASSWORD",
        database = "DATABASE_NAME"
        )

        newCursor = currDB.cursor()

        newCursor.execute("SELECT username, pass FROM users WHERE username = %s AND pass = %s", (uname, passwd))

        newResult = newCursor.fetchall()

        for x in newResult:
            if(x != NULL):
                return 1
            else:
                return 0

Login()
