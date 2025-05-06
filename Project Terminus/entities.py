from collections import deque

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
    "placeholder": EinsteinEntity("PlaceHolder", 20, 5, "spatial_warp"),
    "quantum_wraith": EinsteinEntity("Quantum Wraith", 30, 8, "quantum_leech")
}