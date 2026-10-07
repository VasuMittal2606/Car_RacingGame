# 🏎️ Pygame Car Racing Game

A 2D car racing game built using **Python and Pygame**. The player controls a car around a race track while competing against a computer-controlled car that follows a predefined racing path.

The game includes multiple levels, collision detection, a timer, car movement, and a computer-controlled opponent.

---

## 🎮 Features

- 🏁 6-level racing game
- 🚗 Player-controlled racing car
- 🤖 Computer-controlled opponent
- 🛣️ Track and track-border collision detection
- 🏎️ Car acceleration and deceleration
- ↩️ Left/right rotation
- 🔄 Bounce-back when hitting track boundaries
- 🏁 Finish-line detection
- ⏱️ Level timer
- 📊 Displays current level and player velocity
- 📈 Computer car becomes faster with each level
- 🔁 Level reset and progression system
- 🖼️ Game assets loaded from the project directory
- 🪟 Resizable Pygame window

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| `W` | Move forward |
| `S` | Move backward |
| `A` | Turn left |
| `D` | Turn right |
| Any key | Start the level |

---

## 🧠 How the Game Works

### Player Car

The player controls the red car using the `W`, `A`, `S`, and `D` keys.

The car has:

- Maximum velocity
- Acceleration
- Rotation velocity
- Current velocity
- Rotation angle
- Position

The car's movement is calculated using trigonometry based on its current rotation angle.

### Computer Car

The green car is controlled automatically.

Instead of using keyboard input, it follows a predefined sequence of points on the track.

The computer car:

1. Moves toward the current target point.
2. Calculates the angle required to reach that point.
3. Rotates toward the target.
4. Moves forward.
5. Changes to the next target point after reaching the current one.

The computer car also becomes faster as the player progresses through the levels.

---

## 🏁 Collision Detection

The game uses **Pygame masks** for pixel-level collision detection.

Masks are created for:

- Track border
- Finish line
- Cars

For example:

```python
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_MASK = pygame.mask.from_surface(FINISH)