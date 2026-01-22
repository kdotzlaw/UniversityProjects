# Clue

An interactive game of Clue where players use their cards and the computer's cards to determine who, where, and how. Created using Ruby and object-orientated design.

## Classes

Object-oriented design includes seperating code into reusable classes that are either abstract or concrete.
In this project, the following classes were implemented:

|Class Name | Type | Purpose|
|-          |-     |-       |
|PlayerAbs  | Abstract| Designs player structure|
|Player| Concrete Subclass| Handles the computer player|
|InteractivePlayer| Concrete Subclass| Handles the user player|
|Model| Concrete class| sets up players, sets up cards, deals cards, and runs the game|
|Card| Helper class| Holds structure of cards|
|Guess| Helper class| Holds structure of guesses for accusations or information gathering|

### Players

The abstract Player class outlines the following methods that are then defined in its subclasses, Player and InteractivePlayer:
- **setup**:  receives number of players, index of the current player, a list of all suspects, a list of all locations, a list of all weapons
- **setCard**: sets the card that was dealt to player
- **canAnswer**: receives player index and guess and has the current player answer the guess by either returning a card or nothing
- **getGuess**: indicates that its current players turn if called and returns the current players guess
- **receiveInfo**: receives player index and a card, indicating that the current player has guessed and gotten a card as a response

### Model

This class creates, shuffles, and deals all cards to the players. It also holds the whodunnit? answer. To track whos turn it is, the model assigns players indexes [0-(n-1)] where n is the total number of players and determines the next players turn using `player(i+1)%n`

This class has the following methods:
- **setPlayers**: receives an array of players in the game, initializes them, and sets up each player
- **setupCards**: chooses whodunnit? and deals cards to all players based on index
- **play**: runs the game

## Game Logic

The general process of Clue is:
- while the game is not over:
    - ask current player (i) for guess
    - if guess == accusation:
        - if accusation is correct, game over, current player wins
        - if accusation is wrong, active player is removed from the game
            - if there is only 1 player left, game ends
    - if guess != accusation:
        - ask players if they can show a card from the guess (starting with player i+1)
            - if a player can show card, show card to player i
            - if player cant show card, tell player i
    - if game != over:
        - move active player to player i+1