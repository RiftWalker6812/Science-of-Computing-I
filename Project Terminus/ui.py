import pygame
import math
from constants import LEFT_UI_WIDTH, RIGHT_UI_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, STARSHIP_SPRITE_SIZE

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
                for i, [inv_item, qty] in enumerate(player.inventory[:]):
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
            # Interact button
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
                    if player.exit_dungeon(popup):
                        return True
                    return True
                elif player.move(direction, popup):
                    return True
        for button, item, qty in self.drop_buttons:
            if button.collidepoint(pos):
                for i, [inv_item, inv_qty] in enumerate(player.inventory[:]):
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
                for i, [inv_item, inv_qty] in enumerate(player.inventory[:]):
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
        self.rect = pygame.Rect(368, 182, 800, 500)
        self.close_button = pygame.Rect(self.rect.right - 60, self.rect.bottom - 40, 50, 30)
        self.combat_mode = False
        self.combat_action = None
        self.combat_log_lines = deque(maxlen=5)
        self.log_offset = 0
        self.game_over = False
        self.player = None
        self.entity = None
        self.room = None
        self.quantum_strike_button = None
        self.nano_repair_button = None
        self.quantum_disruptor_button = None
        self.phase_shift_button = None
        self.entity_sprite = pygame.Surface((128, 128), pygame.SRCALPHA)
        for x in range(128):
            for y in range(128):
                color = CYAN if (x + y) % 2 == 0 else WHITE
                self.entity_sprite.set_at((x, y), color)
        self.sprite_scale = 1.0
        self.sprite_timer = 0
        self.hp_animation = {
            "player": {"current": 50, "target": 50, "time": 0},
            "entity": {"current": 0, "target": 0, "time": 0}
        }
        self.tooltip = None
        self.border_timer = 0

    def show(self, text):
        self.active = True
        self.text = text if isinstance(text, list) else [text]
        self.combat_mode = False
        self.combat_log_lines.clear()
        self.log_offset = 0

    def start_combat(self, player, room):
        self.active = True
        self.combat_mode = True
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

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (10, 20, 50, 200), self.rect)
        self.border_timer += 0.1
        border_color = (0, 255, 255, int(255 * (0.8 + 0.2 * math.sin(self.border_timer))))
        pygame.draw.rect(screen, border_color, self.rect, 3)

        if self.combat_mode:
            # Room name
            text = font_large.render(self.text[0], True, WHITE)
            screen.blit(text, (self.rect.x + 400 - text.get_width() // 2, self.rect.y + 20))

            # Health bars (above sprite)
            text = font.render(f"{self.entity.name}: {self.entity.hp}/{self.entity.max_hp}", True, CYAN)
            screen.blit(text, (self.rect.x + 300 - text.get_width() // 2, self.rect.y + 100))
            hp_ratio = self.hp_animation["entity"]["current"] / self.entity.max_hp
            if self.hp_animation["entity"]["time"] > 0:
                t = self.hp_animation["entity"]["time"] / 0.5
                hp_ratio = self.hp_animation["entity"]["current"] + t * (self.hp_animation["entity"]["target"] - self.hp_animation["entity"]["current"])
                self.hp_animation["entity"]["time"] -= delta_time
                if self.hp_animation["entity"]["time"] < 0:
                    self.hp_animation["entity"]["time"] = 0
            pygame.draw.rect(screen, RED, (self.rect.x + 300 - 100, self.rect.y + 130, 200, 20))
            pygame.draw.rect(screen, GREEN, (self.rect.x + 300 - 100, self.rect.y + 130, 200 * hp_ratio, 20))

            text = font.render(f"Droid-E002: {self.player.hp}/50", True, CYAN)
            screen.blit(text, (self.rect.x + 500 - text.get_width() // 2, self.rect.y + 100))
            hp_ratio = self.hp_animation["player"]["current"] / 50
            if self.hp_animation["player"]["time"] > 0:
                t = self.hp_animation["player"]["time"] / 0.5
                hp_ratio = self.hp_animation["player"]["current"] + t * (self.hp_animation["player"]["target"] - self.hp_animation["player"]["current"])
                self.hp_animation["player"]["time"] -= delta_time
                if self.hp_animation["player"]["time"] < 0:
                    self.hp_animation["player"]["time"] = 0
            pygame.draw.rect(screen, RED, (self.rect.x + 500 - 100, self.rect.y + 130, 200, 20))
            pygame.draw.rect(screen, GREEN, (self.rect.x + 500 - 100, self.rect.y + 130, 200 * hp_ratio, 20))

            # Entity sprite (centered)
            self.sprite_timer += 0.1
            scale = 1.0 + 0.02 * math.sin(self.sprite_timer)
            scaled_sprite = pygame.transform.scale(self.entity_sprite, (int(128 * scale), int(128 * scale)))
            screen.blit(scaled_sprite, (self.rect.x + 400 - 64, self.rect.y + 200))

            # Combat log (left side)
            pygame.draw.rect(screen, (0, 0, 0, 100), (self.rect.x + 20, self.rect.y + 250, 300, 200))
            pygame.draw.rect(screen, CYAN, (self.rect.x + 20, self.rect.y + 250, 300, 200), 1)
            visible_lines = list(self.combat_log_lines)[-5 - self.log_offset:-self.log_offset if self.log_offset > 0 else None]
            for i, line in enumerate(visible_lines):
                color = RED if "deals" in line.lower() or "destroyed" in line.lower() else \
                        GREEN if "restored" in line.lower() else \
                        YELLOW if "overheated" in line.lower() or "cools down" in line.lower() or "dodged" in line.lower() else CYAN
                text = font_small.render(line, True, color)
                screen.blit(text, (self.rect.x + 25, self.rect.y + 255 + i * 40))

            # Action buttons (horizontal row at bottom)
            button_width = 120
            spacing = 20
            total_width = 4 * button_width + 3 * spacing
            start_x = self.rect.x + 400 - total_width // 2
            self.phase_shift_button = pygame.Rect(start_x, self.rect.y + 470, button_width, 40)
            self.nano_repair_button = pygame.Rect(start_x + button_width + spacing, self.rect.y + 470, button_width, 40)
            self.quantum_disruptor_button = pygame.Rect(start_x + 2 * (button_width + spacing), self.rect.y + 470, button_width, 40)
            self.quantum_strike_button = pygame.Rect(start_x + 3 * (button_width + spacing), self.rect.y + 470, button_width, 40)

            for button, text_str in [(self.phase_shift_button, "Phase Shift"),
                                    (self.nano_repair_button, "Nano Repair"),
                                    (self.quantum_disruptor_button, "Quantum Disruptor"),
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
                text = font.render(text_str, True, BLACK)
                screen.blit(text, (button.x + 10, button.y + 10))
                if not enabled:
                    pygame.draw.line(screen, RED, button.topleft, button.bottomright, 3)
                    pygame.draw.line(screen, RED, button.topright, button.bottomleft, 3)
                if button == self.nano_repair_button and enabled:
                    text = font_small.render(f"x{nano_qty}", True, CYAN)
                    screen.blit(text, (button.x + 90, button.y + 2))
                elif button == self.quantum_disruptor_button and enabled:
                    disruptor_qty = sum(qty for item, qty in self.player.inventory if item.name == "Quantum Disruptor")
                    text = font_small.render(f"x{disruptor_qty}", True, CYAN)
                    screen.blit(text, (button.x + 90, button.y + 2))

        else:
            for i, line in enumerate(self.text):
                text = font.render(line, True, WHITE)
                screen.blit(text, (self.rect.x + 20, self.rect.y + 20 + i * 30))
            pygame.draw.rect(screen, WHITE, self.close_button)
            text = font.render("Close", True, BLACK)
            screen.blit(text, (self.close_button.x + 5, self.close_button.y + 5))

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
            if self.phase_shift_button and self.phase_shift_button.collidepoint(pos):
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
            elif self.quantum_strike_button and self.quantum_strike_button.collidepoint(pos):
                self.combat_action = "quantum_strike"
                self.hp_animation["entity"]["current"] = self.entity.hp
                self.hp_animation["entity"]["target"] = max(0, self.entity.hp - random.randint(5, 10))
                self.hp_animation["entity"]["time"] = 0.5
                self.hp_animation["player"]["current"] = self.player.hp
                self.hp_animation["player"]["target"] = max(0, self.player.hp - (self.entity.attack // 2 if self.entity.weakened else self.entity.attack))
                self.hp_animation["player"]["time"] = 0.5
                player.combat(room.entity, self)
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