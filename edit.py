#!/usr/bin/env python3
print("Begining Load")
import ev3dev.ev3 as ev3
import os
import time as t
from curses import *
from curses.panel import *
print("Load Finished")

#oh hi, you peeked to the code
#well you should be rewarded somehow
#It's dangerous to go alone.
#Take this:

#-----<Config section>-----------

HiddenFiles = True

keyboard = "Keyboard"

path = "/home/robot/"

inputPoll = 0.2

inputCycle = 0.2

errt = 4

#----</Config section>-----------

button = ev3.Button()
content = []
fname = ""
sy = 0
sx = 0
cy = 0
cx = 0
ay = 0
ax = 0
ky = 0
kx = 0
pky = 0
pkx = 0
m = 0
pm = 0
screen = 0 
error = ""
longest = 0	
CapsLock = False
Shift = False
Symbol = False							#20
Append = False
tempAppend = False

#0 = loading in terminal
#1 = filechoosing in curses
#2 = fileedit
#3 = keyboard  


def fload(filename):
	global content
	global fname
	try:
        	file = open(path + "/" + filename, "r")
	except IOError as e:
		global error
		error = e.strerror
		return False
	else:
		fname = filename
		content = []
		temp = file.readlines()
		for line in temp:
			content.append(line.rstrip("\n")) 	
		file.close()
		return True

def fwrite():
	global content
	global fname
	try:
		file = open(path + "/" + fname, "w")#!!!
	except IOError as e:
		global error
		error = e.strerror
		return False
	else:	
		file.write("\n".join(content))
		file.close()
		return True

def dload(dirname = "."):
	global dir
	tdir = 0
	try:							#40
		tdir = os.listdir(path + "/" + dirname)
	except IOError as e:
		global error
		error = e.strerror
		return False
	else:
		dir = tdir
		dir = hideNames(dir)
		dir.insert(0, "..")
		return True

def hideNames(dir):
	global HiddenFiles
	if HiddenFiles:
		hidden = []
		for name in dir:
			if(name[0] == "."):
				hidden.append(name)
		for name in hidden:
			dir.remove(name)
	return dir

def dirorfile(name):
	if(os.path.isdir(path + "/" + name)):
		return "<d>"
	if(os.path.isfile(path + "/" + name)):
		return "<f>"						#60
	return "<?>"

def uplong(strlist):
	global longest
	i = 0
	for s in strlist:
		if(len(s) > i):
			i = len(s)
	longest = i

def select(entry):
	global path
	if(os.path.isdir(path + "/" + entry + "/")):
		if(not dload(entry)):
			errup()
			return 
		path = path + "/" + entry + "/"
		path = os.path.abspath(path)
		return 
	if(os.path.isfile(path + "/" + entry)):
		if(not fload(entry)):					#80
			errup()
			return
		s1rel()
		s2dep()
		return 
	global error
	error = "Unknown type of file"
	errup()
	

def up():
	global sy
	global sx
	global cy
	global cx
	global ay
	global ax
	global longest
	if(screen == 1):
		
		if(len(dir)> 20):
			if(cy < 0 and sy == 0):
				cy = 19
				sy = len(dir)-20
			if(cy > 19 and sy == len(dir)-20):
				cy = 0
				sy = 0
		else:
			if(cy > len(dir)-1):
				cy = 0
			if(cy < 0):
				cy = len(dir)-1
		if(cy < 2 and sy > 0):
			sy-=1
			cy+=1
		if(cy > 16 and sy < len(dir)-20):
			sy+=1
			cy-=1
		if(longest > 39):	
			if(cx < 0):
				cx = longest-39
			if(cx > longest-39):
				cx = 0
		else:
			cx = 0
		
		browser.move(ay,0)
		typepad.move(ay,0)
		typepad.chgat(-1, A_NORMAL)
		browser.chgat(-1, A_NORMAL)
		ay = cy + sy
		typepad.move(ay,0)
		browser.move(ay,0)
		typepad.chgat(-1, A_REVERSE)
		browser.chgat(-1, A_REVERSE)
		typepad.refresh(sy, 0, 1, 0, 20, 3)	
		browser.refresh(sy, cx, 1, 4 ,20,43)
		if(len(path)>44):
			pathpad.refresh(0, len(path)-44, 0,0,1,43)
		else:
			pathpad.refresh(0, 0, 0, 0, 1, 43)
		
		#update_panels()
		#doupdate()
	
	if(screen == 2):
		#manage wraparound
		if(len(content) > 21):
			if(cy < 0 and sy == 0):
				cy = 20
				sy = len(content)-21
			if(cy > 20 and sy == len(content)-21):
				cy = 0
				sy = 0
		else:
			if(cy > len(content)-1):
				cy = 0
			if(cy < 0):
				cy = len(content)-1
		if(longest > 40):
			if(cx < 0 and sx == 0):
				cx = 39
				sx = longest-40
			if(cx > 39 and sx == longest-40):
				cx = 0
				sx = 0
		else:
			if(cx > longest):
				cx = 0
			if(cx < 0):
				cx = longest
		
		#manage scrolling
		if(cy < 2 and sy > 0):
			sy-=1
			cy+=1
		if(cy > 16 and sy < len(content)-21):
			sy+=1
			cy-=1
		if(cx < 5 and sx > 0):
			sx-=1
			cx+=1
		if(cx > 35 and sx < longest-40):
			sx+=1
			cx-=1
		
		#manage cursor position
		textpad.move(ay,ax)
		textpad.chgat(1, A_NORMAL)
		ay = cy + sy
		ax = cx + sx
		textpad.move(ay, ax)
		textpad.chgat(1, A_REVERSE)
		
		#manage pad position
		indexer.refresh(sy, 0, 0, 0, 20, 3)
		textpad.refresh(sy, sx, 0, 4, 20, 43)
	if(screen == 3):
		global ky
		global kx
		global pky
		global pkx
		if(not ((pkx == 0 and pky == 1 and CapsLock) or (pkx == 0 and pky == 2 and Shift) or (pkx == 0 and pky == 3 and Symbol) or (pkx == 10 and pky == 2 and Append))):
			cap = keyCaps(pky, pkx)
			KArem(pky, cap[0], cap[1])
		cap = keyCaps(ky, kx)
		KAset(ky, cap[0], cap[1])
		pky = ky
		pkx = kx
			
		
		board.refresh(0,0,17,0,20,43)
		#manage custom cursors for a keyboard.
	if(screen == 4):
		global m
		global pm
		if(m < 0):
			m=3
		if(m > 3):
			m=0
		menu.move(pm,0)
		menu.chgat(-1, A_NORMAL)
		pm = m
		menu.move(m, 0)
		menu.chgat(-1, A_REVERSE)
		menu.refresh(0,0, 17, 0, 20,43)

def sup():
	if(screen == 1):
		global sy
		global cy
		global ay
		sy = 0
		cy = 0
		ay = 0
		uplong(dir)
		pathpad.resize(1, len(path)+1)
		typepad.resize(len(dir), 4)	
		browser.resize(len(dir), longest+1)
		pathpad.clear()
		typepad.clear()
		browser.clear()
		stdscr.clear()
		for i, line in enumerate(dir):
			browser.move(i, 0)
			browser.addstr(line)
			typepad.move(i, 0)
			typepad.addstr(dirorfile(line))
		pathpad.attron(A_UNDERLINE)
		pathpad.move(0,0)
		pathpad.addstr(path)
		pathpad.attroff(A_UNDERLINE)
		update_panels()
		doupdate()
	if(screen == 2):
		uplong(content)
		#resize windows to fit contet
		indexer.resize(len(content)+1, 5)
		textpad.resize(len(content)+1, longest+1)
		indexer.clear()
		textpad.clear()
		stdscr.clear()
		for i, line in enumerate(content):
			indexer.move(i, 0)
			indexer.addstr("---|")
			indexer.move(i, 0)
			indexer.addstr(str(i))
			textpad.move(i, 0)
			textpad.addstr(line)
		update_panels()
		doupdate()
	if(screen == 3):  
		#cautious here
		global cable
		cable = keyboardNewCable()
		board.clear()
		board.move(0,0)
		board.addstr(keyboardStorage())
		cap = keyCaps(1, 0)#grabbin' CAPL
		if(CapsLock):
			KAset(1, cap[0], cap[1])
		else:
			KArem(1, cap[0], cap[1])
		cap = keyCaps(2, 0)#grabbin' SHIFT
		if(Shift):
			KAset(2, cap[0], cap[1])
		else:
			KArem(2, cap[0], cap[1])
		cap = keyCaps(3, 0)#grabbin' SYMBOL
		if(Symbol):
			KAset(3, cap[0], cap[1])
		else:
			KArem(3, cap[0], cap[1])
		cap = keyCaps(2, 10)#grabbin' ++
		if(Append):
			KAset(2, cap[0], cap[1])
		else:
			KArem(2, cap[0], cap[1])
		#update the cable 
		#make the keyboard visible 
	if(screen == 4):
		global m
		m = 3 
		menu.clear
		menu.move(0,0)
		menu.addstr("| Exit to Brickman                         |\n| Overwrite the file (Save)                |\n| Exit to fs                               |\n| Close the menu                           |")


def KAset(y, x, l=1):
	board.chgat(y, x, l, A_REVERSE)

def KArem(y, x, l=1):
	board.chgat(y, x, l, A_NORMAL)

def menuselect():
	global m
	global run
	global screen
	global error
	if(m == 0):
		#exit to brickman
		s4rel()
		s3rel()
		s2rel()
		screen = 0
		uncurse()
		run=False
	if(m == 1):
		#overwrite the file (save)
		if(fwrite()):
			error = "File Successfully Saved"
			errup()
		else:
			errup()
		screen = 2
		up()
		screen = 4
		up()
	if(m == 2):
		#exit to fs
		s4rel()
		s3rel()
		s2rel()
		s1dep()
		sup()
		up()
	if(m == 3):
		#close the menu
		s4rel()
		screen = 2
		sup()
		up()
		screen = 3
		sup()
		up()

	

def keyselect(code):
	global cx
	global cy
	global tempAppend
	if(code[0] == "/"):
		command(code[1])
	else:
		addtocontent(code)
	global screen
	if(screen == 3):
		if(Append or tempAppend):
			screen = 2
			sup()
			up()
			screen = 3
			sup()
			up()
			if(tempAppend):
				tempAppend = False
		else:
			s3rel()
			screen = 2
			sup()
			up()
	



#analyze commands
#command list
#/T INSERT TAB (\t)                     
#/C Toggle CapsLock
#/S Toggle Shift
#/F Toggle Symbol
#/B insert backspace
#/E execute inserting new line. also move text after cu$
#/U cy-=1
#/D cy+=1
#/L cx-=1
#/R cx+=1
#/A Toggle Append
#/O screen=4
#// figure out how to jump it through this
#/X completly ignore this command

def command(code):
	global CapsLock
	global Shift
	global Symbol
	global Append
	global tempAppend
	global cy
	global cx
	global content
	if(code == "X"):
		return
	if(code == "C"):
		CapsLock = not CapsLock
		tempAppend = True
	if(code == "S"):
		Shift = not Shift
		tempAppend = True
	if(code == "F"):
		Symbol = not Symbol
		tempAppend = True
	if(code == "A"):
		Append = not Append
	if(code == "U"):
		cy-=1
		tempAppend = True
	if(code == "D"):
		cy+=1
		tempAppend = True
	if(code == "L"):
		cx-=1
		tempAppend = True
	if(code == "R"):
		cx+=1
		tempAppend = True
	if(code == "/"):
		addtocontent("/")
	if(code == "T"):
		addtocontent("\t")
	if(code == "B"):
		if(cx == 0):
			if(cy != 0):
				toedit1=content[ay-1]
				toedit2=content[ay]
				edited = toedit1 + toedit2
				content[ay-1] = edited
				content.pop(ay)
				cx = len(toedit1)
				cy -= 1
		else:
			toedit=content[ay]
			edited = toedit[:ax-1] + toedit[ax:]
			content[ay] = edited
			cx-=1
	if(code == "E"):
		toedit = content[ay]
		tonewline = toedit[ax:]
		edited = toedit[:ax]
		content[ay] = edited
		content.insert(ay+1, tonewline)
		cx = 0
		cy += 1 
	if(code == "O"):
		s4dep()
		
	
def addtocontent(code):
	global cx
	global Shift
	toedit = content[ay]
	edited = toedit[:ax] + code + toedit[ax:]

	content[ay] = edited
	cx+=1
	if(Shift):
		Shift = False
	


def keyjump(code):
	""" 
	key()
	0 = choose
	1 = up
	2 = down
	3 = left
	4 = right
	"""
	global ky
	global kx
	global cable
	if(code == 0):
		keyselect(cable[ky][kx])
		return
	if(code == 1):
		if(ky == 3 and kx == 1):#the space situation 2
			kx = 4	
			ky = 2
			return
		if(ky == 3 and kx > 1):#keypad situation 1
			kx = 9
			ky = 2
			return
		ky-=1#normal situation
		if(ky<0):
			ky = 3#wraparound
			kx = 1
		return
	if(code == 2):
		if(ky == 0 and kx == 11):#backspace situation
			kx = 10
			ky = 1
			return
		if(ky == 2 and kx > 0 and kx < 8):#the space situation 1
			kx = 1
			ky = 3
			return
		if(ky == 2 and kx > 7):#magic due to space
			ky = 3
			kx -= 6
			return
		if(ky == 3 and ( kx == 2 or kx == 4 )):#Keypad situation 4
			kx = 3
			return
		ky+=1#normal situation
		if(ky>3):
			ky = 0#wraparound
			kx = 4
		return
	if(code == 3):
		if(ky == 2 and kx == 10): #over keypad situation 1
			kx = 8
			return
		if(ky == 3 and kx == 4):
			kx = 2
			return
		if(ky == 2 and kx == 9):#Keypad Situation 2
			ky = 3
			kx = 2
			return
		kx-=1#normal situation
		if(kx < 0):
			if(ky == 0):
				kx = 11
			elif(ky == 3):#wraparound
				kx = 4
			else:
				kx = 10
		return
	if(code == 4):
		if(ky == 2 and kx == 8):#OVER KEYPAD SITUATION 2
			kx = 10
			return
		if(ky == 3 and kx == 2):
			kx = 4
			return
		if(ky == 2 and kx == 9):#KEYPAD SITUATION 3
			ky = 3
			kx = 4
			return
		kx+=1#normal situation 
		if(ky == 0):
			if(kx > 11):
				kx = 0
		elif(ky == 3):
			if(kx > 4):	#wraparound	
				kx = 0
		else:
			if(kx > 10):
				kx = 0
		return

def errup():
	global error
	errowin = newwin(7, 34, 7, 6)
	erropnl = new_panel(errowin)
	errowin.box()
	errowin.move(3, 5)
	errowin.addstr(error)
	erropnl.show()
	error = ""
	update_panels()
	doupdate()
	t.sleep(errt)
	errowin.clear()
	erropnl.hide()
	update_panels()
	doupdate()
	up()

def curse():
	global stdscr
	global stdpnl
	stdscr=initscr() #Screen just got cursed
	stdpnl = new_panel(stdscr)
	
def uncurse():
	global stdpnl
	del stdpnl
	endwin()
	print("Curse removed")

def s1dep():
	global browser
	global typepad
	global pathpad
	global screen
	browser = newpad(1,1)
	typepad = newpad(1,1)
	pathpad = newpad(1,1)
	curs_set(0)
	screen = 1
	dload()
	sup()
	up()

def s1rel():
	global browser
	global typepad
	global pathpad
	del browser
	del typepad
	del pathpad

def s2dep():
	global indexer
	global textpad
	global screen
	global cy
	global cx
	global sy
	global sx
	global ay
	global ax
	cy = 0
	cx = 0
	sy = 0
	sx = 0
	ay = 0
	ax = 0
	indexer = newpad(1,5)
	textpad = newpad(1,1)
	curs_set(2)
	screen = 2
	sup()
	up()

def s2rel():
	global indexer
	global textpad
	del indexer
	del textpad

def s3dep():
	global board
	global screen
	board = newpad(5, 45)
	curs_set(0)
	screen = 3

def s3rel():
	global board
	del board

def s4dep():
	global menu
	global screen
	menu = newpad(5, 45)
	screen = 4

def s4rel():
	global menu
	del menu






















def keyboardStorage():
	global keyboard
	global CapsLock
	global Shift
	global Symbol
	big = Shift or CapsLock
	if(keyboard == "Keyboard"):		
		if(Symbol):
			if(big):
				return "|[TAB] !  @  #  $  %  ^  &  *  (  ) [BCKSP]|\n|[CAPL] x  x  x  \'  \"  <  >  [  ]  [ENTER] |\n|[SHIFT] x  x  x  `  :  {  } [fs] [/\\] [++]|\n|[SYMBOL] [________________] [<-] [\\/] [->]|"
			else:
				return "|[Tab] 1  2  3  4  5  6  7  8  9  0 [Bcksp]|\n|[CapL] x  x  ~  ?  =  -  _  |  \\  [Enter] |\n|[Shift] x  x  ;  ,  .  +  / [fs] [/\\] [++]|\n|[Symbol] [________________] [<-] [\\/] [->]|"
		else:
			if(big):
				return "|[TAB] Q  W  E  R  T  Y  U  I  O  P [BCKSP]|\n|[CAPL] A  S  D  F  G  H  J  K  L  [ENTER] |\n|[SHIFT] Z  X  C  V  B  N  M [fs] [/\\] [++]|\n|[SYMBOL] [________________] [<-] [\\/] [->]|"
			else:
				return "|[Tab] q  w  e  r  t  y  u  i  o  p [Bcksp]|\n|[CapL] a  s  d  f  g  h  j  k  l  [Enter] |\n|[Shift] z  x  c  v  b  n  m [fs] [/\\] [++]|\n|[Symbol] [________________] [<-] [\\/] [->]|"
	if(keyboard == "Memeboard"):
		if(Symbol):
			if(big):
				return "|[Dab] !  @  #  $  %  ^  &  *  (  ) [<--]  |\n|[CaBL] x  x  x  \'  \"  <  >  [  ]  [<__/ ] |\n|[$H|FT] x  x  x  `  :  {  } [F4] [/\\] [REEE\n|[~(^^)~] [_A_BAR_IN_SPACE_] [<<] [\\/] [>>]|"
			else:
				return "|[Dab] 1  2  3  4  5  6  7  8  9  0 [<--]  |\n|[CaBL] x  x  ~  ?  =  -  _  |  \\  [<__/ ] |\n|[$H|FT] x  x  ;  ,  .  +  / [F4] [/\\] [REEE\n|[~(^^)~] [_A_BAR_IN_SPACE_] [<<] [\\/] [>>]|"
		else:
			if(big):
				return "|[Dab] Q  W  E  R  T  Y  U  I  O  P [<--]  |\n|[CaBL] A  S  D  F  G  H  J  K  L  [<__/ ] |\n|[$H|FT] Z  X  C  V  B  N  M [F4] [/\\] [REEE\n|[~(^^)~] [_A_BAR_IN_SPACE_] [<<] [\\/] [>>]|"
			else: 
				return "|[Dab] q  w  e  r  t  y  u  i  o  p [<--]  |\n|[CaBL] a  s  d  f  g  h  j  k  l  [<__/ ] |\n|[$H|FT] z  x  c  v  b  n  m [F4] [/\\] [REEE\n|[~(^^)~] [_A_BAR_IN_SPACE_] [<<] [\\/] [>>]|"
	if(keyboard == "Proboard"):
		if(Symbol):
			if(big):
				return "|[/T ] !  @  #  $  %  ^  &  *  (  ) [/B   ]|\n|[/C  ] x  x  x  \'  \"  <  >  [  ]  [/E   ] |\n|[/S   ] x  x  x  `  :  {  } [/O] [/U] [/A]|\n|[/F    ] [                ] [/L] [/D] [/R]|"
			else:
				return "|[/T ] 1  2  3  4  5  6  7  8  9  0 [/B   ]|\n|[/C  ] x  x  ~  ?  =  -  _  |  \\  [/E   ] |\n|[/S   ] x  x  ;  ,  .  +  / [/O] [/U] [/A]|\n|[/F    ] [                ] [/L] [/D] [/R]|"
		else:
			if(big):
				return "|[/T ] Q  W  E  R  T  Y  U  I  O  P [/B   ]|\n|[/C  ] A  S  D  F  G  H  J  K  L  [/E   ] |\n|[/S   ] Z  X  C  V  B  N  M [/O] [/U] [/A]|\n|[/F    ] [                ] [/L] [/D] [/R]|"
			else: 
				return "|[/T ] q  w  e  r  t  y  u  i  o  p [/B   ]|\n|[/C  ] a  s  d  f  g  h  j  k  l  [/E   ] |\n|[/S   ] z  x  c  v  b  n  m [/O] [/U] [/A]|\n|[/F    ] [                ] [/L] [/D] [/R]|"
	return "|[   ] x  x  x  x  x  x  x  x  x  x [     ]|\n|[    ] x  x  x  x  x  x  x  x  x  [     ] |\n|[     ] x  x  x  x  x  x  x [  ] [  ] [  ]|\n|[      ] [                ] [  ] [  ] [  ]|"

def keyboardNewCable():
	global CapsLock
	global Shift
	global Symbol
	big = Shift or CapsLock
	if(Symbol):
		if(big):
			return [["/T","!","@","#","$","%","^","&","*","(",")","/B"],["/C","/X","/X","/X","\'","\"","<",">","[","]","/E"],["/S","/X","/X","/X","`",":","{","}","/O","/U","/A"],["/F"," ","/L","/D","/R"]] 
		else:
			return [["/T","1","2","3","4","5","6","7","8","9","0","/B"],["/C","/X","/X","~","?","=","-","_","|","\\","/E"],["/S","/X","/X",";",",",".","{","}","/O","/U","/A"],["/F"," ","/L","/D","/R"]]
	else:
		if(big):
			return [["/T","Q","W","E","R","T","Y","U","I","O","P","/B"],["/C","A","S","D","F","G","H","J","K","L","/E"],["/S","Z","X","C","V","B","N","M","/O","/U","/A"],["/F"," ","/L","/D","/R"]]
		else:
			return [["/T","q","w","e","r","t","y","u","i","o","p","/B"],["/C","a","s","d","f","g","h","j","k","l","/E"],["/S","z","x","c","v","b","n","m","/O","/U","/A"],["/F"," ","/L","/D","/R"]]

def keyCaps(y,x):
	caps = [[[1,5],[7,1],[10,1],[13,1],[16,1],[19,1],[22,1],[25,1],[28,1],[31,1],[34,1],[36,7]],[[1,6],[8,1],[11,1],[14,1],[17,1],[20,1],[23,1],[26,1],[29,1],[32,1],[35,7]],[[1,7],[9,1],[12,1],[15,1],[18,1],[21,1],[24,1],[27,1],[29,4],[34,4],[39,4]],[[1,8],[10,18],[29,4],[34,4],[39,4]]]
	return caps[y][x]


#   config creation
#   and loading
#   The starting menu 
# settings menu(config overwriting)

#additional functions:
#	cp	-also for dir
#	rm	-also for dir
#	mkdir
#	term	-just keyboard on bash wrapper
#	edit 	-will be the name of default mode
#	mkfile	-not sure 











curse()
s1dep()
run = True
while(run):
	t.sleep(inputCycle)
	while(not button.any()):
		t.sleep(inputPoll)
	if(button.backspace):
		run = False
		if(screen == 1):
			s1rel()
		if(screen == 2):
			s2rel()
		uncurse()
	if(button.up):
		if(screen == 3):
			keyjump(1)
		elif(screen == 4):
			m -=1
		else:
			cy -= 1
		up()

	if(button.down):
		if(screen == 3):
			keyjump(2)
		elif(screen == 4):
			m +=1
		else:
			cy += 1
		up()
	if(button.left):
		if(screen == 3):
			keyjump(3)
		elif(screen != 4):
			cx -= 1
		up()
	if(button.right):
		if(screen == 3):
			keyjump(4)
		elif(screen != 4):
			cx += 1
		up()
	if(button.enter):
		if(screen == 1):
			select(dir[ay])
		elif(screen == 2):
			s3dep()
		elif(screen == 3):
			keyjump(0)
		elif(screen == 4):
			menuselect()
		sup()
		up()


""" 
key()
0 = choose
1 = up
2 = down
3 = left
4 = right

"""

t.sleep(2)
