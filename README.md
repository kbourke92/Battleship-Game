# Battleships

Battleships is a python based game which runs in the Code Institute mock terminal on Heroku.
It is a 2 player turn based game with players placing their ships on a 10x10 grid and taking turns trying to guess where the other player has placed their ships.

[Here is the live version](

## How To Play
Players start by placing their ships on a 10x10 grid. Each player has 3 ships to place.

Players then take turns trying to 'hit' the other players ships.

If there is a hit this is marked by an X while a miss is a O.

The winner is the player who sinks the opponents ships first.

## Features

### Existing Features

- Precise board allocation
  - Players cant see where the opponents ships are
- Play against another person
- Maintain scores
- Notification if a ship has been hit
- Option to start again

<img width="350" height="350" alt="Screenshot 2025-12-01 143150" src="https://github.com/user-attachments/assets/32354e33-7180-46c2-896c-867d1db0529d" />
<img width="175" height="250" alt="Screenshot 2025-12-01 143208" src="https://github.com/user-attachments/assets/d2deb3b3-fa2a-41b1-b599-43c42c932b4b" /> 
<img width="175" height="175" alt="Screenshot 2025-12-01 143227" src="https://github.com/user-attachments/assets/5a30d38a-3fbf-4e73-8ee8-a84bba7e9a62" />




## Testing

I have manually tested this project by doing the following:

### Validator TEsting

- PEP8 Testing
  -  No errors were returned from [PEP8](www.pep8online.com)
 
  <img width="400" height="300" alt="Screenshot 2025-12-01 203741" src="https://github.com/user-attachments/assets/17008f30-500c-43dd-87cd-118a9ed67793" />


### Solved Bugs

- During testing on Pycharm a bug occured where the ships were not displaying. This was due to the emoji not formatting correctly depending on the OS.
- While testing on Pycharm I discovered the game did not end despite the all ships being struck. This was due to there being no check in the code to see if there were any ships left.

### Remaining Bugs

There are no bugs outstanding

## Deployment

This project was deployed using Code Institutes mock terminal for Heroku

- Steps for Deployment
  - Fork or clone this repository
  - Log in or create a new heroku app
  - Set the buildbacks to `Python` and `NodeJS` in that order
  - Link the Heroku app to the repository
  - Click on Deploy
 
## Credits

- Code Institute for the deployment terminal
- [llego.dev](https://llego.dev/posts/how-code-simple-battleship-game-python/) for the inspration for the game
 
