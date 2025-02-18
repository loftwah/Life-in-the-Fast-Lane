### **Phase 2: Enhancing "Life in the Fast Lane"**

---

## **Table of Contents**

1. [ Gameplay Expansion](#gameplay-expansion)
   - [Advanced Action System](#advanced-action-system)
   - [Location Interactions](#location-interactions)
   - [Relationships and Social Mechanics](#relationships-and-social-mechanics)
   - [Game Modes Implementation](#game-modes-implementation)
2. [Visual and Audio Improvements](#visual-and-audio-improvements)
   - [Custom Artwork](#custom-artwork)
   - [Background Music and Sound Effects](#background-music-and-sound-effects)
   - [Animations](#animations)
3. [User Interface Refinement](#user-interface-refinement)
   - [Interactive HUD](#interactive-hud)
   - [Enhanced Menus](#enhanced-menus)
   - [Tooltips and Feedback](#tooltips-and-feedback)
4. [Progression and Balancing](#progression-and-balancing)
   - [Stat Scaling and Caps](#stat-scaling-and-caps)
   - [Economy Balancing](#economy-balancing)
   - [Difficulty Settings](#difficulty-settings)
5. [Technical Enhancements](#technical-enhancements)
   - [Performance Optimization](#performance-optimization)
   - [Cross-Platform Compatibility](#cross-platform-compatibility)
   - [Bug Fixes and Testing](#bug-fixes-and-testing)
6. [Player Engagement Features](#player-engagement-features)
   - [Achievements](#achievements)
   - [Leaderboards](#leaderboards)
   - [Dynamic Events](#dynamic-events)
7. [Sample Implementation Updates](#sample-implementation-updates)
8. [Next Steps](#next-steps)

---

## **Gameplay Expansion**

### **Advanced Action System**
- **Goal**: Add variety and consequences to player actions.
- **Details**:
  - **Multiple Outcomes**: Actions like "Work Overtime" can succeed (extra money) or fail (burnout).
  - **Skill-Based Modifiers**: Higher Education or Health improves action success rates.
- **Code** in `src/player.py`:
  ```python
  def perform_action(self, action, cost):
      if not self.can_perform_action(cost):
          return "Not enough Energy!"
      self.energy -= cost
      if action == "overtime" and random.random() < (self.health / 100):
          effects = {"money": 100, "happiness": -15}
      else:
          effects = {"health": -10, "happiness": -20}  # Burnout
      self.apply_action_effects(action, effects)
      return effects
  ```

### **Location Interactions**
- **Goal**: Make locations interactive and visually distinct.
- **Details**:
  - Players click on locations rendered on-screen to visit them.
  - Each location offers specific actions (e.g., "Work" at Monolith Burgers).
- **Code** in `src/locations.py`:
  ```python
  class Location:
      def __init__(self, name, type, cost, benefits, x, y, image_path):
          self.rect = pygame.Rect(x, y, 100, 50)
          self.image = load_image(image_path)
          self.actions = []  # List of available actions

      def handle_click(self, pos):
          if self.rect.collidepoint(pos):
              return self
          return None

  # Example in game.py
  def render(self):
      # ... (existing render code)
      for location in self.locations:
          self.screen.blit(location.image, location.rect)
  ```
- **Data Update**: Add `x`, `y`, and `image_path` to `locations.json`.

### **Relationships and Social Mechanics**
- **Goal**: Introduce NPCs and social dynamics.
- **Details**:
  - **NPCs**: Roommates, coworkers, friends with relationship levels (0-100).
  - **Social Actions**: "Chat" increases relationship; neglect decreases it.
- **Code** in `src/player.py`:
  ```python
  class Player:
      def __init__(self, name, stats):
          # ... (existing init)
          self.relationships = {}  # e.g., {"Roommate John": 50}

      def socialize(self, npc, effect):
          self.relationships[npc] = min(100, max(0, self.relationships.get(npc, 50) + effect))
          return {"happiness": effect}
  ```

### **Game Modes Implementation**
- **Goal**: Fully implement all game modes from the design doc.
- **Details**:
  - **Classic Mode**: Track progress toward 100% in all stats.
  - **Score Challenge**: Calculate score at turn limit.
  - **Race to Success**: Define specific goals (e.g., $1M).
- **Code** in `src/game.py`:
  ```python
  class Game:
      def __init__(self, screen):
          # ... (existing init)
          self.mode = None
          self.goal = None

      def set_mode(self, mode, goal=None):
          self.mode = mode
          self.goal = goal

      def check_win(self):
          if self.mode == "classic":
              return all(getattr(self.player, stat) >= 100 for stat in ["money", "happiness", "education", "health"])
          elif self.mode == "score":
              return self.turn >= 50  # Example turn limit
          elif self.mode == "race":
              return getattr(self.player, self.goal["stat"]) >= self.goal["value"]
          return False
  ```
- **Menu Update**: Add mode selection in `MainMenu`.

---

## **Visual and Audio Improvements**

### **Custom Artwork**
- **Goal**: Replace placeholders with thematic visuals.
- **Details**:
  - **Characters**: Sprites for player avatars (customizable via stats).
  - **Locations**: Unique images (e.g., `assets/images/housing/serenity_heights.png`).
  - **UI**: Buttons, backgrounds, stat bars.
- **Tools**: Use GIMP, Aseprite, or free assets from OpenGameArt.org.

### **Background Music and Sound Effects**
- **Goal**: Enhance immersion with audio.
- **Details**:
  - **Background Music**: Looping tracks for urban/suburban settings (`assets/sounds/urban_bgm.mp3`).
  - **SFX**: Specific sounds per action (e.g., cash register for work).
- **Code** in `src/game.py`:
  ```python
  def __init__(self, screen):
      # ... (existing init)
      pygame.mixer.music.load("assets/sounds/urban_bgm.mp3")
      pygame.mixer.music.play(-1)  # Loop indefinitely
  ```

### **Animations**
- **Goal**: Add subtle movement for polish.
- **Details**:
  - **Stat Changes**: Fade-in text (e.g., "+$50") when stats update.
  - **Location Hover**: Slight scale-up on mouse hover.
- **Code** in `src/ui/hud.py`:
  ```python
  def render_stat_change(self, effect, x, y):
      for i, (key, value) in enumerate(effect.items()):
          text = self.font.render(f"{key}: {value:+d}", True, WHITE)
          alpha = max(0, 255 - i * 20)  # Fade effect
          text.set_alpha(alpha)
          self.screen.blit(text, (x, y + i * 20))
  ```

---

## **User Interface Refinement**

### **Interactive HUD**
- **Goal**: Make stats clickable for more info or actions.
- **Details**:
  - Clicking "Energy" shows available actions.
  - Clicking "Money" opens a financial overview.
- **Code** in `src/ui/hud.py`:
  ```python
  def handle_click(self, pos):
      for i, stat in enumerate(self.stats):
          rect = pygame.Rect(10, 10 + i * 30, 200, 30)
          if rect.collidepoint(pos):
              return stat.split(":")[0].strip()
      return None
  ```

### **Enhanced Menus**
- **Goal**: Improve navigation and customization.
- **Details**:
  - **Character Creation**: Sliders for stat allocation (Money, Happiness, etc.).
  - **Settings**: Volume control, fullscreen toggle.
- **Code** in `src/ui/menu.py`:
  ```python
  def setup_menu(self):
      self.menu.add.text_input("Name: ", default="Player", onchange=self.set_player_name)
      self.menu.add.slider("Money", 100, 0, 200, step=10, onchange=lambda v: self.stats.update({"money": v}))
      self.menu.add.button("Start", self.start_game)
  ```

### **Tooltips and Feedback**
- **Goal**: Clarify mechanics for players.
- **Details**:
  - Hover over locations to show benefits/costs.
  - Action results displayed as pop-ups.
- **Code** in `src/locations.py`:
  ```python
  def get_tooltip(self):
      return f"{self.name}: Cost: {self.cost}, Benefits: {self.benefits}"
  ```

---

## **Progression and Balancing**

### **Stat Scaling and Caps**
- **Goal**: Prevent runaway stats and ensure meaningful progression.
- **Details**:
  - Cap stats at 100 (or mode-specific values).
  - Diminishing returns for repeated actions (e.g., less Happiness from rest if already high).
- **Code** in `src/player.py`:
  ```python
  def apply_action_effects(self, action, effects):
      for key, value in effects.items():
          current = getattr(self, key)
          new_value = min(100, max(0, current + value * (1 - current / 200)))  # Diminishing returns
          setattr(self, key, int(new_value))
  ```

### **Economy Balancing**
- **Goal**: Make financial choices impactful.
- **Details**:
  - Adjust rent, job pay, and costs based on playtesting.
  - Introduce inflation over turns for realism.
- **Data**: Update `locations.json` and `jobs.json` with balanced values.

### **Difficulty Settings**
- **Goal**: Cater to different skill levels.
- **Details**:
  - **Easy**: Higher starting stats, lower costs.
  - **Hard**: Lower Energy, higher event risks.
- **Code** in `src/game.py`:
  ```python
  def apply_difficulty(self, difficulty):
      multipliers = {"easy": 1.5, "normal": 1.0, "hard": 0.75}
      for stat in ["money", "energy", "health"]:
          setattr(self.player, stat, getattr(self.player, stat) * multipliers[difficulty])
  ```

---

## **Technical Enhancements**

### **Performance Optimization**
- **Goal**: Ensure smooth gameplay on modest hardware.
- **Details**:
  - Use sprite groups for locations (`pygame.sprite.Group`).
  - Limit redraws to dirty areas with `pygame.display.update(rects)`.

### **Cross-Platform Compatibility**
- **Goal**: Run on Windows, macOS, and Linux.
- **Details**:
  - Test file paths with `os.path.join` in `utils.py`.
  - Package with PyInstaller: `pyinstaller --onefile main.py`.

### **Bug Fixes and Testing**
- **Goal**: Stabilize the game.
- **Details**:
  - Write tests in `tests/` (e.g., `test_player.py` for action effects).
  - Log errors to a file for debugging.

---

## **Player Engagement Features**

### **Achievements**
- **Goal**: Reward milestones.
- **Details**:
  - "Millionaire": Earn $1M.
  - "Workaholic": Work 10 turns straight.
- **Code** in `src/game.py`:
  ```python
  def check_achievements(self):
      if self.player.money >= 1000000:
          self.achievements.add("Millionaire")
  ```

### **Leaderboards**
- **Goal**: Add replayability for Score Challenge mode.
- **Details**:
  - Save top scores to `data/leaderboard.json`.
- **Code** in `src/ui/menu.py`:
  ```python
  def show_leaderboard(self):
      leaderboard = load_json("data/leaderboard.json")
      menu = pygame_menu.Menu("Leaderboard", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DARK)
      for entry in leaderboard:
          menu.add.label(f"{entry['name']}: {entry['score']}")
      menu.mainloop(self.game.screen)
  ```

### **Dynamic Events**
- **Goal**: Keep gameplay fresh.
- **Details**:
  - Events scale with player progress (e.g., bigger raises at higher Education).
- **Data Update**: Add `condition` field to `events.json` (e.g., `{"education": ">50"}`).

---

## **Sample Implementation Updates**

### **Updated `src/game.py`**
```python
class Game:
    def __init__(self, screen):
        # ... (existing init)
        self.locations = [
            Housing("Cramped Quarters", 50, {"happiness": -5}, 100, 100, "assets/images/housing/cramped_quarters.png")
        ]
        self.achievements = set()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for loc in self.locations:
                        if loc.handle_click(event.pos):
                            self.player.location = loc
            # ... (existing run code)
            if self.check_win():
                print("You Win!")  # Replace with victory screen
            self.check_achievements()
```

---

## **Next Steps**

1. **Playtesting**: Gather feedback on balance and fun factor.
2. **Multiplayer**: Add local or online play for competitive modes.
3. **Story Elements**: Introduce a light narrative (e.g., "Rise from rags to riches").
4. **Release Prep**: Create a trailer, itch.io page, or Steam listing.
