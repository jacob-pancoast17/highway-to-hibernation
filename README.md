# Seeker

> Authors:
>
> Layla Musallam
>
>Jacob Pancoast
>
> Brenna Henry
>
> Michael Jajkiewicz

---

## Game overview:
Seeker is arcade style game similar to Frogger or Crossyroad. Collect honey, dodge obstacles, and get a high score!

---

## Objective:
Move your bear to safety! Avoid hungry wolves or taking a splash when moving across logs and lilpyads. Hop as far as you can and collect honey for some tasty bonuses! Play different game modes and get your name on the leaderboard!

---

## Controls:
- Use the arrow keys up, down, left, and right to maneuver the bear

- Press escape to view the pause menu

- Press X to give up


---

##  How to run: 
Must install requirements:
` pip install requirements.txt `

To run:
` python3 -m scripts.main `
or
` python -m scripts.main `
depending on your machine!


Enjoy!

---

## Frameworks:
All programming done in Python.

Use of PyArcade and noise from Python library.

 Font sourced from: 
- https://www.1001fonts.com/edit-undo-font.html

 Sound effects sourced from:
- Footstep sfx: https://pixabay.com/sound-effects/film-special-effects-8-bit-snow-footsteps-1-408577/
- Death sfx: https://pixabay.com/sound-effects/film-special-effects-pixel-explosion-319166/
- Honey collection sfx: https://pixabay.com/sound-effects/technology-stop-474070/



---

## Table of Contents:
> * pycache
> 
> * fonts
>
>>> * edit-undo.brk.ttf
>
> * public/scripts
>> * scripts
>>> * engines
>>>> * texture_engine.py
>>>> * time_engine.py
>>>> * world_engine.py
>>>> * world_subengines
>>>>>> * background_subengine.py
>>>>>> * collectible_subengine.py
>>>>>> * drunkards_walk.py
>>>>>> * obstacle_subengine.py
>>>>>> * platform_subengine.py
>>
>>> * objects
>>>> * hostile_object.py
>>>> * den_object.py
>>>> * obstacle_object.py
>>>> * platform_object.py
>>>> * player.py
>>
>>> * screens
>>>> * game_over_screen.py
>>>> * leaderboard_screen.py
>>>> * settings_screen.py
>>>> * stats_screen.py
>>>> * pause_screen.py
>>>> * start_screen.py
>>>> * victory_screen.py
> * constants.py
> * game_view.py
> * firebase_leaderboard.py
> * stats_manager.py
> * main.py
>
> * sfx
>>> * List of sound effects used in game
> * sprites
>>> * List of png/gif used in game
>
> * .gitignore
>
> * README.md
>
> * requirements.txt
>
> * stats.json


## Have fun and seek on!
