#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import a_or_an


class Game(object):
    def __init__(self, player, a_map):
        self.player = player
        self.a_map = a_map

    def play(self):
        """event loop"""
        while True:
            print self.a_map.describe_room()
            raw_input("> ")
            a_map.move_to(1)


class Player(object):
    def __init__(self, gender, age, hair_color):
        self.gender = gender
        self.age = age
        self.hair_color = hair_color


class Map(object):
    def __init__(self, rooms):
        self.rooms = rooms
        self.start = 0
        self.location = self.start

    def describe_room(self, verbose=False):
        room = self.rooms[self.location]
        return room.describe(verbose)

    def possible_exits(self):
        if self.location+1 >= len(self.rooms):
            return []
        return [self.location+1]

    def move_to(self, next_room):
        self.location = next_room
        return self.rooms[self.location]


class Room(object):
    def __init__(self):
        self.about = ""
        self.name = self.__class__.__name__.replace("Room", "")
        if not self.name:
            self.name = ("Where am I? ...and what"
                         " am I doing in this handbasket?")
        self.items = []

        # the first time a room is visited, show the full description.
        # subsequent visits only show the room name and any items.
        self.first_time = True

    def add_item(self, item):
        self.items.append(item)

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
    hallway = HallwayRoom()
    guard = Guard('Guard 1')
    hallway.add_item(guard)
    a_map =  Map(rooms=[OutsideRoom(), hallway])
    player = Player(gender='female', age='74', hair_color='red')
    game = Game(player, a_map)
    game.play()
