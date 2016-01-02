#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
import sys
import unittest

from game import (
        Game, Player, OutsideRoom, Item, Guard, HallwayRoom, Room,
        UnknownCommand,
        )


class TestGame(unittest.TestCase):
    def setUp(self):
        super(TestGame, self).setUp()
        self.player = Player(gender='male', age='10', hair_color='blue')
        self.game = Game(self.player, rooms=[OutsideRoom()])

    def tearDown(self):
        super(TestGame, self).tearDown()

    def test_instantiate_game(self):
        game = Game(self.player, rooms=[])
        self.assertEqual(game.player, self.player)
        self.assertEqual(game.rooms, [])

    def test_room_traversal(self):
        start_room = OutsideRoom()
        end_room = HallwayRoom()

        start_room.add_exit("north", end_room)

        end_room.add_item(Item('feather'))

        self.assertIn(start_room.about, start_room.describe())
        self.assertTrue(start_room.describe().startswith(start_room.name))

        possible_exits = start_room.possible_exits()
        new_room = start_room.move(possible_exits[0])
        self.assertIsInstance(new_room, Room)
        self.assertEqual(new_room.about, end_room.about)
        self.assertIn(end_room.about, new_room.describe())
        self.assertIn('feather', new_room.describe())

        possible_exits = new_room.possible_exits()
        self.assertEqual(possible_exits, [])

    def test_parse_action_direction(self):
        self.assertEqual(self.game.parse_action("ne"), "northeast")

    def test_parse_action_command(self):
        self.assertEqual(self.game.parse_action("q"), "quit")

    def test_parse_action_unknown_command(self):
        self.assertRaises(UnknownCommand, self.game.parse_action, "-invalid-")


class TestScript(unittest.TestCase):
    def setUp(self):
        super(TestScript, self).setUp()
        self.player = Player(gender='male', age='10', hair_color='blue')

        # capture stdout from game loop
        self.stdout = StringIO.StringIO()
        self._orig_stdout = sys.stdout
        sys.stdout = self.stdout

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

        self.game = Game(
            player,
            rooms=[outside, hallway],
            script=['quit']
            )

    def tearDown(self):
        sys.stdout = self._orig_stdout
        super(TestScript, self).tearDown()

    def test_script(self):
        self.assertRaises(SystemExit, self.game.play)

        output = self.stdout.getvalue()
        self.assertIn("Outside", output)
        self.assertIn("Goodbye!", output)

    def test_script_invalid_command(self):
        self.game.script = ['-invalid-']
        self.assertRaises(SystemExit, self.game.play)
        self.assertIn("I don't understand", self.stdout.getvalue())

    def test_script_1(self):
        self.game.script = ['in', 'q']
        self.assertRaises(SystemExit, self.game.play)

        output = self.stdout.getvalue()
        self.assertTrue(output.startswith("Outside"))
        self.assertIn("Hallway", output)
        self.assertIn("Guard 1", output)

        self.assertEqual(self.game.player.location, self.game.rooms[1])


class TestPlayer(unittest.TestCase):
    def test_player(self):
        player = Player(gender='male', age='10', hair_color='blue')
        self.assertEqual(player.gender, 'male')
        self.assertEqual(player.age, '10')
        self.assertEqual(player.hair_color, 'blue')

    def test_has_moved(self):
        player = Player(gender='male', age='10', hair_color='blue')

        # initially, the player starts off by having been "moved" to a
        # new location
        self.assertTrue(player.moved)

        self.assertTrue(player.has_moved())

        # after checking for a move, the flag is reset
        self.assertFalse(player.moved)

    def test_set_location(self):
        """
        test that set_location() sets the location and the moved flag
        """
        hallway = HallwayRoom()
        player = Player(gender='male', age='10', hair_color='blue')

        # the player is initiated without a location
        self.assertIsNone(player.location)

        player.set_location(hallway)

        self.assertEqual(player.location, hallway)
        self.assertTrue(player.moved)


class TestRooms(unittest.TestCase):
    def test_outside(self):
        outside = OutsideRoom()
        self.assertGreater(outside.about, 0)
        self.assertIsInstance(outside.items, list)

    def test_add_item(self):
        rock = Item('rock')
        room = Room()
        before = len(room.items)
        self.assertNotIn(rock, room.items)
        room.add_item(rock)
        self.assertEqual(len(room.items), before+1)
        self.assertIn(rock, room.items)

    def test_show_items(self):
        room = Room()
        room.items = [Item('rock'), Item('egg'), Item('gun')]
        self.assertIn('rock', room.show_items())
        self.assertIn('egg', room.show_items())
        self.assertIn('gun', room.show_items())

    def test_show_no_items(self):
        room = Room()
        room.items = []
        self.assertEqual(room.show_items(), '')

    def test_hallway(self):
        hallway = HallwayRoom()
        self.assertGreater(hallway.about, 0)
        self.assertIsInstance(hallway.items, list)

    def test_hallway_guard(self):
        hallway = HallwayRoom()
        guard = Guard('Guard 1')
        before = len(hallway.items)
        self.assertNotIn(guard, hallway.items)
        hallway.add_item(guard)
        self.assertEqual(len(hallway.items), before+1)
        self.assertIn(guard, hallway.items)

    def test_describe(self):
        hallway = HallwayRoom()
        self.assertIn(hallway.about, hallway.describe())

        # after the first visit, the description is omitted
        self.assertNotIn(hallway.about, hallway.describe())

        # full description can be shown again if requested
        self.assertIn(hallway.about, hallway.describe(verbose=True))

    def test_add_exit(self):
        hallway = HallwayRoom()
        outside = OutsideRoom()

        before = len(hallway.exits)
        self.assertNotIn("north", hallway.exits)

        hallway.add_exit("north", outside)

        self.assertEqual(len(hallway.exits), before+1)
        self.assertIn("north", hallway.exits)
        self.assertEqual(hallway.exits["north"], outside)

    def test_add_exit_by_alias(self):
        hallway = HallwayRoom()
        outside = OutsideRoom()

        before = len(hallway.exits)
        self.assertNotIn("northwest", hallway.exits)

        hallway.add_exit("nw", outside)

        self.assertEqual(len(hallway.exits), before+1)
        self.assertIn("northwest", hallway.exits)
        self.assertEqual(hallway.exits["northwest"], outside)

    def test_add_exit_invalid_direction(self):
        hallway = HallwayRoom()
        self.assertRaises(ValueError, hallway.add_exit, "-invalid-", hallway)

    def test_possible_exits(self):
        """test that possible_exits returns a list of directions"""
        room = HallwayRoom()

        # initially, there are no exits
        self.assertEqual(room.possible_exits(), [])

        room.add_exit("north", room)
        self.assertEqual(room.possible_exits(), ["north"])

        room.add_exit("south", room)
        self.assertEqual(room.possible_exits(), ["north", "south"])

    def test_move(self):
        hallway = HallwayRoom()
        outside = OutsideRoom()
        hallway.add_exit("north", outside)

        self.assertEqual(hallway.move("north"), outside)

    def test_move_non_exit(self):
        hallway = HallwayRoom()
        outside = OutsideRoom()
        hallway.add_exit("north", outside)

        self.assertIsNone(hallway.move("south"))

    def test_move_by_alias(self):
        hallway = HallwayRoom()
        outside = OutsideRoom()
        hallway.add_exit("north", outside)

        self.assertEqual(hallway.move("n"), outside)


class TestItems(unittest.TestCase):
    def test_item_default_desc(self):
        item = Item('rock')
        self.assertEqual(item.name, 'rock')
        self.assertEqual(item.desc, "It's just a rock...")

    def test_item_custom_desc(self):
        item = Item('', 'xyzzy')
        self.assertEqual(item.desc, 'xyzzy')

    def test_item_default_desc_leading_vowel(self):
        item = Item('egg')
        self.assertEqual(item.name, 'egg')
        self.assertEqual(item.desc, "It's just an egg...")

    def test_npc_item(self):
        guard = Guard('Guard')
        self.assertGreater(len(guard.commands), 0)
        self.assertEqual(guard.say(), 'Stop')
        self.assertEqual(guard.name, 'Guard')

    def test_item_say(self):
        item = Item('rock')
        self.assertEqual(item.say(), '...')
