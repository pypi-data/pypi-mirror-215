import sys
import os
import flask
from configparser import ConfigParser as Inifile

currDir = os.getcwd()
cmds = [
	[
		"run",
		"[HOST] [PORT]",
		"Launches the scriptpak server, from ~/scripts/*.sp; if HOST is not given, defaults to 0.0.0.0, if PORT not specified, 8080 will be used, if PORT is not a number, exits with code 1"
	],
	[
		"help",
		None,
		"Displays this message."
	],
	[
		"vars",
		None,
		"Prints all variables from ~/scripts/##vars.ini; exits with code 1 if directory/variables not found or file format is incorrect"
	]
]

def prHelp():
	print("Usage:")
	print("python -m", __package__, "COMMAND [ARGS]\n")
	print("Available COMMANDs:")
	for cmdArr in cmds:
		print(cmdArr[0] + (" " + cmdArr[1] if str(cmdArr[1]) != "None" else "") + ":", " ".join(cmdArr[2:]))

def exProg(err):
	print(__package__ + f": error: {err}\n")
	prHelp()
	sys.exit(1)

def checkVar(file):
	if not os.path.isfile(file):
		exProg(f"{file} doesn't exist")
	cfg = Inifile()
	try:
		cfg.read(file)
	except:
		exProg(f"{file} is invalid")
	return cfg

args = sys.argv[1:]
if not bool(len(args)):
	exProg("unspecified command")
if args[0] == "help":
	prHelp()
if args[0] == "run":
	host = "0.0.0.0"
	port = "8080"
	if len(args) > 1:
		host = args[1]
		if len(args) > 2:
			port = args[2]
	scripDir = os.path.join(currDir, "scripts")
	if not os.path.isdir(scripDir):
		exProg(f"No directory found in {scripDir}")
	if not port.isdigit():
		exProg(f"invalid port \"{port}\"")
	port = int(port)
	app = flask.Flask(__name__)
	def launchFile(file):
		loc = os.path.join(scripDir, file)
		with open(loc, "rb") as fileIO:
			return fileIO.read().decode()
	if os.path.isfile(os.path.join(scripDir, "##index.sp")):
		def launchIndex():
			return launchFile("##index.sp")
		app.add_url_rule("/", view_func=launchIndex)
	app.run(host, port)
if args[0] == "vars":
	varDir = os.path.join(currDir, os.path.join("scripts", "##vars.ini"))
	cfg = checkVar(varDir)
	try:
		cfg["vars"]
	except:
		exProg(f"{varDir} is invalid")
	print(f"All variables from {varDir}:\n")
	for key in cfg["vars"]:
		print(key + ":", cfg["vars"][key])
	if len(cfg["vars"].keys()) == 0:
		print("No variables found")