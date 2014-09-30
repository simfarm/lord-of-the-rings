#!/usr/bin/python

from unique_place import UniquePlace
from monsters.nazgul_iii import Nazgul_III
from monsters.orc_ii import Orc_II
from monsters.orc_archer_ii import OrcArcher_II
from monsters.troll_ii import Troll_II
from monsters.black_numernorian_ii import BlackNumernorian_II
from monsters.mouth_of_sauron import MouthOfSauron
from battle_engine import battle
from items.weapon import Weapon
from items.armor import Armor
from items.potion import Potion
from items.item import Item
import constants

class Isenmouthe(UniquePlace):
    """
    Isenmouthe is a unique place in Udun. In Tolkien's universe it represents a
    scaled-down version of the Black Gate.
    
    If player visits Isenmouthe, he has the opportunity to break through to the 
    Plateau of Gorgoth (the heart of Mordor).
    """
    def __init__(self, name, description, greetings):
        """
        Initializes Isenmouthe.
        
        @param name:            The name of the UniquePlace.
        @param description:     A description of the UniquePlace.
        @param greetings:       The greetings the user gets as he enters.
        """
        #Call parent class init function
        UniquePlace.__init__(self, name, description, greetings)
        
        self._wave = []
        self._wave2 = []
        
        #Create monster wave #1 
        for monster in range(14):
            monster = Orc_II(constants.MONSTER_STATS[Orc_II])
            self._wave.append(monster)
        for monster in range(7):
            monster = OrcArcher_II(constants.MONSTER_STATS[OrcArcher_II])
            self._wave.append(monster)
        for monster in range(6):
            monster = Troll_II(constants.MONSTER_STATS[Troll_II])
            self._wave.append(monster)
        for monster in range(3):
            monster = BlackNumernorian_II(constants.MONSTER_STATS[BlackNumernorian_II])
            self._wave.append(monster)
        
        #Create monster wave #2
        for monster in range(5):
            monster = Orc_II(constants.MONSTER_STATS[Orc_II])
            self._wave2.append(monster)
        for monster in range(4):
            monster = OrcArcher_II(constants.MONSTER_STATS[OrcArcher_II])
            self._wave2.append(monster)
        for monster in range(2):
            monster = Troll_II(constants.MONSTER_STATS[Troll_II])
            self._wave2.append(monster)
        for monster in range(5):
            monster = BlackNumernorian_II(constants.MONSTER_STATS[BlackNumernorian_II])
            self._wave2.append(monster)
        for monster in range(4):
            monster = Nazgul_III(constants.MONSTER_STATS[Nazgul_III])
            self._wave2.append(monster)
        monster = MouthOfSauron(constants.MONSTER_STATS[MouthOfSauron])
        self._wave2.append(monster)
        
        #Create loot
        weapon = Weapon("Troll Hammer", "Enormous and unwieldy", 18, 42, 20)
        armor = Armor("Troll Shield", "Enormous and unwieldy", 14, 36, 2)
        potion = Potion("Orc Draught", "Disgusting", 2, 0, -15)
        potion2 = Potion("Orc Draught", "Potentially toxic", 2, 0, -20)
        item = Item("Orcish Banister", "Potential resale value", 5, 14)
        item2 = Item("Screw and bolts", "Useless", 2, 4)
        self._loot = [weapon, armor, potion, potion2, item, item2]
        
    def enter(self, player):
        """
        Action sequence for Isenmouthe.
        
        @param player:   The current player.
        """
        print self._greetings
        print ""
        print "You see several armies approaching as you near the Isenmouthe."
        raw_input("Press enter to continue. ")
        print ""
        
        #Run battle action sequence
        self._battle(player)
        
    def _battle(self, player):
        """
        Battle sequence for Isenmouthe.
        
        @param player:   The current player.
        """
        #Wave 1
        print "Mouth of Sauron: \"You have overstayed your welcome.\""
        raw_input("Press enter to continue. ")
        print ""
        result = battle(player, constants.BattleEngineContext.STORY, 
            self._wave)
        if not result:
            return
        
        #Wave 2
        print "Mouth of Sauron: \"Time... to... DIE!!!\""
        raw_input("Press enter to continue. ")
        print ""
        result = battle(player, constants.BattleEngineContext.STORY, 
            self._wave2)
        if not result:
            return
            
        #Call victory sequence
        self._victorySequence(player)
        
    def _victorySequence(self, player):
        """
        Victory sequence for Isenmouthe.
        
        @param player:   The current player.
        """
        print "You have secured the north-west route into Mordor!"
        raw_input("Press enter to continue. ")
        print ""
        
        #Give player loot
        if len(self._loot) != 0:
            print "While looting the battlefield, you find strange items."
            raw_input("Press enter to continue. ")
            print ""
            toRemove = []
            for item in self._loot:
                if player.addToInventory(item):
                    toRemove.append(item)
            for item in toRemove:
                self._loot.remove(item)
            print ""
        
        print "Welcome to the heart of Mordor!"
        print ""
        
        self._createPort("south")