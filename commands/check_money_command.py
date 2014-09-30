#!/usr/bin/python

from command import Command
import constants

class CheckMoneyCommand(Command):
    """
    Displays player money.
    """
    def __init__(self, name, explanation, player):
        """
        Initializes new check money command.

        @param name:         Command name.
        @param explanation:  Explanation of command.
        @param player:       The player object.
        """
        #Call parent's init method
        Command.__init__(self, name, explanation)

        self._player = player

    def execute(self):
        """
        Prints player money.
        """
        money = self._player.getMoney()
        name = self._player.getName()

        print "%s currently has %s %s!" % (name, money, constants.CURRENCY)