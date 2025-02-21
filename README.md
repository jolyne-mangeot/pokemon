# Pokémon fan-game
Group project done as a Pygame learning course with OOP paradigm and MVC code architecture. Based on existing combat-focused Pokémon fangames, this work tries to offer dynamic visuals with basic yet expansable features such as fighting areas, mechanics as game-accurate as possible along with our personal take on how to make Pokémon combat more accessible.


## How to play

After running the game through the main.py file or the .exe file, you will be greeted by a title screen.

### START GAME

This will start the game sending you to the load screen where you will either choose a save file or create a new one. creating a new one will prompt you to enter your name and choose a starter (bulbasaur, charmander, or squirtle)

#### Start fight
Enter into combat with another pokemon. trainer vs trainer fights are yet to be implemented so you will only fight wild pokemon.

#### Check pokedex
Check encountered pokemon. this will show all pokemon that you've fought regardless of whether or not you caught a copy of them

#### Manage pokemons
Manage your current team. The pokemon at the top of the list will be the pokemon to fight first.

#### Save
Save the game. Simple as that. Will save your progress up until that point.

QUITTING WITHOUT SAVING THE GAME WILL ERASE ALL YOUR PROGRESS

#### Quit
Quit the game and return to title screen. Don't forget to save beforehand.

### Combat basics
Before starting the fight you will be prompted to choose a biome, different biomes contain different pokemon so make sure to not stay in one biome for too long to be able to fill your pokedex

(there are currently 42 pokemon waiting for you to discover them)

In combat you will be greeted by your pokemon and your enemy pokemon and you will get a choice menu on the bottom left.

You win when the enemy is captured or their HP reaches zero.
You lose when all your pokemon run out of HP

#### attack
Exactly what it says on the tin. Your pokemon will attack and reduce the HP of your enemy. 

Sometimes the pokemon will decide to goof off or do its own thing instead of attacking, nut that's because they have free will.

#### Guard
Increase your defense to take less damage. Strategic

#### Team
Change your current pokemon.
Make sure to not send a weak pokemon to fight one that's much stronger than itself, that's just animal cruelty. or pokemon cruelty. just don't do it.

#### Items
Allows you to choose between using a pokeball or a potion.

Pokeball: Attempt to catch the enemy pokemon. it has a chance of failure.

Potion: Restore the HP of active pokemon.

TIP: reduce the hp of the enemy pokemon to have an easier time catching it

#### Run
Attempt to escape combat. Has a chance to fail.

Failure will switch to the enemy's turn and success will send you back to the main menu.

### OPTIONS
Back to the title screen for this one. In the options you will find settings for volume of music and sound effects, screen resolution and language settings.

Currently the game supports English and French.

After setting your game up as you like it, you have to tap apply for your settings to, well, apply.


# Credits

[Jolyne Mangeot](github.com/jolyne-mangeot)

[Yuliia Sherstiuk](github.com/yuliia-sherstiuk)

[Eltigani Abdallah](github.com/eltigani-abdallah)

[Haytham Hammame](github.com/haytham-hammame) 
