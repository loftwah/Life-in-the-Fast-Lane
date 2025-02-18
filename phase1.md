### **Supplementary Document: Completing "Life in the Fast Lane"**

---

## **Table of Contents**

1. [Dependencies and Setup](#dependencies-and-setup)
2. [Missing Core Mechanics](#missing-core-mechanics)
   - [Energy and Action System](#energy-and-action-system)
   - [Random Events](#random-events)
   - [Progression and Feedback](#progression-and-feedback)
3. [User Interface Enhancements](#user-interface-enhancements)
   - [In-Game HUD](#in-game-hud)
   - [Menu Additions](#menu-additions)
4. [Game State Management](#game-state-management)
   - [Saving and Loading](#saving-and-loading)
   - [Turn Tracking](#turn-tracking)
5. [Assets and Visuals](#assets-and-visuals)
   - [Placeholder Graphics](#placeholder-graphics)
   - [Sound Effects](#sound-effects)
6. [Polish and Usability](#polish-and-usability)
   - [Error Handling](#error-handling)
   - [Tutorial or Onboarding](#tutorial-or-onboarding)
   - [Debugging Tools](#debugging-tools)
7. [Sample Implementation](#sample-implementation)
8. [Next Steps](#next-steps)

---

## **Dependencies and Setup**

### **Required Libraries**
- **pygame**: Core library for game development.
  - Install: `pip install pygame`
- **pygame-menu**: For menu systems.
  - Install: `pip install pygame-menu`
- **Optional**: 
  - `pyinstaller` (to package the game into an executable): `pip install pyinstaller`
  - `pytest` (for unit tests): `pip install pytest`

### **Initial Setup**
- **Python Version**: Use Python 3.8+ for compatibility.
- **Project Initialization**:
  - Create the directory structure from the previous response.
  - Add a `requirements.txt` file:
    ```
    pygame==2.5.2
    pygame-menu==4.4.3
    ```
  - Install dependencies: `pip install -r requirements.txt`
- **Run Check**: Test `main.py` to ensure `pygame` initializes a window.

---

## **Missing Core Mechanics**

### **Energy and Action System**
- **Implementation Details**:
  - Each turn, players spend Energy points on actions (e.g., work costs 2 Energy, leisure costs 1).
  - Energy resets at the start of each turn based on Health and rest actions from the previous turn.
- **Code Addition** in `src/player.py`:
  ```python
  class Player:
      def __init__(self, name, stats):
          # ... (existing init code)
          self.max_energy = self.energy  # Store max energy for reset

      def reset_turn(self):
          # Reset energy based on health and rest
          recovery = min(self.health // 20, 5)  # Health impacts recovery
          self.energy = min(self.max_energy, recovery)
          if self.energy < 0:
              self.energy = 0

      def can_perform_action(self, cost):
          return self.energy >= cost

      def perform_action(self, action, cost):
          if self.can_perform_action(cost):
              self.energy -= cost
              # Add action-specific effects here
              return True
          return False
  ```
- **Integration**: Call `reset_turn()` in `game.py`’s `update()` each turn.

### **Random Events**
- **Purpose**: Add unpredictability (e.g., "Car breaks down," "Promotion offer").
- **Data**: Define in `data/events.json`:
  ```json
  {
    "events": [
      {"id": 1, "name": "Pay Raise", "chance": 0.1, "effect": {"money": 50, "happiness": 10}},
      {"id": 2, "name": "Sick Day", "chance": 0.05, "effect": {"health": -20, "energy": -2}}
    ]
  }
- **Code** in `src/game.py`:
  ```python
  import random
  from src.utils import load_json

  class Game:
      def __init__(self, screen):
          # ... (existing init code)
          self.events = load_json("data/events.json")["events"]

      def trigger_event(self):
          for event in self.events:
              if random.random() < event["chance"]:
                  self.apply_event(event)
                  return event["name"]
          return None

      def apply_event(self, event):
          for key, value in event["effect"].items():
              if hasattr(self.player, key):
                  setattr(self.player, key, getattr(self.player, key) + value)
  ```
- **Usage**: Call `trigger_event()` in `update()` and display the event name to the player.

### **Progression and Feedback**
- **Stat Progression**: Ensure stats (e.g., Education, Happiness) increase/decrease logically:
  - Work increases Money but may decrease Happiness.
  - Studying increases Education but costs Money and Energy.
- **Feedback**: Display stat changes each turn (e.g., "+$50, -10 Happiness").
- **Code Addition** in `src/player.py`:
  ```python
  def apply_action_effects(self, action_type):
      effects = {
          "work": {"money": 50, "happiness": -5, "energy": -2},
          "study": {"education": 5, "money": -20, "energy": -1},
          "rest": {"happiness": 10, "energy": 2}
      }
      action_effects = effects.get(action_type, {})
      for key, value in action_effects.items():
          setattr(self, key, getattr(self, key) + value)
      return action_effects
  ```

---

## **User Interface Enhancements**

### **In-Game HUD**
- **Purpose**: Show player stats, turn number, and current location.
- **Code** in `src/ui/hud.py`:
  ```python
  import pygame
  from game_config import FONT_PATH, FONT_SIZE, WHITE

  class HUD:
      def __init__(self, screen):
          self.screen = screen
          self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

      def render(self, player, turn):
          stats = [
              f"Turn: {turn}",
              f"Name: {player.name}",
              f"Money: ${player.money}",
              f"Happiness: {player.happiness}",
              f"Education: {player.education}",
              f"Health: {player.health}",
              f"Energy: {player.energy}"
          ]
          for i, text in enumerate(stats):
              rendered = self.font.render(text, True, WHITE)
              self.screen.blit(rendered, (10, 10 + i * 30))
  ```
- **Integration**: Add `self.hud = HUD(screen)` in `Game.__init__` and call `self.hud.render(self.player, self.turn)` in `render()`.

### **Menu Additions**
- **In-Game Menu**: Add pause menu with options (Resume, Save, Quit).
- **Code Addition** in `src/ui/menu.py`:
  ```python
  class InGameMenu:
      def __init__(self, game):
          self.game = game
          self.menu = pygame_menu.Menu(
              "Paused",
              SCREEN_WIDTH,
              SCREEN_HEIGHT,
              theme=pygame_menu.themes.THEME_DARK
          )
          self.menu.add.button("Resume", self.resume)
          self.menu.add.button("Save", self.save_game)
          self.menu.add.button("Quit", pygame_menu.events.EXIT)

      def show(self):
          self.menu.mainloop(self.game.screen)

      def resume(self):
          self.menu.disable()

      def save_game(self):
          self.game.save_game()  # Defined later
          self.menu.disable()
  ```
- **Trigger**: Check for ESC key in `game.py`’s `run()` loop to show the menu.

---

## **Game State Management**

### **Saving and Loading**
- **Purpose**: Allow players to save progress.
- **Code** in `src/game.py`:
  ```python
  import json

  class Game:
      def save_game(self):
          state = {
              "player": {
                  "name": self.player.name,
                  "money": self.player.money,
                  "happiness": self.player.happiness,
                  "education": self.player.education,
                  "health": self.player.health,
                  "energy": self.player.energy
              },
              "turn": self.turn
          }
          with open("data/save.json", "w") as f:
              json.dump(state, f)

      def load_game(self):
          try:
              with open("data/save.json", "r") as f:
                  state = json.load(f)
                  self.player = Player(state["player"]["name"], state["player"])
                  self.turn = state["turn"]
          except FileNotFoundError:
              return False
          return True
  ```
- **Menu Update**: Add "Load Game" button in `MainMenu` to call `load_game()`.

### **Turn Tracking**
- **Display**: Already included in HUD.
- **Logic**: Increment `self.turn` in `update()` and reset player energy.

---

## **Assets and Visuals**

### **Placeholder Graphics**
- **Simple Sprites**: Use basic shapes or text for locations until custom art is ready.
  - Example in `src/locations.py`:
    ```python
    class Location:
        def render(self, screen, x, y):
            pygame.draw.rect(screen, (100, 100, 100), (x, y, 100, 50))
            font = pygame.font.Font(None, 24)
            text = font.render(self.name, True, WHITE)
            screen.blit(text, (x + 10, y + 10))
    ```
- **Directory**: Store in `assets/images/` once created (e.g., `housing_cramped_quarters.png`).

### **Sound Effects**
- **Basic Sounds**:
  - Turn end: Short beep (`assets/sounds/turn_end.wav`).
  - Action: Click sound (`assets/sounds/action.wav`).
- **Code** in `src/utils.py`:
  ```python
  def play_sound(path):
      sound = pygame.mixer.Sound(path)
      sound.play()
  ```
- **Usage**: Call `play_sound("assets/sounds/action.wav")` in action methods.

---

## **Polish and Usability**

### **Error Handling**
- **Checks**: Ensure players can’t perform actions with insufficient Energy or Money.
- **Messages**: Display errors via HUD or pop-up (e.g., "Not enough Energy!").
- **Example** in `src/player.py`:
  ```python
  def perform_action(self, action, cost):
      if not self.can_perform_action(cost):
          return "Not enough Energy!"
      self.energy -= cost
      effects = self.apply_action_effects(action)
      return effects
  ```

### **Tutorial or Onboarding**
- **Simple Intro**: Show a text screen after character creation explaining basics:
  - "Each turn is a week. Spend Energy on actions like Work or Rest."
- **Code** in `src/ui/menu.py`:
  ```python
  def show_tutorial(self):
      tutorial = pygame_menu.Menu("Welcome!", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
      tutorial.add.label("Each turn is a week. Use Energy to Work, Study, or Rest.")
      tutorial.add.button("Start", tutorial.disable)
      tutorial.mainloop(self.game.screen)
  ```
- **Trigger**: Call after `start_game()`.

### **Debugging Tools**
- **Console Output**: Print player stats each turn:
  ```python
  def update(self):
      print(f"Turn {self.turn}: {vars(self.player)}")
      # ... (existing update code)
  ```
- **Cheat Mode**: Add a key (e.g., F1) to boost stats for testing.

---

## **Sample Implementation**

### **Updated `src/game.py`**
```python
import pygame
from src.player import Player
from src.ui.menu import MainMenu, InGameMenu
from src.ui.hud import HUD
from src.utils import play_sound

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.player = None
        self.turn = 0
        self.menu = MainMenu(self)
        self.ingame_menu = InGameMenu(self)
        self.hud = HUD(screen)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.player:
                    self.ingame_menu.show()

            if self.player is None:
                self.menu.show()
            else:
                self.update()
                self.render()
            pygame.display.flip()
            clock.tick(60)

    def update(self):
        self.turn += 1
        self.player.reset_turn()
        event = self.trigger_event()
        if event:
            print(f"Event: {event}")  # Replace with UI feedback later

    def render(self):
        self.screen.fill((200, 200, 200))
        self.hud.render(self.player, self.turn)
        # Render locations here once implemented
```

---

## **Next Steps**

1. **Expand Locations**: Implement clickable location objects using `src/locations.py`.
2. **Action Menu**: Add an in-game menu for selecting actions (Work, Study, etc.).
3. **Visuals**: Replace placeholders with real sprites and backgrounds.
4. **Balancing**: Test and tweak stat changes for fairness.
5. **Multiplayer**: Consider networked play for competitive modes (future scope).
