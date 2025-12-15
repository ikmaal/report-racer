# Report Race

A top-down endless driving game where you drive a car down an endless straight road, avoiding obstacles and reporting incidents!

## Features

- **Professional menu screen** - clean, animated menu with instructions
- **Top-down view** of your car driving down a straight road
- **Endless scrolling road** with realistic textures and lane markings
- **Obstacle cars** to avoid with detailed graphics
- **Incident reporting system** - report road accidents, closures, hazards, and weather conditions
- **Interactive gameplay** - identify and report incidents correctly for bonus points
- **10-second timer** - report incidents quickly before time runs out
- **Increasing difficulty** - speed increases and obstacles spawn more frequently as you score higher
- **Score tracking** - earn points for avoiding obstacles and correct incident reports
- **Leaderboard system** - Top 3 high scores with player names
- **Beautiful graphics** - detailed cars, realistic road textures, and visual effects
- **Complete game flow** - menu, gameplay, name input, and game over screens
- **Progressive speed** - Game gets faster as you drive further

## Controls

### Menu
- **Mouse Click** - Navigate menu buttons (Start Game, Quit)

### Gameplay
- **Arrow Keys** or **A/D keys** - Move car left and right
- **Number Keys (1-4)** or **Mouse Click** - Select incident type when reporting

### Game Over
- **SPACE** - Restart the game

## Installation

1. Install Python 3.x if you haven't already
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the game with:

```bash
py car_game.py
```

## Gameplay

### Getting Started
- Click "START GAME" on the menu screen to begin
- The menu provides quick instructions and controls overview

### Normal Driving
- Stay on the road and avoid hitting other cars
- Your score increases as you successfully pass obstacle cars (+10 points)
- The game speeds up as your score increases

### Incident Reporting
- Random incidents will appear on the road (every 5-10 seconds)
- When an incident reaches the middle of the screen, the game pauses
- You'll see 4 different incident type icons to choose from:
  - **Road Accident** - Crashed cars on the road
  - **Road Closure** - Barriers and cones blocking lanes
  - **Road Hazard** - Oil spills or debris on the road
  - **Bad Weather** - Rain and fog conditions
- Click the correct icon that matches the incident
- **Correct report:** +50 points ✓
- **Wrong report:** -25 points ✗
- Your correct/wrong report count is tracked in the top-right corner

## Scoring System

- **Passing obstacle cars:** +10 points each
- **Correct incident report:** +50 points
- **Wrong incident report:** -25 points
- Try to get the highest score possible!

## Tips

- Stay in the center of a lane for better reaction time
- Watch for cars spawning ahead
- Pay close attention to incidents to report them correctly
- The game gets progressively harder - good luck!
- Quick reflexes and good observation skills are key to success!

Enjoy the ride! 🚗💨

