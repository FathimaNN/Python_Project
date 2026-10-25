"""Legends of the Forgotten Realm — single-file Python RPG.
Run this file directly in PyCharm. Save data is stored in eldoria_save.json.
"""

"""Game data: classes, weapons, armor, potions, enemies, bosses and regions."""

CLASSES = {
    "1": {
        "name": "Warrior", "hp": 150, "mana": 45, "attack": 18, "defense": 12,
        "crit": 0.08, "skills": [
            {"name": "Slash", "cost": 5, "power": 1.5},
            {"name": "Shield Bash", "cost": 8, "power": 1.7},
            {"name": "Rage", "cost": 12, "power": 2.2},
            {"name": "Earthquake", "cost": 20, "power": 3.0}
        ]
    },
    "2": {
        "name": "Mage", "hp": 100, "mana": 120, "attack": 22, "defense": 5,
        "crit": 0.12, "skills": [
            {"name": "Fireball", "cost": 8, "power": 1.7},
            {"name": "Ice Blast", "cost": 12, "power": 2.0},
            {"name": "Thunder Strike", "cost": 18, "power": 2.5},
            {"name": "Meteor", "cost": 28, "power": 3.5}
        ]
    },
    "3": {
        "name": "Archer", "hp": 115, "mana": 70, "attack": 17, "defense": 8,
        "crit": 0.20, "skills": [
            {"name": "Multi Shot", "cost": 7, "power": 1.5},
            {"name": "Poison Arrow", "cost": 10, "power": 1.9},
            {"name": "Explosive Arrow", "cost": 16, "power": 2.4},
            {"name": "Sniper Shot", "cost": 24, "power": 3.3}
        ]
    },
    "4": {
        "name": "Assassin", "hp": 95, "mana": 75, "attack": 24, "defense": 4,
        "crit": 0.25, "skills": [
            {"name": "Backstab", "cost": 7, "power": 1.8},
            {"name": "Smoke Bomb", "cost": 10, "power": 2.0},
            {"name": "Shadow Strike", "cost": 16, "power": 2.6},
            {"name": "Instant Kill", "cost": 30, "power": 4.0}
        ]
    }
}

RARITIES = [
    ("Common", 1.0, 0.00, 1),
    ("Uncommon", 1.1, 0.02, 3),
    ("Rare", 1.3, 0.05, 8),
    ("Super Rare", 1.5, 0.08, 15),
    ("Epic", 1.8, 0.12, 25),
    ("Mythical", 2.2, 0.18, 40),
    ("Legendary", 2.8, 0.25, 60),
]

# At least 20 distinct weapons, each with name, rank, damage, crit bonus, price and required level.
_WEAPON_NAMES = [
    "Wooden Sword", "Rusty Axe", "Training Bow", "Stone Dagger",
    "Copper Spear", "Hunter's Knife", "Iron Sword", "Steel Axe",
    "Long Bow", "Silver Dagger", "Crystal Blade", "Shadow Dagger",
    "Lightning Bow", "Frost Spear", "Flame Sword", "Ice Spear",
    "Thunder Hammer", "Storm Katana", "Phoenix Blade", "Demon Slayer",
    "Celestial Staff", "Dragon King's Sword", "Blade of Eternity", "Bow of the Gods"
]
WEAPONS = []
for i, name in enumerate(_WEAPON_NAMES):
    rarity, multiplier, crit_bonus, required_level = RARITIES[min(i // 4, 6)]
    base = 5 + i * 3
    WEAPONS.append({
        "name": name, "rank": rarity, "damage": int(base * multiplier),
        "crit_bonus": crit_bonus, "price": int((20 + i * 35) * multiplier),
        "required_level": required_level
    })

_ARMOR_NAMES = [
    "Cloth Outfit", "Leather Armor", "Guard's Mail", "Forest Ranger Set",
    "Iron Plate", "Moon Robes", "Crystal Armor", "Shadow Suit",
    "Flame Guard", "Frost Warden", "Phoenix Armor", "Demon Lord Armor",
    "Celestial Aegis", "Dragon Scale Armor"
]
ARMOR = []
for i, name in enumerate(_ARMOR_NAMES):
    rarity, multiplier, crit_bonus, required_level = RARITIES[min(i // 2, 6)]
    ARMOR.append({
        "name": name, "rank": rarity,
        "defense": int((2 + i * 2) * multiplier),
        "hp_bonus": int((10 + i * 8) * multiplier),
        "mana_bonus": int((5 + i * 5) * multiplier),
        "crit_resistance": round(min(0.03 + i * 0.012, 0.20), 2),
        "price": int((25 + i * 45) * multiplier),
        "required_level": required_level
    })

POTIONS = [
    {"name": "Small Health Potion", "kind": "health", "amount": 50, "price": 15},
    {"name": "Medium Health Potion", "kind": "health", "amount": 100, "price": 30},
    {"name": "Large Health Potion", "kind": "health", "amount": 250, "price": 60},
    {"name": "Giant Health Potion", "kind": "health", "amount": 500, "price": 100},
    {"name": "Ultimate Health Potion", "kind": "health", "amount": 99999, "price": 180},
    {"name": "Small Mana Potion", "kind": "mana", "amount": 30, "price": 15},
    {"name": "Medium Mana Potion", "kind": "mana", "amount": 75, "price": 30},
    {"name": "Large Mana Potion", "kind": "mana", "amount": 150, "price": 60},
    {"name": "Giant Mana Potion", "kind": "mana", "amount": 300, "price": 100},
    {"name": "Ultimate Mana Potion", "kind": "mana", "amount": 99999, "price": 180},
    {"name": "Balanced Tonic", "kind": "mixed", "amount": 60, "price": 45},
    {"name": "Royal Elixir", "kind": "mixed", "amount": 150, "price": 90},
    {"name": "Warrior's Brew", "kind": "attack_buff", "amount": 5, "price": 55},
    {"name": "Iron Skin Tonic", "kind": "defense_buff", "amount": 5, "price": 55},
    {"name": "Eagle Eye Draught", "kind": "crit_buff", "amount": 0.10, "price": 65},
    {"name": "Champion's Mixture", "kind": "mixed", "amount": 250, "price": 130},
]

ENEMY_NAMES = [
    "Goblin", "Wolf", "Slime", "Zombie", "Skeleton",
    "Orc", "Bandit", "Troll", "Dark Archer", "Giant Spider",
    "Vampire", "Werewolf", "Necromancer", "Ice Golem", "Fire Demon",
    "Sand Raider", "Desert Scorpion", "Ancient Guardian", "Cursed Knight", "Ruins Wraith",
    "Castle Hound", "Blood Mage", "Lava Beast", "Magma Troll", "Ash Dragon",
    "Frost Wolf", "Snow Ogre", "Glacier Witch", "Sky Harpy", "Storm Giant",
    "Void Stalker", "Demon Hound", "Soul Reaper", "Abyss Knight", "Realm Destroyer"
]

BOSSES = {
    10: "Goblin King",
    20: "Forest Guardian",
    30: "Ancient Golem",
    40: "Vampire Lord",
    50: "Dragon Rider",
    60: "Demon General",
    70: "Ice Titan",
    80: "Shadow Emperor",
    90: "Celestial Dragon",
    100: "Ancient Demon King",
}

REGIONS = [
    "Village", "Forest", "Cave", "Desert", "Ruins",
    "Castle", "Volcano", "Frozen Mountain", "Sky Temple", "Demon Realm"
]


"""Player character model and leveling logic."""
class Player:
    def __init__(self, name, class_key):
        template = CLASSES[class_key]
        self.name = name
        self.hero_class = template["name"]
        self.class_key = class_key
        self.level = 1
        self.exp = 0
        self.gold = 100
        self.max_hp = template["hp"]
        self.hp = self.max_hp
        self.max_mana = template["mana"]
        self.mana = self.max_mana
        self.attack = template["attack"]
        self.defense = template["defense"]
        self.crit = template["crit"]
        self.crit_damage = 1.8
        self.weapon = None
        self.armor = None
        self.potions = {"Small Health Potion": 3, "Small Mana Potion": 2}
        self.inventory = []
        self.bosses_defeated = []
        self.enemies_defeated = 0
        self.weapons_collected = []
        self.rare_items_found = []
        self.regions_unlocked = 1
        self.buff_turns = 0
        self.attack_buff = 0
        self.defense_buff = 0
        self.crit_buff = 0
        self.play_seconds = 0

    def total_attack(self):
        return self.attack + (self.weapon["damage"] if self.weapon else 0) + self.attack_buff

    def total_defense(self):
        return self.defense + (self.armor["defense"] if self.armor else 0) + self.defense_buff

    def total_crit(self):
        return min(0.75, self.crit + (self.weapon["crit_bonus"] if self.weapon else 0) + self.crit_buff)

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.level * 50 and self.level < 100:
            self.exp -= self.level * 50
            self.level += 1
            self.max_hp += 12
            self.max_mana += 6
            self.attack += 3
            self.defense += 2
            self.hp = self.max_hp
            self.mana = self.max_mana
            print(f"\nLEVEL UP! You are now level {self.level}. Your stats increased!")
            if self.level % 5 == 0:
                print("Milestone reached: your skills become stronger!")

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"], data["class_key"])
        player.__dict__.update(data)
        return player


"""JSON save/load functions."""
import json
import os

SAVE_FILE = "eldoria_save.json"


def save_game(player):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(player.to_dict(), file, indent=4)
        print(f"Game saved to {SAVE_FILE}.")
    except (OSError, TypeError) as error:
        print("Could not save game:", error)


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No saved game found. Start a new game first.")
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        player = Player.from_dict(data)
        print(f"Welcome back, {player.name}!")
        return player
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print("Save file could not be loaded:", error)
        return None


"""Main game loop, combat, shop, inventory and progression."""
import random
import time
def ask_choice(prompt, valid):
    while True:
        value = input(prompt).strip()
        if value in valid:
            return value
        print("Invalid choice. Please try again.")


def pause():
    input("\nPress Enter to continue...")


class Game:
    def __init__(self):
        self.player = None
        self.start_time = time.time()

    def main_menu(self):
        while True:
            print("""
========================================
 LEGENDS OF THE FORGOTTEN REALM
========================================
1. New Game
2. Continue (Load Save)
3. Instructions
4. Exit
""")
            choice = ask_choice("Choose: ", {"1", "2", "3", "4"})
            if choice == "1":
                self.new_game()
                self.adventure_loop()
            elif choice == "2":
                self.player = load_game()
                if self.player:
                    self.adventure_loop()
            elif choice == "3":
                self.instructions()
            else:
                print("Farewell, hero of Eldoria!")
                return

    def instructions(self):
        print("""
HOW TO PLAY
- Create a hero and choose Warrior, Mage, Archer, or Assassin.
- Visit the shop to buy gear and potions.
- Choose Explore to fight enemies and gain EXP and gold.
- Bosses appear at levels 10, 20, ... 100. Defeat a boss to unlock the next region.
- Save often. Continue loads your JSON save file.
- In battle: Attack, Skills, Heal, Use Potion, Defend, Inventory, Stats, Run.
""")
        pause()

    def new_game(self):
        print("\nChoose your hero:")
        name = input("Enter Player Name: ").strip() or "Hero"
        for key, template in CLASSES.items():
            print(f"{key}. {template['name']} (HP {template['hp']}, Mana {template['mana']}, "
                  f"Attack {template['attack']}, Defense {template['defense']})")
        class_key = ask_choice("Choose class (1-4): ", set(CLASSES))
        self.player = Player(name, class_key)
        self.start_time = time.time()
        print(f"\nWelcome, {name} the {self.player.hero_class}! Eldoria needs you.")
        self.show_stats()
        pause()

    def adventure_loop(self):
        if not self.player:
            return
        while self.player.hp > 0 and self.player.level < 100 or (
            self.player and self.player.hp > 0 and 100 in self.player.bosses_defeated
        ):
            if self.player.level >= 100 and 100 in self.player.bosses_defeated:
                self.victory_screen()
                return
            print(f"""
--- {self.player.name} | Level {self.player.level} | HP {self.player.hp}/{self.player.max_hp}
Gold: {self.player.gold} | Region: {REGIONS[min((self.player.level - 1)//10, 9)]}
1. Explore and Battle
2. Village Shop
3. Inventory
4. View Stats
5. World Map
6. Save Game
7. Return to Main Menu
""")
            choice = ask_choice("Choose: ", {"1", "2", "3", "4", "5", "6", "7"})
            if choice == "1":
                self.explore()
                if self.player.hp <= 0:
                    self.game_over()
                    return
            elif choice == "2":
                self.shop()
            elif choice == "3":
                self.inventory_menu()
            elif choice == "4":
                self.show_stats()
                pause()
            elif choice == "5":
                self.show_map()
                pause()
            elif choice == "6":
                save_game(self.player)
            elif choice == "7":
                save_game(self.player)
                return

    def show_stats(self):
        p = self.player
        print(f"""
===== HERO STATS =====
Name: {p.name} | Class: {p.hero_class}
Level: {p.level} | EXP: {p.exp}/{p.level * 50}
HP: {p.hp}/{p.max_hp} | Mana: {p.mana}/{p.max_mana}
Attack: {p.total_attack()} | Defense: {p.total_defense()}
Critical chance: {p.total_crit():.0%} | Critical damage: x{p.crit_damage}
Gold: {p.gold}
Weapon: {p.weapon['name'] if p.weapon else 'None'}
Armor: {p.armor['name'] if p.armor else 'None'}
Potions: {p.potions}
Enemies defeated: {p.enemies_defeated}
Bosses defeated: {len(p.bosses_defeated)}/10
""")

    def show_map(self):
        print("\n===== WORLD MAP =====")
        for i, region in enumerate(REGIONS, start=1):
            status = "UNLOCKED" if i <= self.player.regions_unlocked else "LOCKED"
            print(f"{i}. {region} - {status}")
        print("A region opens when you defeat its boss.")

    def explore(self):
        p = self.player
        next_boss_level = ((p.level // 10) + 1) * 10
        if p.level % 10 == 0 and p.level not in p.bosses_defeated:
            enemy_name = BOSSES[p.level]
            is_boss = True
        elif p.level >= 9 and p.level % 10 == 9 and p.level + 1 in BOSSES and p.level + 1 not in p.bosses_defeated:
            print(f"\nYou sense a boss nearby. Prepare for level {p.level + 1}!")
            enemy_name = random.choice(ENEMY_NAMES[min((p.level-1)//3, len(ENEMY_NAMES)-1):])
            is_boss = False
        else:
            low = min((p.level - 1) // 3, len(ENEMY_NAMES) - 1)
            high = min(low + 5, len(ENEMY_NAMES))
            enemy_name = random.choice(ENEMY_NAMES[low:high])
            is_boss = False

        scale = p.level
        enemy = {
            "name": enemy_name,
            "max_hp": (130 + scale * 15) if is_boss else (35 + scale * 13),
            "hp": (130 + scale * 15) if is_boss else (35 + scale * 13),
            "attack": (12 + scale * 3) if is_boss else (5 + scale * 2),
            "defense": (5 + scale) if is_boss else (scale // 2)
        }
        if is_boss:
            enemy["max_hp"] *= 2
            enemy["hp"] = enemy["max_hp"]
            print(f"\n!!! BOSS ENCOUNTER: {enemy_name} !!!")
        else:
            print(f"\nA wild {enemy_name} appears!")
        self.battle(enemy, is_boss)

    def battle(self, enemy, is_boss):
        p = self.player
        turn = 0
        defending = False
        while enemy["hp"] > 0 and p.hp > 0:
            turn += 1
            print(f"\n{p.name}: HP {p.hp}/{p.max_hp}, Mana {p.mana}/{p.max_mana}")
            print(f"{enemy['name']}: HP {enemy['hp']}/{enemy['max_hp']}")
            print("""1. Attack
2. Skills
3. Heal
4. Use Potion
5. Defend
6. Inventory
7. View Stats
8. Run""")
            action = ask_choice("Your action: ", set("12345678"))
            enemy_turn = True
            if action == "1":
                self.player_attack(enemy)
            elif action == "2":
                self.use_skill(enemy)
            elif action == "3":
                before = p.hp
                p.hp = min(p.max_hp, p.hp + 35)
                print(f"You recovered {p.hp-before} HP.")
            elif action == "4":
                self.use_potion(in_battle=True)
            elif action == "5":
                defending = True
                print("You brace yourself. The next incoming attack is reduced by 50%.")
            elif action == "6":
                self.inventory_menu()
                enemy_turn = False
            elif action == "7":
                self.show_stats()
                enemy_turn = False
            elif action == "8":
                if is_boss:
                    print("You cannot run from a boss battle!")
                elif random.random() < 0.65:
                    print("You escaped safely.")
                    return
                else:
                    print("Escape failed!")
            if enemy["hp"] <= 0:
                break
            if enemy_turn:
                damage = max(1, enemy["attack"] - p.total_defense())
                if random.random() < 0.10:
                    damage = int(damage * 1.5)
                    print(f"{enemy['name']} lands a critical hit!")
                if is_boss and turn % 3 == 0:
                    damage = int(damage * 1.5)
                    enemy["hp"] = min(enemy["max_hp"], enemy["hp"] + 10)
                    print(f"{enemy['name']} uses a special attack and heals 10 HP!")
                if defending:
                    damage = max(1, int(damage * 0.5))
                    defending = False
                p.hp = max(0, p.hp - damage)
                print(f"{enemy['name']} hits you for {damage} damage.")
            if p.buff_turns > 0:
                p.buff_turns -= 1
                if p.buff_turns == 0:
                    p.attack_buff = p.defense_buff = p.crit_buff = 0
                    print("Your temporary potion buffs have worn off.")

        if p.hp <= 0:
            return
        print(f"\nYou defeated {enemy['name']}!")
        p.enemies_defeated += 1
        exp_gain = 35 + p.level * 12 + (100 if is_boss else 0)
        gold_gain = random.randint(15, 35) + p.level * 4 + (150 if is_boss else 0)
        p.gold += gold_gain
        p.gain_exp(exp_gain)
        print(f"You gained {exp_gain} EXP and {gold_gain} gold.")
        self.loot_drop(is_boss)
        if is_boss:
            boss_level = p.level if p.level in BOSSES else min(100, ((p.level + 9)//10)*10)
            if boss_level not in p.bosses_defeated:
                p.bosses_defeated.append(boss_level)
            p.regions_unlocked = min(10, len(p.bosses_defeated) + 1)
            print(f"Boss defeated! New region unlocked. Bosses defeated: {len(p.bosses_defeated)}")
            if boss_level == 100:
                self.victory_screen()

    def player_attack(self, enemy):
        p = self.player
        damage = max(1, p.total_attack() - enemy["defense"])
        if random.random() < p.total_crit():
            damage = int(damage * p.crit_damage)
            print("CRITICAL HIT!")
        enemy["hp"] = max(0, enemy["hp"] - damage)
        print(f"You deal {damage} damage.")

    def use_skill(self, enemy):
        p = self.player
        skills = CLASSES[p.class_key]["skills"]
        for i, skill in enumerate(skills, start=1):
            print(f"{i}. {skill['name']} (Mana {skill['cost']}, power x{skill['power']})")
        print("0. Cancel")
        choice = ask_choice("Choose skill: ", {str(i) for i in range(len(skills)+1)})
        if choice == "0":
            return
        skill = skills[int(choice)-1]
        if p.mana < skill["cost"]:
            print("Not enough mana! Try a potion or a normal attack.")
            return
        p.mana -= skill["cost"]
        damage = max(1, int(p.total_attack() * skill["power"] - enemy["defense"]))
        if random.random() < p.total_crit():
            damage = int(damage * p.crit_damage)
            print("SKILL CRITICAL HIT!")
        enemy["hp"] = max(0, enemy["hp"] - damage)
        print(f"{skill['name']} deals {damage} damage!")

    def use_potion(self, in_battle=False):
        p = self.player
        available = [(name, count) for name, count in p.potions.items() if count > 0]
        if not available:
            print("You have no potions.")
            return
        for i, (name, count) in enumerate(available, start=1):
            print(f"{i}. {name} x{count}")
        print("0. Cancel")
        choice = ask_choice("Choose potion: ", {str(i) for i in range(len(available)+1)})
        if choice == "0":
            return
        name = available[int(choice)-1][0]
        potion = next(item for item in POTIONS if item["name"] == name)
        p.potions[name] -= 1
        if potion["kind"] == "health":
            restored = p.max_hp if potion["amount"] > 9000 else potion["amount"]
            old = p.hp
            p.hp = min(p.max_hp, p.hp + restored)
            print(f"Recovered {p.hp-old} HP.")
        elif potion["kind"] == "mana":
            restored = p.max_mana if potion["amount"] > 9000 else potion["amount"]
            old = p.mana
            p.mana = min(p.max_mana, p.mana + restored)
            print(f"Recovered {p.mana-old} Mana.")
        elif potion["kind"] == "mixed":
            p.hp = min(p.max_hp, p.hp + potion["amount"])
            p.mana = min(p.max_mana, p.mana + potion["amount"] // 2)
            print("Recovered HP and Mana.")
        elif potion["kind"] == "attack_buff":
            p.attack_buff = potion["amount"]
            p.buff_turns = 3
            print("Attack increased for 3 turns.")
        elif potion["kind"] == "defense_buff":
            p.defense_buff = potion["amount"]
            p.buff_turns = 3
            print("Defense increased for 3 turns.")
        elif potion["kind"] == "crit_buff":
            p.crit_buff = potion["amount"]
            p.buff_turns = 3
            print("Critical chance increased for 3 turns.")

    def loot_drop(self, is_boss):
        p = self.player
        p.gold += random.randint(5, 20)
        if random.random() < (0.75 if is_boss else 0.35):
            potion = random.choice(POTIONS)
            p.potions[potion["name"]] = p.potions.get(potion["name"], 0) + 1
            print(f"Loot: found {potion['name']}!")
        if random.random() < (1.0 if is_boss else 0.12):
            eligible = [w for w in WEAPONS if w["required_level"] <= p.level]
            weapon = random.choice(eligible)
            p.inventory.append({"type": "weapon", "item": weapon.copy()})
            p.weapons_collected.append(weapon["name"])
            if weapon["rank"] not in ("Common", "Uncommon"):
                p.rare_items_found.append(weapon["name"])
            print(f"Loot: found {weapon['rank']} weapon: {weapon['name']}!")
        if random.random() < (1.0 if is_boss else 0.08):
            eligible = [a for a in ARMOR if a["required_level"] <= p.level]
            armor = random.choice(eligible)
            p.inventory.append({"type": "armor", "item": armor.copy()})
            print(f"Loot: found armor: {armor['name']}!")

    def inventory_menu(self):
        p = self.player
        while True:
            print("\n===== INVENTORY =====")
            print("Potions:", p.potions)
            if not p.inventory:
                print("No gear or materials in inventory.")
            else:
                for i, entry in enumerate(p.inventory, start=1):
                    item = entry["item"]
                    print(f"{i}. [{entry['type']}] {item['name']} ({item['rank']})")
            print("1. Equip item  2. Unequip gear  3. Drop item  4. Sell item  5. Use potion  0. Back")
            choice = ask_choice("Choose: ", {"0", "1", "2", "3", "4", "5"})
            if choice == "0":
                return
            if choice == "5":
                self.use_potion()
                continue
            if choice == "2":
                slot = ask_choice("Unequip (w)eapon or (a)rmor? ", {"w", "a"})
                if slot == "w":
                    p.weapon = None
                else:
                    p.armor = None
                print("Gear unequipped.")
                continue
            if not p.inventory:
                print("Inventory is empty.")
                continue
            index = self.ask_item_index(len(p.inventory))
            if index is None:
                continue
            entry = p.inventory[index]
            item = entry["item"]
            if choice == "1":
                if item["required_level"] > p.level:
                    print("Your level is too low to equip this item.")
                elif entry["type"] == "weapon":
                    p.weapon = item
                    print(f"Equipped {item['name']}.")
                elif entry["type"] == "armor":
                    p.armor = item
                    p.max_hp += item["hp_bonus"]
                    p.max_mana += item["mana_bonus"]
                    p.hp = min(p.max_hp, p.hp + item["hp_bonus"])
                    print(f"Equipped {item['name']}.")
            elif choice == "3":
                removed = p.inventory.pop(index)
                print(f"Dropped {removed['item']['name']}.")
            elif choice == "4":
                removed = p.inventory.pop(index)
                price = max(1, int(removed["item"]["price"] * 0.4))
                p.gold += price
                print(f"Sold {removed['item']['name']} for {price} gold.")

    def ask_item_index(self, length):
        while True:
            raw = input(f"Item number (1-{length}, or 0 to cancel): ").strip()
            try:
                number = int(raw)
                if number == 0:
                    return None
                if 1 <= number <= length:
                    return number - 1
            except ValueError:
                pass
            print("Enter a valid item number.")

    def shop(self):
        p = self.player
        while True:
            print(f"\n===== VILLAGE SHOP | Gold: {p.gold} =====")
            print("1. Buy Weapon  2. Buy Armor  3. Buy Potion  4. Sell Inventory Item  0. Exit")
            choice = ask_choice("Choose: ", {"0", "1", "2", "3", "4"})
            if choice == "0":
                return
            if choice == "1":
                self.buy_from_list(WEAPONS, "weapon")
            elif choice == "2":
                self.buy_from_list(ARMOR, "armor")
            elif choice == "3":
                for i, potion in enumerate(POTIONS, start=1):
                    print(f"{i}. {potion['name']} - {potion['price']} gold")
                index = self.ask_item_index(len(POTIONS))
                if index is not None:
                    potion = POTIONS[index]
                    if p.gold >= potion["price"]:
                        p.gold -= potion["price"]
                        p.potions[potion["name"]] = p.potions.get(potion["name"], 0) + 1
                        print("Potion purchased.")
                    else:
                        print("Not enough gold.")
            elif choice == "4":
                self.sell_inventory_item()

    def buy_from_list(self, items, kind):
        p = self.player
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item['name']} [{item['rank']}] Level {item['required_level']} - {item['price']} gold")
        index = self.ask_item_index(len(items))
        if index is None:
            return
        item = items[index]
        if p.level < item["required_level"]:
            print("Your level is too low for this item.")
        elif p.gold < item["price"]:
            print("Not enough gold.")
        else:
            p.gold -= item["price"]
            p.inventory.append({"type": kind, "item": item.copy()})
            print(f"Purchased {item['name']}.")

    def sell_inventory_item(self):
        p = self.player
        if not p.inventory:
            print("Nothing to sell.")
            return
        for i, entry in enumerate(p.inventory, start=1):
            print(f"{i}. {entry['item']['name']} - sell for {max(1, int(entry['item']['price']*0.4))} gold")
        index = self.ask_item_index(len(p.inventory))
        if index is not None:
            entry = p.inventory.pop(index)
            price = max(1, int(entry["item"]["price"] * 0.4))
            p.gold += price
            print(f"Sold item for {price} gold.")

    def game_over(self):
        print("\n========== GAME OVER ==========")
        print(f"{self.player.name} has fallen in Eldoria.")
        print("1. Retry from level 1 (new hero)  2. Load Save  3. Exit to main menu")
        choice = ask_choice("Choose: ", {"1", "2", "3"})
        if choice == "1":
            self.new_game()
            self.adventure_loop()
        elif choice == "2":
            loaded = load_game()
            if loaded:
                self.player = loaded
                self.adventure_loop()

    def victory_screen(self):
        elapsed = int(time.time() - self.start_time) + self.player.play_seconds
        p = self.player
        print("""
========================================
       VICTORY - ELDORIA IS SAVED!
========================================""")
        print(f"Player: {p.name} | Class: {p.hero_class}")
        print(f"Final Level: {p.level} | Total Gold: {p.gold}")
        print(f"Bosses Defeated: {len(p.bosses_defeated)} | Enemies Defeated: {p.enemies_defeated}")
        print(f"Weapons Collected: {len(p.weapons_collected)} | Rare Items Found: {len(p.rare_items_found)}")
        print(f"Play time this session: {elapsed} seconds")
        print(f"Final Score: {p.level * 100 + p.enemies_defeated * 10 + p.gold}")
        save_game(p)
        print("The Ancient Demon King has been defeated. Peace returns to Eldoria!")
        self.player = None


"""Legends of the Forgotten Realm - beginner-friendly command-line RPG."""



def main():
    game = Game()
    game.main_menu()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nThe adventure has ended. Thanks for playing!")
