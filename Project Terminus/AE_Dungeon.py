import pygame
import random
import os
import math
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864
GRID_SIZE = 5
ROOM_SIZE = 150
DUNGEON_WIDTH = GRID_SIZE * ROOM_SIZE  # 750 pixels
LEFT_UI_WIDTH = 286
RIGHT_UI_WIDTH = 360
ROOM_COUNT = 10
DOOR_SIZE = 12
STARSHIP_SPRITE_SIZE = 128

# Colors
STARRY_BLUE = (10, 20, 50)
SILVER = (200, 200, 200)
BLUE = (50, 100, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Pagoda")

# Load sci-fi font (Orbitron, fallback to Arial)
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, "ASSETS", "orbitron.ttf")
try:
    font = pygame.font.Font(font_path, 24)
    font_small = pygame.font.Font(font_path, 18)
    font_large = pygame.font.Font(font_path, 28)
except FileNotFoundError:
    print(f"Error: Could not find '{font_path}'. Falling back to Arial.")
    font = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)
    font_large = pygame.font.SysFont("arial", 28)

# Load starship sprite
sprite_path = os.path.join(script_dir, "ASSETS", "prufer.png")
try:
    starship_sprite = pygame.image.load(sprite_path).convert_alpha()
    starship_sprite = pygame.transform.scale(starship_sprite, (STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE))
except FileNotFoundError:
    print(f"Error: Could not find '{sprite_path}'. Using placeholder.")
    starship_sprite = pygame.Surface((STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE), pygame.SRCALPHA)
    for x in range(STARSHIP_SPRITE_SIZE):
        for y in range(STARSHIP_SPRITE_SIZE):
            color = CYAN if (x + y) % 2 == 0 else WHITE
            starship_sprite.set_at((x, y), color)

# Room Descriptions Dictionary
ROOM_DESCRIPTIONS = {
    "pagoda_wooden": ["Pagoda Style", "The floors are woody, polished to a mirror sheen, reflecting cyan lights."],
    "quantum_vault": ["Quantum Vault", "Metallic walls pulse with unstable energy, humming softly."],
    "starlit_chamber": ["Starlit Chamber", "A domed ceiling reveals a starry void, serene yet unsettling."],
    "mirror_hall": ["Mirror Hall", "Mirrored walls create infinite reflections, distorting reality."],
    "core_sanctum": ["Core Sanctum", "A white platform glows faintly, the heart of the pagoda’s anomaly."]
}

# Item Class
class Item:
    def __init__(self, name: str, unrevealed_name, description, unrevealed_description, revealed=False):
        self.name = name
        self.unrevealed_name = unrevealed_name
        self.description = description
        self.unrevealed_description = unrevealed_description
        self.revealed = revealed

# Global Items Dictionary
ITEMS = {
    "quantum_crystal": Item(
        name="Quantum Crystal",
        unrevealed_name="Glowing Shard",
        description="A pulsating crystal containing 1 unit of Quanta.",
        unrevealed_description="A mysterious shard emitting faint light.",
        revealed=False
    ),
    "nano_repair_kit": Item(
        name="Nano Repair Kit",
        unrevealed_name="Strange Device",
        description="Restores 15-25 HP to the droid, 10% chance to overheat.",
        unrevealed_description="A compact device with unknown function.",
        revealed=False
    ),
    "quantum_disruptor": Item(
        name="Quantum Disruptor",
        unrevealed_name="Odd Gadget",
        description="Deals 10 damage and weakens enemy attack by 50% for 1 turn.",
        unrevealed_description="A peculiar gadget with erratic energy.",
        revealed=False
    )
}

# Einstein-Entity Class
class EinsteinEntity:
    def __init__(self, name: str, hp: int, attack: int, ability: str):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.ability = ability
        self.weakened = False  # Track Quantum Disruptor debuff

# Global EE Dictionary
EE_ENTITIES = {
    "Warper": EinsteinEntity("PlaceHolder", 20, 5, "spatial_warp"),
    "quantum_wraith": EinsteinEntity("Quantum Wraith", 30, 8, "quantum_leech")
}

class Room:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rect = pygame.Rect(grid_x * ROOM_SIZE, grid_y * ROOM_SIZE, ROOM_SIZE, ROOM_SIZE)
        self.doors = {"north": False, "south": False, "east": False, "west": False}
        self.items = random.sample(list(ITEMS.values()), k=random.randint(0, 3))
        self.entity = None
        self.does_have_sleeping_entity = False
        self.scanned = False
        if grid_x == 0 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["starlit_chamber"]
        elif grid_x == 2 and grid_y == 2:
            self.description = ROOM_DESCRIPTIONS["core_sanctum"]
        else:
            self.description = random.choice(list(ROOM_DESCRIPTIONS.values()))

    def get_door_rects(self):
        door_rects = []
        for direction in ["north", "south", "east", "west"]:
            if self.doors[direction]:
                if direction == "north":
                    door_rects.append(pygame.Rect(
                        self.rect.centerx - DOOR_SIZE // 2, self.rect.top - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "south":
                    door_rects.append(pygame.Rect(
                        self.rect.centerx - DOOR_SIZE // 2, self.rect.bottom - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "east":
                    door_rects.append(pygame.Rect(
                        self.rect.right - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
                elif direction == "west":
                    door_rects.append(pygame.Rect(
                        self.rect.left - DOOR_SIZE // 2, self.rect.centery - DOOR_SIZE // 2,
                        DOOR_SIZE, DOOR_SIZE
                    ))
        return door_rects

class Dungeon:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.rooms = []
        self.visited = set()
        self.generate_dungeon()

    def generate_dungeon(self):
        start_x, start_y = 0, 2
        start_room = Room(start_x, start_y)
        self.grid[start_y][start_x] = start_room
        self.rooms.append(start_room)
        available = [(start_x, start_y)]

        enemy_rooms = 0  # Track the number of rooms with enemies
        max_enemies = 5  # Set a maximum number of enemies

        while len(self.rooms) < ROOM_COUNT and available:
            curr_x, curr_y = random.choice(available)
            curr_room = self.grid[curr_y][curr_x]

            directions = []
            if curr_y > 0 and not self.grid[curr_y - 1][curr_x]:
                directions.append("north")
            if curr_y < GRID_SIZE - 1 and not self.grid[curr_y + 1][curr_x]:
                directions.append("south")
            if curr_x < GRID_SIZE - 1 and not self.grid[curr_y][curr_x + 1]:
                directions.append("east")
            if curr_x > 0 and not self.grid[curr_y][curr_x - 1]:
                directions.append("west")

            if not directions:
                available.remove((curr_x, curr_y))
                continue

            direction = random.choice(directions)
            new_x, new_y = curr_x, curr_y
            if direction == "north":
                new_y -= 1
                curr_room.doors["north"] = True
            elif direction == "south":
                new_y += 1
                curr_room.doors["south"] = True
            elif direction == "east":
                new_x += 1
                curr_room.doors["east"] = True
            elif direction == "west":
                new_x -= 1
                curr_room.doors["west"] = True

            new_room = Room(new_x, new_y)
            new_room.doors[{"north": "south", "south": "north", "east": "west", "west": "east"}[direction]] = True
            self.grid[new_y][new_x] = new_room
            self.rooms.append(new_room)
            available.append((new_x, new_y))

            # Spawn enemies with higher probability and ensure a minimum number
            if (new_x, new_y) != (0, 2) and (random.random() < 0.3 or enemy_rooms < max_enemies):
                new_room.entity = random.choice(list(EE_ENTITIES.values()))
                enemy_rooms += 1

class Player:
    def __init__(self, dungeon):
        self.current_room = dungeon.rooms[0]
        self.hp = 50
        self.quanta = 0  # Renamed from quantium
        self.inventory = []
        self.base_attack = 5
        self.dungeon = dungeon
        self.overheated = False  # Track Nano Repair Kit overheat
        self.dodge_active = False  # Track Phase Shift (Dodge)
        self.exiting = False  # Track extraction animation
        self.exit_animation_start = 0  # Animation start time

    def move(self, direction, popup):
        new_x, new_y = self.current_room.grid_x, self.current_room.grid_y
        if direction == "north" and self.current_room.doors["north"]:
            new_y -= 1
        elif direction == "south" and self.current_room.doors["south"]:
            new_y += 1
        elif direction == "east" and self.current_room.doors["east"]:
            new_x += 1
        elif direction == "west" and self.current_room.doors["west"]:
            new_x -= 1
        else:
            print(f"No portal to the {direction}")
            return False

        new_room = self.dungeon.grid[new_y][new_x]
        if new_room:
            self.quanta += 1  # Increment quanta for moving to a new room
            self.current_room = new_room
            print(f"Moved to Room at ({new_room.grid_x}, {new_room.grid_y})")
            if (new_room.grid_x, new_room.grid_y) not in self.dungeon.visited:
                self.dungeon.visited.add((new_room.grid_x, new_room.grid_y))
            if new_room.entity:
                popup.start_combat(self, new_room)
            return True
        print(f"No room to the {direction}")
        return False

    def exit_dungeon(self, popup):
        """Initiate the extraction sequence if conditions are met."""
        if self.current_room.grid_x == 0 and self.current_room.grid_y == 2:
            if self.quanta >= 10:
                self.exiting = True
                self.exit_animation_start = pygame.time.get_ticks() / 1000.0
                return True
            else:
                popup.show(["Mission Incomplete", "Insufficient Quanta to stabilize the Pagoda."])
                return False
        return False

    def combat(self, entity, popup):
        action = popup.combat_action
        popup.combat_log_lines.append(f"--- New Turn ---")

        # Reset dodge and overheat at turn start
        self.dodge_active = False
        if self.overheated:
            popup.combat_log_lines.append("Nano Repair Kit cools down!")
            self.overheated = False

        # Collect indices to remove to avoid modifying inventory during iteration
        to_remove = []

        # Player action
        if action == "quantum_strike":
            damage = random.randint(5, 10) + (self.quanta // 5)
            if random.random() < 0.2 and self.quanta >= 1:
                damage *= 2
                self.quanta -= 1
                popup.combat_log_lines.append(f"Critical Quantum Strike! You deal {damage} damage to {entity.name}!")
            else:
                popup.combat_log_lines.append(f"You deal {damage} damage to {entity.name}!")
            entity.hp -= damage
        elif action == "nano_repair_kit":
            for i, [item, qty] in enumerate(self.inventory[:]):  # Copy list
                if item.name == "Nano Repair Kit" and qty > 0:
                    heal = random.randint(15, 25)
                    self.hp = min(50, self.hp + heal)
                    qty -= 1
                    if qty == 0:
                        to_remove.append(i)
                    else:
                        self.inventory[i][1] = qty
                    popup.combat_log_lines.append(f"Used Nano Repair Kit. Restored {heal} HP!")
                    if random.random() < 0.1:
                        self.overheated = True
                        popup.combat_log_lines.append("Nano Repair Kit overheated!")
                    break
        elif action == "quantum_disruptor":
            for i, [item, qty] in enumerate(self.inventory[:]):  # Copy list
                if item.name == "Quantum Disruptor" and qty > 0:
                    entity.hp -= 10
                    entity.weakened = True
                    qty -= 1
                    if qty == 0:
                        to_remove.append(i)
                    else:
                        self.inventory[i][1] = qty
                    popup.combat_log_lines.append(f"Used Quantum Disruptor. Dealt 10 damage and weakened {entity.name}!")
                    break
        elif action == "phase_shift":
            if self.quanta >= 3:
                self.quanta -= 3
                if random.random() < 0.7:
                    self.dodge_active = True
                    popup.combat_log_lines.append("Phase Shift successful! Dodging next attack!")
                else:
                    popup.combat_log_lines.append("Phase Shift failed!")

        # Remove items after iteration
        for i in sorted(to_remove, reverse=True):
            self.inventory.pop(i)
        to_remove.clear()

        # Entity action (if alive and not dodged)
        if entity.hp > 0 and not self.dodge_active:
            attack = entity.attack // 2 if entity.weakened else entity.attack
            self.hp -= attack
            popup.combat_log_lines.append(f"{entity.name} deals {attack} damage!")
            entity.weakened = False  # Reset debuff

        # Resolve combat
        if self.hp <= 0:
            popup.combat_log_lines.append("Droid-E002 destroyed! Mission failed.")
            popup.combat_mode = False
            popup.game_over = True
        elif entity.hp <= 0:
            popup.combat_log_lines.append(f"{entity.name} defeated! Gained 1 Quantum Crystal.")
            self.current_room.entity = None
            for i, [item, qty] in enumerate(self.inventory):
                if item.name == "Quantum Crystal":
                    qty += 1
                    self.quanta += 1
                    self.inventory[i][1] = qty
                    break
            else:
                self.inventory.append([ITEMS["quantum_crystal"], 1])
                self.quanta += 1
            popup.combat_mode = False  # End combat only when the enemy is defeated

class LeftUI:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, LEFT_UI_WIDTH, SCREEN_HEIGHT)
        self.item_buttons = []

    def draw(self, screen, room):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Room name
        text = font.render(room.description[0], True, WHITE)
        screen.blit(text, (20, 20))
        # Room description with word-wrapping
        words = room.description[1].split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < 250:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (20, 60 + i * 30))

        # Objects list (after scan)
        self.item_buttons = []
        if room.scanned and room.items:
            text = font.render("Objects:", True, WHITE)
            screen.blit(text, (20, 160))
            for i, item in enumerate(room.items):
                name = item.name if item.revealed else item.unrevealed_name
                button = pygame.Rect(20, 200 + i * 60, 250, 50)
                pygame.draw.rect(screen, WHITE, button)
                pygame.draw.rect(screen, BLACK, button, 2)
                text = font.render(name, True, BLACK)
                screen.blit(text, (button.x + 10, button.y + 15))
                self.item_buttons.append((button, item))

    def handle_click(self, pos, player, room):
        if not room.scanned:
            print("Room not scanned, cannot collect items")
            return False
        total_items = sum(qty for _, qty in player.inventory)
        if total_items >= 10:
            print("Inventory full (10 items)")
            return False
        for button, item in self.item_buttons:
            if button.collidepoint(pos):
                print(f"Attempting to collect {item.name}")
                print(f"Current inventory: {[(i.name, q) for i, q in player.inventory]}")
                room.items.remove(item)
                item.revealed = True
                found = False
                for i, [inv_item, qty] in enumerate(player.inventory[:]):  # Copy list
                    if inv_item.name == item.name:
                        qty += 1
                        player.inventory[i][1] = qty
                        found = True
                        print(f"Incremented {item.name} to {qty}")
                        break
                if not found:
                    player.inventory.append([item, 1])
                    print(f"Added new {item.name} to inventory")
                if item.name == "Quantum Crystal":
                    player.quanta += 1
                    print(f"Quanta increased to {player.quanta}")
                print(f"Updated inventory: {[(i.name, q) for i, q in player.inventory]}")
                return True
        return False

class RightUI:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH, 0, RIGHT_UI_WIDTH, SCREEN_HEIGHT)
        self.buttons = {
            "north": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 200, 160, 50),
            "south": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 190, 200, 160, 50),
            "east": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 260, 160, 50),
            "west": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 190, 260, 160, 50),
            "scan": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 320, 330, 50),
            "exit": pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 380, 330, 50)
        }
        self.drop_buttons = []
        self.drop_all_buttons = []
        self.interact_buttons = []

    def draw(self, screen, player):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text = font.render(f"Droid-E002: HP {player.hp}/50", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 20))
        text = font.render(f"Quanta: {player.quanta}/20", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 60))

        for direction, rect in self.buttons.items():
            enabled = (direction != "scan" and direction != "exit" and player.current_room.doors.get(direction, False)) or \
                      direction == "scan" or \
                      (direction == "exit" and player.current_room.grid_x == 0 and player.current_room.grid_y == 2)
            color = WHITE if enabled else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text = font.render(direction.capitalize(), True, BLACK)
            screen.blit(text, (rect.x + 10, rect.y + 15))

        # Inventory label and count
        total_items = sum(qty for _, qty in player.inventory)
        text = font.render("Inventory", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 450))
        text = font.render(f"{total_items}/10", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - RIGHT_UI_WIDTH + 100, 450))
        
        self.drop_buttons = []
        self.drop_all_buttons = []
        self.interact_buttons = []
        for i, [item, quantity] in enumerate(player.inventory):
            name = item.name if item.revealed else item.unrevealed_name
            text = font.render(f"{name}: {quantity}", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - RIGHT_UI_WIDTH + 20, 480 + i * 30))
            # Interact button (placeholder)
            interact_button = pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 210, 480 + i * 30, 40, 30)
            pygame.draw.rect(screen, WHITE, interact_button)
            text = font.render("I", True, BLACK)
            screen.blit(text, (interact_button.x + 15, interact_button.y + 8))
            self.interact_buttons.append((interact_button, item))
            # Drop button
            drop_button = pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 260, 480 + i * 30, 30, 30)
            pygame.draw.rect(screen, WHITE, drop_button)
            text = font.render("D", True, BLACK)
            screen.blit(text, (drop_button.x + 10, drop_button.y + 8))
            self.drop_buttons.append((drop_button, item, 1))
            # Drop All button
            drop_all_button = pygame.Rect(SCREEN_WIDTH - RIGHT_UI_WIDTH + 300, 480 + i * 30, 50, 30)
            pygame.draw.rect(screen, WHITE, drop_all_button)
            text = font.render("All", True, BLACK)
            screen.blit(text, (drop_all_button.x + 10, drop_all_button.y + 8))
            self.drop_all_buttons.append((drop_all_button, item, quantity))

    def handle_click(self, pos, player, popup):
        for direction, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if direction == "scan":
                    player.current_room.scanned = True
                    popup.show(["Quantum Scan Results:", "Room scanned. Objects visible."])
                    print("Room scanned. Objects visible in left UI.")
                    return True
                elif direction == "exit" and player.current_room.grid_x == 0 and player.current_room.grid_y == 2:
                    player.exit_dungeon(popup)
                    return True
                elif player.move(direction, popup):
                    return True
        for button, item, qty in self.drop_buttons:
            if button.collidepoint(pos):
                for i, [inv_item, inv_qty] in enumerate(player.inventory[:]):  # Copy list
                    if inv_item.name == item.name:
                        inv_qty -= qty
                        if inv_item.name == "Quantum Crystal":
                            player.quanta -= qty
                        player.current_room.items.append(item)
                        if inv_qty <= 0:
                            player.inventory.pop(i)
                        else:
                            player.inventory[i][1] = inv_qty
                        print(f"Dropped {qty} {item.name}")
                        print(f"Updated inventory: {[(i.name, q) for i, q in player.inventory]}")
                        print(f"Room items: {[i.name for i in player.current_room.items]}")
                        return True
                return True
        for button, item, qty in self.drop_all_buttons:
            if button.collidepoint(pos):
                for i, [inv_item, inv_qty] in enumerate(player.inventory[:]):  # Copy list
                    if inv_item.name == item.name:
                        if inv_item.name == "Quantum Crystal":
                            player.quanta -= qty
                        for _ in range(qty):
                            player.current_room.items.append(item)
                        player.inventory.pop(i)
                        print(f"Dropped {qty} {item.name} as individual items")
                        print(f"Updated inventory: {[(i.name, q) for i, q in player.inventory]}")
                        print(f"Room items: {[i.name for i in player.current_room.items]}")
                        return True
                return True
        for button, item in self.interact_buttons:
            if button.collidepoint(pos):
                print(f"Interact with {item.name} (placeholder)")
                return True
        return False

class Popup:
    def __init__(self):
        self.active = False
        self.text = []
        self.rect = pygame.Rect(368, 182, 800, 500)  # 800x500 centered
        self.close_button = pygame.Rect(self.rect.right - 60, self.rect.bottom - 40, 50, 30)
        self.combat_mode = False
        self.exit_mode = False  # New mode for exit popup
        self.combat_action = None
        self.combat_log_lines = deque(maxlen=5)  # Max 5 lines, scrollable
        self.log_offset = 0  # For scrolling
        self.game_over = False
        self.exit_game = False  # Flag to exit game
        self.reset_game = False  # Flag to reset game
        self.player = None
        self.entity = None
        self.room = None
        # Action buttons (combat)
        self.quantum_strike_button = None
        self.nano_repair_button = None
        self.quantum_disruptor_button = None
        self.phase_shift_button = None
        # Exit buttons
        self.exit_game_button = None
        self.new_dungeon_button = None
        self.construct_button = None
        # Entity sprite (placeholder)
        self.entity_sprite = pygame.Surface((128, 128), pygame.SRCALPHA)
        for x in range(128):
            for y in range(128):
                color = CYAN if (x + y) % 2 == 0 else WHITE
                self.entity_sprite.set_at((x, y), color)
        self.sprite_scale = 1.0
        self.sprite_timer = 0
        # HP bar animations
        self.hp_animation = {
            "player": {"current": 50, "target": 50, "time": 0},
            "entity": {"current": 0, "target": 0, "time": 0}
        }
        # Tooltip
        self.tooltip = None
        # Border animation
        self.border_timer = 0

    def show(self, text):
        self.active = True
        self.text = text if isinstance(text, list) else [text]
        self.combat_mode = False
        self.exit_mode = False
        self.combat_log_lines.clear()
        self.log_offset = 0

    def show_exit(self, player):
        self.active = True
        self.text = ["You have left the dungeon"]
        self.combat_mode = False
        self.exit_mode = True
        self.combat_log_lines.clear()
        self.log_offset = 0

        # Check if the player has at least one Quantum Crystal
        has_crystals = any(item.name == "Quantum Crystal" and qty > 0 for item, qty in player.inventory)
        if has_crystals:
            self.text.append("You have the materials needed to begin assembly.")

    def start_combat(self, player, room):
        self.active = True
        self.combat_mode = True
        self.exit_mode = False
        self.combat_action = None
        self.combat_log_lines.clear()
        self.log_offset = 0
        self.player = player
        self.entity = room.entity
        self.room = room
        self.text = [f"Combat in {room.description[0]}"]
        self.hp_animation["entity"]["current"] = room.entity.hp
        self.hp_animation["entity"]["target"] = room.entity.hp
        self.hp_animation["entity"]["time"] = 0
        self.hp_animation["player"]["current"] = player.hp
        self.hp_animation["player"]["target"] = player.hp
        self.hp_animation["player"]["time"] = 0

    def draw(self, screen, delta_time):
        if not self.active:
            return

        # Dimmed overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Popup background
        pygame.draw.rect(screen, (10, 20, 50, 200), self.rect)
        self.border_timer += 0.1
        border_color = (0, 255, 255, int(255 * (0.8 + 0.2 * math.sin(self.border_timer))))
        pygame.draw.rect(screen, border_color, self.rect, 3)

        if self.combat_mode:
            if not (self.player and self.entity and self.room):
                text = font.render("Error: Combat data missing!", True, RED)
                screen.blit(text, (self.rect.x + 20, self.rect.y + 20))
                return

            try:
                # Room name
                text = font_large.render(self.text[0], True, WHITE)
                screen.blit(text, (self.rect.x + 400 - text.get_width() // 2, self.rect.y + 20))

                # Health bars background for clarity
                hp_background = pygame.Rect(self.rect.x + 100, self.rect.y + 80, 600, 80)
                pygame.draw.rect(screen, (0, 0, 0, 100), hp_background)

                # Enemy health bar and text (left side)
                text = font.render(f"{self.entity.name}: {self.entity.hp}/{self.entity.max_hp}", True, CYAN)
                screen.blit(text, (self.rect.x + 100, self.rect.y + 80))
                hp_ratio = self.hp_animation["entity"]["current"] / self.entity.max_hp if self.entity.max_hp > 0 else 0
                if self.hp_animation["entity"]["time"] > 0:
                    t = self.hp_animation["entity"]["time"] / 0.5
                    hp_ratio = self.hp_animation["entity"]["current"] + t * (self.hp_animation["entity"]["target"] - self.hp_animation["entity"]["current"])
                    self.hp_animation["entity"]["time"] -= delta_time
                    if self.hp_animation["entity"]["time"] < 0:
                        self.hp_animation["entity"]["time"] = 0
                pygame.draw.rect(screen, RED, (self.rect.x + 100, self.rect.y + 110, 150, 20))
                pygame.draw.rect(screen, GREEN, (self.rect.x + 100, self.rect.y + 110, 150 * max(0, min(1, hp_ratio)), 20))

                # Player health bar and text (right side)
                text = font.render(f"Droid-E002: {self.player.hp}/50", True, CYAN)
                screen.blit(text, (self.rect.x + 800 - 150 - 10, self.rect.y + 80))
                hp_ratio = self.hp_animation["player"]["current"] / 50 if self.player.hp > 0 else 0
                if self.hp_animation["player"]["time"] > 0:
                    t = self.hp_animation["player"]["time"] / 0.5
                    hp_ratio = self.hp_animation["player"]["current"] + t * (self.hp_animation["player"]["target"] - self.hp_animation["player"]["current"])
                    self.hp_animation["player"]["time"] -= delta_time
                    if self.hp_animation["player"]["time"] < 0:
                        self.hp_animation["player"]["time"] = 0
                pygame.draw.rect(screen, RED, (self.rect.x + 800 - 150 - 10, self.rect.y + 110, 150, 20))
                pygame.draw.rect(screen, GREEN, (self.rect.x + 800 - 150 - 10, self.rect.y + 110, 150 * max(0, min(1, hp_ratio)), 20))

                # Entity sprite (centered)
                self.sprite_timer += 0.1
                scale = 1.0 + 0.02 * math.sin(self.sprite_timer)
                scaled_sprite = pygame.transform.scale(self.entity_sprite, (int(128 * scale), int(128 * scale)))
                screen.blit(scaled_sprite, (self.rect.x + 400 - 64, self.rect.y + 250 - 64))

                # Combat log (left side, moved down)
                pygame.draw.rect(screen, (0, 0, 0, 100), (self.rect.x + 20, self.rect.y + 320, 300, 150))
                pygame.draw.rect(screen, CYAN, (self.rect.x + 20, self.rect.y + 320, 300, 150), 1)
                visible_lines = list(self.combat_log_lines)[-5 - self.log_offset:-self.log_offset if self.log_offset > 0 else None]
                for i, line in enumerate(visible_lines):
                    color = RED if "deals" in line.lower() or "destroyed" in line.lower() else \
                            GREEN if "restored" in line.lower() else \
                            YELLOW if "overheated" in line.lower() or "cools down" in line.lower() or "dodged" in line.lower() else CYAN
                    text = font_small.render(line, True, color)
                    screen.blit(text, (self.rect.x + 25, self.rect.y + 325 + i * 30))

                # Action buttons (horizontal row at bottom)
                button_width = 120
                button_height = 40
                spacing = 30
                total_width = 4 * button_width + 3 * spacing
                start_x = self.rect.x + 400 - total_width // 2
                self.phase_shift_button = pygame.Rect(start_x, self.rect.y + 460, button_width, button_height)
                self.nano_repair_button = pygame.Rect(start_x + button_width + spacing, self.rect.y + 460, button_width, button_height)
                self.quantum_disruptor_button = pygame.Rect(start_x + 2 * (button_width + spacing), self.rect.y + 460, button_width, button_height)
                self.quantum_strike_button = pygame.Rect(start_x + 3 * (button_width + spacing), self.rect.y + 460, button_width, button_height)

                for button, text_str in [(self.phase_shift_button, "Phase Shift"),
                                        (self.nano_repair_button, "Nano Repair"),
                                        (self.quantum_disruptor_button, "Disruptor"),
                                        (self.quantum_strike_button, "Quantum Strike")]:
                    mouse_pos = pygame.mouse.get_pos()
                    enabled = True
                    if button == self.nano_repair_button:
                        nano_qty = sum(qty for item, qty in self.player.inventory if item.name == "Nano Repair Kit")
                        enabled = nano_qty > 0 and not self.player.overheated
                    elif button == self.quantum_disruptor_button:
                        disruptor_qty = sum(qty for item, qty in self.player.inventory if item.name == "Quantum Disruptor")
                        enabled = disruptor_qty > 0
                    elif button == self.phase_shift_button:
                        enabled = self.player.quanta >= 3
                    color = CYAN if enabled and button.collidepoint(mouse_pos) else SILVER if enabled else GRAY
                    pygame.draw.rect(screen, color, button)
                    text = font_small.render(text_str, True, BLACK)
                    text_x = button.x + (button_width - text.get_width()) // 2
                    text_y = button.y + (button_height - text.get_height()) // 2
                    screen.blit(text, (text_x, text_y))
                    if not enabled:
                        pygame.draw.line(screen, RED, button.topleft, button.bottomright, 3)
                        pygame.draw.line(screen, RED, button.topright, button.bottomleft, 3)
                    if button == self.nano_repair_button and enabled:
                        text = font_small.render(f"x{nano_qty}", True, CYAN)
                        screen.blit(text, (button.x + button_width - text.get_width() - 5, button.y + button_height + 5))
                    elif button == self.quantum_disruptor_button and enabled:
                        disruptor_qty = sum(qty for item, qty in self.player.inventory if item.name == "Quantum Disruptor")
                        text = font_small.render(f"x{disruptor_qty}", True, CYAN)
                        screen.blit(text, (button.x + button_width - text.get_width() - 5, button.y + button_height + 5))
            except Exception as e:
                print(f"Error rendering combat UI: {e}")
                text = font.render("Combat UI Error!", True, RED)
                screen.blit(text, (self.rect.x + 20, self.rect.y + 20))
        elif self.exit_mode:
            # Exit popup
            text = font_large.render(self.text[0], True, WHITE)
            screen.blit(text, (self.rect.x + 400 - text.get_width() // 2, self.rect.y + 100))

            # Add the label in the center
            label = "Thanks for trying out AE: Assembly Alpha v0.7"
            sub_label = "Prequel of AE: TERMINUS"
            label_text = font.render(label, True, CYAN)
            sub_label_text = font.render(sub_label, True, CYAN)
            screen.blit(label_text, (self.rect.x + 400 - label_text.get_width() // 2, self.rect.y + 200))
            screen.blit(sub_label_text, (self.rect.x + 400 - sub_label_text.get_width() // 2, self.rect.y + 240))

            # Exit buttons (horizontal row at bottom)
            button_width = 150
            button_height = 40
            spacing = 30
            total_width = 3 * button_width + 2 * spacing
            start_x = self.rect.x + 400 - total_width // 2
            self.exit_game_button = pygame.Rect(start_x, self.rect.y + 460, button_width, button_height)
            self.new_dungeon_button = pygame.Rect(start_x + button_width + spacing, self.rect.y + 460, button_width, button_height)
            self.construct_button = pygame.Rect(start_x + 2 * (button_width + spacing), self.rect.y + 460, button_width, button_height)

            for button, text_str in [(self.exit_game_button, "Exit Game"),
                                    (self.new_dungeon_button, "Enter New Dungeon"),
                                    (self.construct_button, "Construct Assembly")]:
                mouse_pos = pygame.mouse.get_pos()
                color = CYAN if button.collidepoint(mouse_pos) else SILVER
                pygame.draw.rect(screen, color, button)
                text = font_small.render(text_str, True, BLACK)
                text_x = button.x + (button_width - text.get_width()) // 2
                text_y = button.y + (button_height - text.get_height()) // 2
                screen.blit(text, (text_x, text_y))
        else:
            # Non-combat, non-exit popup
            for i, line in enumerate(self.text):
                text = font.render(line, True, WHITE)
                screen.blit(text, (self.rect.x + 20, self.rect.y + 20 + i * 30))
            pygame.draw.rect(screen, WHITE, self.close_button)
            text = font.render("Close", True, BLACK)
            screen.blit(text, (self.close_button.x + 5, self.close_button.y + 5))

        # Tooltip
        if self.tooltip:
            mouse_pos = pygame.mouse.get_pos()
            text = font_small.render(self.tooltip, True, WHITE)
            tooltip_rect = pygame.Rect(mouse_pos[0] + 10, mouse_pos[1] + 10, 200, 30)
            pygame.draw.rect(screen, BLACK, tooltip_rect)
            pygame.draw.rect(screen, CYAN, tooltip_rect, 1)
            screen.blit(text, (tooltip_rect.x + 5, tooltip_rect.y + 5))

    def handle_click(self, pos, player, room):
        if not self.active:
            return False
        if not self.rect.collidepoint(pos):
            return False
        if self.combat_mode:
            self.tooltip = None
            mouse_pos = pos
            # Quantum Strike
            if self.quantum_strike_button and self.quantum_strike_button.collidepoint(pos):
                self.combat_action = "quantum_strike"
                self.hp_animation["entity"]["current"] = self.entity.hp
                self.hp_animation["entity"]["target"] = max(0, self.entity.hp - random.randint(5, 10))
                self.hp_animation["entity"]["time"] = 0.5
                self.hp_animation["player"]["current"] = self.player.hp
                self.hp_animation["player"]["target"] = max(0, self.player.hp - (self.entity.attack // 2 if self.entity.weakened else self.entity.attack))
                self.hp_animation["player"]["time"] = 0.5
                player.combat(room.entity, self)
                return True
            # Nano Repair Kit
            elif self.nano_repair_button and self.nano_repair_button.collidepoint(pos):
                nano_qty = sum(qty for item, qty in player.inventory if item.name == "Nano Repair Kit")
                if nano_qty > 0 and not player.overheated:
                    self.combat_action = "nano_repair_kit"
                    self.hp_animation["player"]["current"] = self.player.hp
                    self.hp_animation["player"]["target"] = min(50, self.player.hp + random.randint(15, 25))
                    self.hp_animation["player"]["time"] = 0.5
                    self.hp_animation["entity"]["current"] = self.entity.hp
                    self.hp_animation["entity"]["target"] = self.entity.hp
                    self.hp_animation["entity"]["time"] = 0.5
                    player.combat(room.entity, self)
                    return True
            # Quantum Disruptor
            elif self.quantum_disruptor_button and self.quantum_disruptor_button.collidepoint(pos):
                disruptor_qty = sum(qty for item, qty in player.inventory if item.name == "Quantum Disruptor")
                if disruptor_qty > 0:
                    self.combat_action = "quantum_disruptor"
                    self.hp_animation["entity"]["current"] = self.entity.hp
                    self.hp_animation["entity"]["target"] = max(0, self.entity.hp - 10)
                    self.hp_animation["entity"]["time"] = 0.5
                    self.hp_animation["player"]["current"] = self.player.hp
                    self.hp_animation["player"]["target"] = self.player.hp
                    self.hp_animation["player"]["time"] = 0.5
                    player.combat(room.entity, self)
                    return True
            # Phase Shift (Dodge)
            elif self.phase_shift_button and self.phase_shift_button.collidepoint(pos):
                if player.quanta >= 3:
                    self.combat_action = "phase_shift"
                    self.hp_animation["player"]["current"] = self.player.hp
                    self.hp_animation["player"]["target"] = self.player.hp
                    self.hp_animation["player"]["time"] = 0.5
                    self.hp_animation["entity"]["current"] = self.entity.hp
                    self.hp_animation["entity"]["target"] = self.entity.hp
                    self.hp_animation["entity"]["time"] = 0.5
                    player.combat(room.entity, self)
                    return True
        elif self.exit_mode:
            if self.exit_game_button and self.exit_game_button.collidepoint(pos):
                self.exit_game = True
                self.active = False
                return True
            elif self.new_dungeon_button and self.new_dungeon_button.collidepoint(pos):
                self.reset_game = True
                self.active = False
                return True
            elif self.construct_button and self.construct_button.collidepoint(pos):
                print("Construct Project Assembly: Feature not implemented")
                return True
        elif self.close_button.collidepoint(pos):
            self.active = False
            if self.game_over:
                return False
            return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL and self.combat_mode:
            self.log_offset = max(0, min(self.log_offset - event.y, len(self.combat_log_lines) - 5))
        elif event.type == pygame.MOUSEMOTION and self.combat_mode:
            self.tooltip = None
            if self.nano_repair_button and self.nano_repair_button.collidepoint(event.pos):
                self.tooltip = ITEMS["nano_repair_kit"].description
            elif self.quantum_disruptor_button and self.quantum_disruptor_button.collidepoint(event.pos):
                self.tooltip = ITEMS["quantum_disruptor"].description

# Main game
dungeon = Dungeon()
player = Player(dungeon)
left_ui = LeftUI()
right_ui = RightUI()
popup = Popup()
clock = pygame.time.Clock()
running = True

# Removed popup.show() for initial room entry
dungeon.visited.add((0, 2))

# Starship position (dynamic for animation)
starship_pos = [573 - STARSHIP_SPRITE_SIZE, 357 + ROOM_SIZE//2 - STARSHIP_SPRITE_SIZE//2]  # [445, 368]
EXIT_ANIMATION_DURATION = 2.0  # 2 seconds

while running:
    delta_time = clock.get_time() / 1000  # Convert ms to seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if popup.active and not popup.rect.collidepoint(event.pos):
                continue  # Ignore clicks outside popup
            if popup.handle_click(event.pos, player, player.current_room):
                if popup.game_over or popup.exit_game:
                    running = False
                elif popup.reset_game:
                    # Reset game state
                    dungeon = Dungeon()
                    player = Player(dungeon)
                    left_ui = LeftUI()
                    right_ui = RightUI()
                    popup = Popup()
                    dungeon.visited.add((0, 2))
                    starship_pos = [573 - STARSHIP_SPRITE_SIZE, 357 + ROOM_SIZE//2 - STARSHIP_SPRITE_SIZE//2]
                    popup.reset_game = False
                continue
            if left_ui.handle_click(event.pos, player, player.current_room):
                continue
            if right_ui.handle_click(event.pos, player, popup):
                continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and popup.active and not popup.combat_mode and not popup.exit_mode:
                popup.active = False
        elif event.type in (pygame.MOUSEWHEEL, pygame.MOUSEMOTION):
            popup.handle_event(event)

    # Handle starship exit animation
    if player.exiting:
        current_time = pygame.time.get_ticks() / 1000.0
        elapsed = current_time - player.exit_animation_start
        progress = min(elapsed / EXIT_ANIMATION_DURATION, 1.0)
        # Move starship left from x=445 to x=-128
        starship_pos[0] = 445 - progress * (445 + 128)
        if progress >= 1.0:
            player.exiting = False
            popup.show_exit(player)  # Pass the player object

    screen.fill(STARRY_BLUE)
    # Draw left UI
    left_ui.draw(screen, player.current_room)
    # Draw dungeon
    offset = (573, 57)
    for room in dungeon.rooms:
        offset_rect = room.rect.move(offset)
        if (room.grid_x, room.grid_y) in dungeon.visited:
            color = GREEN if room == player.current_room else SILVER
        else:
            color = GRAY
        pygame.draw.rect(screen, color, offset_rect)
        pygame.draw.rect(screen, CYAN, offset_rect, 4)
        for door_rect in room.get_door_rects():
            offset_door = door_rect.move(offset)
            pygame.draw.rect(screen, WHITE, offset_door)
    # Draw starship
    screen.blit(starship_sprite, (int(starship_pos[0]), int(starship_pos[1])))
    # Draw right UI and popup
    right_ui.draw(screen, player)
    popup.draw(screen, delta_time)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()