Feature: Playing the game

Scenario: Queueing for a game
Given I want to play a game
And I have no unfinished games
When I start my AI
Then my AI gets registered
And waits for another AI to play against

Scenario: Starting a game
Given n-1 AIs are waiting to play a game
And the gamemode of the game needs n players
When a new AI gets registered
Then a new game gets created
And all n AIs get registered for this game

Scenario: Getting the game state
When my AI sends a request
Then my AI receives the game's state

Scenario: Getting the game board
When my AI sends a request
Then my AI receives the game's board

Scenario: Getting the active players
When my AI sends a request
Then it receives if it's my AI's turn

Scenario: Making a turn
Given it is my AI's turn
When my AI sends a request with a new turn
Then the turn gets recorded
And it's anothers AI's turn

Scenario: Finishing a game
Given the game has begun
When my AI does the last move
Then the game gets saved
And statistics get updated

Scenario: Winning and Loosing a game
Given the game has finished
When my AI sends a request
Then it gets told if it has won
And it receives the recorded game's URL
