import sys
import threading
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="template", static_folder="static")

from classes.Team import Team
from classes.Service import Service
from classes.Game import Game

##########Services##########

from services import ropeman
from services import nadmozg
from services import piratemap
from services import ropeman
from services import blackgold
from services import sharing
from services import hanoifones
from services import FHMMaintenance
from services import hacker_diary
from services import santamachine
from services import jokes
from services import n4w_secrets
from services import dungeon
from services import gdps
from services import pizza1337
from services import simpleCalc
from services import rpncalc
from services import poemwriter
from services import killing_as_a_service
from services import ATM_machine
from services import temperature
from services import spiderman
from services import tattletale

#######End of services########

@app.route("/")
def renderIndex():
	return render_template("index.html", teamList = teamList, teamListStatus = teamListStatus)

@app.route("/sendFlag")
def renderSendFlag():
	return render_template("sendFlag.html", teamList = teamList, serviceList = serviceList)

@app.route("/getFlagID")
def renderGetFlagID():
	return render_template("getFlagID.html", teamList = teamList, serviceList = serviceList)

@app.route('/submit', methods=['POST'])
def submitFlag():
	flag = request.form.get('flag', None)
	team_name = request.form.get('team', None)
	service_name = request.form.get('service', None)
	status = game.submitFlags(team_name, service_name, flag)
	return status

@app.route('/flagid', methods=['GET'])
def getFlagID():
	username = request.args.get('enemy_name')
	service_name = request.args.get('service')
	flagid = game.getFlagID(service_name, username)
	return str(flagid)

def routine():
	game.setFlags(teamListStatus)
	game.getFlags()
	game.updateLog()
	threading.Timer(300, routine).start()

if __name__ == "__main__":

	teamList = {"CrunchyFan": Team("CrunchyFan", "10.7.40.2", "mario.png"),
				"UmamiPad": Team("UmamiPad", "10.7.40.3", "luigi.png")
				}
	
	serviceList = {	'nadmozg': Service('nadmozg', '20077', nadmozg),
					'piratemap': Service('piratemap', '20048', piratemap),
					'FHMMaintenance': Service('FHMMaintenance', '20011', FHMMaintenance),
					'ropeman': Service('ropeman', '20029', ropeman),
					'blackgold': Service('blackgold', '20076', blackgold),
					'sharing': Service('sharing', '20075', sharing),
					'hanoifones': Service('hanoifones', '20050', hanoifones),
					'hacker_diary': Service('hacker_diary', '20030', hacker_diary),
					'santamachine': Service('santamachine', '20073', santamachine),
					'jokes': Service('jokes', '20136', jokes),
					'n4w_secrets': Service('n4w_secrets', '20120', n4w_secrets),
					'dungeon': Service('dungeon', '20100', dungeon),
					'pizza1337': Service('pizza1337', '20140', pizza1337),
					'simpleCalc': Service('simpleCalc', '20056', simpleCalc),
					'rpncalc': Service('rpncalc', '20009', rpncalc),
					'poemwriter': Service('poemwriter', '20026', poemwriter),
					'killing_as_a_service': Service('killing_as_a_service', '20113', killing_as_a_service),
					'ATM_machine': Service('ATM_machine', '20061', ATM_machine),
					'gdps': Service('gdps', '20037',gdps),
					'temperature': Service('temperature', '25096',temperature),
					'spiderman': Service('spiderman', '30000',spiderman),
					'tattletale': Service('tattletale', '13007',tattletale)
	}

	teamListStatus = { }
	for teamName, team in teamList.iteritems():
		serviceListStatus = { }
		for serviceName, service in serviceList.iteritems():
			serviceListStatus[serviceName] = "Down"
		teamListStatus[teamName] = serviceListStatus

	honeypotList = {'poemwriter','gdps'}

	game = Game(teamList, serviceList, honeypotList)
	
	newGame = 0
	for arg in sys.argv:
		if arg == "-n":
			newGame = 1
	if newGame:
		game.resetLog()
	else:
		game.restoreLog()
	
	threading.Timer(2, routine).start()
	app.run(host = "0.0.0.0")
