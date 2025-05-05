import pygame
import random
import os

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

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Pagoda")
font = pygame.font.SysFont("arial", 24)

# Load starship sprite
script_dir = os.path.dirname(os.path.abspath(__file__))
sprite_path = os.path.join(script_dir, "ASSETS", "prufer.png")
try:
    starship_sprite = pygame.image.load(sprite_path).convert_alpha()
    starship_sprite = pygame.transform.scale(starship_sprite, (STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE))
except FileNotFoundError:
    print(f"Error: Could not find '{sprite_path}'. Ensure 'prufer.png' is in the 'ASSETS' folder.")
    print(f"Current working directory: {os.getcwd()}")
    starship_sprite = pygame.Surface((STARSHIP_SPRITE_SIZE, STARSHIP_SPRITE_SIZE), pygame.SRCALPHA)
    for x in range(STARSHIP_SPRITE_SIZE):
        for y in range(STARSHIP_SPRITE_SIZE):
            color = CYAN if (x + y) % 2 == 0 else WHITE
            starship_sprite.set_at((x, y), color)
except pygame.error as e:
    print(f"Error: Failed to load '{sprite_path}'. File may be corrupted or not a valid PNG. Error: {e}")
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
        description="A pulsating crystal containing 1 unit of Quantium.",
        unrevealed_description="A mysterious shard emitting faint light.",
        revealed=False
    ),
    "nano_repair_kit": Item(
        name="Nano Repair Kit",
        unrevealed_name="Strange Device",
        description="Restores 20 HP to the droid.",
        unrevealed_description="A compact device with unknown function.",
        revealed=False
    ),
    "quantum_disruptor": Item(
        name="Quantum Disruptor",
        unrevealed_name="Odd Gadget",
        description="Deals 10 extra damage to Einstein-Entities.",
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

# Global EE Dictionary
EE_ENTITIES = {
    "placeholder": EinsteinEntity("PlaceHolder", 20, 5, "spatial_warp"),
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

            if (new_x, new_y) != (0, 2) and random.random() < 0.1:
                new_room.entity = random.choice(list(EE_ENTITIES.values()))

class Player:
    def __init__(self, dungeon):
        self.current_room = dungeon.rooms[0]
        self.hp = 50
        self.quantium = 0
        self.inventory = []
        self.base_attack = 5
        self.dungeon = dungeon

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
            self.current_room = new_room
            print(f"Moved to Room at ({new_room.grid_x}, {new_room.grid_y})")
            if (new_room.grid_x, new_room.grid_y) not in self.dungeon.visited:
                self.dungeon.visited.add((new_room.grid_x, new_room.grid_y))
                popup.show(["Room Entry", new_room.description[0], new_room.description[1]])
            if new_room.entity:
                popup.start_combat(self, new_room)
            return True
        print(f"No room to the {direction}")
        return False

    def exit_dungeon(self):
        """Initiate the process of exiting the quantum pagoda."""
        pass

    def combat(self, entity, popup):
        action = popup.combat_action
        popup.combat_log = []
        if action == "attack":
            damage = self.base_attack
            for item, qty in self.inventory:
                if item.name == "Quantum Disruptor" and qty > 0:
                    damage += 10
                    break
            entity.hp -= damage
            popup.combat_log.append(f"You deal {damage} damage to {entity.name}!")
        elif action == "use_item":
            item_name = popup.selected_item
            if item_name:
                for item, qty in self.inventory:
                    if item.name == item_name and qty > 0:
                        if item_name == "Nano Repair Kit":
                            self.hp = min(50, self.hp + 20)
                            popup.combat_log.append("Used Nano Repair Kit. Restored 20 HP!")
                        elif item_name == "Quantum Disruptor":
                            entity.hp -= 10
                            popup.combat_log.append("Used Quantum Disruptor. Dealt 10 damage!")
                        qty -= 1
                        if qty == 0:
                            self.inventory.remove([item, qty])
                        break
        elif action == "flee":
            if random.random() < 0.5:
                popup.combat_log.append("Escaped from combat!")
                popup.combat_mode = False
                return
            else:
                popup.combat_log.append("Failed to flee!")

        if entity.hp > 0:
            self.hp -= entity.attack
            popup.combat_log.append(f"{entity.name} deals {entity.attack} damage!")
            if random.random() < 0.1:
                if entity.ability == "spatial_warp":
                    valid_rooms = [(r.grid_x, r.grid_y) for r in self.dungeon.rooms if (r.grid_x, r.grid_y) != (0, 2)]
                    new_x, new_y = random.choice(valid_rooms)
                    self.current_room = self.dungeon.grid[new_y][new_x]
                    popup.combat_log.append("PlaceHolder warps you to another room!")
                    popup.combat_mode = False
                elif entity.ability == "quantum_leech":
                    for item, qty in self.inventory:
                        if item.name == "Quantum Crystal" and qty > 0:
                            qty -= 1
                            self.quantium -= 1
                            if qty == 0:
                                self.inventory.remove([item, qty])
                            popup.combat_log.append("Quantum Wraith steals 1 Quantum Crystal!")
                            break

        if self.hp <= 0:
            popup.combat_log = ["Droid-E002 destroyed! Mission failed."]
            popup.combat_mode = False
            popup.game_over = True
        elif entity.hp <= 0:
            popup.combat_log = [f"{entity.name} defeated! Gained 1 Quantum Crystal."]
            self.current_room.entity = None
            for item, qty in self.inventory:
                if item.name == "Quantum Crystal":
                    qty += 1
                    self.quantium += 1
                    break
            else:
                self.inventory.append([ITEMS["quantum_crystal"], 1])
                self.quantium += 1
            popup.combat_mode = False

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
                for i, [inv_item, qty] in enumerate(player.inventory):
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
                    player.quantium += 1
                    print(f"Quantium increased to {player.quantium}")
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
        text = font.render(f"Quantium: {player.quantium}/20", True, WHITE)
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
                elif direction == "exit" and player.current_room.grid_x == 0 and player.current_room.grid_y == 2:
                    player.exit_dungeon()
                elif player.move(direction, popup):
                    return True
        for button, item, qty in self.drop_buttons:
            if button.collidepoint(pos):
                for i, [inv_item, inv_qty] in enumerate(player.inventory):
                    if inv_item.name == item.name:
                        inv_qty -= qty
                        if inv_item.name == "Quantum Crystal":
                            player.quantium -= qty
                        player.current_room.items.append(item)
                        if inv_qty <= 0:
                            player.inventory.pop(i)
                        else:
                            player.inventory[i][1] = inv_qty
                        print(f"Dropped {qty} {item.name}")
                        print(f"Updated inventory: {[(i.name, q) for i, q in player.inventory]}")
                        print(f"Room items: {[i.name for i in player.current_room.items]}")
                        break
                return True
        for button, item, qty in self.drop_all_buttons:
            if button.collidepoint(pos):
                for i, [inv_item, inv_qty] in enumerate(player.inventory):
                    if inv_item.name == item.name:
                        if inv_item.name == "Quantum Crystal":
                            player.quantium -= qty
                        for _ in range(qty):
                            player.current_room.items.append(item)
                        player.inventory.pop(i)
                        print(f"Dropped {qty} {item.name} as individual items")
                        print(f"Updated inventory: {[(i.name, q) for i, q in player.inventory]}")
                        print(f"Room items: {[i.name for i in player.current_room.items]}")
                        break
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
        self.rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.close_button = pygame.Rect(self.rect.right - 60, self.rect.bottom - 40, 50, 30)
        self.combat_mode = False
        self.combat_action = None
        self.combat_log = []
        self.selected_item = None
        self.attack_button = pygame.Rect(self.rect.x + 180, self.rect.bottom - 40, 50, 30)
        self.item_button = pygame.Rect(self.rect.x + 120, self.rect.bottom - 40, 50, 30)
        self.flee_button = pygame.Rect(self.rect.x + 60, self.rect.bottom - 40, 50, 30)
        self.item_select_buttons = []
        self.game_over = False

    def show(self, text):
        self.active = True
        self.text = text if isinstance(text, list) else [text]
        self.combat_mode = False

    def start_combat(self, player, room):
        self.active = True
        self.combat_mode = True
        self.combat_action = None
        self.combat_log = []
        self.selected_item = None
        self.text = [
            "Einstein-Entity Encounter!",
            f"Name: {room.entity.name}, HP: {room.entity.hp}/{room.entity.max_hp}",
            f"Droid-E002 HP: {player.hp}/50",
            "Choose an action:"
        ]

    def draw(self, screen):
        if not self.active:
            return
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        y_offset = 20
        for line in self.text:
            text = font.render(line, True, WHITE)
            screen.blit(text, (self.rect.x + 20, self.rect.y + y_offset))
            y_offset += 30
        for line in self.combat_log:
            text = font.render(line, True, WHITE)
            screen.blit(text, (self.rect.x + 20, self.rect.y + y_offset))
            y_offset += 30

        if self.combat_mode:
            pygame.draw.rect(screen, WHITE, self.attack_button)
            text = font.render("Attack", True, BLACK)
            screen.blit(text, (self.attack_button.x + 5, self.attack_button.y + 5))
            pygame.draw.rect(screen, WHITE, self.item_button)
            text = font.render("Item", True, BLACK)
            screen.blit(text, (self.item_button.x + 5, self.item_button.y + 5))
            pygame.draw.rect(screen, WHITE, self.flee_button)
            text = font.render("Flee", True, BLACK)
            screen.blit(text, (self.flee_button.x + 5, self.flee_button.y + 5))
            if self.combat_action == "use_item":
                self.item_select_buttons = []
                y_offset = 200
                for item, qty in self.player.inventory:
                    if item.name in ["Nano Repair Kit", "Quantum Disruptor"] and qty > 0:
                        button = pygame.Rect(self.rect.x + 20, self.rect.y + y_offset, 200, 30)
                        pygame.draw.rect(screen, WHITE, button)
                        text = font.render(item.name, True, BLACK)
                        screen.blit(text, (button.x + 5, button.y + 5))
                        self.item_select_buttons.append((button, item.name))
                        y_offset += 40
        else:
            pygame.draw.rect(screen, WHITE, self.close_button)
            text = font.render("Close", True, BLACK)
            screen.blit(text, (self.close_button.x + 5, self.close_button.y + 5))

    def handle_click(self, pos, player, room):
        if not self.active:
            return False
        if self.combat_mode:
            if self.combat_action == "use_item":
                for button, item_name in self.item_select_buttons:
                    if button.collidepoint(pos):
                        self.selected_item = item_name
                        self.combat_action = "use_item"
                        player.combat(room.entity, self)
                        return True
            elif self.attack_button.collidepoint(pos):
                self.combat_action = "attack"
                self.player = player
                player.combat(room.entity, self)
                return True
            elif self.item_button.collidepoint(pos):
                self.combat_action = "use_item"
                return True
            elif self.flee_button.collidepoint(pos):
                self.combat_action = "flee"
                self.player = player
                player.combat(room.entity, self)
                return True
        elif self.close_button.collidepoint(pos):
            self.active = False
            if self.game_over:
                return False
            return True
        return False

# Main game
dungeon = Dungeon()
player = Player(dungeon)
left_ui = LeftUI()
right_ui = RightUI()
popup = Popup()
clock = pygame.time.Clock()
running = True

# Show starting room popup
dungeon.visited.add((0, 2))
popup.show(["Room Entry", dungeon.rooms[0].description[0], dungeon.rooms[0].description[1]])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if popup.handle_click(event.pos, player, player.current_room):
                if popup.game_over:
                    running = False
            left_ui.handle_click(event.pos, player, player.current_room)
            right_ui.handle_click(event.pos, player, popup)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and popup.active and not popup.combat_mode:
                popup.active = False

    screen.fill(STARRY_BLUE)
    # Draw left UI first
    left_ui.draw(screen, player.current_room)
    # Draw dungeon
    offset = (573, 57)  # Adjusted for right UI width
    for room in dungeon.rooms:
        offset_rect = room.rect.move(offset)
        color = BLUE if room == player.current_room else SILVER
        pygame.draw.rect(screen, color, offset_rect)
        pygame.draw.rect(screen, CYAN, offset_rect, 4)
        for door_rect in room.get_door_rects():
            offset_door = door_rect.move(offset)
            pygame.draw.rect(screen, WHITE, offset_door)
    # Draw starship
    starship_pos = (573 - STARSHIP_SPRITE_SIZE, 357 + ROOM_SIZE//2 - STARSHIP_SPRITE_SIZE//2)
    screen.blit(starship_sprite, starship_pos)
    # Draw right UI and popup
    right_ui.draw(screen, player)
    popup.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()