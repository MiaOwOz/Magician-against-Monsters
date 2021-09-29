import time
import random
##import digitalio
##import board
import sys
from enum import Enum

class AttackType(Enum):
    STANDARD = 0
    MAGIC = 1

FLEEING_CHANCE = 25
HEALING_AMOUNT = 150
STANDARD_ACCURACY = 75
MAGIC_ACCURACY = 60

#led_red = digitalio.DigitalInOut(board.D10)
#led_green = digitalio.DigitalInOut(board.D11)
#led_blue = digitalio.DigitalInOut(board.D12)
#led_red.direction = digitalio.Direction.OUTPUT
#led_green.direction = digitalio.Direction.OUTPUT
#led_blue.direction = digitalio.Direction.OUTPUT

player = {
    "name": "Player",
    "attack": 100,
    "magicAttack": 150,
    "critRate": 35,
    "critDamage": 2,
    "currentHP": 500,
    "maxHP": 500,
    "remainingPotions": 3
}

enemy = {
    "name": "Monster",
    "attack": 100,
    "critRate": 35,
    "critDamage": 2,
    "currentHP": 500,
    "maxHP": 500,
    "remainingPotions": 3
}

def drawGame():
    # Draw HP Bar of Monster
    filledBlocks = int(enemy["currentHP"] / 10 / 5)
    emptyBlocks = 10 - filledBlocks

    print( ("█" * filledBlocks) + ("░" * emptyBlocks) + " (" + str(enemy["currentHP"]) + " / " + str(enemy["maxHP"]) + " HP)")

    # Draw Monster
    print("    _________         .    .")
    print("   (..       \_    ,  |\  /|")
    print("    \       O  \  /|  \ \/ /")
    print("     \______    \/ |   \  / ")
    print("        vvvv\    \ |   /  |")
    print("        \^^^^  ==   \_/   |")
    print("         `\_   ===    \.  |")
    print("          / /\_   \ /      |")
    print("          |/   \_  \|      /")
    print("                \________/")

    time.sleep(1.0)

    # Make a free space
    print("")

    # Draw Magician
    print("         /^\  ")
    print("    /\   \"V\"")
    print("   /__\   I ")
    print("  //..\\  I")
    print("  \].`[/  I")
    print("  /l\/j\  (]")
    print(" /. ~~ ,\/I")
    print(" \\L__j^\/I")
    print("  \/--v}  I")
    print("  |    |  I")
    print("  |    |  I")
    print("  |    l  I")
    print("_/j  L l\_!")

    print("")

    # Draw Player HP Bar
    playerBlocks = int(player["currentHP"] / 10 / 5)
    emptyPlayerBlocks = 10 - playerBlocks

    print( ("█" * playerBlocks) + ("░" * emptyPlayerBlocks) + " (" + str(player["currentHP"]) + " / " + str(player["maxHP"]) + " HP)")

    time.sleep(1.0)

def enemyMove():
    print("Das Monster attackiert!")
    time.sleep(1.0)
    attack(enemy, player, AttackType.STANDARD)

def setHP(entity, value):
    entity["currentHP"] = value

def restoreHP(entity, value):
    entity["currentHP"] = entity["currentHP"] + value

def removeHP(entity, value):
    entity["currentHP"] = entity["currentHP"] - value

def getHP(entity):
    return entity["currentHP"]

def heal(entity):
    if entity["currentHP"] >= 500:
        print("Du hast bereits das maximum an Lebenspunkten!")
        time.sleep(2.0)
        movePrompt()
        return

    healingPossibilities = entity["remainingPotions"]
    if healingPossibilities > 1:
        currentEntityHP = entity["currentHP"]
        if (currentEntityHP + 150) >= 500:
            setHP(entity, 500)
        else:
            restoreHP(player, HEALING_AMOUNT)

        print("Es wurden " + str(HEALING_AMOUNT) + " HP wiederhergestellt.")
        entity["remainingPotions"] = healingPossibilities - 1
        time.sleep(2.0)
    else:
        print("Du hast keine Heiltränke mehr übrig!")
        time.sleep(2.0)
        movePrompt()

def attack(attacker, target, type):
    attackDamage = attacker["attack"] if type == AttackType.STANDARD else attacker["magicAttack"]

    hit = random.randint(1, 100)

    if type == AttackType.STANDARD:
        if hit > STANDARD_ACCURACY:
            print("Daneben!")
            time.sleep(2.0)
            if(attacker == player):
                enemyMove()
            else:
                movePrompt()
            return
    else:
        if hit > MAGIC_ACCURACY:
            print("Daneben!")
            time.sleep(2.0)
            enemyMove()
            return

    critRate = attacker["critRate"]
    critDamage = attacker["critDamage"]

    number = random.randint(1, 100)

    crit = True if number < critRate else False

    if crit:
        attackDamage = attackDamage * critDamage

    removeHP(target, attackDamage)

    if crit:
        print(target["name"] + " wurden " + str(attackDamage) + " HP Schaden zugefügt! (Crit Hit)")
        #for x in range(6):
        #    led_red.value = True
        #    time.sleep(0.2)
        #    led_red.value = False
        #    time.sleep(0.2)
    else:
        print(target["name"] + " wurden " + str(attackDamage) + " HP Schaden zugefügt!")
        #for x in range(6):
        #    led_blue.value = True
        #    time.sleep(0.2)
        #    led_blue.value = False
        #    time.sleep(0.2)

    time.sleep(1.0)

    if getHP(target) <= 0:
        print(target["name"] + " wurde besiegt!")
        if target == enemy:
            print("Du hast den Kampf gewonnen! Glückwunsch!")
        else:
            print("Du hast den Kampf verloren!")
        sys.exit()
    else:
        if attacker == player:
            enemyMove()
            movePrompt()
        else:
            movePrompt()

def movePrompt():
    drawGame()

    print(player["name"] + ", was wirst du tun?")
    print("A - Angriff | M - Magie | H - Heilung | F - Flucht")
    move = input()

    if move == "A" or move == "a":
        print(player["name"] + " greift an!")
        time.sleep(0.7)
        attack(player, enemy, AttackType.STANDARD)
    elif move == "M" or move == "m":
        print(player["name"] + " nutzt Magie!")
        time.sleep(0.7)
        attack(player, enemy, AttackType.MAGIC)
    elif move == "H" or move == "h":
        heal(player)
        enemyMove()
    elif move == "F" or move == "f":
        print("Versuche zu fliehen...")
        time.sleep(2.0)

        if random.randint(1, 100) < FLEEING_CHANCE:
            print("Du bist erfolgreich geflohen!")
            sys.exit()
        else:
            print("Flucht gescheitert!")
            time.sleep(1.0)
        enemyMove()
    else:
        print("Ungültige Eingabe!")
        movePrompt()

player["name"] = input("Wie heißt du? : ")
print("Hallo, " + player["name"] + "! Du wirst nun eine spannende (naja, nicht wirklich) Reise erleben!")
time.sleep(2.5)
print("Oh nein! Ein Monster! Schnell, besiege es!")
time.sleep(2.0)
movePrompt()
