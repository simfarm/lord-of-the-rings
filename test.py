#!/usr/bin/python

import signal
import unittest

import xmlrunner
from mock import (MagicMock, patch)

class NextTurnTest(unittest.TestCase):
    """
    Tests _nextTurn in game.py.

    A few iterations:
    -testNextTurn: Command does not involve passage of time.
    -testNextTurn2: Command does involve passage of time. Chance of battle = 0%.
    -testNextTurn3: Command does involve passage of time. Chance of battle = 100%.
    """
    def testNextTurn(self):
        """
        Testing that helpCommand.execute.called when command does not
        involve passage of time.
        """
        from game import Game
        g = Game()

        #Create mock objects
        helpCommand = MagicMock()
        helpCommand.execute = MagicMock()
        helpCommand._time = False
        battle = MagicMock()
        g._parser.getNextCommand = MagicMock(return_value=helpCommand)

        g._nextTurn()
        errorMsg = "battle should not have been called but was."
        self.assertFalse(battle.called, errorMsg)
        errorMsg = "Game._nextTurn() failed to execute command"
        self.assertTrue(helpCommand.execute.called, errorMsg)
        
    def testNextTurn2(self):
        """
        Testing that helpCommand.execute.called when command involves
        a passing of time. Battle probability = 0%. 
        """
        from game import Game
        from space import Space
        from player import Player
        from battle_engine import battle
        
        g = Game()
        space = Space("Shire", "Home of the Russians", "Eregion", battleProbability = 0)
        player = Player("Russian", space)
        
        #Create mock objects
        helpCommand = MagicMock()
        helpCommand.execute = MagicMock()
        helpCommand._time = True
        battle = MagicMock()
        g._parser.getNextCommand = MagicMock(return_value=helpCommand)

        g._nextTurn()
        errorMsg = "battle should not have been called but was."
        self.assertFalse(battle.called, errorMsg)
        errorMsg = "Game._nextTurn() failed to execute command"
        self.assertTrue(helpCommand.execute.called, errorMsg)

    def testNextTurn3(self):
        """
        Testing that helpCommand.execute.called when command involves
        a passing of time and battle probability = 100%. Here, _battlePhase()
        should get called.
        """
        from game import Game
        from space import Space
        from player import Player
        from battle_engine import battle

        g = Game()
        space = Space("Shire", "Home of the Russians", "Eregion", battleProbability = 1)
        player = Player("Russian", space)
        
        #Create mock objects
        helpCommand = MagicMock()
        helpCommand._time = True
        nextCommand = MagicMock()
        nextCommand.execute = MagicMock(return_value=True)
        g._battlePhase = MagicMock()
        g._parser.getNextCommand = MagicMock(return_value=helpCommand)

        g._nextTurn()
        errorMsg = "g._nextTurn() failed to execute command."
        self.assertTrue(helpCommand.execute.called, errorMsg)
        errorMsg = "battle was supposed to have been called but was not."
        self.assertTrue(g._battlePhase.called, errorMsg)

class ExecutionCheckTest(unittest.TestCase):
    """
    Tests _executionCheck method in game.py.
    """
    def testPositiveCase(self):
        """
        Here, player can move in all directions. Therefore, all of the movement
        commands should work and executionCheck() should return True for all 
        movement commands.
        """
        from game import Game
        from space import Space
        from player import Player

        from commands.north_command import NorthCommand
        from commands.south_command import SouthCommand
        from commands.east_command import EastCommand
        from commands.west_command import WestCommand
        
        g = Game()
        g._player = MagicMock()

        g._player.canMoveNorth = MagicMock(return_value=True)
        g._player.canMoveSouth = MagicMock(return_value=True)
        g._player.canMoveEast = MagicMock(return_value=True)
        g._player.canMoveWest = MagicMock(return_value=True)

        northCmd = NorthCommand("north", "For movement", g._player)
        southCmd = SouthCommand("south", "For movement", g._player)
        eastCmd = EastCommand("east", "For movement", g._player)
        westCmd = WestCommand("west", "For movement", g._player)
        
        nextCommand = northCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned True for northCmd but did not."
        self.assertEqual(result, True, errorMsg)

        nextCommand = southCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned True for southCmd but did not."
        self.assertEqual(result, True, errorMsg)

        nextCommand = eastCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned True for eastCmd but did not."
        self.assertEqual(result, True, errorMsg)

        nextCommand = westCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned True for westCmd but did not."
        self.assertEqual(result, True, errorMsg)
    
    def testNegativeCase(self):
        """
        Here, player cannot move in any direction. Therefore, all of the movement
        commands should not work and executionCheck() should return False for all 
        movement commands.
        """
        from game import Game
        from space import Space
        from player import Player

        from commands.north_command import NorthCommand
        from commands.south_command import SouthCommand
        from commands.east_command import EastCommand
        from commands.west_command import WestCommand
        
        g = Game()
        g._player = MagicMock()

        g._player.canMoveNorth = MagicMock(return_value=False)
        g._player.canMoveSouth = MagicMock(return_value=False)
        g._player.canMoveEast = MagicMock(return_value=False)
        g._player.canMoveWest = MagicMock(return_value=False)

        northCmd = NorthCommand("north", "For movement", g._player)
        southCmd = SouthCommand("south", "For movement", g._player)
        eastCmd = EastCommand("east", "For movement", g._player)
        westCmd = WestCommand("west", "For movement", g._player)
        
        nextCommand = northCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned False for northCmd but did not."
        self.assertEqual(result, False, errorMsg)

        nextCommand = southCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned False for southCmd but did not."
        self.assertEqual(result, False, errorMsg)

        nextCommand = eastCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned False for eastCmd but did not."
        self.assertEqual(result, False, errorMsg)

        nextCommand = westCmd
        result = g._executionCheck(nextCommand)
        errorMsg = "_executionCheck() should have returned False for westCmd but did not."
        self.assertEqual(result, False, errorMsg)

class BattlePhaseTest(unittest.TestCase):
    """
    Tests game._battlePhase(). 
    """
    def testPositiveCase(self):
        """
        Mocks battleProbability such that battle() should get called.
        """
        from game import Game
        import battle_engine
        import constants
        
        #Create test objects
        g = Game()

        space = MagicMock()
        space.getRegion = MagicMock(return_value = constants.RegionType.ERIADOR)
        space.getBattleProbability = MagicMock(return_value=1)

        g._player = MagicMock()
        g._player.getLocation = MagicMock(return_value = space)
       
        battle_engine.battle = MagicMock()
        constants.BattleEngine.RUN_PROBABILITY_SUCCESS = 1
       
       #Assert that battle() is called when it should be called
        rawInputMock = MagicMock(return_value = "run")
        with patch('battle_engine.raw_input', create=True, new=rawInputMock):
            g._battlePhase()
        errorMsg = "battle() should have been called but was not."
        self.assertTrue(battle_engine.battle.called, errorMsg)       
    
    def testNegativeCase(self):
        """
        Mocks battleProbability such that battle() should not get called.
        """
        from game import Game
        import battle_engine
        import constants

        #Create test objects
        g = Game()

        space = MagicMock()
        space.getRegion = MagicMock(return_value = constants.RegionType.ERIADOR)
        space.getBattleProbability = MagicMock(return_value = 0)

        g._player = MagicMock()
        g._player.getLocation = MagicMock(return_value = space)
       
        battle_engine.battle = MagicMock()
        constants.BattleEngine.RUN_PROBABILITY_SUCCESS = 1
       
       #Assert that battle() is called when it should be called
        rawInputMock = MagicMock(return_value = "run")
        with patch('battle_engine.raw_input', create=True, new=rawInputMock):
            g._battlePhase()
        errorMsg = "battle() should have been called but was not."
        self.assertFalse(battle_engine.battle.called, errorMsg)       

class battleSetupTest(unittest.TestCase):
    """
    Tests _battleSetup helper function in battle_engine.py.
    """
    def testRandomBattle(self):
        """
        Tests that output for random battles is correct.
        """
        from battle_engine import _battleSetup
        from monsters.monster import Monster
        import constants
        
        #Create mock objects
        player = MagicMock()
        space = MagicMock()

        player.getLocation = MagicMock(return_value = space)
        space.getRegion = MagicMock(return_value = constants.RegionType.ERIADOR)
        space.getBattleBonusDifficulty = MagicMock(return_value = 1.5)

        context = constants.BattleEngineContext.RANDOM

        #Run helper method and verify return information
        result = _battleSetup(player, context)
        
        errorMsg = "battleBonusDifficulty was not returned correctly."
        self.assertEqual(result[0], 1.5, errorMsg)

        errorMsg = "List of monster objects was not generated correctly."
        for object in result[1]:
            self.assertTrue(isinstance(object, Monster), errorMsg)
    
    def testStoryBattle(self):
        from battle_engine import _battleSetup
        import constants
        
        #Create mock objects
        player = MagicMock()
        space = MagicMock()

        player.getLocation = MagicMock(return_value = space)
        space.getRegion = MagicMock(return_value = constants.RegionType.ERIADOR)
        space.getBattleBonusDifficulty = MagicMock(return_value = 1.5)

        context = constants.BattleEngineContext.STORY

        #Run helper method and verify return information
        result = _battleSetup(player, context)
        
        errorMsg = "battleBonusDifficulty was not returned correctly."
        self.assertEqual(result, 1.5, errorMsg)

class MonsterNumGenTest(unittest.TestCase):
    """
    Tests _monsterNumGen() of battle_engine.py.
    """
    def testMonsterGen(self):
        from player import Player
        from space import Space
        from battle_engine import _monsterNumGen
        import constants

        #Create test objects
        eriadorSpace = Space("Eriador", "", constants.RegionType.ERIADOR)
        barrowDownsSpace = Space("Barrow Downs", "", constants.RegionType.BARROW_DOWNS)
        highPassSpace = Space("High Pass", "", constants.RegionType.HIGH_PASS)
        enedwaithSpace = Space("Enedwaith", "", constants.RegionType.ENEDWAITH)
        moriaSpace = Space("Moria", "", constants.RegionType.MORIA)
        rhovanionSpace = Space("Rhovanion", "", constants.RegionType.RHOVANION)
        rohanSpace = Space("Rohan", "", constants.RegionType.ROHAN)
        gondorSpace = Space("Gondor", "", constants.RegionType.GONDOR)
        mordorSpace = Space("Mordor", "", constants.RegionType.MORDOR)
        
        player = Player("Russian", eriadorSpace)
        result = _monsterNumGen(player)
        
        #Test for valid outputs for the game's regions
        errorMsg = "_monsterNumGen failed for ERIADOR."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", barrowDownsSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for BARROW_DOWNS."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", highPassSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for HIGH_PASS."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", enedwaithSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for ENEDWAITH."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", moriaSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for MORIA."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", rhovanionSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for RHOVANION."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", rohanSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for ROHAN."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", gondorSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for GONDOR."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

        player = Player("Russian", gondorSpace)
        result = _monsterNumGen(player)
        errorMsg = "_monsterNumGen failed for MORDOR."
        self.assertTrue(isinstance(result, int), errorMsg)
        self.assertTrue(result >= 0, errorMsg)

class MonsterAttackPhaseTest(unittest.TestCase):
    """
    Tests _monsterAttackPhase of battle_engine.py.
    """
    def testMonsterAttackPhase(self):
        """
        Create three monsters and call this method. Verify that player stats 
        are changed appropriately. In this instance, player health remains 
        above zero.
        """
        from space import Space
        from player import Player
        from monsters.monster import Monster
        from battle_engine import _monsterAttackPhase

        space = Space("Shire", "", "Eregion")
        player = Player("Russian", space)
        
        monster = Monster("Jack", "", [10, 2, 2], "", "")
        monster2 = Monster("Jack", "", [10, 2, 2], "", "")
        monster3 = Monster("Jack", "", [10, 2, 2], "", "")
        monsters = [monster, monster2, monster3]

        #Pretest
        errorMsg = "Player instantiated with incorrect starting HP."
        self.assertEqual(player._hp, 20, errorMsg)

        #Test
        rawInputMock = MagicMock(return_value = "enter")
        with patch('battle_engine.raw_input', create=True, new=rawInputMock):
            _monsterAttackPhase(player, monsters)
        errorMsg = "Player health should be at 14 but is not."
        self.assertEqual(player._hp, 14, errorMsg)

    def testMonsterAttackPhase(self):
        """
        Create three monsters and call this method. Verify that player stats 
        are changed appropriately. In this instance, player health should 
        equal zero and _monsterAttackPhase should return False.
        """
        from space import Space
        from player import Player
        from monsters.monster import Monster
        from battle_engine import _monsterAttackPhase

        space = Space("Shire", "", "Eregion")
        player = Player("Russian", space)
        
        monster = Monster("Jack", "", [10, 20, 2], "", "")
        monster2 = Monster("Jack", "", [10, 20, 2], "", "")
        monster3 = Monster("Jack", "", [10, 20, 2], "", "")
        monsters = [monster, monster2, monster3]

        #Pretest
        errorMsg = "Player instantiated with incorrect starting HP."
        self.assertEqual(player._hp, 20, errorMsg)

        #Test
        rawInputMock = MagicMock(return_value = "enter")
        with patch('battle_engine.raw_input', create=True, new=rawInputMock):
            result =_monsterAttackPhase(player, monsters)
        errorMsg = "Player health should be at 0 but is not."
        self.assertEqual(player._hp, 0, errorMsg)

        errorMsg = "_monsterAttackPhase should have returned False but did not."
        self.assertFalse(result, errorMsg)

class ItemFindTest(unittest.TestCase):
    """
    Tests _itemFind of battle_engine.py
    """ 
    def testItemSpawn(self):
        """
        Here, experience gained is at the top of the unique probability distribution.
        Verifies that a low-, high-, and elite-level unique is generated.
        """
        from space import Space
        from player import Player
        from battle_engine import _itemFind
        import items.unique_items   
        import constants

        space = Space("", "", "")
        player = Player("", space)
        player._weightLimit = 1000

        experience = constants.ItemFind.lowLevel[1]
        
        #Pretest
        inventory = player._inventory._items
        errorMsg = "Player inventory was not empty to start with."
        self.assertEqual(inventory, [], errorMsg)
       
        #Test
        _itemFind(player, experience)

        lowLevelInInventory = 0
        for item in player._inventory._items:
            if item in items.unique_items.lowLevelFindableUniques:
                lowLevelInInventory += 1

        highLevelInInventory = 0
        for item in player._inventory._items:
            if item in items.unique_items.highLevelFindableUniques:
                highLevelInInventory += 1

        eliteLevelInInventory = 0
        for item in player._inventory._items:
            if item in items.unique_items.eliteLevelFindableUniques:
                eliteLevelInInventory += 1

        errorMsg = "Player inventory is supposed to have a low-level unique but does not."
        self.assertTrue(lowLevelInInventory >= 1, errorMsg)
        errorMsg = "Player inventory is supposed to have a high-level unique but does not."
        self.assertTrue(highLevelInInventory >= 1, errorMsg)
        errorMsg = "Player inventory is supposed to have an elite-level unique but does not."
        self.assertTrue(eliteLevelInInventory >= 1, errorMsg)

    def testLevelLimit(self):
        """
        Spawn for low-level uniques caps out at 14. In other words, if player is
        level 15 or higher, lowLevelFindableUniques will no longer spawn.

        This test tests that this is actually the case.
        """
        import space
        import player
        from items.unique_items import lowLevelFindableUniques


class ParserTest(unittest.TestCase):
    """
    Tests Parser class.
    """
    def testGetNextCommand(self):
        from parser import Parser
        commandWords = MagicMock()
        p = Parser(commandWords)

        #Create mock objects
        #raw_input = MagicMock(side_effect=["unrecognized command", "good command"])
        p._commandRecognized = MagicMock(side_effect=[False, True])
        fakeCommand = MagicMock()
        p._commandWords.getCommand = MagicMock(return_value=fakeCommand) 

        #Patch raw_input and call getNextCommand()
        rawInputMock = MagicMock(side_effect=["unrecognized cmd", "valid cmd"])
        with patch('parser.raw_input', create=True, new=rawInputMock):
            command = p.getNextCommand()

        #Assert calls made
        errorMsg = "Expected raw_input to be called twice."
        self.assertEqual(rawInputMock.call_count, 2, errorMsg)
        errorMsg = "Expected Parser._commandRecognized() to be called twice."
        self.assertEqual(p._commandRecognized.call_count, 2, errorMsg)
        errorMsg = "Parser.getNextCommand() did not respond expected command."
        self.assertEqual(command, fakeCommand, errorMsg)

    def testCommandRecognized(self):
        from parser import Parser
        commandWords = MagicMock()
        commandWords.isCommand = MagicMock(return_value=True)
        p = Parser(commandWords)

        result = p._commandRecognized("valid command")

        errorMsg = "Expected Parser._commandRecognized() to return True."
        self.assertTrue(result, errorMsg) 

class ItemTest(unittest.TestCase):
    """
    Tests Item class.
    """
    def testItem(self):
        from items.item import Item
        
        name = "Generic item"
        description = "Generic description"
        weight = 9
        cost = 10
        
        item = Item(name, description, weight, cost)

        errorMsg = "Expected item name to be '%s'." % name
        self.assertEqual(item.getName(), name, errorMsg)
        errorMsg = "Expected item description to be '%s'." % description 
        self.assertEqual(item.getDescription(), description, errorMsg)
        errorMsg = "Expected item weight to be '%s'." % weight 
        self.assertEqual(item.getWeight(), weight, errorMsg)
        errorMsg = "Expected item cost to b e '%s'." % cost
        self.assertEqual(item.getCost(), cost, errorMsg)

class ItemSetTest(unittest.TestCase):
    """
    Tests ItemSet class.
    """
    INITIAL_COUNT = 3
    INITIAL_WEIGHT = 4

    def setUp(self):
        from items.item import Item
        from items.item_set import ItemSet

        sword = Item("sword", "made by elves", 2, 2)
        helmet = Item("helmet", "made by men", 1, 1)
        potion = Item("potion", "restores health", 1, 1)

        self._itemList = [sword, helmet, potion]
        self._items = ItemSet([sword, helmet, potion])

    def tearDown(self):
        self._itemList = self._items = None

    def testInitItemSet(self):
        errorMsg = "ItemSet object has more objects than it was given " \
                    "during initialization."
        self.assertEqual(len(self._items._items), ItemSetTest.INITIAL_COUNT, errorMsg)

        errorMsg = "ItemSet object does not include all objects given " \
                    "during initialization."
        for item in self._itemList:
            self.assertTrue(item in self._items._items, errorMsg)

    def testCountItems(self):
        expectedCount = ItemSetTest.INITIAL_COUNT
        actualCount = self._items.count()
        
        errorMsg = "Actual count and expected count different for ItemSet object."
        self.assertEqual(expectedCount, actualCount, errorMsg)

    def testAddRemoveContainsItems(self):
        from items.item import Item
        antidote = Item("antidote", "cures poison", 1, 1)

        #Verify item not included in collection
        errorMsg = "ItemSet.containsItem() claimed to contain item not present."
        self.assertFalse(self._items.containsItem(antidote), errorMsg)

        #Add item
        self._items.addItem(antidote)

        errorMsg = "ItemSet.containsItem() failed to identify existing item." 
        self.assertTrue(self._items.containsItem(antidote), errorMsg)

        errorMsg = "ItemSet.containsItemWithName() failed to identify existing item."
        self.assertTrue(self._items.containsItemWithName("antidote"), errorMsg)

        #Remove item
        self._items.removeItem(antidote)

        errorMsg = "ItemSet.containsItem() claimed to contain item not present."
        self.assertFalse(self._items.containsItem(antidote), errorMsg)

    def testItemsWeight(self):
        from items.item import Item 

        errorMsg = "Initial weight of ItemSet object incorrect."
        expectedWeight = ItemSetTest.INITIAL_WEIGHT
        actualWeight = self._items.getWeight()
        self.assertEqual(expectedWeight, actualWeight, errorMsg)

        heavyRock = Item("heavy rock", "weighs a ton", 2000, 0)

        #Add item
        self._items.addItem(heavyRock)

        errorMsg = "ItemSet.weight() reported incorrect weight." 
        expectedWeight += 2000
        actualWeight = self._items.getWeight()
        self.assertEqual(expectedWeight, actualWeight, errorMsg)

        #Remove item
        self._items.removeItem(heavyRock)

        expectedWeight -= 2000
        actualWeight = self._items.getWeight()
        self.assertEqual(expectedWeight, actualWeight, errorMsg)

    def testItemSetIter(self):
        #Verify iterator returns by ItemSet object visits the exact
        #collection of objects added to ItemSet

        #(Implicitly) use iterator in for loop
        for item in self._items:
            #Verify item returned is recognized
            errorMsg = "ItemSet iterator returned unrecognized object."
            self.assertTrue(item in self._itemList, errorMsg)

            #Remove item from original list of items
            self._itemList.remove(item)

        #Assert all items are accounted for
        errorMsg = "ItemSet object contained Item not added during initialization."
        self.assertEqual(len(self._itemList), 0, errorMsg)

class SpaceTest(unittest.TestCase):
    """
    Test for spaces.
    """
    def testItems(self):
        from space import Space
        from items.item import Item
        import constants
        
        #Prepare items
        blade = Item("blade", "appears to be dull", 1, 1)
        bow = Item("bow", "long bow", 2, 2) 

        #Create space
        space = Space("shire", "Home of the Hobbits.", constants.RegionType.MORDOR)
        items = space.getItems()

        #Assert space initially empty
        errorMsg = "New space contains items; should be empty" 
        self.assertEqual(items.count(), 0, errorMsg)

        errorMsg = "Space claims to contain item even though it is empty."
        self.assertFalse(space.containsItem(blade), errorMsg)
        self.assertFalse(space.containsItem(bow), errorMsg)

        #Add blade
        space.addItem(blade)
        errorMsg = "Space failed to report that it contained item known to exist."
        self.assertTrue(space.containsItem(blade), errorMsg)

        #Add bow 
        space.addItem(bow)
        self.assertTrue(space.containsItem(bow), errorMsg)

        #Get room's items. Assert blade and bow exist
        items = space.getItems()
        self.assertEqual(items.count(), 2, "Room should contain exactly two items.")
        self.assertTrue(items.containsItem(blade), "Could not find blade in room's set of items.")
        self.assertTrue(items.containsItem(bow), "Could not find bow in room's set of items.")

        #Remove blade
        space.removeItem(blade)
        errorMsg = "Space claims to have item that was removed."
        self.assertFalse(space.containsItem(blade), errorMsg)
        errorMsg = "Space missing item that should still exist."
        self.assertTrue(space.containsItem(bow), errorMsg)

        #Get room's items. Assert only bow exists
        items = space.getItems()
        self.assertEqual(items.count(), 1, "Room should contain exactly one item.")
        self.assertFalse(items.containsItem(blade), 
                "Blade found in room (even though it was removed).")
        self.assertFalse(items.containsItemWithName("blade"), "Blade found in room (even though it was removed).")
        self.assertTrue(items.containsItem(bow), "Could not find bow in room's set of items.")

    def testRegion(self):
        from space import Space
        import constants

        space = Space("West Emnet", "Horses for riding", "Rohan")

        errorMsg = "space.getRegion() should return 'Rohan.'"
        self.assertEquals(space.getRegion(), "Rohan", errorMsg)

    def testCities(self):
        from space import Space
        from cities.city import City

        #Create city
        newYorkCity = City("New York City", "An enormous city", "Come test here")

        #Create space
        newYork = Space("New  York", "A huge space", "Welcome to our space", city = newYorkCity)

        #Assert city in space
        errorMsg = "space.getCity() should return newYorkCity but does not."
        self.assertEqual(newYork.getCity(), newYorkCity, errorMsg)

    def testUniquePlace(self):
        from space import Space
        from unique_place import UniquePlace

        #Create UniquePlace
        dmitriyHouse = UniquePlace("Dmitriy's House", "Lots of vodka", "[Knocks once.]")

        #Create space
        chocolateMountain = Space("Chocolate Mountain", "Chocolate rain here", "Welcome.", uniquePlace = dmitriyHouse)
        
        #Assert uniquePlace in space
        errorMsg = "space.getUniquePlace() should return dmitriyHouse but does not."
        self.assertEqual(chocolateMountain.getUniquePlace(), dmitriyHouse, errorMsg)
        
class MovementTest(unittest.TestCase):
    """
    Tests the movement methods of space and movement commands.  
    """
    def testMovement(self):
        """
        General, encompassing test for movement, including movement commands.
        """
        from space import Space
        from player import Player
        from commands.north_command import NorthCommand
        from commands.south_command import SouthCommand
        from commands.west_command import WestCommand
        from commands.east_command import EastCommand
        from constants import Direction
        
        space = Space("Shire", "Home of the hobbits", "Mordor")
        player = Player("Russian", space)
        
        northCmd = NorthCommand("North", "Moves player north", player)
        southCmd = SouthCommand("South", "Moves player south", player)
        eastCmd = EastCommand("East", "Moves player east", player)
        westCmd = WestCommand("West", "Moves player west", player)
        
        #Non-movement case - ports not created
        errorMsg = "Player should still be in space but is not."

        northCmd.execute()
        self.assertEqual(player.getLocation(), space, errorMsg)
        player._location = space

        southCmd.execute()
        self.assertEqual(player.getLocation(), space, errorMsg)
        player._location = space

        eastCmd.execute()
        self.assertEqual(player.getLocation(), space, errorMsg)
        player._location = space

        westCmd.execute()
        self.assertEqual(player.getLocation(), space, errorMsg)
        player._location = Space

        #Create destinations and two-way ports
        north = Space("North Space", "Very cold", "Welcome")
        south = Space("South Space", "Very warm", "Welcome")
        east = Space("East Space", "Very mountainous", "Welcome")
        west = Space("West Space", "Coastal", "Welcome")

        space.createExit("north", north, outgoingOnly = False)
        space.createExit("south", south, outgoingOnly = False)
        space.createExit("east", east, outgoingOnly = False)
        space.createExit("west", west, outgoingOnly = False)

        #Test getExit() for destination spaces
        errorMsg = "getExit() test failed."
        self.assertEqual(north.getExit("south"), space, errorMsg)
        self.assertEqual(south.getExit("north"), space, errorMsg)
        self.assertEqual(east.getExit("west"), space, errorMsg)
        self.assertEqual(west.getExit("east"), space, errorMsg)

        #Test ports created using _isExit() for space
        errorMsg = "Ports are supposed to be created but are not - using _isExit()."
        self.assertEqual(space._isExit("north"), True, errorMsg)
        self.assertEqual(space._isExit("south"), True, errorMsg)
        self.assertEqual(space._isExit("east"), True, errorMsg)
        self.assertEqual(space._isExit("west"), True, errorMsg)

        #Test ports created without using direct access for Space
        errorMsg = "Ports are supposed to be created but were not - by direct attribute access."
        self.assertEqual(space._exits[Direction.NORTH], north, errorMsg)
        self.assertEqual(space._exits[Direction.SOUTH], south, errorMsg)
        self.assertEqual(space._exits[Direction.EAST], east, errorMsg)
        self.assertEqual(space._exits[Direction.WEST], west, errorMsg)

        #Test ports created without using direct access for destination Spaces
        errorMsg = "Ports are supposed to have been created but were not - by direct attribute access for destination spaces."
        self.assertEqual(north._exits[Direction.SOUTH], space, errorMsg)
        self.assertEqual(south._exits[Direction.NORTH], space, errorMsg)
        self.assertEqual(east._exits[Direction.WEST], space, errorMsg)
        self.assertEqual(west._exits[Direction.EAST], space, errorMsg)
                                      
        #Test two-way movement
        player._location = space
        northCmd.execute()
        errorMsg = "Player should be in north space but is not."
        self.assertEqual(player.getLocation(), north, errorMsg)
        southCmd.execute()
        errorMsg = "Player should be in space but is not."
        self.assertEqual(player.getLocation(), space, errorMsg)

        player._location = space
        southCmd.execute()
        errorMsg = "Player should be in south space but is not."
        self.assertEqual(player.getLocation(), south, errorMsg)
        northCmd.execute()
        errorMsg = "Player should be in space but is not."
        self.assertEqual(player.getLocation(), space, errorMsg)

        player._location = space
        eastCmd.execute()
        errorMsg = "Player should be in east space but is not."
        self.assertEqual(player.getLocation(), east, errorMsg)
        westCmd.execute()
        errorMsg = "Player should be in space but is not."
        self.assertEqual(player.getLocation(), space, errorMsg)

        player._location = space
        westCmd.execute()
        errorMsg = "Player should be in west space but is not."
        self.assertEqual(player.getLocation(), west, errorMsg)
        eastCmd.execute()
        errorMsg = "Player should be in space but is not."
        self.assertEqual(player.getLocation(), space, errorMsg)

        #Test clearExit() method
        errorMsg = "Port should have been cleared but was not."

        space.clearExit("north", False)
        self.assertEqual(space._exits[Direction.NORTH], None, errorMsg)
                        
        space.clearExit("south", False)
        self.assertEqual(space._exits[Direction.SOUTH], None, errorMsg)
        
        space.clearExit("east", False)
        self.assertEqual(space._exits[Direction.EAST], None, errorMsg)
        
        space.clearExit("west", False)
        self.assertEqual(space._exits[Direction.WEST], None, errorMsg)
       
    def testMovement2(self):
        """
        Tests for one-way ports and one-way movement.
        """
        from space import Space
        from player import Player
        from commands.north_command import NorthCommand
        from commands.south_command import SouthCommand
        from commands.west_command import WestCommand
        from commands.east_command import EastCommand
        
        space = Space("Shire", "Home of the hobbits", "Mordor")
        player = Player("Russian", space)
        
        northCmd = NorthCommand("North", "Moves player north", player)
        southCmd = SouthCommand("South", "Moves player south", player)
        eastCmd = EastCommand("East", "Moves player east", player)
        westCmd = WestCommand("West", "Moves player west", player)
        
        north = Space("North Space", "Very cold", "Welcome")
        south = Space("South Space", "Very warm", "Welcome")
        east = Space("East Space", "Very mountainous", "Welcome")
        west = Space("West Space", "Coastal", "Welcome")
        
        #Create one-way ports
        space.createExit("north", north, outgoingOnly = True)
        space.createExit("south", south, outgoingOnly = True)
        space.createExit("east", east, outgoingOnly = True)
        space.createExit("west", west, outgoingOnly = True)

        #Test one-way movement
        player._location = space
        northCmd.execute()
        errorMsg = "Player should be in north space but is not."
        self.assertEqual(player.getLocation(), north, errorMsg)
        southCmd.execute()
        errorMsg = "Player should be in north space but is not."
        self.assertEqual(player.getLocation(), north, errorMsg)
        
        player._location = space
        southCmd.execute()
        errorMsg = "Player should be in south space but is not."
        self.assertEqual(player.getLocation(), south, errorMsg)
        northCmd.execute()
        errorMsg = "Player should be in south but is not."
        self.assertEqual(player.getLocation(), south, errorMsg)
        
        player._location = space
        eastCmd.execute()
        errorMsg = "Player should be in east space but is not."
        self.assertEqual(player.getLocation(), east, errorMsg)
        westCmd.execute()
        errorMsg = "Player should be in east but is not."
        self.assertEqual(player.getLocation(), east, errorMsg)
        
        player._location = space
        westCmd.execute()
        errorMsg = "Player should be in west space but is not."
        self.assertEqual(player.getLocation(), west, errorMsg)
        eastCmd.execute()
        errorMsg = "Player should be in west but is not."
        self.assertEqual(player.getLocation(), west, errorMsg)

class PickUpTest(unittest.TestCase):
    """
    Test PickUp class.
    """
    def testExecute(self):
        """
        Test case: player picks up an item that may be picked up.
        """
        from space import Space
        from player import Player
        from items.item import Item
        from commands.pick_up_command import PickUpCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        item = Item("Dagger", "A trusty blade", 0, 0)
        pickUpCmd = PickUpCommand("pick up", "Picks up an object", player)
        
        space.addItem(item)

        #Test pre-test conditions
        self.assertTrue(space.containsItem(item), "Space should have item but does not.")
        
        inventory = player.getInventory()
        self.assertFalse(inventory.containsItem(item), "Player inventory should not have item but does.")
        
        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(item), "Player equipment should not have item but does.")
            
        #Execute pickUpCmd and assert item in player inventory but not in space and not in equipment
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.pick_up_command.raw_input', create=True, new=rawInputMock):
            pickUpCmd.execute()
            
        self.assertFalse(space.containsItem(item), "Space should not have item but does.")
        
        inventory = player.getInventory()
        self.assertTrue(inventory.containsItem(item), "Player should have item in inventory but does not.")

        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(item), "Player should not have item in equipment but does.")
        
    def testExecute2(self):
        """
        Test case: player tries to pick up non-existent item.
        """
        from space import Space
        from player import Player
        from commands.pick_up_command import PickUpCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        pickUpCmd = PickUpCommand("pick up", "Picks up an object", player)

        #Test pre-test conditions
        self.assertEqual(space._items._items, [], "Space should have no items but does.")
        self.assertEqual(player._inventory._items, [], "player._inventory should have no items but does.")
        self.assertEqual(player._equipped._items, [], "player._equipped should have no items but does.")
            
        #Execute pickUpCmd and test that nothing has changed
        rawInputMock = MagicMock(return_value="Shiny Acorns")
        with patch('commands.pick_up_command.raw_input', create=True, new=rawInputMock):
            pickUpCmd.execute()
            
        self.assertEqual(space._items._items, [], "Space should have no items but does - post-test.")
        self.assertEqual(player._inventory._items, [], "player._inventory should have no items but does - post-test.")
        self.assertEqual(player._equipped._items, [], "player._equipped should have no items but does - post-test.")
        
class DropTest(unittest.TestCase):
    """
    Test Drop class.
    """
    def testExecute(self):
        """
        Test case where items in inventory and equipment.
        """
        from space import Space
        from player import Player
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.drop_command import DropCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        dropCmd = DropCommand("drop", "Drops an object from inventory to space", player)
        
        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield of Faith", "Quenches fiery darts", 2, 2, 2) 

        player.addToInventory(weapon)
        player.equip(weapon)
        player.addToInventory(armor)
        player.equip(armor)

        #Test pre-test conditions
        self.assertFalse(space.containsItem(weapon), "Space should not have weapon but does.")
        self.assertFalse(space.containsItem(armor), "Space should not have armor but does.")
        
        inventory = player.getInventory()
        self.assertTrue(inventory.containsItem(weapon), "Inventory should have weapon but does not.")
        self.assertTrue(inventory.containsItem(armor), "Inventory should have armor but does not.")

        equipped = player.getEquipped()
        self.assertTrue(equipped.containsItem(weapon), "Equipped should have weapon but does not.")
        self.assertTrue(equipped.containsItem(armor), "Equipped should have armor but does not.")

        #Assert item in space but not in player inventory and not in equipment
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.drop_command.raw_input', create=True, new=rawInputMock):
            dropCmd.execute()
        rawInputMock = MagicMock(return_value="Shield of Faith")
        with patch('commands.drop_command.raw_input', create=True, new=rawInputMock):
            dropCmd.execute()
            
        self.assertTrue(space.containsItemString("Dagger"), "Space should have weapon but does not.")
        self.assertTrue(space.containsItemString("Shield of Faith"), "Space should have armor but does not.")
        
        inventory = player.getInventory()
        self.assertFalse(inventory.containsItem(weapon), "Inventory should not have weapon but does.")
        self.assertFalse(inventory.containsItem(armor), "Inventory should not have armor but does.")
        
        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(weapon), "Equipment should not have armor but does.")
        self.assertFalse(equipped.containsItem(armor), "Equipment should not have armor but does.")

    def testExecute2(self):
        """
        Test case where items in inventory but not in equipment.
        """
        from space import Space
        from player import Player
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.drop_command import DropCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        dropCmd = DropCommand("drop", "Drops an object from inventory to space", player)
        
        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield of Faith", "Quenches fiery darts", 2, 2, 2)

        player.addToInventory(weapon)
        player.addToInventory(armor)
        
        #Test pre-test conditions
        self.assertFalse(space.containsItem(weapon), "Space should not have weapon but does.")
        self.assertFalse(space.containsItem(armor), "Space should not have armor but does.")
        
        inventory = player.getInventory()
        self.assertTrue(inventory.containsItem(weapon), "Inventory should have weapon but does not.")
        self.assertTrue(inventory.containsItem(armor), "Inventory should have armor but does not.")

        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(weapon), "Equipped should not have weapon but does.")
        self.assertFalse(equipped.containsItem(armor), "Equipped should not have armor but does.")

        #Assert item in space but not in player inventory and not in equipment
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.drop_command.raw_input', create=True, new=rawInputMock):
            dropCmd.execute()
        rawInputMock = MagicMock(return_value="Shield of Faith")
        with patch('commands.drop_command.raw_input', create=True, new=rawInputMock):
            dropCmd.execute()
            
        self.assertTrue(space.containsItemString("Dagger"), "Space should have weapon but does not.")
        self.assertTrue(space.containsItemString("Shield of Faith"), "Space should have armor but does not.")
        
        inventory = player.getInventory()
        self.assertFalse(inventory.containsItem(weapon), "Inventory should not have weapon but does.")
        self.assertFalse(inventory.containsItem(armor), "Inventory should not have armor but does.")
        
        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(weapon), "Equipment should not have weapon but does.")
        self.assertFalse(equipped.containsItem(armor), "Equipment should not have armor but does.")

    def testExecute3(self):
        """
        Test case for when player does not have item in either inventory or equipment.
        """
        from space import Space
        from player import Player
        from commands.drop_command import DropCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        dropCmd = DropCommand("drop", "Drops an object from inventory to space", player)
        
        #Test pre-test conditions
        self.assertEqual(space._items._items, [], "Space should have no items but does.")
        self.assertEqual(player._inventory._items, [], "player._inventory should have no items but does.")
        self.assertEqual(player._equipped._items, [], "player._equipped should have no items but does.")

        #Attempt to drop item that does not exist
        rawInputMock = MagicMock(return_value="Melted Cheese")
        with patch('commands.drop_command.raw_input', create=True, new=rawInputMock):
            dropCmd.execute()
            
        self.assertEqual(space._items._items, [], "Space should have no items but does - post-test.")
        self.assertEqual(player._inventory._items, [], "player._inventory should have no items but does - post-test.")
        self.assertEqual(player._equipped._items, [], "player._equipped should have no items but does - post-test.")

class EquipTest(unittest.TestCase):
    """
    Tests Equip Command.
    """
    def testPositiveCase(self):
        """
        Testcase: for equipping an item that may be equipped.
        """
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.equip_command import EquipCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)

        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield", "Very faithful", 2, 2, 2) 

        inventory = player.getInventory()
        inventory.addItem(weapon)
        inventory.addItem(armor)

        #Equipping equippable items
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()

        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()
            
        equipped = player.getEquipped()

        self.assertTrue(inventory.containsItem(weapon), "Inventory should still have weapon but does not.")
        self.assertTrue(inventory.containsItem(armor), "Inventory should still have armor but does not.")
        
        self.assertTrue(equipped.containsItem(weapon), "Player failed to equip equipable weapon.")
        self.assertTrue(equipped.containsItem(armor), "Player failed to equip equipable armor.")
        
    def testNegativeCase1(self):
        """
        Attempting to equip items not in inventory.
        """
        from player import Player
        from space import Space
        from commands.equip_command import EquipCommand

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)
        
        #Test pre-test conditions
        inventory = player.getInventory()
        errorMsg = "player._inventory is supposed to be empty but is not."
        self.assertEqual(inventory.count(), 0, errorMsg)

        equipped = player.getEquipped()
        errorMsg = "player._equipped is supposed to be empty but is not."
        self.assertEqual(equipped.count(), 0, errorMsg)
        
        #Trying to equip items not in inventory
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()

        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()

        errorMsg = "player._inventory is supposed to be empty but is not."
        self.assertEqual(inventory.count(), 0, errorMsg)
        errorMsg = "player._equipped is supposed to be empty but is not."
        self.assertEqual(equipped.count(), 0, errorMsg)

    def testNegativeCase2(self):
        """
        Attempting to equip an item that may not be equipped.

        In this instance, item is of the Item class.
        """
        from player import Player
        from space import Space
        from items.item import Item
        from commands.equip_command import EquipCommand

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)
        
        item = Item("Charm", "Unknown effects", 1, 1)
        
        inventory = player.getInventory()
        inventory.addItem(item)

        #Trying to equip item that cannot be equipped
        rawInputMock = MagicMock(return_value="Charm")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()

        self.assertTrue(inventory.containsItem(item), "Inventory should have item.")
        
        equipped = player.getEquipped()
        self.assertFalse(equipped.containsItem(item), "Player equipped item of Item class.")

    def testNegativeCase3(self):
        """
        Attempting to equip items that are already equipped.
        """
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.equip_command import EquipCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)

        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield", "of faith", 2, 2, 2)

        inventory = player.getInventory()
        inventory.addItem(weapon)
        inventory.addItem(armor)
        
        equipped = player.getEquipped()
        equipped.addItem(weapon)
        equipped.addItem(armor)

        #Test - preconditions
        errorMsg = "Weapon and armor are supposed to be in inventory but are not."
        self.assertTrue(weapon in inventory._items, errorMsg)
        self.assertTrue(armor in inventory._items, errorMsg)
        errorMsg = "Inventory is supposed to have two items."
        self.assertEqual(player._inventory.count(), 2, errorMsg)
        
        errorMsg = "Weapon is supposed to be in player._equipped but is not."
        self.assertTrue(weapon in player._equipped, errorMsg)
        errorMsg = "Armor is supposed to be in player._equipped but it is not."
        self.assertTrue(armor in player._equipped, errorMsg)
        errorMsg = "player._equipped is supposed to have two items but does not."
        self.assertEqual(player._equipped.count(), 2, errorMsg)

        #Equipping an item that is already equipped
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute() 
            
        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute() 

        #Test still only two equipped items
        errorMsg = "Weapon and armor are supposed to be in inventory but are not."
        self.assertTrue(weapon in player._inventory, errorMsg)
        self.assertTrue(armor in player._inventory, errorMsg)
        errorMsg = "Player inventory is only supposed to have two items."
        self.assertEqual(player._inventory.count(), 2, errorMsg)
            
        errorMsg = "Weapon is supposed to be in player._equipped but is not."
        self.assertTrue(weapon in player._equipped, errorMsg)
        errorMsg = "Armor is supposed to be in player._equipped but it is not."
        self.assertTrue(armor in player._equipped, errorMsg)
        errorMsg = "Player is supposed to have two equipped items but lists more."
        self.assertEqual(player._equipped.count(), 2, errorMsg)

    def testPlayerWeaponStats(self):
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from commands.equip_command import EquipCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        defaultAttack = player._attack
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)

        weapon = Weapon("Sword of the Spirit", "Sharper than any double-edged sword", 1, 1, 1)
        player.addToInventory(weapon)

        #Test preconditions
        errorMsg = "Weapon should be in player._inventory._items but is not."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        errorMsg = "Weapon shoud not be in player._equipped._items but is not."
        self.assertTrue(weapon not in player._equipped._items, errorMsg)

        #Equip weapon and check that _totalAttack and _weaponAttack update
        rawInputMock = MagicMock(return_value="Sword of the Spirit")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute() 

        errorMsg = "Weapon should be in player._inventory._items but is not."
        self.assertTrue(player._inventory.containsItem(weapon), errorMsg)
        errorMsg = "Weapon should be equipped but is not."
        self.assertTrue(player._equipped.containsItem(weapon), errorMsg)

        #Test for change
        errorMsg = "player._attack changed with weapon equip when it should not have."
        self.assertEqual(player._attack, defaultAttack, errorMsg)
        errorMsg = "player._weaponAttack not updated to correct value."
        self.assertEqual(player._weaponAttack, weapon._attack, errorMsg)
        errorMsg = "player._totalAttack not updated to correct value."
        self.assertEqual(player._totalAttack, defaultAttack + weapon._attack, errorMsg)

    def testPlayerArmorStats(self):
        from player import Player
        from space import Space
        from items.armor import Armor
        from commands.equip_command import EquipCommand
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        equipCmd = EquipCommand("Equip", "Equips item in inventory to player", player)

        armor = Armor("Shield of Faith", "For quenching fiery darts", 1, 1, 1)
        player.addToInventory(armor)

        #Test preconditions
        errorMsg = "Armor should be in player._inventory._items but is not."
        self.assertTrue(armor in player._inventory._items, errorMsg)
        errorMsg = "Armor should not be in player._equipped._items but is not."
        self.assertTrue(armor not in player._equipped._items, errorMsg)

        #Equip armor and check that player._defense updates
        rawInputMock = MagicMock(return_value="Shield of Faith")
        with patch('commands.equip_command.raw_input', create=True, new=rawInputMock):
            equipCmd.execute()

        errorMsg = "Armor should be in inventory but is not."
        self.assertTrue(player._inventory.containsItem(armor), errorMsg)
        errorMsg = "Armor should be equipped but is not."
        self.assertTrue(player._equipped.containsItem(armor), errorMsg)
        
        #Test for change
        errorMsg = "player._armorDefense stat was not updated correctly."
        self.assertEqual(player._armorDefense, armor._defense, errorMsg)
                         
class UnequipTest(unittest.TestCase):
    """
    Tests Unequip Command.
    """
    def testPositiveCase(self):
        """
        Unequipping an unequippable item.
        """
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.unequip_command import UnequipCommand

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        unequipCmd = UnequipCommand("unequip", "Unequips currently equipped item", player)

        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield", "of faith", 2, 2, 2)

        player.addToInventory(weapon)
        player.addToInventory(armor)
        player.equip(weapon)
        player.equip(armor)

        #Test preconditions
        errorMsg = "Weapon and Armor should be in inventory but are not."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)

        errroMsg = "Weapon and Armor should be in equipped but are not."
        self.assertTrue(weapon in player._equipped._items, errorMsg)
        self.assertTrue(armor in player._equipped._items, errorMsg)
        
        #Attempting to unequip item not currently equipped
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()
        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()

        errorMsg = "Weapon and Armor should be in inventory but are not."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)

        errorMsg = "Player should not have weapon in equipped."
        self.assertFalse(player._equipped.containsItem(weapon), errorMsg)
        errorMsg = "Player should not have armor in equipped."
        self.assertFalse(player._equipped.containsItem(armor), errorMsg)
        
    def testNegativeCase(self):
        """
        Attempting to unequip an item that is not currently equipped.
        Item is in inventory. 
        """
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from items.armor import Armor
        from commands.unequip_command import UnequipCommand

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        unequipCmd = UnequipCommand("unequip", "Unequips currently equipped item", player)

        weapon = Weapon("Dagger", "A trusty blade", 2, 2, 2)
        armor = Armor("Shield", "of faith", 2, 2, 2)

        player.addToInventory(weapon)
        player.addToInventory(armor)

        #Test preconditions
        errorMsg = "Weapon and Armor should be in inventory but are not."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)
        
        #Attempting to unequip item not currently equipped
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()
        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()

        errorMsg = "Weapon and Armor should be in inventory but are not."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)

        errorMsg = "Player should not have weapon in equipped but does."
        self.assertFalse(player._equipped.containsItem(weapon), errorMsg)
        errorMsg = "Player should not have armor in equipped but does."
        self.assertFalse(player._equipped.containsItem(armor), errorMsg)
        
    def testNegativeCase2(self):
        """
        Attempting to unequip an item that is not currently equipped.
        Item is not in inventory. 
        """
        from player import Player
        from space import Space
        from commands.unequip_command import UnequipCommand

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        unequipCmd = UnequipCommand("unequip", "Unequips currently equipped item", player)

        #Test preconditions
        errorMsg = "Inventory should be empty."
        self.assertEqual(player._inventory.count(), 0, errorMsg)
        errorMsg = "Equipment should be empty."
        self.assertEqual(player._equipped.count(), 0, errorMsg)
        
        #Attempting to unequip item not currently equipped
        rawInputMock = MagicMock(return_value="Dagger")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()
        rawInputMock = MagicMock(return_value="Shield")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute()

        errorMsg = "Inventory should still be empty."
        self.assertEqual(player._inventory.count(), 0, errorMsg)
        errorMsg = "Equipment should still be empty."
        self.assertEqual(player._equipped.count(), 0, errorMsg)
        
    def testPlayerWeaponStats(self):
        """
        Tests that player-specific attributes such as player._totalAttack
        and player._weaponAttack reset with unequip.
        """
        from player import Player
        from space import Space
        from items.weapon import Weapon
        from commands.unequip_command import UnequipCommand
        import constants
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        unequipCmd = UnequipCommand("Unequip", "Unequips item in inventory to player", player)

        weapon = Weapon("Sword of the Spirit", "Sharper than any double-edged sword", 1, 1, 1)
        player.addToInventory(weapon)
        player.equip(weapon)

        #Test preconditions
        errorMsg = "Weapon should be in inventory and equipped."
        self.assertTrue(weapon in player._inventory._items, errorMsg)

        #Test player-specific attributes to change back to defaults
        rawInputMock = MagicMock(return_value="Sword of the Spirit")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute() 

        errorMsg = "player._weaponAttack should be zero but it is not."
        self.assertEqual(player._weaponAttack, 0, errorMsg)
        errorMsg = "player._totalAttack should be player._attack but it is not."
        self.assertEqual(player._totalAttack, player._attack, errorMsg)
        
    def testPlayerArmorStats(self):
        """
        Tests that player._defense resets with unequip.
        """
        from player import Player
        from space import Space
        from items.armor import Armor
        from commands.unequip_command import UnequipCommand
        import constants
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        unequipCmd = UnequipCommand("Unequip", "Unequips item in inventory to player", player)

        armor = Armor("Shield of Faith", "For quenching fiery darts", 1, 1, 1)
        player.addToInventory(armor)
        player.equip(armor)

        #Test preconditions
        errorMsg = "Armor should be in player inventory and equipped."
        self.assertTrue(armor in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._equipped._items , errorMsg)

        #Test for change back to player defaults        
        rawInputMock = MagicMock(return_value="Shield of Faith")
        with patch('commands.unequip_command.raw_input', create=True, new=rawInputMock):
            unequipCmd.execute() 

        errorMsg = "player._armorDefense should be zero after unequip."
        self.assertEqual(player._armorDefense, 0, errorMsg)

class UsePotionTest(unittest.TestCase):
    """
    Tests UsePotion command.
    """
    def testPostiveCase(self):
        """
        Player has potion and uses potion.
        """
        from commands.use_potion_command import UsePotionCommand
        from space import Space
        from player import Player
        from items.potion import Potion

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        inventory = player.getInventory()
        usePotionCmd = UsePotionCommand("use potion", "Uses potion in inventory.", player)
        
        player._totalMaxHp = 20
        player._hp = 1
        healing = 10
        correctFinalHp = player._hp + healing
        
        potion = Potion("Enormous Potion", "So big", 1, healing, 10)
        player._inventory.addItem(potion)

        #Test preconditions
        errorMsg = "Potion should be in player._inventory but is not."
        self.assertTrue(potion in player._inventory._items, errorMsg)
        errorMsg = "player._hp should be 1 but is not."
        self.assertEqual(player._hp, 1, errorMsg)
        
        #Test for proper change in player._inventory and player._hp
        rawInputMock = MagicMock(return_value="Enormous Potion")
        with patch('commands.use_potion_command.raw_input', create = True, new = rawInputMock):
            usePotionCmd.execute()
            
        errorMsg = "Inventory still contains potion when it should not."
        self.assertFalse(inventory.containsItem(potion), errorMsg)
        errorMsg = "Player health not at correct amount."
        self.assertEqual(player._hp, correctFinalHp, errorMsg)

    def testNegativeCase(self):
        """
        Player has no potions in inventory.
        """
        from commands.use_potion_command import UsePotionCommand
        from space import Space
        from player import Player
        from items.potion import Potion
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        usePotionCmd = UsePotionCommand("use potion", "Uses potion in inventory.", player)
        
        player._totalMaxHp = 20
        player._hp = 10
        startingHp = player._hp

        #Test preconditions
        errorMsg = "Player should have no potions."
        self.assertEqual(player._inventory.count(), 0, errorMsg)
        errorMsg = "player._hp should be 10 but is not."
        self.assertEqual(player._hp, 10, errorMsg)

        #Tests that player._inventory._items and player._hp do not change
        rawInputMock = MagicMock(return_value="Enormous Potion")
        with patch('commands.use_potion_command.raw_input', create = True, new = rawInputMock):
            usePotionCmd.execute()
            
        errorMsg = "Inventory should still not have any potions."
        self.assertEqual(player._inventory.count(), 0, errorMsg)
        errorMsg = "player._hp changed when it should not have."
        self.assertEqual(player._hp, startingHp, errorMsg)
        
class WeaponTest(unittest.TestCase):
    """
    Tests Weapon class.
    """
    def testWeapon(self):
        from items.weapon import Weapon

        sword = Weapon("Sword", "A cheap sword", 3, 2, 1)

        self.assertEqual(sword.getName(), "Sword", "Name did not initialize correctly.")
        self.assertEqual(sword.getDescription(), "A cheap sword", "Description did not initialize correctly.")
        self.assertEqual(sword.getWeight(), 3, "Weight did not initialize correctly.")
        self.assertEqual(sword.getCost(), 2, "Cost did not initialize correctly.")
        self.assertEqual(sword.getAttack(), 1, "Damage did not initialize correctly.")
        
class ArmorTest(unittest.TestCase):
    """
    Tests Armor class.
    """
    def testArmor(self):
        from items.armor import Armor
        
        shield = Armor("Shield", "A cheap shield", 3, 2, 1)

        #Tests that shield initialized correctly
        self.assertEqual(shield.getName(), "Shield", "Name did not initialize correctly.")
        self.assertEqual(shield.getDescription(), "A cheap shield", "Description did not initialize correctly.")
        self.assertEqual(shield.getWeight(), 3, "Weight did not initialize correctly.")
        self.assertEqual(shield.getCost(), 2, "Cost did not initialize correctly.")
        self.assertEqual(shield.getDefense(), 1, "Defense did not initialize correctly.")

class Potion(unittest.TestCase):
    """
    Tests Potion class.
    """
    def testPotion(self):
        from items.potion import Potion

        potion = Potion("Potion", "A small potion", 3, 2, 1)
        
        #Tests for correct initialization
        self.assertEqual(potion.getName(), "Potion", "Name did not initialize correctly.")
        self.assertEqual(potion.getDescription(), "A small potion", "Description did not initialize correctly.")
        self.assertEqual(potion.getWeight(), 3, "Weight did not initialize correctly.")
        self.assertEqual(potion.getCost(), 2, "Cost did not initialize correctly.")
        self.assertEqual(potion.getHealing(), 1, "Healing did not initialize correctly.")

class PlayerTest(unittest.TestCase):
    """
    Tests Player class.
    """
    def testInit(self):
        from player import Player
        from space import Space
        import constants

        space = Space("Shire", "Home of the Hobbits", "Mordor")
        player = Player("Frodo", space)

        errorMsg = "Frodo", "player._name did not initialize correctly."
        self.assertEqual(player._name, "Frodo", errorMsg)
        errorMsg = "player._location did not initialize correctly."
        self.assertEqual(player._location, space, errorMsg)
        errorMsg = "player._money did not initialize correctly."
        self.assertEqual(player._money, constants.PlayerInitialization.MONEY, errorMsg)
        errorMsg = "player._experience was not intialized correctly."
        self.assertEqual(player._experience, constants.PlayerInitialization.EXPERIENCE, errorMsg)
        errorMsg = "player._level was not initialized correctly."
        self.assertEqual(player._level, constants.PlayerInitialization.LEVEL, errorMsg)
        
        errorMsg = "player._hp was not initialized correctly."
        self.assertEqual(player._hp, constants.PlayerInitialization.MAX_HP, errorMsg)
        errorMsg = "Player was not created with full health."
        self.assertEqual(player._maxHp, constants.PlayerInitialization.MAX_HP, errorMsg)
        errorMsg = "player_attack was not initialized correctly."
        self.assertEqual(player._attack, constants.PlayerInitialization.ATTACK, errorMsg)
        errorMsg = "player._weightLimit was not initialized correctly."
        self.assertEqual(player._weightLimit, constants.PlayerInitialization.WEIGHT_LIMIT, errorMsg)
        
        emptyList = []
        errorMsg = "player._inventory was not initialized correctly."
        self.assertEqual(player._inventory.getItems(), emptyList, errorMsg)
        errorMsg = "player._equipped was not initialized correctly."
        self.assertEqual(player._equipped.getItems(), emptyList, errorMsg)

        errorMsg = "player._weaponAttack was not initialized correctly."
        self.assertEqual(player._weaponAttack, constants.PlayerInitialization.WEAPON_ATTACK, errorMsg)
        errorMsg = "player._armorDefense was not initialized correctly."
        self.assertEqual(player._armorDefense, constants.PlayerInitialization.ARMOR_DEFENSE, errorMsg)
        
        errorMsg = "self._charmAttack did not initialize correctly."
        self.assertEqual(player._charmAttack, constants.PlayerInitialization.CHARM_ATTACK, errorMsg)
        errorMsg = "self._charmDefense did not initialize correctly."
        self.assertEqual(player._charmDefense, constants.PlayerInitialization.CHARM_DEFENSE, errorMsg)
        errorMsg = "self._charmHp did not initialize correctly."
        self.assertEqual(player._charmHp, constants.PlayerInitialization.CHARM_HP, errorMsg)
        
        errorMsg = "player._totalAttack did not initiate correctly."
        self.assertEqual(player._totalAttack, player._attack + player._weaponAttack + 
            player._charmAttack, errorMsg)
        errorMsg = "player._totalDefense did not initialize correctly."
        self.assertEqual(player._totalDefense, player._armorDefense + player._charmDefense, errorMsg)
        errorMsg = "player._totalMaxHp did not initialize correctly."
        self.assertEqual(player._totalMaxHp, player._maxHp + player._charmHp, errorMsg)
        
    def testAttack(self):
        from player import Player
        from space import Space
        from monsters.monster import Monster
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        monster = MagicMock()
        monster.takeAttack = MagicMock()
        
        #Player attacks monster
        player.attack(monster)
        errorMsg = "Player did not attack monster."
        self.assertTrue(monster.takeAttack.called, errorMsg)

    def testTakeAttack(self):
        """
        Tests player.takeAttack when attack is more than
        player._hp.
        """
        from player import Player
        from space import Space

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        
        OVERKILL = player._totalMaxHp + 10000

        player.takeAttack(OVERKILL)
        errorMsg = "player._hp should be 0 but is not."
        self.assertEqual(player._hp, 0, errorMsg)

    def testTakeAttack2(self):
        """
        Tests player.takeAttack when attack is less than
        player._hp
        """
        from player import Player
        from space import Space

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        
        UNDERKILL = player._totalMaxHp - 1

        player.takeAttack(UNDERKILL)
        errorMsg = "player._hp should be 1 but is not."
        self.assertEqual(player._hp, 1, errorMsg)

    def takeAttack3(self):
        """
        Tests player.takeAttack when player is equipped with
        armor.
        """
        from player import Player
        from space import Space
        from items.armor import Armor
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        armor = Armor("Shield of Faith", "Quenches fiery darts", 2, 2, 2)
        player.equip(armor)

        #Testcase - armorDefense is more than attack
        player._hp = 10
        player.takeAttack(1)
        errorMsg = "Testcase - armorDefense is more than attack failed."
        self.assertEqual(player._hp, 10, errorMsg)
        
        #Testcase - armorDefense is equal to attack
        player._hp = 10
        player.takeAttack(2)
        errorMsg = "Testcase - armorDefense is attack failed."
        self.assertEqual(player._hp, 10, errorMsg)
        
        #Testcase - armorDefense is less than attack
        player._hp = 10
        player.takeAttack(3)
        errorMsg = "Testcase - armorDefense is less than attack failed."
        self.assertEqual(player._hp, 9, errorMsg)
        
    def testIncreaseExperience(self):
        from player import Player
        from space import Space
        import constants

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)
        player._updateLevel = MagicMock()

        #Test that player._experience increases correctly and that _updateLevel() is called
        player.increaseExperience(10000)
        
        errorMsg = "Player experience failed to increase."
        self.assertEqual(player._experience, constants.PlayerInitialization.EXPERIENCE + 10000, errorMsg)
        errorMsg = "player._updateLevel() was not called."
        self.assertTrue(player._updateLevel.called, errorMsg)
        
    def testUpdateLevel(self):
        from math import floor
        
        from player import Player
        from space import Space
        import constants

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        #Determine default player stats
        defaultLevel = player._level
        defaultMaxHp = player._totalMaxHp
        defaultAttack = player._attack
        defaultTotalAttack = player._totalAttack

        #Increase player experience and run player._updateLevel
        originalExperience = player._experience
        player._experience = 10000 + originalExperience
        player._updateLevel()

        #Test that stats have increased
        errorMsg = "Player level did not increase."
        self.assertTrue(player._level > defaultLevel, errorMsg)
        errorMsg = "Player Hp did not increase."
        self.assertTrue(player._totalMaxHp > defaultMaxHp, errorMsg)
        errorMsg = "Player attack did not increase."
        self.assertTrue(player._attack > defaultAttack, errorMsg)
        errorMsg = "Player totalAttack did not increase."
        self.assertTrue(player._totalAttack > defaultTotalAttack, errorMsg)

        #Test for proper player stat change
        errorMsg = "Player level is incorrect."
        self.assertEqual(player._level, 20, errorMsg)
        errorMsg = "Player Hp is incorrect ; %s." 
        self.assertEqual(player._maxHp, 571, errorMsg)
        errorMsg = "Player attack is incorrect %s."
        self.assertEqual(player._attack, 105, errorMsg)
        
    def testHeal(self):
        """
        Where healing amount is more than the amount possible. 
        """
        from player import Player
        from space import Space

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        player._totalMaxHp = 10
        player._hp = 9
        healAmount = 1000
        
        player.heal(healAmount)

        self.assertEqual(player._hp, player._totalMaxHp, "Healing test #1 failed.")

    def testHeal2(self):
        """
        Where healing amount is less than the amount possible.
        """
        from player import Player
        from space import Space

        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        player._totalMaxHp = 10
        player._hp = 8
        healAmount = 1
        expectedHp = player._hp + healAmount
        
        player.heal(healAmount)

        self.assertEqual(player._hp, expectedHp, "Healing test #2 failed.")
        
    def testEquip(self):
        from player import Player
        from space import Space
        from items.item import Item
        from items.weapon import Weapon
        from items.armor import Armor
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        newItem = Item("Chainik Reakettle", "Makes good tea", 1, 1)
        newWeapon = Weapon("Gun of Hurlocker", "Oppressive, but friendly", 2, 3, 1)
        newArmor = Armor("Cookies of Miles", "Defends against sadness", 2, 4, 1)
        
        player.addToInventory(newItem)
        player.addToInventory(newWeapon)
        player.addToInventory(newArmor)

        #Pretest player-specific items-based attributes
        errorMsg = "_weaponAttack should be 0 but it is not."
        self.assertEqual(player._weaponAttack, 0, errorMsg)
        errorMsg = "_armorDefense should be 0 but it is not."
        self.assertEqual(player._armorDefense, 0, errorMsg)
        errorMsg = "_totalAttack should be simply attack but it is not."
        self.assertEqual(player._totalAttack, player._attack, errorMsg)

        #Attempt to equip items
        player.equip(newItem)
        self.assertFalse(newItem in player._equipped._items, "Equipped %s and should not have." % newItem)
        player.equip(newWeapon)
        self.assertTrue(newWeapon in player._equipped._items, "Failed to equip %s." % newWeapon)
        player.equip(newArmor)
        self.assertTrue(newArmor in player._equipped._items, "Failed to equip %s." % newArmor)

        #Test for change in player's items-specific attributes
        errorMsg = "player._weaponAttack should be newWeapon._attack but is not."
        self.assertEqual(player._weaponAttack, newWeapon._attack, errorMsg)
        errorMsg = "_armorDefense should be newArmor._defense but is not."
        self.assertEqual(player._armorDefense, newArmor._defense, errorMsg)
        errorMsg = "_totalAttack should have been updated but was not."
        self.assertEqual(player._totalAttack, player._attack + newWeapon._attack, errorMsg)

    def testUnequip(self):
        from player import Player
        from space import Space
        from items.item import Item
        from items.weapon import Weapon
        from items.armor import Armor
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        newItem = Item("Chainik Reakettle", "Makes good tea", 1, 1)
        newWeapon = Weapon("Gun of Hurlocker", "Oppressive, but friendly", 2, 3, 1)
        newArmor = Armor("Cookies of Miles", "Defends against sadness", 2, 4, 1)
        
        player.addToInventory(newItem)
        player.addToInventory(newWeapon)
        player.addToInventory(newArmor)

        player.equip(newWeapon)
        player.equip(newArmor)
        
        #Attempt to unequip items
        player.unequip(newWeapon)
        self.assertFalse(newWeapon in player._equipped._items, "Failed to unequip %s" % newWeapon)
        player.unequip(newArmor)
        self.assertFalse(newArmor in player._equipped._items, "Failed to unequip %s" % newArmor)

        #Check to see that item-specific attributes reset to defaults
        errorMsg = "player._weaponAttack should be 0 but it is not."
        self.assertEqual(player._weaponAttack, 0, errorMsg)
        errorMsg = "player._armorDefense should be 0 but it is not."
        self.assertEqual(player._armorDefense, 0, errorMsg)
        errorMsg = "totalAttack should be simply attack but it is not."
        self.assertEqual(player._totalAttack, player._attack, errorMsg)
        
    def testAddToInventory(self):
        from player import Player
        from space import Space
        from items.item import Item
        from items.weapon import Weapon
        from items.armor import Armor
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        newItem = Item("Chainik Reakettle", "Makes good tea", 0, 0)
        newWeapon = Weapon("Gun of Hurlocker", "Oppressive, but friendly", 0, 0, 0)
        newArmor = Armor("Cookies of Miles", "Defends against sadness", 0, 0, 0)

        player.addToInventory(newItem)
        player.addToInventory(newWeapon)
        player.addToInventory(newArmor)
        
        #Test add items to inventory
        errorMsg = "Failed to add item to inventory."
        self.assertTrue(newItem in player._inventory._items, errorMsg)
        self.assertTrue(newWeapon in player._inventory._items, errorMsg)
        self.assertTrue(newArmor in player._inventory._items, errorMsg)

    def testRemoveFromInventory(self):
        from player import Player
        from space import Space
        from items.item import Item
        from items.weapon import Weapon
        from items.armor import Armor
        from items.item_set import ItemSet
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        item = Item("Chainik Reakettle", "Makes good tea", 1, 1)
        weapon = Weapon("Gun of Hurlocker", "Oppressive, but friendly", 2, 3, 1)
        armor = Armor("Cookies of Miles", "Defends against sadness", 2, 4, 1)

        player.addToInventory(item)
        player.addToInventory(weapon)
        player.addToInventory(armor)

        player.equip(weapon)
        player.equip(armor)

        #Pretest: items in player._inventory        
        errorMsg = "Failed to initialize test character correctly."
        self.assertTrue(item in player._inventory._items, errorMsg)
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)

        #Testing player.removeFromInventory()
        player.removeFromInventory(item)
        player.removeFromInventory(weapon)
        player.removeFromInventory(armor)
        
        errorMsg = "Failed to remove item from inventory."
        self.assertFalse(item in player._inventory, errorMsg)
        self.assertFalse(weapon in player._inventory, errorMsg)
        self.assertFalse(armor in player._inventory, errorMsg)

        #Test that items get unequipped
        errorMsg = "Failed to remove item from equipped."
        self.assertFalse(weapon in player._equipped._items, errorMsg)
        self.assertFalse(armor in player._equipped._items, errorMsg)

        #Test that item-specific character attributes are reset to original values
        errorMsg = "player._weaponAttack should be 0 but it is not."
        self.assertEqual(player._weaponAttack, 0, errorMsg)
        errorMsg = "player._armorDefense should be 0 but it is not."
        self.assertEqual(player._armorDefense, 0, errorMsg)
        errorMsg = "player._totalAttack should be player._attack but it is not."
        self.assertEqual(player._totalAttack, player._attack, errorMsg)

    def testCanMoveDirection(self):
        """
        Tests if canMoveDirection() methods work.
        """
        from player import Player
        from space import Space
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("Frodo", space)

        north = Space("North Space", "Very cold", "Welcome")
        south = Space("South Space", "Very warm", "Welcome")
        east = Space("East Space", "Very mountainous", "Welcome")
        west = Space("West Space", "Coastal", "Welcome")

        #Pretest - no ports created
        errorMsg = "player.canMoveDirection() negative case failed."
        self.assertFalse(player.canMoveNorth(), errorMsg)
        self.assertFalse(player.canMoveSouth(), errorMsg)
        self.assertFalse(player.canMoveEast(), errorMsg)
        self.assertFalse(player.canMoveWest(), errorMsg)

        #Create ports 
        space.createExit("north", north, outgoingOnly = False)
        space.createExit("south", south, outgoingOnly = False)
        space.createExit("east", east, outgoingOnly = False)
        space.createExit("west", west, outgoingOnly = False)

        #Test that player-movement methods work
        errorMsg = "player.canMoveNorth() failed."
        self.assertTrue(player.canMoveNorth(), errorMsg)
        errorMsg = "player.canMoveSouth() failed."
        self.assertTrue(player.canMoveSouth(), errorMsg)
        errorMsg = "player.canMoveEast() failed."
        self.assertTrue(player.canMoveEast(), errorMsg)
        errorMsg = "player.canMoveWest() failed."
        self.assertTrue(player.canMoveWest(), errorMsg)

class InnTest(unittest.TestCase):
    """
    Tests Inn objects.

    Iterations:
    -For when player chooses to stay at inn and has money to do so.
    -For when player chooses to stay at inn and does not have money to do so.
    -For when player chooses not to stay at inn.
    -For invalid user input.
    """
    def testPositiveCase(self):
        """
        For when player chooses to stay at Inn and has enough money to do so.
        """
        from player import Player
        from space import Space
        from cities.inn import Inn
        from cities.city import City

        testInn = Inn("Chris' Testing Inn", "Come test here", "Hi", 5)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' Inn", testInn)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
                
        player._hp = 1
        player._money = 10

        #Player chooses to stay at the inn
        rawInputMock = MagicMock(side_effect = ["enter", "yes", "enter"])
        with patch('cities.inn.raw_input', create=True, new=rawInputMock):
            testInn.enter(player)
        
        #Test that player._money and player._hp are updated to correct values
        self.assertEqual(player._money, 5, "Player's money not decreased by correct amount.")
        self.assertEqual(player._hp, player._totalMaxHp, "Player's health not increased to full health.")
        
    def testNegativeCase2(self):
        """
        For when player chooses to stay at Inn and does not have enough money to do so.
        """
        from player import Player
        from space import Space
        from cities.inn import Inn
        from cities.city import City

        testInn = Inn("Chris' Testing Inn", "Come test here", "Hi", 5)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' Inn", testInn)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
                
        player._hp = 1
        player._money = 2

        #Player chooses to stay at the inn
        rawInputMock = MagicMock(side_effect = ["enter", "yes", "enter"])
        with patch('cities.inn.raw_input', create=True, new=rawInputMock):
            testInn.enter(player)
        
        #Test that player._money and player._hp do not change
        self.assertEqual(player._money, 2, "Player money changed when it should not have.")
        self.assertEqual(player._hp, 1, "Player's health changed when it should not have.")

    def testNegativeCase3(self):
        """
        For when player chooses not to stay at the inn.
        """
        from player import Player
        from space import Space
        from cities.inn import Inn
        from cities.city import City

        testInn = Inn("Chris' Testing Inn", "Come test here", "Hi", 5)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' Inn", testInn)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
                
        player._hp = 1
        player._money = 10

        #Player chooses not to stay at the inn
        rawInputMock = MagicMock(side_effect = ["enter", "no", "enter"])
        with patch('cities.inn.raw_input', create=True, new=rawInputMock):
            testInn.enter(player)
        
        #Test that player._money and player._hp do not change
        self.assertEqual(player._money, 10, "Player money changed when it should not have.")
        self.assertEqual(player._hp, 1, "Player's health changed when it should not have.")
        
    def testNegativeCase4(self):
        """
        For invalid user input.
        """
        from player import Player
        from space import Space
        from cities.inn import Inn
        from cities.city import City

        testInn = Inn("Chris' Testing Inn", "Come test here", "Hi", 5)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' Inn", testInn)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
        
        #For invalid user input
        rawInputMock = MagicMock(side_effect = ["enter", "gobbledigook", 
            "enter", "no", "enter"])
        with patch('cities.inn.raw_input', create=True, new=rawInputMock):
            testInn.enter(player)
        
class ShopSellItems(unittest.TestCase):
    """
    Tests Shop's ability to sell items.
    """
    def testPositiveCase(self):
        """
        Player sells three items.
        
        Components:
        -Items should be removed from player._inventory and player._equipped
        -player._money should be increased by half of the value of the items
        -Items should be added to shop wares at full cost
        """
        from player import Player
        from space import Space
        from cities.shop import Shop
        from cities.city import City
        from items.weapon import Weapon
        from items.armor import Armor
        from items.potion import Potion
        import constants
        
        testShop = Shop("Chris' Testing Shop", "Come test here", "Hi", constants.RegionType.ERIADOR, 5, 10)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' shop", testShop)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        testShop._items._items = []
        
        #Create starting inventory and equipment
        weapon = Weapon("Knife", "Jack of all trades", 3, 1, 1)
        armor = Armor("Leather Tunic", "Travel cloak", 3, 1, 1)
        potion = Potion("Potion", "Vodka", 3, 1, 1)

        inventory = player._inventory
        player.addToInventory(weapon)
        player.addToInventory(armor)
        player.addToInventory(potion)

        equipped = player.getEquipped()
        player.equip(weapon)
        player.equip(armor)

        #Test that that items are in player._inventory and player._equipped
        self.assertTrue(inventory.containsItemWithName("Knife"), "Knife not added to inventory.")
        self.assertTrue(inventory.containsItemWithName("Leather Tunic"), "Leather Tunic not added to inventory.")
        self.assertTrue(inventory.containsItemWithName("Potion"), "Potion not added to inventory.")
    
        errorMsg = "Player items were not equipped correctly."
        self.assertTrue(equipped.containsItem(weapon), errorMsg)
        self.assertTrue(equipped.containsItem(armor), errorMsg)
                        
        #Player chooses to sell items
        rawInputMock = MagicMock(side_effect = ["sell", "Knife", "yes", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
        rawInputMock = MagicMock(side_effect = ["sell", "Leather Tunic", "yes", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
        rawInputMock = MagicMock(side_effect = ["sell", "Potion", "yes", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
        
        #Test items no longer in player._inventory and player._equipped
        errorMsg = "Knife that was sold is still in inventory"
        self.assertFalse(inventory.containsItemWithName("Knife"), errorMsg)
        errorMsg = "Leather tunic that was sold is still in inventory"
        self.assertFalse(inventory.containsItemWithName("Leather Tunic"), errorMsg)
        errorMsg = "Potion that was sold is still in inventory"
        self.assertFalse(inventory.containsItemWithName("Potion"), errorMsg)

        errorMsg = "Knife that was sold is still in equipped"
        self.assertFalse(equipped.containsItemWithName("Knife"), errorMsg)
        errorMsg = "Leather tunic that was sold is still in equipped"
        self.assertFalse(equipped.containsItemWithName("Leather Tunic"), errorMsg)

        #Test that items now appear in shop wares
        errorMsg = "Items are now supposed to be in shop inventory but are not."
        self.assertTrue(weapon in testShop._items._items, errorMsg)
        self.assertTrue(armor in testShop._items._items, errorMsg)
        self.assertTrue(potion in testShop._items._items, errorMsg)

        #New shop wares' prices are set to full cost
        errorMsg = "Item costs not set back to full amount."
        for item in testShop._items._items:
            self.assertEqual(item._cost, 1, errorMsg)

        #Player's money should increase by the half the cost of the items - 1.5 in our case
        errorMsg = "player._money not increased to correct amount."
        self.assertEqual(player._money, 21.5, errorMsg)

    def testNegativeCase(self):
        """
        Testing that Shop can handle invalid user input.
        """
        from player import Player
        from space import Space
        from cities.shop import Shop
        from cities.city import City
        from items.item import Item
        import constants
        
        testShop = Shop("Chris' Testing Shop", "Come test here", "Hi", constants.RegionType.ERIADOR, 5, 10)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' shop", testShop)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        goldNugget = Item("Gold Nugget", "Potentially cheese!", 1, 1)
        player.addToInventory(goldNugget)

        #Test preconditions
        errorMsg = "goldNugget is supposed to be in player._inventory."
        self.assertTrue(goldNugget in player._inventory._items, errorMsg)

        #Player attempts to sell an invalid item
        rawInputMock = MagicMock(side_effect = ["sell", "gobbledigook", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)

        #Player gives invalid input when prompted to confirm item sell
        rawInputMock = MagicMock(side_effect = ["sell", "Gold Nugget", "enter", "gobbledigook", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
            
class ShopPurchaseItems(unittest.TestCase):
    """
    Tests Shop's ability to allow for item purchases. 
    """
    def testPositiveCase(self):
        """
        Player purchases three items.

        Testing:
        -Items in inventory
        -Items not in equipped
        -Items not in shop wares
        -player._money updated correctly
        """
        from player import Player
        from space import Space
        from cities.shop import Shop
        from cities.city import City
        from items.weapon import Weapon
        from items.armor import Armor
        from items.potion import Potion

        testShop = Shop("Chris' Testing Shop", "Come test here", "Hi", "Shire", 0, 10)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' shop", testShop)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        player._money = 20
        
        testWeapon = Weapon("Knife", "Russian", 1, 1, 1)
        testArmor = Armor("Shield of Faith", "Also Russian", 1, 1, 1)
        testPotion = Potion("Medium Potion of Healing", "A good concoction. Made by Master Wang.", 1, 5, 3)
        testShop._items.addItem(testWeapon)
        testShop._items.addItem(testArmor)
        testShop._items.addItem(testPotion)

        #Test preconditions
        errorMsg = "Player does not start with 20 rubles."
        self.assertEqual(player._money, 20, errorMsg)
        errorMsg = "Our test shop was generated with the wrong number of items."
        self.assertEqual(testShop._items.count(), 3, errorMsg)
        errorMsg = "Items in shop inventory are of the wrong type."
        for item in testShop._items._items:
            self.assertTrue(isinstance(item, Weapon) or isinstance(item, Armor) or isinstance(item, Potion), errorMsg)

        #Player purchases items
        rawInputMock = MagicMock(side_effect = ["purchase", "Knife", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
        rawInputMock = MagicMock(side_effect = ["purchase", "Shield of Faith", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
        rawInputMock = MagicMock(side_effect = ["purchase", "Medium Potion of Healing", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)
       
        #Test items in inventory
        errorMsg = "Knife that was purchased was not added to inventory."
        self.assertTrue(player._inventory.containsItemWithName("Knife"), errorMsg)
        errorMsg = "Shield of Faith that was purchased was not added to inventory."
        self.assertTrue(player._inventory.containsItemWithName("Shield of Faith"), errorMsg)
        errorMsg = "Medium Potion that was purchased was not added to inventory."
        self.assertTrue(player._inventory.containsItemWithName("Medium Potion of Healing"), errorMsg)

        #Test items not in equipped
        errorMsg = "Knife that was purchased is in equipped."
        self.assertFalse(player._equipped.containsItemWithName("Knife"), errorMsg)
        errorMsg = "Shield of Faith that was purchased is in equipped."
        self.assertFalse(player._equipped.containsItemWithName("Shield of Faith"), errorMsg)
        errorMsg = "Medium Potion that was purchased is in equipped."
        self.assertFalse(player._equipped.containsItemWithName("Medium Potion of Healing"), errorMsg)
        
        #Test items not in shop wares
        errorMsg = "Knife that was purchased is still in shop wares."
        self.assertFalse(testPotion in testShop._items._items, errorMsg)
        errorMsg = "Shield of Faith that was purchased is still in shop wares."
        self.assertFalse(testPotion in testShop._items._items, errorMsg)
        errorMsg = "Medium Potion that was purchased is still in shop wares."
        self.assertFalse(testPotion in testShop._items._items, errorMsg)
        
        #player._money should decrease by the cost of the purchases, which is 5
        errorMsg = "player._money not decreased by correct amount."
        self.assertEqual(player._money, 13, errorMsg)
        
    def testNegativeCase(self):
        """
        Player attempts to purchase an item that is too expensive.

        Testing:
        -Item not in inventory
        -Item not in equipped
        -Item in shop wares
        -player._money unchanged
        """
        from player import Player
        from space import Space
        from cities.shop import Shop
        from cities.city import City
        from items.potion import Potion

        testShop = Shop("Chris' Testing Shop", "Come test here", "Hi", "Shire", 0, 10)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' shop", testShop)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        player._money = 20    

        testPotion = Potion("SuperDuperLegendary Potion", "A Wang concoction. Made by Master Wang.", 1, 35, 1000)
        testShop._items.addItem(testPotion)
        
        #Test preconditions
        errorMsg = "Player does not start with 20 rubles."
        self.assertEqual(player._money, 20, errorMsg)
        errorMsg = "Our test shop was generated with the wrong number of items."
        self.assertEqual(testShop._items.count(), 1, errorMsg)
        errorMsg = "SuperDuperLegendary Potion not in testShop._items."
        self.assertTrue(testPotion in testShop._items._items, errorMsg)
        
        #Player attempts to purchase potion
        rawInputMock = MagicMock(side_effect = ["purchase", "SuperDuperLegendary Potion of Healing", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)

        #Test potion not in inventory, not in equipped, in shop wares
        errorMsg = "SuperDuperLegendary Potion of Healing that was purchased was added to inventory."
        self.assertFalse(player._inventory.containsItemWithName("SuperDuperLegendary Potion of Healing"), errorMsg)
        errorMsg = "SuperDuperLegendary Potion of Healing that was purchased is in equipped."
        self.assertFalse(player._equipped.containsItemWithName("SuperDuperLegendary Potion of Healing"), errorMsg)
        errorMsg = "SuperDuperLegendary Potion of Healing that was purchased is no longer in shop wares."
        self.assertTrue(testPotion in testShop._items._items, errorMsg)
        
        #player._money should be unchanged
        errorMsg = "player._money changed when it was not supposed to."
        self.assertEqual(player._money, 20, errorMsg)

    def testNegativeCase2(self):
        """
        Player attempts to purchase an item that does not exist.

        Testing:
        -Inventory unchanged
        -Equipment unchanged
        -Shop wares unchanged
        -player._money unchanged
        """
        from player import Player
        from space import Space
        from cities.shop import Shop
        from cities.city import City
        from items.potion import Potion

        testShop = Shop("Chris' Testing Shop", "Come test here", "Hi", "Shire", 0, 10)
        testCity = City("Test City", "Testing city", "Hello to testing city. See Chris' shop", testShop)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        player._money = 20    

        #Test preconditions
        errorMsg = "Player does not start with 20 rubles."
        self.assertEqual(player._money, 20, errorMsg)
        errorMsg = "Player inventory should be empty."
        self.assertEqual(len(player._inventory._items), 0, errorMsg)
        errorMsg = "Player equipment should be empty."
        self.assertEqual(len(player._inventory._items), 0, errorMsg)
        errorMsg = "Our test shop was generated with the wrong number of items."
        self.assertEqual(testShop._items.count(), 0, errorMsg)

        #Player attempts to purchase a non-existent item
        rawInputMock = MagicMock(side_effect = ["purchase", "gobbledigook", "enter", "quit", "enter"])
        with patch('cities.shop.raw_input', create = True, new = rawInputMock):
            testShop.enter(player)

        #Inventory, equipment, and shop wares should be unchanged
        errorMsg = "Player inventory changed when it should not have."
        self.assertEqual(len(player._inventory._items), 0, errorMsg)
        errorMsg = "Player equipment changed when it should not have."
        self.assertEqual(len(player._equipped._items), 0, errorMsg)
        errorMsg = "Shop wares changed when it should not have."
        self.assertEqual(testShop._items.count(), 0, errorMsg)
         
        #player._money should not change
        errorMsg = "Player's money incorrectly decreased when purchasing invalid item."
        self.assertEqual(player._money, 20, errorMsg)

class Square(unittest.TestCase):
    """
    Tests square buildings.
    """
    def testPositiveCase(self):
        """
        Player talks to various people in Square.

        Testing:
        -Person has several items to give (Master Wang).
        -Person has one item to give (Miles).
        -Person has no items to give (Putin).
        """
        from player import Player
        from space import Space
        from cities.square import Square
        from cities.city import City
        from items.weapon import Weapon
        from items.armor import Armor
        from items.potion import Potion
        from items.item import Item

        weapon = Weapon("Sword of the Spirit", "Sharper than any double-edged sword", 1, 1, 1)
        armor = Armor("Shield of Faith", "Quenches fiery darts", 1, 1, 1)
        potion = Potion("Leaves from Tree of Life", "For healing the nations", 1, 1, 1)
        cookies = Item("Miles' Famous Cookies", "Gross this time", 1, 1)
        
        talk = {"Master Wang": "I am Master Wang, creator various things in this Lord of the Rings game", "Miles": "Hello, I am Miles, the cookie legend", "Putin": "Oppression, engage...."}
        items = {"Master Wang": [weapon, armor, potion], "Miles": cookies}
        testSquare = Square("Chris' Testing Square", "Testing Square", "Come test here", talk, items)
        
        testCity = City("Test City", "Testing city", "Hello to Test City. See Chris' Square", testSquare)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
        inventory = player._inventory
        
        #Test: talking to Master Wang (several items to give)
        rawInputMock = MagicMock(side_effect = ["Master Wang", "enter", "quit", "enter"])
        with patch('cities.square.raw_input', create = True, new = rawInputMock):
            testSquare.enter(player)

        #Check that Master Wang's items are now in inventory
        errorMsg = "Weapon is supposed to be in inventory but is not."
        self.assertTrue(weapon in inventory, errorMsg)
        errorMsg = "Armor is supposed to be in inventory but is not."
        self.assertTrue(armor in inventory, errorMsg)
        errorMsg = "Potion is supposed to be in inventory but is not."
        self.assertTrue(potion in inventory, errorMsg)

        #Check that items are no longer in square._items
        errorMsg = "Weapon is not supposed to be in testSquare._items but is."
        self.assertFalse(weapon in testSquare._items, errorMsg)
        errorMsg = "Armor is not supposed to be in testSquare._items but is."
        self.assertFalse(armor in testSquare._items, errorMsg)
        errorMsg = "Potion is not supposed to be in testSquare._items but is."
        self.assertFalse(potion in testSquare._items, errorMsg)
        
        #Test: talking to Miles (one item to give)
        rawInputMock = MagicMock(side_effect = ["Miles", "enter", "quit", "enter"])
        with patch('cities.square.raw_input', create = True, new = rawInputMock):
            testSquare.enter(player)

        #Check that item associated with Miles is now in inventory
        errorMsg = "Cookies is supposed to be in inventory but is not."
        self.assertTrue(cookies in inventory, errorMsg)

        #Check that item is no longer in square._items
        errorMsg = "Cookies is not supposed to be in testSquare._items but is."
        self.assertFalse(cookies in testSquare._items, errorMsg)

        #Test: talking to Putin (no items to give)
        rawInputMock = MagicMock(side_effect = ["Putin", "enter", "quit", "enter"])
        with patch('cities.square.raw_input', create = True, new = rawInputMock):
            testSquare.enter(player)
            
    def testNegativeCase(self):
        """
        Player attempts to talk to invalid person.
        """
        from player import Player
        from space import Space
        from cities.square import Square
        from cities.city import City
        
        talk = {}
        items = {}
        testSquare = Square("Chris' Testing Square", "Testing Square", "Come test here", talk, items)
        
        testCity = City("Test City", "Testing city", "Hello to Test City. See Chris' Square", testSquare)
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)
        
        rawInputMock = MagicMock(side_effect = ["gobbledigook", "enter", "quit", "enter"])
        with patch('cities.square.raw_input', create = True, new = rawInputMock):
            testSquare.enter(player)
            
class City(unittest.TestCase):
    """
    Tests City's ability to handle a series of commands.

    The series of commands:
    -Player enters City, enters Inn, leaves Inn, leaves City.
    -Player enters City, enters Shop, leaves Shop, leaves City.
    -Player enters City, enters Square, leaves Square.
    -Player "gobbledigooks", leave City.
    """
    def testCity(self):
        from player import Player
        from space import Space
        from cities.city import City
        from cities.inn import Inn
        from cities.shop import Shop
        from cities.square import Square
        import constants
        
        testInn = Inn("Seth N' Breakfast Test Inn", "Testing inn", "Come test here", 3)
        testShop = Shop("Pookie Tea Shop", "Full of chi hua-huas", "Moofey, moofey meep", constants.RegionType.ERIADOR, 5, 5)
        testSquare = Square("Chocolate Mountain", "Origin of Chocolate Rain", "Meepey, meepey moof")
        testCity = City("TestCity", "Chris' unique testing city", "Come test here", buildings = [testInn, testShop, testSquare])
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity)
        player = Player("Frodo", space)

        #Test that City can handle a series of commands
        cityInputMock = MagicMock(side_effect = ["Seth N' Breakfast Test Inn", "leave", "Pookie Tea Shop",
            "leave", "Chocolate Mountain", "gobbledigook", "leave"])
        innInputMock = MagicMock(side_effect = ["no"])
        shopInputMock = MagicMock(side_effect = ["quit"])
        squareInputMock = MagicMock(side_effect = ["quit"])
        
        with patch('cities.city.raw_input', create = True, new = cityInputMock):
            with patch('cities.inn.raw_input', create = True, new = innInputMock):
                testCity.enter(player)
            with patch('cities.shop.raw_input', create = True, new = shopInputMock):
                testCity.enter(player)
            with patch('cities.square.raw_input', create = True, new = squareInputMock):
                testCity.enter(player)
        
class UniquePlace(unittest.TestCase):
    """
    Tests for correct UniquePlace initialization.
    """
    def testInit(self):
        from unique_place import UniquePlace

        testUniquePlace = UniquePlace("Chris' Unique Testing Room", "Come test here", "Here's some chocolate for coming")

        errorMsg = "testUniquePlace._name was not initialized correctly."
        self.assertEqual(testUniquePlace._name, "Chris' Unique Testing Room", errorMsg)
        errorMsg = "testUniquePlace._description was not initialized correctly."
        self.assertEqual(testUniquePlace._description, "Come test here", errorMsg)
        errorMsg = "testUniquePlace._greetings was not initialized correctly."
        self.assertEqual(testUniquePlace._greetings, "Here's some chocolate for coming", errorMsg)

class EnterCommand(unittest.TestCase):
    """
    Tests for Enter Command. In these tests, player enters
    different combinations of places.

    Iterations:
    -testPositiveCase:     one city and one unique place to enter.
    -testPositiveCase2:    multiple cities and one unique place to enter.
    -testPositiveCase3:    one city and multiple cities to enter.
    -testPositiveCase4:    multiple cities and multiple unique places to enter.
    -testNegativeCase:     no destinations to enter.
    -testNegativeCase2:    places to enter, invalid user input.
    """
    def testPositiveCase(self):
        """
        One city and one unique place to enter.

        Player chooses to:
        -Enter City, leave
        -Enter UniquePlace
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace
        
        testCity = City("Jim's Mobile Fun City", "Jim's unique testing city", "Come test here")
        testUniquePlace = UniquePlace("Master Wang's Magical Testing Place", "Come test here", "Hi I'm made of cheese.")
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity, uniquePlace = testUniquePlace)
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)
        
        #Testing enter command's ability to execute a series of commands
        spaceInputMock = MagicMock(side_effect = 
            ["Jim's Mobile Fun City", "Master Wang's Magical Testing Place"])
        cityInputMock = MagicMock(side_effect = ["enter", "leave", "enter", "leave"])
        
        with patch('commands.enter_command.raw_input', create = True, new = spaceInputMock):
            with patch('cities.city.raw_input', create = True, new = cityInputMock):
                enterCmd.execute()

    def testPositiveCase2(self):
        """
        Multiple cities and one unique place to enter.

        Player choses to:
        -Enter City, leave
        -Enter City, leave
        -Enter City, leave
        -Enter UniquePlace
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace
        
        testCity1 = City("Jim's Mobile Fun City", "Jim's unique testing city", "Come test here")
        testCity2 = City("Seth's Sans-Shabbiness Shack Sh-City", "Seth's unique testing city", "Come test here")
        testCity3 = City("Miles' Magical Cookie Jail City", "Miles' unique testing city", "Come test here")
        testUniquePlace = UniquePlace("Master Wang's Magical Testing Place", "Come test here", "Hi I'm made of cheese.")
        
        space = Space("Shire", "Home of the Hobbits", "Mordor",
            city = [testCity1, testCity2, testCity3], uniquePlace = testUniquePlace)
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)

        #Testing enter command's ability to execute a series of commands
        spaceInputMock = MagicMock(side_effect = 
            ["Jim's Mobile Fun City", "Seth's Sans-Shabbiness Shack Sh-City", 
            "Miles' Magical Cookie Jail City", "Master Wang's Magical Testing Place"])
        cityInputMock = MagicMock(side_effect = ["enter", "leave", "enter", "leave",
            "enter", "leave", "enter", "leave"])
        with patch('commands.enter_command.raw_input', create = True, new = spaceInputMock):
            with patch('cities.city.raw_input', create = True, new = cityInputMock):
                enterCmd.execute()

    def testPositiveCase3(self):
        """
        One city and multiple cities to enter.

        Player choses to:
        -Enter City, leave
        -Enter UniquePlace
        -Enter UniquePlace
        -Enter UniquePlace
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace
        
        testCity = City("Jim's Mobile Fun City", "Jim's unique testing city", "Come test here")
        testUniquePlace1 = UniquePlace("Master Wang's Magical Testing Place", "Come test here", "Hi I'm made of cheese.")
        testUniquePlace2 = UniquePlace("Jim's Magic Castle of Time-Shifting", "Many different colours", "What time is it?")
        testUniquePlace3 = UniquePlace("Russian Armadillo Mound", "Where Texas meets Russia", "I'm confused.")
        
        space = Space("Shire", "Home of the Hobbits", "Mordor",
            city = testCity, uniquePlace = [testUniquePlace1, testUniquePlace2, testUniquePlace3])
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)

        #Testing enter command's ability to execute a series of commands
        spaceInputMock = MagicMock(side_effect = 
            ["Jim's Mobile Fun City", "Master Wang's Magical Testing Place", 
            "Jim's Magic Castle of Time-Shifting", "Russian Armadillo Mound"])
        cityInputMock = MagicMock(side_effect = ["enter", "leave", "enter",
            "leave", "enter", "leave", "enter", "leave"])
        with patch('commands.enter_command.raw_input', create = True, new = spaceInputMock):
            with patch('cities.city.raw_input', create = True, new = cityInputMock):
                enterCmd.execute()

    def testPositiveCase4(self):
        """
        Multiple cities and multiple unique places to enter.

        Player choses to:
        -Enter City, leave
        -Enter City, leave
        -Enter City, leave
        -Enter UniquePlace
        -Enter UniquePlace
        -Enter UniquePlace
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace
        
        testCity1 = City("Jim's Mobile Fun City", "Jim's unique testing city", "Come test here")
        testCity2 = City("Seth's Sans-Shabbiness Shack Sh-City", "Seth's unique testing city", "Come test here")
        testCity3 = City("Miles' Magical Cookie Jail City", "Miles' unique testing city", "Come test here")
        testUniquePlace1 = UniquePlace("Master Wang's Magical Testing Place", "Come test here", "Hi I'm made of cheese.")
        testUniquePlace2 = UniquePlace("Jim's Magic Castle of Time-Shifting", "Many different colours", "What time is it?")
        testUniquePlace3 = UniquePlace("Russian Armadillo Mound", "Where Texas meets Russia", "I'm confused.")
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor",
            city = [testCity1, testCity2, testCity3], uniquePlace = [testUniquePlace1, testUniquePlace2, testUniquePlace3])
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)

        #Testing enter command's ability to execute a series of commands
        spaceInputMock = MagicMock(side_effect = 
            ["Jim's Mobile Fun City", "Seth's Sans-Shabbiness Shack Sh-City", 
            "Miles' Magical Cookie Jail City", "Master Wang's Magical Testing Place",
            "Jim's Magic Castle of Time-Shifting", "Russian Armadillo Mound"])
        cityInputMock = MagicMock(side_effect = ["enter", "leave", "enter", "leave", "enter", "leave", "enter", "leave"])
        with patch('commands.enter_command.raw_input', create = True, new = spaceInputMock):
            with patch('cities.city.raw_input', create = True, new = cityInputMock):
                enterCmd.execute()
                
    def testNegativeCase(self):
        """
        Trying to enter when there are no possible destinations.
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from space import Space
        
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)

        rawInputMock = MagicMock(side_effect = ["enter"])
        with patch('commands.enter_command.raw_input', create = True, new = rawInputMock):
            enterCmd.execute()
            
    def testNegativeCase2(self):
        """
        Trying to enter where there are valid destinations but
        user gives inputs a place that does not exist.
        """
        from commands.enter_command import EnterCommand
        from player import Player
        from cities.city import City
        from space import Space

        testCity = City("Jim's Mobile Fun City", "Jim's unique testing city", "Come test here")
        space = Space("Shire", "Home of the Hobbits.", "Mordor", testCity)
        player = Player("The Funlaps", space)
        enterCmd = EnterCommand("Enter Command", "Tests Entering", player)

        rawInputMock = MagicMock(side_effect = ["enter", "gobbledigook", "cancel"])
        with patch('commands.enter_command.raw_input', create = True, new = rawInputMock):
            enterCmd.execute()

class DescribeCommand(unittest.TestCase):
    """
    Tests Describe Command.
    
    Iterations:
    -With no cities/unique places.
    -With one city and one unique place.
    -With multiple cities and multiple unique places.
    """
    def testCase(self):
        from commands.describe_command import DescribeCommand
        from player import Player
        from space import Space

        #With no cities/unique places
        space = Space("Shire", "Home of the Hobbits.", "Mordor")
        player = Player("The Bagginses", space)
        describeCmd = DescribeCommand("Test Describe Command", "Tests describing", player)
        
        describeCmd.execute()
    
    def testCase2(self):
        from commands.describe_command import DescribeCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace

        #With one city and one unique place
        testCity = City("Master Wang's Oriental Fun City", "Chris's testing city", "Come test here")
        testUniquePlace = UniquePlace("The UniquePlace of Testing", "Weird things sometimes happen when you test.", "Welcome to UniquePlace of Testing.")
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = testCity, uniquePlace = testUniquePlace)
        player = Player("The Bagginses", space)
        describeCmd = DescribeCommand("Test Describe Command", "Tests describing", player)
        
        describeCmd.execute()

    def testCase3(self):
        from commands.describe_command import DescribeCommand
        from player import Player
        from space import Space
        from cities.city import City
        from unique_place import UniquePlace

        #With multiple cities and multiple unique places
        testCity1 = City("Master Wang's Oriental Fun City", "Chris' unique testing city", "Come test here")
        testCity2 = City("Chocolate Mountain", "Next to Vanilla Mountain", "Hi I'm Jim")
        testUniquePlace1 = UniquePlace("The UniquePlace of Testing", "Weird things sometimes happen when you test.", "Welcome to UniquePlace of Testing.")
        testUniquePlace2 = UniquePlace("Ukraine", "Not in great shape", "Welcome to Ukraine")
        space = Space("Shire", "Home of the Hobbits.", "Mordor", city = [testCity1, testCity2], uniquePlace = [testUniquePlace1, testUniquePlace2])
        player = Player("The Bagginses", space)
        describeCmd = DescribeCommand("Test Describe Command", "Tests describing", player)
        
        describeCmd.execute()

class CheckEquipmentCommand(unittest.TestCase):
    """
    Checks that "check equipment" does not crash the game.

    Testing:
    -Does not crash game when player has no equipped items.
    -Does not crash game when player has equipped items.
    """
    def testCase1(self):
        from space import Space
        from commands.check_equipment_command import CheckEquipmentCommand
        from player import Player

        space = Space("Shire", "Full of chocolate", "Mordor")
        player = Player("Russian", space)
        checkEquipmentCmd = CheckEquipmentCommand("Check Equipment Command", "Test command", player)

        checkEquipmentCmd.execute()

    def testCase2(self):
        from space import Space
        from commands.check_equipment_command import CheckEquipmentCommand
        from player import Player
        from items.weapon import Weapon
        from items.armor import Armor

        space = Space("Shire", "Full of chocolate", "Mordor")
        player = Player("Russian", space)
        weapon = Weapon("Sword of the Spirit", "Divides soul and spirit", 3, 3, 3)
        armor = Armor("Shield of Faith", "For fiery darts", 3, 3, 3)
        checkEquipmentCmd = CheckEquipmentCommand("Check Equipment Command", "Test command", player)

        player._equipped._items = [weapon, armor]

        checkEquipmentCmd.execute()

class CheckInventoryCommand(unittest.TestCase):
    """
    Checks that "check inventory" does not crash the game given
    a sample of potential inventories.

    Testing:
    -Does not crash with an empty inventory.
    -Does not crash with equipment.
    -Does not crash with a combination of equipment and items.
    """
    def testCase1(self):
        #For empty inventory
        from space import Space
        from player import Player
        from commands.check_inventory_command import CheckInventoryCommand

        space = Space("Chocolate Mountain", "Home of Chocolate Rain", "Mordor")
        player = Player("Russian", space)
        checkInventoryCmd = CheckInventoryCommand("Check Inventory Command", "Test command", player)

        checkInventoryCmd.execute()

    def testCase2(self):
        #With equipment in inventory
        from space import Space
        from player import Player
        from commands.check_inventory_command import CheckInventoryCommand
        from items.armor import Armor
        from items.weapon import Weapon

        space = Space("Chocolate Mountain", "Home of Chocolate Rain", "Mordor")
        player = Player("Russian", space)
        checkInventoryCmd = CheckInventoryCommand("Check Inventory Command", "Test command", player)
        weapon = Weapon("Sword of the Spirit", "Divides soul and spirit", 2, 2, 2)
        armor = Armor("Breastplate of Righteousness", "Made of light", 2, 2, 2)

        player.addToInventory(weapon)
        player.addToInventory(armor)

        errorMsg = "weapon and armor should be in player._inventory._items"
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)
        
        checkInventoryCmd.execute()
        
    def testCase3(self):
        #With equipment and arbitrary items in inventory
        from space import Space
        from player import Player
        from commands.check_inventory_command import CheckInventoryCommand
        from items.armor import Armor
        from items.weapon import Weapon
        from items.potion import Potion
        from items.item import Item

        space = Space("Chocolate Mountain", "Home of Chocolate Rain", "Mordor")
        player = Player("Russian", space)
        checkInventoryCmd = CheckInventoryCommand("Check Inventory Command", "Test command", player)
        
        weapon = Weapon("Sword of the Spirit", "Divides soul and spirit", 0, 0, 0)
        armor = Armor("Breastplate of Righteousness", "Made of light", 0, 0, 0)
        potion = Potion("Vodka", "Russian's favorite", 0, 0, 0)
        item = Item("Piece of Cardboard", "For arts and crafts", 0, 0)
        item2 = Item("Scotch Tape", "School supplies", 0, 0)

        player.addToInventory(weapon)
        player.addToInventory(armor)
        player.addToInventory(potion)
        player.addToInventory(item)
        player.addToInventory(item2)

        errorMsg = "Testing inventory was initialized incorrectly."
        self.assertTrue(weapon in player._inventory._items, errorMsg)
        self.assertTrue(armor in player._inventory._items, errorMsg)
        self.assertTrue(potion in player._inventory._items, errorMsg)
        self.assertTrue(item in player._inventory._items, errorMsg)
        self.assertTrue(item2 in player._inventory._items, errorMsg)
        
        checkInventoryCmd.execute()

class CheckMoneyCommand(unittest.TestCase):
    """
    Checks that "check money" does not crash the game.
    """
    def testCase(self):
        from space import Space
        from player import Player
        from commands.check_money_command import CheckMoneyCommand

        space = Space("Chocolate Mountain", "Home of Chocolate Rain", "Mordor")
        player = Player("Russian", space)
        checkMoneyCmd = CheckMoneyCommand("Check Money Command", "Test command", player)

        checkMoneyCmd.execute()

class CheckStatsCommand(unittest.TestCase):
    """
    Checks that "check stats" does not crash the game from a variety of
    different locations across the game map.
    """
    def testCase(self):
        from space import Space
        from player import Player
        from commands.check_stats_command import CheckStatsCommand

        space = Space("Chocolate Mountain", "Home of Chocolate Rain", "Mordor")
        player = Player("Russian", space)
        checkStatsCmd = CheckStatsCommand("Check Stats Command", "Test command", player)

        checkStatsCmd.execute()

class CheckMapCommand(unittest.TestCase):
    """
    Checks that running MapCommand does not crash the game.
    """
    def testCase(self):
        """
        Tests whether game crashes when ports exist in all four directions.
        """
        from space import Space
        from player import Player
        from commands.map_command import MapCommand

        #Create dummy world map
        central = Space("Central", "Center Space", "Mordor")
        north = Space("North", "North Space", "Mordor")
        south = Space("South", "South Space", "Mordor")
        east = Space("East", "East Space", "Mordor")
        west = Space("West", "West Space", "Mordor")
        
        #Link dummy spaces
        central.createExit("north", north, outgoingOnly = False)
        central.createExit("south", south, outgoingOnly = False)
        central.createExit("east", east, outgoingOnly = False)
        central.createExit("west", west, outgoingOnly = False)
        
        player = Player("Russian", central)
        mapCmd = MapCommand("Map Command", "Test command", player)

        #Execute mapCmd on a variety of player locations
        mapCmd.execute()
        
        player._location = north
        mapCmd.execute()
        
        player._location = south
        mapCmd.execute()
        
        player._location = east
        mapCmd.execute()
        
        player._location = west
        mapCmd.execute()
        
    def testCase2(self):
        """
        Tests whether game crashes when multiple ports exist in all four 
        directions.
        """
        from space import Space
        from player import Player
        from commands.map_command import MapCommand

        #Create dummy world map
        central = Space("Central", "Center Space", "Mordor")
        north = Space("North", "North Space", "Mordor")
        north2 = Space("North2", "North Space2", "Mordor")
        south = Space("South", "South Space", "Mordor")
        south2 = Space("South2", "South Space2", "Mordor")
        east = Space("East", "East Space", "Mordor")
        east2 = Space("East2", "East Space2", "Mordor")
        west = Space("West", "West Space", "Mordor")
        west2 = Space("West2", "West Space2", "Mordor")
        
        #Link dummy spaces
        central.createExit("north", north, outgoingOnly = False)
        central.createExit("south", south, outgoingOnly = False)
        central.createExit("east", east, outgoingOnly = False)
        central.createExit("west", west, outgoingOnly = False)
        central.createExit("north", north2, outgoingOnly = False)
        central.createExit("south", south2, outgoingOnly = False)
        central.createExit("east", east2, outgoingOnly = False)
        central.createExit("west", west2, outgoingOnly = False)
        
        player = Player("Russian", central)
        mapCmd = MapCommand("Map Command", "Test command", player)

        #Execute mapCmd on a variety of player locations
        mapCmd.execute()
        
        player._location = north
        mapCmd.execute()
        
        player._location = south
        mapCmd.execute()
        
        player._location = east
        mapCmd.execute()
        
        player._location = west
        mapCmd.execute()
        
        player._location = north2
        mapCmd.execute()
        
        player._location = south2
        mapCmd.execute()
        
        player._location = east2
        mapCmd.execute()
        
        player._location = west2
        mapCmd.execute()
        
class monster(unittest.TestCase):
    """
    Tests Monster objects.
    """
    def testInit(self):
        from monsters.monster import Monster

        monster = Monster("Jack", "@$$", [10, 5, 7], "Moof", "Meep")

        #Test monster initialized correctly
        errorMsg = "monster._name should be 'Jack'"
        self.assertEqual(monster._name, "Jack", errorMsg)
        errorMsg = "monster._description should be '@$$'"
        self.assertEqual(monster._description, "@$$", errorMsg)
        errorMsg = "monster._hp should be 10"
        self.assertEqual(monster._hp, 10, errorMsg)
        errorMsg = "monster._attack should be 5"
        self.assertEqual(monster._attack, 5, errorMsg)
        errorMsg = "monster._experience should be 7"
        self.assertEqual(monster._experience, 7, errorMsg)
        errorMsg = "monster._attackString sound be 'Moof'"
        self.assertEqual(monster._attackString, "Moof", errorMsg)
        errorMsg = "monster._deathString should be 'Meep'"
        self.assertEqual(monster._deathString, "Meep", errorMsg)

    def testAttack(self):
        from monsters.monster import Monster

        monster = Monster("Jack", "@$$", [10, 5, 7], "Moof", "Meep")
        
        player = MagicMock()
        player.takeAttack = MagicMock()

        #Test monster.attack()
        monster.attack(player)
        errorMsg = "monster.attack() failed to carry attack to player."
        player.takeAttack.assert_called_with(5)

    def testTakeAttack(self):
        from monsters.monster import Monster

        monster = Monster("Jack", "@$$", [10, 5, 7], "Moof", "Meep")

        #Test monster.takeAttack() - attack is less than total hp
        monster.takeAttack(3)
        errorMsg = "monster.takeAttack() testcase #1 failed."
        self.assertEqual(monster._hp, 7, errorMsg)

        #Test monster.takeAttack() - attack is more than total hp
        monster.takeAttack(1000)
        errorMsg = "monster.takeAttack() testcase #2 failed"
        self.assertEqual(monster._hp, 0, errorMsg)

class monsterFactory(unittest.TestCase):
    """
    Tests monster_factory's getMonsters().
    
    Testing:
    -Number spawn equals base when bonusDifficulty is set to zero.
    -That monster stats are base stats given zero bonusDifficulty.
    -That monster stats increase as a percentage over default as
    bonusDifficulty increases.
    -That regional distributions are present with monster spawns.
    """
    def testDefaultSpawnNumber(self):
        """
        Tests that spawn equals base when bonusDifficulty is set to zero.
        """
        from factories.monster_factory import getMonsters       
        import constants

        constants.RegionType.ERIADOR = 1
       
        spawn = getMonsters(5, constants.RegionType.ERIADOR, 0)

        errorMsg = "getMonsters() should have spawned five monsters but did not."
        self.assertEqual(len(spawn), 5, errorMsg)

    def testDefaultStatGeneration(self):
        #Testing difficulty feature - that default stats are implemented when
        #difficulty set to zero.
        """
        Changed monster spawn distribution of ERIADOR such that Trolls are spawned
        100% of the time. getMonsters is to spawn three Trolls using the new
        monster distribution.
        """
        from factories.monster_factory import getMonsters
        from monsters.troll import Troll
        import constants
       
        constants.REGIONAL_MONSTER_DISTRIBUTION = {1: {Troll: [0, 1]}}

        monsters = getMonsters(3, 1, 0)

        #Tests that monsters are spawned
        errorMsg = "getMonsters() should have spawned three monsters but did not."
        self.assertEqual(len(monsters), 3, errorMsg)
        
        #Test that monsters are spawned with correct stats
        for monster in monsters:
            errorMsg = "monster._hp was not initiated correctly."
            self.assertEqual(monster._hp, constants.MONSTER_STATS[Troll][0], errorMsg)
            errorMsg = "monster._attack was not initiated correctly."
            self.assertEqual(monster._attack, constants.MONSTER_STATS[Troll][1], errorMsg)
            errorMsg = "monster._experience was not initiated correctly."
            self.assertEqual(monster._experience, constants.MONSTER_STATS[Troll][2], errorMsg)
            
    def testDifficultyBonusStats(self):
        #-Testing difficulty feature - that monster stats increase as
        #percentage over default. For instance, difficulty = 1 should result
        #in monsters with 200% base monster stats.
        """
        Changed monster distribution of ERIADOR such that Trolls are spawned 100%
        of the time. getMonsters is to spawn Trolls with 200% base stats. 
        """
        from factories.monster_factory import getMonsters
        from monsters.troll import Troll
        import constants
        
        constants.REGIONAL_MONSTER_DISTRIBUTION = {1: {Troll: [0, 1]}}

        monsters = getMonsters(3, 1, 1)

        #Tests that monsters are spawned
        errorMsg = "getMonsters() should have spawned three monsters but did not."
        self.assertEqual(len(monsters), 3, errorMsg)
        
        #Test that monsters have been spawned with double stats
        for monster in monsters:
            errorMsg = "monster._hp was not initiated correctly."
            self.assertEqual(monster._hp, 2 * constants.MONSTER_STATS[Troll][0], errorMsg)
            errorMsg = "monster._attack was not initiated correctly."
            self.assertEqual(monster._attack, 2 * constants.MONSTER_STATS[Troll][1], errorMsg)
            errorMsg = "monster._experience was not initiated correctly."
            self.assertEqual(monster._experience, 2 * constants.MONSTER_STATS[Troll][2], errorMsg)
    
    def testRegionalSpawn(self):
        #-Testing that regional spawns work: that monster spawn reflects
        #regional monster distributions held in constants.
        """
        Tests that monsters of each type in a region's distribution
        spawn, given a large enough sample size.
        """
        from factories.monster_factory import getMonsters
        from monsters.troll import Troll
        from monsters.nazgul import Nazgul
        from monsters.goblin import Goblin
        from monsters.great_goblin import GreatGoblin
        import constants
        
        #Testcase #1: RegionType.ERIADOR
        constants.REGIONAL_MONSTER_DISTRIBUTION = {constants.RegionType.ERIADOR: {Troll: [0, .5], Nazgul: [.5, 1]}}
           
        monstersEriador = getMonsters(5000, constants.RegionType.ERIADOR, 0)

        #Checking to see that Nazgul and Trolls are spawned
        numberNazgul = 0
        numberTroll = 0
        for monster in monstersEriador:
            if isinstance(monster, Nazgul):
                numberNazgul += 1
            elif isinstance(monster, Troll):
                numberTroll += 1
            else:
                raise AssertionError("Invalid monster type.")

        errorMsg = "Did not spawn five thousand monsters - Eriador"
        self.assertEqual(len(monstersEriador), 5000, errorMsg)
        errorMsg = "No nazgul spawned."
        self.assertTrue(numberNazgul != 0, errorMsg)
        errorMsg = "No trolls spawned."
        self.assertTrue(numberTroll != 0, errorMsg)
        
        #Testcase #2: RegionType.HIGH_PASS
        constants.REGIONAL_MONSTER_DISTRIBUTION = {constants.RegionType.HIGH_PASS: {Goblin: [0, .5], GreatGoblin: [.5, 1]}}
        
        monstersHighPass = getMonsters(5000, constants.RegionType.HIGH_PASS, 0)

        #Checking to see that Goblins and Great Goblins are spawned
        numberGoblin = 0
        numberGreatGoblin = 0
        for monster in monstersHighPass:
            if isinstance(monster, Goblin):
                numberGoblin += 1
            elif isinstance(monster, GreatGoblin):
                numberGreatGoblin += 1
            else:
                raise AssertionError("Invalid monster type.")
            
        errorMsg = "Did not spawn five thousand monsters - High Pass"
        self.assertEqual(len(monstersHighPass), 5000, errorMsg)
        errorMsg = "No goblins spawned."
        self.assertTrue(numberGoblin != 0, errorMsg)
        errorMsg = "No great goblins spawned."
        self.assertTrue(numberGreatGoblin != 0, errorMsg)
        
def handle_pdb(signal, frame):
    """
    Signal handler method that invokes pdb.

    @param signal:      Signal
    @param frame:       Frame
    """
    import pdb
    pdb.Pdb().set_trace(frame)

if __name__ == '__main__':
    #Add signal handler that invokes PDG
    signal.signal(signal.SIGINT, handle_pdb)

    #Supress output from game with "buffer=true"
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
