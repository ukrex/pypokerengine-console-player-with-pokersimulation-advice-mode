The purpose of this project was to implement PyPokerEngine Custom player module extended with the
capabilities of PokerSimulation library. To implement this project the interface between those two
libraries was built:
 - PyPokerEngine AI development library for Texas Hold'em Poker
   https://ishikota.github.io/PyPokerEngine/ and
 - PokerSimulation library to evaluate actions in Texas Hold'em Poker
   https://towardsdatascience.com/how-to-build-a-poker-simulation-tool-with-python-449eddd59613

Presented application includes three pre-build AI PyPokerEngine player modules and extended
Console player module with added PokerSimulation library capabilities. This enhancement allows any poker player
to practice the real-time Poker game with pre-build AI PyPokerEngine players using PokerSimulation advise tools.

Before starting the game you should define number of max rounds to be played, initial stack value for every player,
small blind betting amount and the player names into appropriate config statements in this main.py file below.
Read PyPokerEngine library documentation to learn about the strategies used for PyPokerEngine AI player modules.

Console player module also provides the opportunity to use the help file with the image of
starting hand play preferences from the "Poker Simulation with Python" article by Diego Salinas
https://towardsdatascience.com/how-to-build-a-poker-simulation-tool-with-python-449eddd59613. Enjoy your poker.

This project is licensed under the terms of the MIT license.
