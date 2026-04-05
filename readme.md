<div align="center">

# ⚔️ Ancient Dungeon Quest

**A 2D side-scrolling fantasy fighting game built with Python & Pygame**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=for-the-badge&logo=pygame&logoColor=white)
![OOP](https://img.shields.io/badge/Paradigm-OOP-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)

<br/>

> *"Embark on a thrilling journey trapped within the depths of an enigmatic and ancient dungeon.  
> Each level challenges players with progressively complex and unique enemies.  
> Escape or fight — the choice is yours."*

<br/>

![Start Screen](docs/Ancient%20Dungeon%20Quest%20Start.png)

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Gameplay Screenshots](#-gameplay-screenshots)
- [Features](#-features)
- [Game Mechanics](#-game-mechanics)
- [Characters](#-characters)
- [Enemies & Stages](#-enemies--stages)
- [Controls](#-controls)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [OOP Concepts Applied](#-oop-concepts-applied)
- [Credits](#-credits)

---

## 🏰 About

**Ancient Dungeon Quest** is a 2D action fighting game developed in Python using Pygame as a final project for **Object-Oriented Programming (ITPC-102)**. Players choose a warrior class and battle through 5 increasingly difficult stages, each featuring a unique enemy with its own AI, attack patterns, and special mechanics. The game features sprite sheet animation, real-time combat, health/mana systems, projectile mechanics, chest loot drops, and a full victory/game-over flow.

---

## 📸 Gameplay Screenshots

<table>
  <tr>
    <td align="center"><strong>Character Select — Samurai</strong></td>
    <td align="center"><strong>Character Select — Warrior</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Select Character (Samurai).png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Select Character (Warrior).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Stage 1 — Goblin the Thief</strong></td>
    <td align="center"><strong>Stage 1 — Enemy Defeated</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Stage 1.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Stage 1 (Defeated).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Stage 2 — One-Eyed Banshee Bat</strong></td>
    <td align="center"><strong>Stage 2 — Enemy Defeated</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Stage 2.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Stage 2 (Defeated).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Stage 3 — Undead Warrior</strong></td>
    <td align="center"><strong>Stage 3 — Enemy Defeated</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Stage 3.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Stage 3 (Defeated).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Stage 4 — Scorching Abyss Worm</strong></td>
    <td align="center"><strong>Stage 4 — Enemy Defeated</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Stage 4.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Stage 4 (Defeated).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Stage 5 — Final Boss</strong></td>
    <td align="center"><strong>Victory Screen</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Stage 5.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Stage 5 (Defeated).png" width="420"/></td>
  </tr>
  <tr>
    <td align="center"><strong>Pause Screen</strong></td>
    <td align="center"><strong>Game Over / Died</strong></td>
  </tr>
  <tr>
    <td><img src="docs/Ancient Dungeon Quest Pause.png" width="420"/></td>
    <td><img src="docs/Ancient Dungeon Quest Defeated(Died).png" width="420"/></td>
  </tr>
</table>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎮 Character Selection | Choose between **Samurai** (fast, long-range slash) or **Warrior** (strong, aerial attacks) |
| 🗺️ 5 Unique Stages | Each stage has a distinct background, enemy, and difficulty scaling |
| 🧠 Enemy AI | Each enemy moves, chases, attacks, and knockbacks independently |
| 💥 Projectile System | Fire Worm launches fireballs — reflect them back to deal damage |
| 🏆 Chest & Loot System | Defeat enemies to reveal chests containing health potions |
| ❤️ Health & Mana Bars | Real-time UI bars with regen mechanics |
| ⏸️ Pause Screen | Mid-game pause with player stat display |
| 🔄 Retry System | Countdown-based retry with full state reset per stage |
| 🎖️ Victory Screen | Full end-screen with Retry and Exit buttons after defeating the final boss |
| 🎵 Audio | BGM + enemy-specific sound effects for immersion |

---

## ⚙️ Game Mechanics

### Combat
- **Attack** with `P` — chains between Attack 1 and Attack 2 for the Samurai
- **Jump Attack** — Warrior can attack mid-air for different hitbox coverage
- **Dash** — Hold `SHIFT` while moving to spend mana and boost speed
- **Mana Cost** — Attacking and dashing consume mana; mana regenerates over time

### Fireball Reflection (Stage 4 — Fire Worm)
The Scorching Abyss Worm is **immune to melee attacks**. It launches fireballs at the player which must be **reflected back** by attacking them at the right moment. A reflected fireball deals significant damage to the worm.

### Skeleton Regen (Stage 3 — Undead Warrior)
The Undead Warrior passively **regenerates health over time**. It also regains a burst of HP when it successfully counterattacks. Pressure is key.

### Retry & Full Reset
- Dying on any stage prompts `Press R to retry` — a 3-second countdown plays, then the stage resets cleanly.
- The **Retry** button on the victory screen performs a full game reset back to Stage 1 with fresh enemies, chests, and player stats.

---

## 🧙 Characters

### 🗡️ Samurai — Haruki (Ronin)
- **Speed:** Fast (`15 px/frame`)
- **Attack Style:** Chained dual-attack combo (Attack 1 → Attack 2)
- **Attack Range:** Wide horizontal slash
- **Mana Cost per Attack:** 15

### 🛡️ Warrior
- **Speed:** Steady (`9 px/frame`)
- **Attack Style:** Ground attack + aerial jump attack with wide AOE
- **Jump Attack Hitbox:** Covers a broad downward arc
- **Mana Cost per Attack:** 15

---

## 👾 Enemies & Stages

| Stage | Enemy | Special Trait |
|---|---|---|
| **Stage 1** | 🐉 Goblin the Thief (Lv. 2) | Basic melee AI, chases player |
| **Stage 2** | 👁️ One-Eyed Banshee Bat (Lv. 4) | Flying — no gravity, dash attacks |
| **Stage 3** | 💀 Undead Warrior (Lv. 7) | Health regeneration, counter-regen on block |
| **Stage 4** | 🐛 Scorching Abyss Worm (Lv. 10) | **Melee immune** — defeat via fireball reflection |
| **Stage 5** | 🧙 Corrupted Sorcerer (Lv. 15) | Humanoid boss AI, magic attacks |

---

## 🎮 Controls

| Key | Action |
|---|---|
| `A` / `D` | Move Left / Right |
| `W` | Jump |
| `P` | Attack (chains combo) |
| `SHIFT` + Move | Dash (costs mana) |
| `E` | Interact (open chest, advance level) |
| `R` | Retry stage (when Game Over) |
| `ESC` | Pause / Unpause |
| `SPACE` | Start game from main menu |

---

## 📁 Project Structure

```
GAME_OOP_FINALS/
│
├── newMain.py              # Main game loop, stage management, UI
├── newCharacters.py        # All character & enemy classes (OOP)
├── Items.py                # Chest, Item, and heal effect logic
│
├── assets/
│   ├── images/
│   │   ├── background/     # Stage backgrounds (1st–final stage)
│   │   ├── warrior/        # Warrior sprite sheets
│   │   ├── samurai/        # Samurai sprite sheets
│   │   ├── Monsters_Creatures_Fantasy/  # All enemy sprites
│   │   ├── fireball/       # Fireball projectile sprites
│   │   ├── wizard/         # Final boss sprites
│   │   ├── items/          # Health potion image
│   │   ├── objects/        # Chest sprite sheet
│   │   └── UI/             # HUD elements, stat cards, scroll
│   ├── audio/              # BGM and sound effects
│   └── fonts/              # Custom pixel fonts
│
├── docs/                   # Gameplay screenshots (used in this README)
├── build/ dist/            # PyInstaller build output
├── ADQ-Presentation.pptx   # OOP project presentation
├── newMain.spec            # PyInstaller spec file
└── readme.md               # This file
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Install Dependencies

```bash
pip install pygame
```

> No other external libraries are required.

---

## ▶️ How to Run

```bash
# Clone or download the project
cd GAME_OOP_FINALS

# Run the game
python newMain.py
```

To build a standalone executable (Windows):

```bash
pip install pyinstaller
pyinstaller newMain.spec
```

The compiled `.exe` will appear in the `dist/` folder.

---

## 🧩 OOP Concepts Applied

This project was built as a demonstration of core Object-Oriented Programming principles:

### 🔷 Encapsulation
Each game entity (player, enemy, chest, item) encapsulates its own state (health, position, animation, alive status) and behavior (move, attack, update, draw) within its class. External code interacts only through clean method calls.

### 🔷 Inheritance
```
Character (base)
├── Monster (ground AI)
│   ├── Monster_Skeleton (regen variant)
│   ├── Flyenemy (flying variant)
│   ├── Wormenemy (projectile-based boss)
│   └── fireball (projectile entity)
└── Monster_humanoid (final boss AI)
```
All enemy types extend `Character`, inheriting sprite loading, animation, and draw logic — while overriding `move()`, `update()`, and `attack()` for unique behavior.

### 🔷 Polymorphism
The `Stage` class calls `enemy.move()` and `enemy.update()` uniformly regardless of the actual enemy type at runtime. Each enemy class handles its own movement pattern and attack logic transparently.

### 🔷 Abstraction
`Character.load_images()` abstracts sprite sheet slicing. `Stage.levelstart()` abstracts the entire game loop for a given level. UI drawing functions abstract all HUD rendering behind clean function calls.

---

## 👤 Credits

| Role | Name |
|---|---|
| Developer | **Bryan Mamuyac** |
| Course | ITPC-102 — Object-Oriented Programming |
| School | DMMMSU MLUC, San Fernando |
| Engine | [Pygame](https://www.pygame.org/) |
| Sprite Assets | Monsters Creatures Fantasy Pack |
| Fonts | Ancient, Turok, Chase (custom pixel fonts) |

---

<div align="center">

**Ancient Dungeon Quest** — *Will you escape, or will the dungeon claim you?*

⭐ If you enjoyed this project, consider leaving a star!

</div>