# dRuBbLe
A Silly Game With Silly Stools!

## The History of dRuBbLe
A game we used to play while drinking in college.

### Single dRuBbLe
Throw it up, bounce it on the stool, try to keep it bouncing.

### Double dRuBbLe
First person throws it, second person tries to bounce it as far as they can on the stool.

### Triple dRuBbLe
First person throws it, second person bounces it to the third person, who bounces it to the first person who has run behind them.

## Dynamics Model
The player is modeled as a mass that is allowed to translate in the horizontal *x* and vertical *y* directions. 
A spring and damper attach the player to the ground in the *y* coordinate.
The stool is modeled as a point mass that is first offset vertically from the player mass, then radially from this offset point by an additional distance *l*, where the rotation of the offset relative to the vertical axis is given by the angle $\theta$.

![Dynamics Model Diagram](https://github.com/radcli14/drubble/extra_data/figs/diagram.png)

## Task List Before Release
- [ ] Move buttons out of the way so I can add a banner ad on the high score screen
- [ ] Add audio for setting ball speed, button presses
- [ ] Add a background screen connecting the last screen to the first, geographically
- [ ] Add one more base audio file

## Future Task List
- [ ] Add a VolleyDrubble sub-game
- [ ] Add a Triple Drubble sub-game
- [ ] Include a banner ad
- [ ] Add networked multiplayer mode
