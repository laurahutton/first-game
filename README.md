# first-game
Game I am working on -- also first repository!

#jewel thief - break window from outside, pick the right room (guard in wrong ones)
#find the hidden safe under the desk - break the code
#fight guards and run out
from sys import exit
from random import randint
import my_game_opening

def Compass(object):
	#lists all the rooms in flow order
	Rooms = {
		Failure(): 'failure',
		Outside(): 'outside',
		Hallway(): 'hallway',
		Office(): 'office',
		Hallway2(): 'hallway_2',
		Finished(): 'finished',
	}
	
def Map(Room):
	#gets the game moving from room to room
	def __init__(self, Rooms):
		self.Rooms = Rooms
	

	
def Failure(Room):
	death = {
		"Some art theif you are",
		"More like international fail-er!",
		"Whomp, whomp, whOoOomp",
		}
	
def Outside(Room):
	
	beginning = input('my_game_opening')
	print beginning
	print "You are standing out the museum with only a rock, a grappling hook, and a gun."
	print "What do you do?\n"
	
	get_in = raw_input("> ")
	
	if "throw" and "rock" in get_in:
		print "\nYou throw the rock you have into the nearest window."
		print "The window shatters causing the museum's alarm to go off."
		print "Immidetaly guards rush out and surround you."
		print "Before you have to chance to run they lift their guns and fire."
		return 'failure'
		
	if "throw" and "hook" in get_in:
		print "\nYou pull out your grappling hook and begin whipping it around your head."
		print "You walk over to where you can see a good latching point the building."
		print "You release the hook and hear the satisfying 'clink' of it latching on."
		print "After checking the tighteness of the latching you begin climbing up."
		print "Within 15 minutes you have it to the top and begin looking for an entry point."
		print "You see a vent and take the rope from your grappling hook to begin lowering"
		print "yourself down."
		return 'hallway'
		
	if "gun" in get_in:
		print "\nYou pull out your gun and examine it."
		print "It's nothing special - just enough to get the job done if you are caught."
		print "You return it to your inventory."
		return 'get_in'

def Hallway(Room):
	print "\nNext room"
	#pat on the back for getting the game to play though
	print "You did it, Laura!"

def Office(Room):
	pass
	
def Hallway2(Room):
	pass
	
def Finished(obejct):
	pass
	
play.game()
