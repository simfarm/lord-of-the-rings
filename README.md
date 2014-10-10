Lord of the Rings
=======

Lord of the Rings is a object-oriented game loosely based on JRR Tolkien's Lord of the Rings. The user wins by dropping the One Ring into the fiery depths of Mount Doom. 

Gameplay
=======

Player navigates the world by moving from tile to tile on the game map. Some tiles are connected to other tiles by default and some connections can be opened after defeating bosses/visiting certain places. Tiles have cities and other places to visit.

Cities have the following:
* Inns - allow for player heal.
* Shops - allow for the purchasing of items.
* Squares - allows the user to interface with sprites.

Player can collect a vast array of items during the course of the game. Items come in four different types:
* Weapons - add to player attack.
* Armor - add to player defense. How this works: if player gets attacked for four damage and armor wields two damage, player only receives two damage.
* Charms - may add bonuses to health, attack, and defense.
* General items - have novelty and sell value. For instance: Gold Chunk.

Items may be gained through a variety of means:
* Buying items in the shops contained in cities.
* Receiving items as gifts from the people contained in city squares.
* Finding items that are randomly distributed throughout the game's tiles. As each game world is instantiated, powerful items are dispursed throughout the world.
* Receiving items after the game's many battles. The is the only way to receive the game's elite unique items.

Stats work as you'd expect:
* HP - the amount of damage player can take.
* Attack - player attack.
* Experience - increasing this results in leveling up.

Bottom line: player moves from tile to tile until he ends up in the Mount Doom tile. There will be random battles and boss battles along the way.

Guide 
=======

The player's first priority should be moving east until he/she is at Rivendell. Talk to the people at the Council of Elrond for some of the early game's best items. After that, there are three ways across the Misty Mountains: 
* Over High Pass (boss fight).
* Through the Mines of Moria (random battles).
* Through Isenguard (boss fight).
Player should choose either of the first two choices.

The player should make levelling up a priority in the early stages of the game. After max level is reached, player may choose to visit some of the harder places in Mordor to fight such that he/she can obtain some of the game's elite unique items.

You may be able to find the three elven rings randomly distributed throughout the game map. These items are incredibly powerful and will make the game substantially easier.

Status
=======


Installation
=======

No installation necessary, except certain modules required to run tests.

Tests
=======

To test the game, type:
$ ./test.py

You should see output similar to the following:

Ran 98 tests in 0.01s
 
OK

(The number of tests may vary)
