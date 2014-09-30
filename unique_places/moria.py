#!/usr/bin/python

from unique_place import UniquePlace
from battle_engine import battle
from items.item import Item
from items.weapon import Weapon
from items.armor import Armor
import constants

import random

class Moria(UniquePlace):
    """
    Moria is a unique place in MistyMountainsSouth. In Tolkien's universe, 
    Moria is an enormous underground city built by dwarves and now overrun 
    with orcs.
    
    If player visits Moria, the amount of time that he spends in Moria is a 
    randomly generated variable from 15-25 turns. In each turn, player has a 
    chance of encountering a party of orcs. Each encounter increases the 
    probability of a future encounter until player is running from orcs 
    constantly.
    
    How this works:
    -There are three "travel" methods: low-risk travel, medium-risk travel, 
    and high-risk travel. Which method is called is dependent on self._danger.
    -If player has an encounter with monsters, self._danger increase by one.
    -Each of the three travel methods has its own PDF used for determining 
    whether the player runs into monsters.
    
    Additional notes:
    -Player has the opportunity to run into Balrog in Moria. Balrog is an 
    extremely powerful monster that the player should run from.
    -Player has the opportunity to pick up items as he ventures through Moria.
    """
    def __init__(self, name, description, greetings):
        """
        Initializes Moria.
        
        @param name:            The name of the UniquePlace.
        @param description:     A description of the UniquePlace.
        @param greetings:       The greetings the user gets as he enters.
        """
        #Call parent class init function
        UniquePlace.__init__(self, name, description, greetings)
        
        #Initializing danger tracker
        self._danger = 0
        
        #Strings for low-risk activity
        self._sneakString = [("You continue through narrow halls,"
        " seeking to avoid detection...."), 
        "You creep by an rotting library....", 
        "You creep down a mine shaft....",
        "You sneak through some ancient tunnels....", 
        "You creep through a maze of machinery....", 
        "You sneak past a series of corpses....", 
        "You sneak past some strange glyphs...."]
        
        #Strings for neutral activity
        self._neutralString = [("You find the staircase littered with the" 
        " corpses of dwarven warriors."),
        "You pass an enormous mine shaft.",
        "You appear to be lost and turn back around.",
        "You find yourself in an enormous hall, ending an a winding staircase.",
        "You pass by what used to be a meeting place.",
        "You trust your gut in making a series of turns.",
        "You find yourself trapped and needing to turn around."]
        
        #Strings for battle encounter
        self._encounterString = ["You hear some footsteps....",
        "You think you see some shadows moving....",
        "You hear a series of agitated grunting....", 
        "You see shadows darting along in the distance....",
        "You hear whispers in the darkness...."]
        
        #Strings if player is running from monsters
        self._runString = ["You run over some rotting corpses!",
        "You run past an spiral staircase!",
        "You dart along some minecarts!",
        "You dash along a hall of columns!",
        "You dash along a large mine shaft!",
        "You dart past some ancient tombs!",
        "You climb over a pile of rubble!"]
        
        #Spawn loot
        description = "Taken from a slain dwarven warrior"
        weapon = Weapon("Rusty Axe", description, 6, 8, 12)
        description = "Worker's mallet"
        weapon2 = Weapon("Dwarven Hammer", description, 10, 12, 16)
        description = "Steeped in history"
        weapon3 = Weapon("Aeowyln", description, 8, 22, 18)
        description = "Historical significance"
        weapon4 = Weapon("Durnhelm", description, 4, 18, 3)
        description = "Old but still effective"
        armor = Armor("Iron Cap", description, 3, 4, 1)
        description = "May increase magic find"
        armor2 = Armor("Boots of Travel", description, 2, 8, 2)
        description = "One of Middle Earth's rarest metals"
        item = Item("Mithril", description, 0, 84)
        description = "Magical properties?"
        item2 = Item("Ancient Runes", description, 2, 42)
        self._loot = [weapon, weapon2, weapon3, weapon4, armor, armor2, item, 
            item2]
        
    def enter(self, player):
        """
        Action sequence for Moria.
        
        @param player:   The current player.
        """
        #Story
        print self._greetings
        print ""
        
        print ("You enter into a once-glorious hall, moving quickly among" 
            " the shadows.")
        raw_input("Press enter to continue. ")
        print ""
        
        #Generate length of time spent in Moria
        timeInMoria = random.randrange(15, 25)

        #Player journeys through Moria
        for time in range(timeInMoria):
            if self._danger < constants.MORIA_LOW_RISK_UPPER_LIMIT:
                result = self._lowRiskTravel(player)
            elif self._danger < constants.MORIA_MED_RISK_UPPER_LIMIT:
                result = self._mediumRiskTravel(player)
            else:
                result = self._highRiskTravel(player)
            
            #Unpack results
            statement = result[0]
            battleOccurence = result[1]
                        
            #Execute action sequence
            print statement
            raw_input("Press enter to continue. ")
            print ""
            
            if battleOccurence:
                result = battle(player, constants.BattleEngineContext.RANDOM)
                if not result:
                    self._danger = 0
                    return
        
        #Ending sequence
        print "You emerge from the Mines!"
        raw_input("Press enter to continue. ")
        print ""
        
        self._danger = 0
        self._createPort("east")
        
    def _lowRiskTravel(self, player):
        """
        Determines outcome of the player as he ventures through the 
        Mines of Moria.
        
        @param player:  The current player.
        """
        chance = random.random()
        if chance < constants.MORIA_LOW_RISK_SNEAK_UPPER_LIMIT:
            statement = random.choice(self._sneakString)
            battle = False
            self._itemFind(player)
        elif chance < constants.MORIA_LOW_RISK_NEUTRAL_UPPER_LIMIT:
            statement = random.choice(self._neutralString)
            battle = False
            self._itemFind(player)
        else:
            statement = random.choice(self._encounterString)
            self._danger += 1
            battle = True
        
        return statement, battle
            
    def _mediumRiskTravel(self, player):
        """
        Determines outcome of the player as he ventures through the 
        Mines of Moria.
        
        @param player:  The current player.
        """
        chance = random.random()
        if chance < constants.MORIA_MED_RISK_SNEAK_UPPER_LIMIT:
            statement = random.choice(self._sneakString)
            battle = False
            self._itemFind(player)
        elif chance < constants.MORIA_MED_RISK_NEUTRAL_UPPER_LIMIT:
            statement = random.choice(self._neutralString)
            battle = False
            self._itemFind(player)
        else:
            statement = random.choice(self._encounterString)
            self._danger += 1
            battle = True
               
        return statement, battle
        
    def _highRiskTravel(self, player):
        """
        Determines outcome of the player as he ventures through the 
        Mines of Moria.
        
        @param player:  The current player.
        """
        chance = random.random()
        if chance < constants.MORIA_HIGH_RISK_NEUTRAL_UPPER_LIMIT:
            statement = random.choice(self._neutralString)
            battle = False
            self._itemFind(player)
        else:
            statement = random.choice(self._runString)
            self._danger += 1
            battle = True
        
        return statement, battle
        
    def _itemFind(self, player):
        """
        Helper method that determines if the player finds an item and what 
        item.
        
        @param player:  The current player.
        """
        chance = random.random()
        if self._loot and chance < constants.MORIA_ITEM_FIND_PROB:
            item = random.choice(self._loot)
            print ("You found %s while venturing through the Mines of Moria!" 
                % item.getName())
            
            if player.addToInventory(item):
                self._loot.remove(item)
            
            raw_input("Press enter to continue. ")
            print ""