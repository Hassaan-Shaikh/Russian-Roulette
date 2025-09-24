import random as rand
import time

is_game_playing = True
do_exit = False

cylinder = [False] * 6
current_chamber_index = 0
ammo_count = 1

current_player = 0 # 0 means you
num_extra_players = 0
multiplayer_mode = False
players = ["Player 1"]
is_ai = [False]

def load_gun(ammo_count = 1):
  if ammo_count < 1: ammo_count = 1 # Must have atleast one round in the chamber
  if ammo_count > 5: ammo_count = 5 # Ensure a chance of survival

  message = f"Revolver empty! Loading {ammo_count} "
  message += "bullets.\n" if ammo_count > 1 else "bullet.\n"
  print(message)
  i = 0
  while i < ammo_count:
    chosen_chamber = rand.randint(0, 5)
    if not cylinder[chosen_chamber]:
      cylinder[chosen_chamber] = True
      i += 1

  #for i in range(ammo_count):
  #  chosen_chamber = rand.randint(0, 5)
  #  if not cylinder[chosen_chamber]:
  #    cylinder[chosen_chamber] = True

def shoot_gun():
  global current_chamber_index
  if cylinder[current_chamber_index]:
    cylinder[current_chamber_index] = False
    current_chamber_index = (current_chamber_index + 1) % 6
    return True
  current_chamber_index = (current_chamber_index + 1) % 6
  return False

def shuffle_cylinder():
  global current_chamber_index
  current_chamber_index = rand.randint(0, 5)
  return shoot_gun()

def check_cylinder():
  if any(cylinder):
    return True
  return False

def user_input():
  choice = 0
  while choice not in [1, 2]:
    try:
      print("Choices:")
      print("\t1. Shoot Gun")
      print("\t2. Rotate Cylinder & Shoot Again")
      choice = int(input("Enter choice: "))
      if choice not in [1, 2]:
        print("Invalid choice.")
        time.sleep(1)
    except ValueError:
      print("Invalid input. Enter a number.")
      time.sleep(1)
  return choice

def ai_input():
  return rand.randint(1, 2)

def check_player_killed(player_killed):
  global current_player
  global is_game_playing
  if player_killed:
    print(f"*Bang!* {players[current_player]} died!")
    players.pop(current_player) # Use pop to remove the player at the current index
    is_ai.pop(current_player) # Use pop to remove the corresponding AI status

    if not multiplayer_mode:
      is_game_playing = False # Set is_game_playing to False instead of calling sys.exit()
      input("Press Enter to exit...")
    elif multiplayer_mode and len(players) == 1:
      print(f"{players[0]} survived.")
      is_game_playing = False # End game when only one player remains
      input("Press Enter to exit...")

    # Adjust current_player index if it's now out of bounds
    if len(players) > 0:
        current_player = current_player % len(players)
    else:
        current_player = 0 # Or handle this case as needed when players list is empty

  else:
    current_player = (current_player + 1) % len(players) if len(players) > 0 else 0
    print("*Click!* The chamber was empty.")
  print()

def play_round():
  if len(players) == 0: return

  global current_chamber_index
  global current_player

  if not check_cylinder():
    load_gun(ammo_count)

  print(f"{players[current_player]}'s turn.")
  if not is_ai[current_player]:
    choice = user_input()
  else:
    choice = ai_input()

  if choice == 1:
    player_shot = shoot_gun()
    print("Pulling the trigger...")
  elif choice == 2:
    player_shot = shuffle_cylinder()
    print("Rotating cylinder and shooting again...")

  time.sleep(2)

  check_player_killed(player_shot)

print("\tRussian Roulette")
name = input(f"Enter your name or leave blank to be called '{players[0]}': ")
players[0] = name if name else players[0]
is_ai_input = input("Do you want an AI to play in your place? 'Y' for AI, blank for Human: ")
confirm = is_ai_input[0].lower() == "y" if is_ai_input else False
is_ai[0] = confirm
print("How many more are with you?")

while True:
    try:
        num_extra_players = int(input("Type a number: "))
        break # Exit the loop if input is a valid integer
    except ValueError:
        print("Invalid input. Please enter a number.")
        time.sleep(1)

multiplayer_mode = num_extra_players > 0

for i in range(1, num_extra_players + 1):
  name = input(f"Type a name for Player {i + 1} or leave blank for the default 'Player {i + 1}': ")
  if name:
    players.append(name)
  else:
    players.append("Player " + str(i + 1))
  is_ai_input = input("Is this player an AI? 'Y' for AI, blank for Human: ")
  confirm = is_ai_input[0].lower() == "y" if is_ai_input else False
  is_ai.append(confirm)

print(f"Number of players: {len(players)}")
ammo_count = int(input("Enter the number of bullets in the revolver (No less than 1 and no more than 5): "))

if multiplayer_mode:
  current_player = rand.randint(0, len(players) - 1)
  print(f"\n\nThe game begins with {players[current_player]}.")
else:
  print("Begin!")

while is_game_playing:
  play_round()
  if not multiplayer_mode and is_game_playing:
    print("\nContinue Playing?")
    do_exit = input("Type 'Y' to continue, leave blank to exit: ")[0].lower() if do_exit else False
    if do_exit != "y":
      input("Press Enter to exit...")
      is_game_playing = False
