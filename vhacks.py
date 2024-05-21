#!/bin/python2
#coding: utf-8

import os
import sys 
import time
import json
import requests
import faker
import random
import base64
import shutil
import mysql.connector

from faker import Faker
from datetime import datetime
from getpass import getpass

sys.path.append(os.path.abspath("assets/script"))
import core
import script

def helpPage():
	print("")
	print("Core Command")
	print("=============")
	print("")
	print("")
	print("\tCommands                Description")
	print("\t---------               ------------")
	print("\t?                       Help menu")
	print("\tbanner                  Display an awesome vhacks banner")
	print("\tclear                   Clean the screen")
	print("\texit                    Exit the program")
	print("\thelp                    Help menu")
	print("\tlogout                  Log out of your account")
	print("\tinstall                 Installing viruses")
	print("")
	
def hackingHelpPage():
	print("")
	print("Hacking Command")
	print("================")
	print("")
	print("")
	print("\tCommands                Description")
	print("\t---------               ------------")
	print("\tlogout                  Log out of target account")
	print("\tput                     Puts the virus on the target")
	print("\ttransfer                Send balance to your account")

def listVirus():
	print("")
	print("Viruses")
	print("========")
	print("")
	print("")
	print("\tName                    Description")
	print("\t-----                   ------------")
	print("\tspyware                 Memantau data target")

def hackPrompt(myIpv4, targetIpv4):
	while True:
		console = raw_input("\nvhconsole > {} > ".format(targetIpv4)).split()
		if console[0] == "logout":
			core.printv("[{}] log out".format(datetime.now().strftime(core.getStrftime)))
			break
		elif console[0] == "?" or console[0] == "help":
			hackingHelpPage()
		else:
			core.printv("[{}] Perintah tidak ditemukan".format(datetime.now().strftime(core.getStrftime)))

def prompt(email, server):
	banner = random.choice([core.banner1, core.banner2, core.banner3, core.banner4, core.banner5])
	os.system("clear")
	mysqlData = core.mysqlFetchone(server, email)
	print(banner)
	print("                                                                        ]")
	print("\033[A        [ vhacks 1.0-dev")
	print("                                                                        ]")
	print("\033[A+ -- --=[ Your IPv4: {} (Don't share your IPv4)".format(mysqlData[4]))
	print("                                                                        ]")
	print("\033[A+ -- --=[ {} Hacking - Level {} ({}/{}) - {} Balance".format(mysqlData[7], core.getLevel(mysqlData[6]), mysqlData[6], core.getCountExp(core.getLevel(mysqlData[6])), core.convert(mysqlData[5])))
	while True:
		mysqlData = core.mysqlFetchone(server, email)
		try:
			console = raw_input("\nvhconsole > ").split()
			if console[0] == "?" or console[0] == "help":
				helpPage()
			elif console[0] == "banner":
				return prompt(email, server)
			elif console[0] == "clear":
				os.system("clear")
			elif console[0] == "logout":
				logout = raw_input("[?] Ingin melanjutkan keluar? [Y/n]: ")
				if logout == "Y" or logout == "y":
					os.remove("data/session/profile.json")
					break
				elif logout == "N" or logout == "n":
					core.printv("[{}] Logout canceled".format(datetime.now().strftime(core.getStrftime)))
			elif console[0] == "install":
				try:
					if console[1] == "spyware":
						i = raw_input("[?] Gunakan $10.000 untuk memasang {}? [Y/n]: ".format(console[1]))
						if i == "Y" or i == "y":
							mysqlData = core.mysqlFetchone(server, email)
							if mysqlData[5] >= 10000:
								core.printv("\n[{}] Installing spyware ...".format(datetime.now().strftime(core.getStrftime)))
								core.installing("spyware")
								core.mysqlSQL("UPDATE app_vhacks_{} SET balance='{}', spyware='{}' WHERE email='{}'".format(server, mysqlData[5]-10000, mysqlData[10]+1, email))
								core.printv("[{}] Spyware installed".format(datetime.now().strftime(core.getStrftime)))
							else:
								core.printv("[{}] Saldo anda kurang".format(datetime.now().strftime(core.getStrftime)))
						elif i == "N" or i == "n":
							core.printv("[{}] Install spyware canceled".format(datetime.now().strftime(core.getStrftime)))
					else:
						listVirus()
				except IndexError:
					core.printv("usage: install <viruses name>")
					listVirus()
			elif console[0] == "exit":
				core.printv("[-] Exit the program")
				sys.exit()
			elif console[0] == "hack":
				mysqlData = core.mysqlFetchone(server, email)
				try:
					if console[1] == mysqlData[4]:
						core.printv("[{}] Tidak bisa meretas data anda sendiri".format(datetime.now().strftime(core.getStrftime)))
					else:
						core.printv("\nScanning data {} ...".format(console[1]))
						mysqlDataAll = core.mysqlFetchall(server)
						if console[1] in str(mysqlDataAll):
							core.scanningData(server, console[1])
							targetMysqlData = core.mysqlFetchone(server, console[1])
							if mysqlData[8] >= targetMysqlData[7]:
								hackPrompt(mysqlData[4], console[1])
							else:
								core.printv("[{}] Tolong tingkatkan bypasser anda".format(datetime.now().strftime(core.getStrftime)))
						else:
							core.printv("[{}] Ipv4 target tidak ditemukan".format(datetime.now().strftime(core.getStrftime)))
				except IndexError:
					core.printv("usage: hack <ipv4 target>")
			else:
				core.printv("[{}] Perintah tidak ada".format(datetime.now().strftime(core.getStrftime)))
		except KeyboardInterrupt:
			break
		except IndexError:
			helpPage()

def main(server = random.choice(core.getServer)):
	os.system("clear")
	core.printv("[*] Menjalankan vhacks v1.0 ...")
	core.printv("[*] Memeriksa sesi ...")
	while True:
		server = random.choice(core.getServer)
		if os.path.exists("data/session"):
			if os.path.exists("data/session/profile.json"):
				try:
					profileData = json.loads(open("data/session/profile.json", "r").read())
					email = profileData["email"]
					password = profileData["password"]
					server = profileData["server"]
					mysqlData = core.mysqlFetchall(server)
					if email in str(mysqlData):
						mysqlData = core.mysqlFetchone(server, email)
						if password == mysqlData[3]:
							prompt(email, server)
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
					print("")
					print("")
					print("[1] Server One           Users ({}/200)".format(core.getUserCount("server_one")))
					print("[2] Server Two           Users ({}/200)".format(core.getUserCount("server_two")))
					print("[3] Server Three         Users ({}/200)".format(core.getUserCount("server_three")))
					server = raw_input("\n[?] Choice Server [1/2/3]: ")
					if server == "1":
						server = "server_one"
						mysqlData = core.mysqlFetchall(server)
						email = raw_input("[?] Email: ")
						if email in str(mysqlData):
							password = getpass("[?] Password: ")
							mysqlData = core.mysqlFetchone(server, email)
							if password == mysqlData[3]:
								open("data/session/profile.json", "w").write(json.dumps({
									"email": mysqlData[2],
									"password": mysqlData[3],
									"server": server
								}, indent=2))
							else:
								core.printv("[*] Kata sandi salah")
						else:
							core.printv("[*] Email tidak terdaftar")
					elif server == "2":
						server = "server_two"
						mysqlData = core.mysqlFetchall(server)
						email = raw_input("[?] Email: ")
						if email in str(mysqlData):
							password = getpass("[?] Password: ")
							mysqlData = core.mysqlFetchone(server, email)
							if password == mysqlData[3]:
								open("data/session/profile.json", "w").write(json.dumps({
									"email": mysqlData[2],
									"password": mysqlData[3],
									"server": server
								}, indent=2))
							else:
								core.printv("[*] Kata sandi salah")
						else:
							core.printv("[*] Email tidak terdaftar")
					elif server == "3":
						server = "server_three"
						mysqlData = core.mysqlFetchall(server)
						email = raw_input("[?] Email: ")
						if email in str(mysqlData):
							password = getpass("[?] Password: ")
							mysqlData = core.mysqlFetchone(server, email)
							if password == mysqlData[3]:
								open("data/session/profile.json", "w").write(json.dumps({
									"email": mysqlData[2],
									"password": mysqlData[3],
									"server": server
								}, indent=2))
							else:
								core.printv("[*] Kata sandi salah")
						else:
							core.printv("[*] Email tidak terdaftar")
					else:
						core.printv("[{}] Server tidak tersedia".format(datetime.now().strftime(core.getStrftime)))
				except KeyboardInterrupt:
					os.rmdir("data/session")
		else:
			try:
				os.system("clear")
				core.printv("\t[ R E G I S T E R ]\n")
				email = raw_input("[?] Email: ")
				mysqlData = core.mysqlFetchall(server)
				if email in str(mysqlData):
					core.printv("[*] Email telah terdaftar")
				else:
					password = getpass("[?] New Password: ")
					if len(password) > 8:
						core.mysqlSQL("INSERT INTO app_vhacks_{} (guid, email, password, ipv4) VALUES ('{}', '{}', '{}', '{}')".format(server, core.getGuid, email, password, core.getIpv4))
						os.mkdir("data/session")
						open("data/session/profile.json", "w").write(json.dumps({
							"email": email,
							"password": password,
							"server": server
						}, indent=2))
						core.printv("[*] Berhasil membuat akun")
						prompt(email, server)
					else:
						core.printv("[*] Password anda belum aman")
			except KeyboardInterrupt:
				os.mkdir("data/session")
main()