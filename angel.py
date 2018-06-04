#!/usr/bin/env python3
# -*- coding: UTF-8-*-
import socks,sys,os,getopt,time,re,requests,json
import threading
import math
proxies={
         'http':'socks5://127.0.0.1:9050',
         'https':'socks5://127.0.0.1:9050'}
die=False
### Func ###
def send(soc,value):
        soc.send(value.encode())
def recv(soc):
        return soc.recv(1024).decode()  
        
def privmsg(soc,target,msg):
        send(soc,"PRIVMSG "+target+' :'+msg+'\r\n')

def auth(soc,nick,ident,server,realname):
        send(soc,("USER " + nick + " " + nick + " " + nick + ": Name is Angel, I'm here to help\r\n"))
        data=recv(soc)
        send(soc,("NICK %s\r\n" % nick))
def join(soc,channel):
        print("[+] Join")
        channel='#'+channel
        while channel not in recv(soc):
                print("[+] Trying to join in: " + channel)
                send(soc,("JOIN " + channel + "\n"))
                data=recv(soc)
                print(data)
        print("[+] - Joined "+channel)
def convert_size(size_bytes):
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
def quote(url):
        from bs4 import BeautifulSoup
        try:
                r = requests.get(url,stream=True,headers={'user-agent':'w3m/0.52'}, timeout=5, proxies=proxies)
                data=''
                title=False
                for i in r.iter_content(chunk_size=512,decode_unicode=False):
                    data += i.decode('utf-8',errors='ignore')
                    if '</title>' in data.lower():
                        html = BeautifulSoup(data, 'html.parser')
                        try:title=html.title.text.strip()
                        except:pass
                        break
                    elif len(data) > 70000:
                        break
                retorna=title
        except Exception as error:
                print("Quote block-> Error:"+str(error))
                retorna="Sorry, i don't know wtf u are doing"
        return retorna
def getlist():
        print("[*] Updating")
        data=requests.get('https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty')
        return json.loads(data.text)

def getnews(soc,channel):
        global die
        print(die)
        last=000000
        channel="#"+channel
        while not die:
            new=getlist()[0]
            if last != new:
                print("[*] Reading the new")
                brutenew=requests.get("https://hacker-news.firebaseio.com/v0/item/"+str(new)+".json?print=pretty")
                newtosend=json.loads(brutenew.text)
                try:
                    if newtosend['url']:
                        privmsg(soc,channel,str(newtosend['title']+' >> '+newtosend['url']))
                    else:
                        continue
                except Exception as error:
                    print(error)
            last=new
            time.sleep(30)

def ping():
        print("[!] - Ping Receive")
        return ("PONG :pingis\n")
def help():
        msg="""Usage:
                -s  ->  IRC Server Address
                -p  ->  Server Port
                -n  ->  Bot NickName
                -i  ->  Bot Ident
                -R  ->  Bot Realname
                -c  ->  Channel
                -P  ->  Bot Password
                -h  ->  This.
                -N  ->  Don't use Onion proxy"""
        print(msg)
        sys.exit(0)
def main(argv):
    global die
    try:
        opts,args = getopt.getopt(argv, "s:p:n:i:R:P:c:hN")
        use_proxy=True
    except Exception as Error:
        print(Error)
        help()
    for opt, arg in opts:
        if opt == '-s':
            server = arg
        elif opt == '-p':
            port = arg
        elif opt == '-c':
            channel = arg
        elif opt == '-n':
            nick = arg
        elif opt == '-i':
            ident = arg
        elif opt == '-R':
            realname = arg
        elif opt == '-P':
            password = arg
        elif opt == '-h':
            help()
        elif opt == '-N':
            use_proxy=False
        else:
            help()
    print("[+] Socket")
    if use_proxy:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True) 
    soc = socks.socksocket()
    try:
            print("[+] Connection")
            soc.connect((server,int(port)))
    except Exception as error:
            print ("ERROR:", error)
    print("[*] Connected")
    auth(soc,nick,ident,server,realname)
    join(soc,channel)
    while True:
            data=recv(soc)
            print(data)
            if data.startswith("PING"):
                    send(soc,ping())
            try:
                    username=data.split('!')[0].strip(':')
                    origem=data.split('PRIVMSG')[1].split(' :')[0]
                    msg=data.split('PRIVMSG')[1].split(' :')[1]
                    print('Channel: '+origem+'> '+username+' :'+msg)
                    link=re.findall('([https:\/\/[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]?)',msg)
                    if link:
                        if '#' in origem:
                            privmsg(soc,origem, quote(link[0]))
                        else:
                            privmsg(soc,username,quote(link[0]))
                    if msg.startswith("bye"):
                        die=True
                        soc.close()
                        sys.exit(0)
                    elif msg.startswith('startnews'):
                        die=False
                        t = threading.Thread(target=getnews, args=(soc,channel))
                        t.start()
                    elif msg.startswith('stopnews'):
                        die=True
                    elif msg.startswith('key'):
                        privmsg(soc,origem,str('replace_me'))
                        
            except Exception as error:
                    print("Error: ", error)
                    print(data)
### Main ###
if __name__ == "__main__":
    main(sys.argv[1:])
