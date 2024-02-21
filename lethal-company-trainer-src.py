from pymem import *
from pymem.process import *
import time
from win32api import GetKeyState
from os import system
import sys

system("title Lethal Company Simple Trainer")
PLAYER_CONTROLLER_BASE_OFFSET = 0x0072A200
PLAYER_CONTROLLER_OFFSETS = [0xF50,0x1F0,0x160,0x70,0xA0]
HEALTH_OFFSET = 0x59C
SPEED_OFFSET = 0x418
JUMP_OFFSET = 0x44C

DEFAULT_SPEED = 4.5999999
DEFAULT_JUMP = 13.0

try:
	pm = pymem.Pymem('Lethal Company.exe')
	print("[\033[1;32m+\033[0;0m] successfully attached to the game process")
except pymem.exception.ProcessNotFound:
	print("[\033[1;35mError\033[0;0m] can't find the game, is it started :) ?")
	sys.exit()

def ptr2Addr(base,offsets):
	address = pm.read_longlong(base)
	for i in offsets:
		if i != offsets[-1]:
				address = pm.read_longlong(address + i)
	return address + offsets[-1]

def main():
	PlayerModule = module_from_name(pm.process_handle,"mono-2.0-bdwgc.dll").lpBaseOfDll

	try:
		player = pm.read_longlong(ptr2Addr(PlayerModule + PLAYER_CONTROLLER_BASE_OFFSET,PLAYER_CONTROLLER_OFFSETS))
	except pymem.exception.MemoryReadError:
		print("[\033[1;35mError\033[0;0m] can't find the player, start again when you are in a level :)")
		sys.exit()
		
	print("[\033[1;32m+\033[0;0m] successfully found the player")
    
	godmode = 0
	speed = 0
	jump = 0
    
    
	run = True
	while run:
		if GetKeyState(0x70) < 0: #F1
			godmode = (godmode + 1) % 2
			print("godemode " + "\033[1;32menabled\033[0;0m"*godmode + "\033[1;35mdisabled\033[0;0m"*((godmode+1)%2))
			time.sleep(0.5)
			
		if GetKeyState(0x71) < 0: #F2
			speed = (speed + 1) % 2
			if speed:	pm.write_float(player + SPEED_OFFSET,10.0)
			else:	pm.write_float(player + SPEED_OFFSET,DEFAULT_SPEED)
			print("speed hack " + "\033[1;32menabled\033[0;0m"*speed + "\033[1;35mdisabled\033[0;0m"*((speed+1)%2))
			time.sleep(0.5)
			
		if GetKeyState(0x72) < 0: #F3
			jump = (jump + 1) % 2
			if jump:	pm.write_float(player + JUMP_OFFSET,50.0)
			else:	pm.write_float(player + JUMP_OFFSET,DEFAULT_JUMP)
			print("jump hack " + "\033[1;32menabled\033[0;0m"*jump + "\033[1;35mdisabled\033[0;0m"*((jump+1)%2))
			time.sleep(0.5)

		if godmode:
			pm.write_int(player + HEALTH_OFFSET,1000)
	
if __name__ == '__main__':
	main()
