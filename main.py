name = None
import os
import time
import random
import colorama
from datetime import date
from colorama import Fore as fg
from replit import db
from localStoragePy import localStoragePy
option = None
opponent = None
tutorial = "inactive"
match = "ranked"
ranked_warned = False
reward = 0

localStorage = localStoragePy('RockPaperScissorsRPG', 'sqlite')

cyan = fg.LIGHTCYAN_EX
white = fg.LIGHTWHITE_EX
green = fg.LIGHTGREEN_EX
red = fg.RED
yellow = fg.LIGHTYELLOW_EX

def getName():
  os.system('clear')
  global name
  name = input("username: ")
  print("hello", name)
  time.sleep(1)
  createPlayer()
  menu()

def start_up():
  load_game()
  os.system('clear')
  print("Rock Paper Scissors RPG")
  print(f"{cyan}------------{white}")
  print("1. New Game")
  print(f"2. Load ({name})")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    localStorage.clear()
    
    createPlayer()
    getName()
  elif option == "2":
    menu()
  else:
    start_up()

def menu():
  global ranked_warned
  save_game()
  player.setRank()
  os.system('clear')
  print(f"{white}Menu / ${player.cash} / Lv.{player.lvl} / {player.rank} ")
  print(f"{cyan}------------{white}")
  print(f"1. Ranked ({player.rank} League)")
  print(f"2. Casual")
  print("3. Inventory")
  print("4. Store")
  print(f"{cyan}------------{white}")
  print("5. Settings (Coming Soon)")
  print("6. Tutorial (Coming Soon)")
  print("0. Exit")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    match = "ranked"
    startGame()
  elif option == "2":
    match = "casual"
    startGame()
  elif option == "3":
    inventory()
  elif option == "4":
    store()
  elif option == "5":
    print(f"{red}coming soon")
    time.sleep(3)
    menu()
  elif option == "6":
    print(f"{red}coming soon, for instructions see the read me doument!")
    time.sleep(3)
    menu()
  elif option == "0":
    start_up()
  else:
    menu()

def startGame():
  save_game()
  global reward
  player.setRank()
  os.system('clear')
  getOpponent()
  print("Connecting to totally real server...")
  time.sleep(1)
  os.system('clear')
  print("Getting definitely not a bot opponent...")
  time.sleep(1)
  os.system('clear')
  print(f"{cyan}------------{white}")
  print(f"{green}{name}{white} vs {red}{opponent.name}")
  print(f"{cyan}------------{white}")
  time.sleep(2)
  gameSpace()


def gameSpace():
  save_game()
  #deathChecking
  if player.hp <= 0:
    if opponent.hp <= 0:
      tie()
    else:
      lose()
  else:
    if opponent.hp <= 0:
      win(reward)
  
  os.system('clear')
  print(f"{green}{name} hp: {player.hp} {white}/{red} {opponent.name} hp: {opponent.hp}{white}")
  print(f"{cyan}charge: {player.charge}")
  print(f"------------{white}")
  print("1. Rock")
  print("2. Paper")
  print("3. Scissors")
  print(f"{cyan}0. Charge")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    player.attack("rock")
  elif option == "2":
    player.attack("paper")
  elif option == "3":
    player.attack("scissors")
  if option == "0":
    player.attack("skip")
  else:
    gameSpace()

def lose():
  os.system('clear')
  print(f"{red}You have lost against {opponent.name}")
  print(f"-1 Level")
  time.sleep(2)
  opponent.hp = opponent.max_hp
  player.hp = player.max_hp
  player.lvl -= 1
  menu()

def win(reward):
  player.setRank()
  rew = reward
  if match == "casual":
    rew = 0
  else:
    pass
  os.system('clear')
  print(f"{green}You have won against {opponent.name}")
  print(f"{cyan}------------{white}")
  if match == "casual":
    print(f"+1 Item")
  if match == "ranked":
    print(f"+${rew}")
    print(f"+1 Level")
    print(f"+1 Item")
    player.cash += rew
  time.sleep(2)
  opponent.hp = opponent.max_hp
  player.hp = player.max_hp
  player.lvl += 1
  itemReward(1,"both")

def tie():
  player.setRank()
  os.system('clear')
  print(f"{yellow}You have tied against {opponent.name}")
  print(f"{green}+1 Level")
  time.sleep(2)
  opponent.hp = opponent.max_hp
  player.hp = player.max_hp
  player.lvl += 1
  menu()

def itemReward(cycles,type):
  save_game()
  os.system('clear')
  item = eval("game.items." + str(dir(game.items)[random.randint(26, len(dir(game.items)) - 1)]))
  if type == "both":
    pass
  if type == "common":
    if item.rarity == "rare":
      itemReward(cycles,type="common")
    if item.rarity == "common":
      pass
  if type == "rare":
    if item.rarity == "rare":
      pass
    if item.rarity == "common":
      itemReward(cycles,type="rare")
  print(f"{white}You Have Received,")
  print(f"{item.rarity} {item.element} {item.type}:")
  print(f"{cyan}------------{white}")
  print(f"{item.color}{item.name} {white}")
  print(f"- Attack: {item.atk}")
  print(f"- Defense: {item.defn}")
  print(f"- Hurt: {item.hurt}")
  print(f"{item.tooltip}")
  print(f"{cyan}------------{white}")
  print("1.Accept")
  print("2.Decline")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    player.inventory.append(item.name)
    if cycles <= 1:
      menu()
    itemReward(cycles - 1, type)
  elif option == "2":
    if cycles <= 1:
      menu()
    itemReward(cycles - 1, type)
  else:
    itemReward(cycles, type)

def inventory():
  save_game()
  os.system('clear')
  print(f"{name}'s Inventory")
  print(f"{cyan}------------{white}")
  for i in player.inventory:
    item = eval(f"game.items.{i.lower()}")
    print(f"-{item.color}{i}{white}")
  print(f"{cyan}------------{white}")
  print("1.Inspect Item")
  print("2.Eqiup")
  print("3.Character")
  print("0.Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    inspect_item()
  elif option == "2":
    equip()
  elif option == "3":
    character()
  elif option == "0":
    menu()
  else:
    inventory()

def character():
  save_game()
  os.system('clear')
  print(f"{name}")
  print(f"{cyan}------------{white}")
  print(f"Health: {player.max_hp}")
  print(f"{cyan}------------{white}")
  print(f"equiped: {player.weapon.color}{player.weapon.name}{white}")
  print(f"{cyan}------------{white}")
  print(f"attack: {player.weapon.atk}")
  print(f"defense: {player.weapon.defn}")
  print(f"{cyan}------------{white}")
  print("1.Rename")
  print("0.Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    print(f"{red}Coming Soon")
    time.sleep(3)
  elif option == "0":
    menu()
  else:
    inventory()

def inspect_item():
  save_game()
  os.system('clear')
  print(f"{name}'s Inventory")
  print(f"{cyan}------------{white}")
  cycles = 1
  for i in player.inventory:
    print(f"{cycles}. {i}")
    cycles += 1
  print(f"{cyan}------------{white}")
  print("0.Back")
  option = input(f"{green}{name}>{white}")
  if option == "0":
    menu()
  elif int(option) in range(len(player.inventory) + 1):
    item_in_inv = player.inventory[int(option) - 1].lower()
    item = eval(f"game.items.{item_in_inv}")
    item_page(item)
  else:
    inspect_item()

def equip():
  save_game()
  os.system('clear')
  print(f"{name}'s Inventory")
  print(f"{cyan}------------{white}")
  cycles = 1
  for i in player.inventory:
    print(f"{cycles}. {i}")
    cycles += 1
  print(f"{cyan}------------{white}")
  print("0.Back")
  option = input(f"{green}{name}>{white}")
  if int(option) in range(len(player.inventory) + 1):
    item_in_inv = player.inventory[int(option) - 1].lower()
    item = eval(f"game.items.{item_in_inv}")
    player.weapon = item
    inventory()
  if option == "0":
    menu()
  else:
    equip()

def item_page(item):
  save_game()
  os.system('clear')
  print(f"{item.color}{item.name} {white}")
  print(f"{cyan}------------{white}")
  print(f"{item.rarity} {item.element} {item.type}")
  print(f"- Attack: {item.atk}")
  print(f"- Defense: {item.defn}")
  print(f"- Hurt: {item.hurt}")
  print(f"{item.tooltip}")
  print(f"{cyan}------------{white}")
  print("0.Done")
  option = input(f"{green}{name}>{white}")
  if option == "0":
    menu()
  else:
    item_page()

def store():
  save_game()
  os.system('clear')
  print(f"Store  ${player.cash}")
  print(f"{cyan}------------{white}")
  print("1. Weapons")
  print("2. Armors")
  print("3. Item Packs")
  print("0. Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    weapon_shop()
  elif option == "2":
    armor_shop()
  elif option == "3":
    pack_shop()
  elif option == "0":
    menu()
  else:
    store()

def weapon_shop():
  save_game()
  os.system('clear')
  print(f"Store > Weapons ${player.cash}")
  print(f"{cyan}------------{white}")
  print(f"1.{green} Rock_Bomb {white}/ $20")
  print(f"2.{green} Spikey_Rock {white}/ $20")
  print(f"3.{green} Scissor_Blade {white}/ $20")
  print(f"4.{cyan} Snippers {white}/ $40")
  print(f"{cyan}------------{white}")
  print(f"{white}5. Inspect Items")
  print(f"0. Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      weapon_shop()
    if player.cash >= 20:
      player.cash -= 20
      player.inventory.append("Rock_Bomb")
      weapon_shop()
  elif option == "2":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      weapon_shop()
    if player.cash >= 20:
      player.cash -= 20
      player.inventory.append("Spikey_Rock")
      weapon_shop()
  elif option == "3":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      weapon_shop()
    if player.cash >= 20:
      player.cash -= 20
      player.inventory.append("Scissor_Blade")
      weapon_shop()
  elif option == "4":
    if player.cash < 40:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      weapon_shop()
    if player.cash >= 40:
      player.cash -= 40
      player.inventory.append("Snippers")
      weapon_shop()
  elif option == "5":
    weapon_shop()
  elif option == "0":
    store()
  else:
    weapon_shop()

def armor_shop():
  save_game()
  os.system('clear')
  print(f"Store > Armors ${player.cash}")
  print(f"{cyan}------------{white}")
  print(f"1.{green} Rock_Bomb {white}/ $10")
  print(f"2.{green} Spikey_Rock {white}/ $10")
  print(f"3.{green} Scissor_Blade {white}/ $10")
  print(f"4.{cyan} Snippers {white}/ $20")
  print(f"{cyan}------------{white}")
  print(f"{white}5. Inspect Items")
  print(f"0. Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      armor_shop()
    if player.cash >= 20:
      player.cash -= 20
      
  elif option == "2":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      armor_shop()
    if player.cash >= 20:
      player.cash -= 20
      
  elif option == "3":
    if player.cash < 20:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      armor_shop()
    if player.cash >= 20:
      player.cash -= 20
      
  elif option == "4":
    if player.cash < 40:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      armor_shop()
    if player.cash >= 40:
      player.cash -= 40
  elif option == "5":
    store()
  elif option == "0":
    store()
  else:
    armor_shop()

def pack_shop():
  save_game()
  os.system('clear')
  print(f"Store > Packs ${player.cash}")
  print(f"{cyan}------------{white}")
  print(f"1.{green} Common Booster Pack{white} / $100")
  print(f"2.{cyan} Rare Booster Pack{white} / $200")
  print(f"0. Back")
  option = input(f"{green}{name}>{white}")
  if option == "1":
    if player.cash < 100:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      store()
    if player.cash >= 100:
      player.cash -= 100
      itemReward(5,"common")
  elif option == "2":
    if player.cash < 200:
      print(f"{red}Not Enough Cash")
      time.sleep(1)
      store()
    if player.cash >= 200:
      player.cash -= 200
      itemReward(10,"rare")
  elif option == "0":
    store()
  else:
    pack_shop()

def getOpponent():
  save_game()
  global opponent
  randomNumber = random.randint(1, 3)
  if randomNumber == 1:
    opponent = sarah
  elif randomNumber == 2:
    opponent = joe
  elif randomNumber == 3:
    opponent = hikaru

class game:
  ranks = [
    "Iron",
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond",
    "Master",
    "Grandmaster"
  ]
  class items:
    class rock_bomb:
      name = "Rock_Bomb"
      rarity = "common"
      color = green
      type = "weapon"
      element = "rock"
      atk = 5
      defn = 0
      hurt = 2
      tooltip = "the explosion gets your target, but watch out for the shrapnel."
    class spikey_rock:
      name = "Spikey_Rock"
      rarity = "common"
      color = green
      type = "weapon"
      element = "rock"
      atk = 5
      defn = 0
      hurt = 1
      tooltip = "hurts to hold but hurts, a lot more to be hit by."
    class scissor_blade:
      name = "Scissor_Blade"
      rarity = "common"
      color = green
      type = "weapon"
      element = "scissor"
      atk = 3
      defn = 0
      hurt = 0
      tooltip = "you thought a paper cut was bad?"
    class taxes:
      name = "Taxes"
      rarity = "common"
      color = green
      type = "armor"
      element = "paper"
      atk = 0
      defn = 5
      hurt = 2
      tooltip = "hurts to do, but you're safer in the end."
    class snippers:
      name = "Snippers"
      rarity = "rare"
      color = cyan
      type = "weapon"
      element = "scissors"
      atk = 5
      defn = 0
      hurt = 0
      tooltip = "This is honestly a violent game when you think about it"
    class rolling_pin:
      name = "Rolling_Pin"
      rarity = "rare"
      color = cyan
      type = "weapon"
      element = "rock"
      atk = 5
      defn = 2
      hurt = 0
      tooltip = "Good for baking"
    class golden_snips:
      name = "Golden_Snips"
      rarity = "rare"
      color = cyan
      type = "weapon"
      element = "scissors"
      atk = 7
      defn = 0
      hurt = 1
      tooltip = "So heavy the hurt a little, very shiny"
    class rock_helmet:
      name = "Rock_Helmet"
      rarity = "common"
      color = cyan
      type = "weapon"
      element = "rock"
      atk = 0
      defn = 4
      hurt = 1
      tooltip = "Bad for your neck"


def getAttack(person):
    attack = person.rolls[random.randint(0, 5)]
    return attack

class sarah:
  name = "sarah"
  weapon = game.items.scissor_blade
  hp = 10
  max_hp = 10
  charge = 0
  rolls = ["scissors","scissors","scissors","rock","paper","skip"]
  lvl = 1

class joe:
  name = "joe"
  weapon = game.items.rock_bomb
  hp = 10
  max_hp = 10
  charge = 0
  rolls = ["scissors","rock","rock","rock","paper","skip"]
  lvl = 1

class hikaru:
  name = "hikaru"
  weapon = game.items.rock_bomb
  hp = 10
  max_hp = 10
  charge = 0
  rolls = ["paper","paper","rock","scissors","skip","skip"]
  lvl = 1

startHp = None
startLvl = None
startDmg = None

class player:
  weapon = "Scissor_Blade"
  armor = None
  inventory = ["Scissor_Blade"]
  hp = 0
  charge = 0
  max_hp = 0
  lvl = 0
  rank = None
  cash = 0
  def attack(choice):
    player.charge += 1
    opponent.charge += 1
    choice2 = getAttack(opponent)
    
    if choice == "rock":
      boost = player.charge
      player.charge = 0
      boost2 = opponent.charge
      if choice2 == "rock":
        opponent.charge = 0
        battle.damageCalc("tie", boost, boost2)
      if choice2 == "paper":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "scissors":
        opponent.charge = 0
        battle.damageCalc("win", boost, boost2)
      if choice2 == "skip":
        opponent.charge += 1
        battle.damageCalc("win", boost, boost2)
      else:
        gameSpace()
        
    if choice == "paper":
      boost = player.charge
      player.charge = 0
      boost2 = opponent.charge
      if choice2 == "rock":
        opponent.charge = 0
        battle.damageCalc("win", boost, boost2)
      if choice2 == "paper":
        opponent.charge = 0
        battle.damageCalc("tie", boost, boost2)
      if choice2 == "scissors":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "skip":
        opponent.charge += 1
        battle.damageCalc("win", boost, boost2)
      else:
        gameSpace()
        
    if choice == "scissors":
      boost = player.charge
      player.charge = 0
      boost2 = opponent.charge
      if choice2 == "rock":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "paper":
        opponent.charge = 0
        battle.damageCalc("win", boost, boost2)
      if choice2 == "scissors":
        opponent.charge = 0
        battle.damageCalc("tie", boost, boost2)
      if choice2 == "skip":
        opponent.charge += 1
        battle.damageCalc("win", boost, boost2)

    if choice == "skip":
      player.charge += 1
      boost = player.charge
      boost2 = opponent.charge
      if choice2 == "rock":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "paper":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "scissors":
        opponent.charge = 0
        battle.damageCalc("lose", boost, boost2)
      if choice2 == "skip":
        opponent.charge += 1
        battle.damageCalc("tie", boost, boost2)

        
    else:
        gameSpace()

  def setRank():
    global reward
    if player.lvl in range(0,10):
      player.rank = game.ranks[0]
      reward = 20
    if player.lvl in range(11,20):
      player.rank = game.ranks[1]
      reward = 50
    if player.lvl in range(21,30):
      player.rank = game.ranks[2]
      reward = 100
    if player.lvl in range(31,40):
      player.rank = game.ranks[3]
      reward = 200
    if player.lvl in range(41,50):
      player.rank = game.ranks[4]
      reward = 500
    if player.lvl in range(51,60):
      player.rank = game.ranks[5]
      reward = 1000
    if player.lvl in range(61,70):
      player.rank = game.ranks[6]
      reward = 5000
    if player.lvl >= 71:
      player.rank = game.ranks[7]
      reward = 10_000

def createPlayer():
  player.hp = 10
  player.max_hp = 10
  player.lvl = 1
  player.cash = 100
  player.setRank()
  save_game()
  

class battle:
  def damageCalc(a,boost,enemyBoost):
    weapon = eval(f"game.items.{player.weapon.lower()}")
    if a == "tie":
      os.system('clear')
      print(f"{yellow}you and {opponent.name}'s attacks tied!")
      time.sleep(1)
      gameSpace()
    if a == "win":
      damage = weapon.atk + boost
      opponent.hp -= damage
      player.hp -= weapon.hurt
      os.system('clear')
      print(f"{green}your attack hit {opponent.name}!")
      time.sleep(1)
      gameSpace()
    if a == "lose":
      os.system('clear')
      print(f"{red}you were hit by {opponent.name}'s attack!")
      time.sleep(1)
      damage = opponent.weapon.atk + enemyBoost
      player.hp -= damage
      opponent.hp -= opponent.weapon.hurt
      gameSpace()
    if a == "skip":
      os.system('clear')
      print(f"{cyan}you and {opponent.name} are both charging!")
      time.sleep(1)
      gameSpace()

def save_game():
    localStorage.setItem('RPS_name', name) 
    localStorage.setItem('RPS_hp', player.hp)
    localStorage.setItem('RPS_max_hp', player.max_hp)
    localStorage.setItem('RPS_lvl', player.lvl)
    localStorage.setItem('RPS_cash', player.cash)
    localStorage.setItem('RPS_inv', player.inventory)
    localStorage.setItem('RPS_weapon', player.weapon)
    localStorage.setItem('RPS_ranked_warned', ranked_warned)

def load_game():
  global name, ranked_warned
  try:
    name = localStorage.getItem('RPS_name')
    player.hp = int(localStorage.getItem('RPS_hp'))
    player.max_hp = int(localStorage.getItem('RPS_max_hp'))
    player.lvl = int(localStorage.getItem('RPS_lvl'))
    player.cash = int(localStorage.getItem('RPS_cash'))
    invPlaceHold = localStorage.getItem('RPS_inv').split()
    player.weapon = localStorage.getItem('RPS_weapon')
    ranked_warned = localStorage.getItem('RPS_ranked_warned')
    for i in range(len(invPlaceHold)):
      player.inventory.append(invPlaceHold[i].replace("\'", "").replace("[", "").replace(",", "").replace("]", ""))
  except TypeError:
    createPlayer()
    save_game()
start_up()
