class Player:
    def __init__(self, dungeon):
        self.current_room = dungeon.rooms[0]
        self.hp = 50
        self.quanta = 0
        self.inventory = []
        self.base_attack = 5
        self.dungeon = dungeon
        self.overheated = False
        self.dodge_active = False

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
            if new_room.entity:
                popup.start_combat(self, new_room)
            return True
        print(f"No room to the {direction}")
        return False

    def exit_dungeon(self, popup):
        """Initiate the process of exiting the quantum pagoda."""
        if self.quanta >= 10:
            popup.show(["Mission Success", "Quantum Pagoda stabilized. Returning to base."])
            return True
        else:
            popup.show(["Mission Incomplete", "Insufficient Quanta to stabilize the Pagoda."])
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
            for i, [item, qty] in enumerate(self.inventory[:]):
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
            for i, [item, qty] in enumerate(self.inventory[:]):
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
            if random.random() < 0.1:
                if entity.ability == "spatial_warp":
                    valid_rooms = [(r.grid_x, r.grid_y) for r in self.dungeon.rooms if (r.grid_x, r.grid_y) != (0, 2)]
                    new_x, new_y = random.choice(valid_rooms)
                    self.current_room = self.dungeon.grid[new_y][new_x]
                    popup.combat_log_lines.append("PlaceHolder warps you to another room!")
                    popup.combat_mode = False
                elif entity.ability == "quantum_leech":
                    for i, [item, qty] in enumerate(self.inventory[:]):
                        if item.name == "Quantum Crystal" and qty > 0:
                            qty -= 1
                            self.quanta -= 1
                            if qty == 0:
                                to_remove.append(i)
                            else:
                                self.inventory[i][1] = qty
                            popup.combat_log_lines.append("Quantum Wraith steals 1 Quantum Crystal!")
                            break

        # Remove items after iteration
        for i in sorted(to_remove, reverse=True):
            self.inventory.pop(i)

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
            popup.combat_mode = False