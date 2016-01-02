#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import a_or_an


class UnknownCommand(Exception):
    pass


# dict of supported directions. key is the canonical direction
# name and the value is a list of aliases for that direction.
DIRECTIONS = {
    'north':     ['north',      'n'],
    'northeast': ['northeast', 'ne'],
    'northwest': ['northwest', 'nw'],
    'south':     ['south',      's'],
    'southeast': ['southeast', 'se'],
    'southwest': ['southwest', 'sw'],
    'east':      ['east',       'e'],
    'west':      ['west',       'w'],
    'up':        ['up',         'u'],
    'down':      ['down',       'd'],
    'in':        ['in',    'inside'],
    'out':       ['out',  'outside'],
    }


class Game(object):
    def __init__(self, player, rooms, script=None):
        self.player = player
        self.rooms = rooms

        if not self.player.location:
            if self.rooms:
                self.player.set_location(self.rooms[0])

        # list of commands used for testing
        self.script = script

    def play(self):
        """event loop"""
        while True:
            room = self.player.location
            if self.player.has_moved():
                print room.describe()

            try:
                action = self.next_action()
            except UnknownCommand:
                print "I don't understand.\n"
                continue

            if action == "quit":
                self.end()
                break

            elif action == "look":
                print room.describe(verbose=True)

            elif action in DIRECTIONS:
                new_room = room.move(action)
                if new_room:
                    self.player.set_location(new_room)
                else:
                    print "You can't go that way.\n"

            elif action == "help":
                self.help()

    def help(self):
        commands = '\n'.join(self.valid_commands())
        print "Valid commands are:\n%s" % commands

    def next_action(self):
        """
        fetch the next command from either the interactive user or a
        test script and return a canonical command.  skip any empty
        input.
        """
        while True:
            try:
                if self.script is not None:
                    action = self.script.pop(0)
                else:
                    action = raw_input("> ")
                if action:
                    return self.parse_action(action)
            except (EOFError, KeyboardInterrupt, IndexError):
                self.end()

    def parse_action(self, action):
        commands = self.valid_commands()

        try:
            return commands[action.lower()]
        except KeyError:
            raise UnknownCommand(action)

    def valid_commands(self):
        commands = {
            'quit': 'quit',
            'q':    'quit',
            'look': 'look',
            'l':    'look',
            'help': 'help',
            }

        for direction, aliases in DIRECTIONS.iteritems():
            for alias in aliases:
                commands.update({alias: direction})
                commands.update({direction: direction})
        return commands


    def end(self):
        print "\nGoodbye!\n"
        raise SystemExit()


class Player(object):
    def __init__(self, gender, age, hair_color):
        self.gender = gender
        self.age = age
        self.hair_color = hair_color
        self.location = None
        self.moved = True

    def has_moved(self):
        moved = self.moved
        self.moved = False
        return moved

    def set_location(self, location):
        self.location = location
        self.moved = True


class Room(object):
    def __init__(self):
        self.about = ""
        self.name = self.__class__.__name__.replace("Room", "")
        if not self.name:
            self.name = ("Where am I? ...and what"
                         " am I doing in this handbasket?")

        self.items = []

        # self.exits is a dict where the key is the direction of the
        # exit and the value is the room object that the exit leads to.
        # only directions listed in DIRECTIONS are allowed.
        self.exits = dict()

        # the first time a room is visited, show the full description.
        # subsequent visits only show the room name and any items.
        self.first_time = True

    def add_item(self, item):
        self.items.append(item)

    def add_exit(self, exit, room):
        direction = self.normalize_direction(exit)
        if not direction:
            raise ValueError("invalid direction: %s" % exit)
        self.exits[direction] = room

    def possible_exits(self):
        return self.exits.keys()

    def move(self, direction):
        direction = self.normalize_direction(direction)
        return self.exits.get(direction)

    def normalize_direction(self, alias):
        for direction, aliases in DIRECTIONS.iteritems():
            if alias.lower() in aliases:
                return direction
        return None

    def show_items(self):
        if not self.items:
            return ""
        return  "Items at this location:\n%s " % '\n'.join(
                '%s' % i for i in self.items
                )

    def describe(self, verbose=False):
        if self.first_time or verbose:
            self.first_time = False
            return self.name + '\n' + self.about + '\n\n' + self.show_items()
        else:
            return self.name + '\n' + self.show_items()


class OutsideRoom(Room):
    def __init__(self):
        super(OutsideRoom, self).__init__()
        self.about = ("You are standing outside the museum with"
                      " only a rock, a grappling hook, and a gun.")


class HallwayRoom(Room):
    def __init__(self):
        super(HallwayRoom, self).__init__()
        self.about = ("You have landed in a hallway with beautiful"
                      " art hanging on the walls. But you have your"
                      " eyes on a bigger prize.")


class Item(object):
    def __init__(self, name, desc=None):
       self.name = name
       self.desc = desc
       if self.desc is None:
           self.desc = "It's just %s..." % a_or_an(self.name)

    def __str__(self):
        return self.name

    def say(self):
        return '...'


class Guard(Item):
    def __init__(self, name, desc=None):
        super(Guard, self).__init__(name, desc)
        self.commands = ['Stop']

    def say(self):
        return self.commands[0]


if __name__ == "__main__":
    # initialize rooms
    outside = OutsideRoom()

    hallway = HallwayRoom()
    guard = Guard('Guard 1')
    hallway.add_item(guard)

    # connect rooms
    outside.add_exit("in", hallway)
    hallway.add_exit("out", outside)

    # initialize game and play
    player = Player(gender='female', age='74', hair_color='red')
    game = Game(player, rooms=[outside, hallway])
    game.play()
