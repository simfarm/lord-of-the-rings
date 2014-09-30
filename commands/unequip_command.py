#!/usr/bin/python

from command import Command

class UnequipCommand(Command):
    """
    Unequips player with currently equipped item.
    """
    def __init__(self, name, explanation, player):
        """
        Initializes unequip command.

        @param name:         Command name.
        @param explanation:  Explanation of command.
        @param player:       The player object.
        """
        #Call parent's init method
        Command.__init__(self, name, explanation)

        self._player = player

    def execute(self):
        """
        Unequips player with item in inventory.
        """
        equipped = self._player.getEquipped()

        #If no items to unequip
        if equipped.count() == 0:
            print "No items to unequip."
            return

        #User prompt
        print "%s may unequip:" % self._player.getName()
        for item in equipped:
            print "\t%s" % item.getName()
        print ""
        
        itemToUnequip = raw_input("Which item do you want to unequip? \n")
        itemEquipment = equipped.getItemByName(itemToUnequip)
        
        #Check if item is currently equipped
        if not itemEquipment:
            print ""
            print "%s is not currently equipped!" % itemToUnequip
            return

        #Unequips player with item
        statement = self._player.unequip(itemEquipment)
        print statement