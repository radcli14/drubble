# dRuBbLe

![Icon](game/a/icon.png)

![Splash](game/a/splash.png | width=400)

## Summary

Bounce a kick ball off the top of a bar stool, with views of Washington, D.C. in the background

Three game modes
* Single dRuBbLe - Bounce as far and high as possible
* Double dRuBbLe - Alternate bounces with a computer player
* Volley dRuBbLe - Don't let the ball stop on your side

Three difficulty settings
* Easy - Pace is slower, and stool is wider
* Hard - Pace and stool width are realistic
* Silly - Pace is silly fast, stool is silly skinny

## How to play:

There are two virtual sticks which appear as crosshairs on the screen. 
Touch the stick on the lower left to move the stool. 
Touch the stick on the lower right to move the player.
Use the action button in the upper right to start the game.
Tap once to set the launch angle.
Tap again to set the speed and launch the ball.
The options button in the upper left will return to the game selection screen.
Your goal is to bounce the ball off the top of your stool, as far and as high as possible. 

There are three game modes, with a fourth planned:
### Single dRuBbLe
Throw it up, bounce it on the stool, try to keep it bouncing. 
Your score is the product of your distance, max height, and number of bounces.

### Double dRuBbLe
First person throws it, second person tries to bounce it as far as they can on the stool.
The two players alternate shots.

### Volley dRuBbLe
First person bounces it over the center barrier, second person attempts to return it.
The round ends when either player can no longer return the ball, at which time the last player to hit the ball over the barrier earns a point.
Bounces are unlimited, and bounces of the ground are allowed.

### Triple dRuBbLe (Planned)
First person throws it, second person bounces it to the third person, who bounces it to the first person who has run behind them.

## The History of dRuBbLe
A game we used to play while drinking in college.

## Dynamics Model
The player is modeled as a mass that is allowed to translate in the horizontal *x* and vertical *y* directions. 
A spring and damper attach the player to the ground in the *y* coordinate.
The stool is modeled as a point mass that is first offset vertically from the player mass by a distance *d*, then radially from this offset point by an additional distance *l*, where the rotation of the offset relative to the vertical axis is given by the angle $\theta$.
Given the description above, the dynamics are represented by a 4 degree-of-freedom 4-DOF system where the generalized coordinates are **q** = (*x*, *y*, *l*, *$\theta$*), which is visually represented in Figure 1.

![Dynamics Model Diagram](extra_data/figs/diagram.png)

**Figure 1 - Dynamics Model Diagram**



## Task List 
### Before Release
- [x] Move sticks and buttons out of the way so I can add a banner ad on the high score screen
- [x] Fix the computer player control
- [x] Put in limits for the states to prevent crashing
- [x] Add a tutorial
- [x] Add audio for setting ball speed, button presses
- [x] Add a background screen connecting the last screen to the first, geographically
- [x] Add one more base audio file
- [x] Cancel animations before any new animation to ensure that widgets get removed when they are supposed to

### Future
- [x] Add a Volley dRuBbLe sub-game
- [ ] Add a Triple dRuBbLe sub-game
- [x] Include a banner ad
- [ ] Add networked multiplayer mode
- [ ] Create a ball cannon
- [ ] Add statistical plots to the high scores
- [ ] Add additional players, and a selection screen