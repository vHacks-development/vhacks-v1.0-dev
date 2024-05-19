import os
import sys 
import time
import json
import requests
import faker
import random
import base64
import shutil

from faker import Faker
from datetime import datetime
from getpass import getpass

sys.path.append(os.path.abspath("assets/script"))
import core
import script


def prompt(email, server):
	os.system("clear")
	
	mysqlCursor = core.mysqlConn.cursor()
	mysqlCursor.execute("SELECT * FROM app_vhacks_{} WHERE email='{}'".format(server, email))
	mysqlData = mysqlCursor.fetchone()
	
	print("                                                                        ]")
	print("\033[A        [ vhacks 1.0-dev")
	print("                                                                        ]")
	print("\033[A+ -- --=[ Your IPv4: {} (Don't share your IPv4)".format(mysqlData[4]))
	print("                                                                        ]")
	print("\033[A+ -- --=[ {} Hacking - Level {} ({}/{}) - {} Balance".format(mysqlData[7], core.getLevel(mysqlData[6]), mysqlData[6], core.getCountExp(core.getLevel(mysqlData[6])), core.convert(mysqlData[5])))

def main(server = core.getServer):
	os.system("clear")
	core.printv("[*] Menjalankan vhacks v1.0 ...")
	core.printv("[*] Memeriksa sesi ...")
	while True:
		if os.path.exists("data/session"):
			if os.path.exists("data/session/profile.json"):
				try:
					profileData = json.loads(open("data/session/profile.json", "r").read())
					
					email = base64.b64decode(base64.b64decode(profileData["email"]))
					password = base64.b64decode(base64.b64decode(profileData["password"]))
					server = base64.b64decode(base64.b64decode(profileData["server"]))
					
					mysqlCursor = core.mysqlConn.cursor()
					mysqlCursor.execute("SELECT * FROM app_vhacks_{}".format(server))
					mysqlData = mysqlCursor.fetchall()
					
					if email in str(mysqlData):
						mysqlCursor = core.mysqlConn.cursor()
						mysqlCursor.execute("SELECT * FROM app_vhacks_{} WHERE email='{}'".format(server, email))
						mysqlData = mysqlCursor.fetchone()
						
						if password == mysqlData[3]:
							prompt(email, server)
							break
						else:
							core.printv("[*] Data tidak ditemukan")
							os.remove("data/session/profile.json")
					else:
						core.printv("[*] Data tidak ditemukan")
						os.remove("data/session/profile.json")
				except TypeError:
					core.printv("[*] Data tidak ditemukan")
					os.remove("data/session/profile.json")
			else:
				try:
					os.system("clear")
					core.printv("\t[ L O G - I N ]")
					server = raw_input("\n[?] Server [1/2/3]: ")
					email = raw_input("[?] Email: ")
					
					mysqlCursor = core.mysqlConn.cursor()
					mysqlCursor.execute("SELECT * FROM app_vhacks_{}".format(server))
					mysqlData = mysqlCursor.fetchall()
					
					if email in str(mysqlData):
						password = getpass("[?] Password: ")
						
						mysqlCursor = core.mysqlConn.cursor()
						mysqlCursor.execute("SELECT * FROM app_vhacks_{} WHERE email='{}'".format(server, email))
						mysqlData = mysqlCursor.fetchone()
						
						if password == base64.b64decode(mysqlData[3]):
							open("data/session/profile.json", "w").write(json.dumps({
								"email": base64.b64encode(base64.b64encode(mysqlData[2])),
								"password": base64.b64encode(base64.b64encode(mysqlData[3])),
								"server": base64.b64encode(base64.b64encode(server))
							}, indent=2))
							
						else:
							core.printv("[*] Kata sandi salah")
					else:
						core.printv("[*] Email tidak terdaftar")
				except KeyboardInterrupt:
					os.rmdir("data/session")
		else:
			try:
				os.system("clear")
				core.printv("\t[ R E G I S T E R ]\n")
				email = raw_input("[?] Email: ")
				
				mysqlQuery = "SELECT * FROM app_vhacks_{}".format(server)
				mysqlCursor = core.mysqlConn.cursor()
				mysqlCursor.execute(mysqlQuery)
				mysqlData = mysqlCursor.fetchall()
				
				if email in str(mysqlData):
					core.printv("[*] Email telah terdaftar")
				else:
					password = getpass("[?] New Password: ")
					if len(password) > 8:
						
						mysqlQuery = "INSERT INTO app_vhacks_{} (guid, email, password, ipv4) VALUES ('{}', '{}', '{}', '{}')".format(server, core.getGuid, email, password, core.getIpv4)
						mysqlCursor = core.mysqlConn.cursor()
						mysqlCursor.execute(mysqlQuery)
						core.mysqlConn.commit()
						
						os.mkdir("data/session")
						open("data/session/profile.json", "w").write(json.dumps({
							"email": base64.b64encode(base64.b64encode(email)),
							"password": base64.b64encode(base64.b64encode(password)),
							"server": base64.b64encode(base64.b64encode(server))
						}, indent=2))
						core.printv("[*] Berhasil membuat akun")
						prompt(email, server)
						break
					else:
						core.printv("[*] Password anda belum aman")
			except KeyboardInterrupt:
				os.mkdir("data/session")
main()