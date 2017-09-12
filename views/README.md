# Redesign of STARS View

This directory holds code for the prototyping of the new views in STARS.

## Controls

These apply to a view that has focus. Most are bound to the Canvas in the view. Some are bound to the container window for the canvas.

### Key-Bindings

 - `b` brushing
 - `l` linking
 - `r` reset
 - `t` travel
 - `z` zoom

### Mouse Events

#### Zooming on

 - `Mouse Down` start lasso
 - `Mouse Down-Move` grow lasso
 - `Mouse Up` end lasso

#### Brushing on

This involves a sequence of events

 1. `Mouse Down` start to draw brush window
 2. `Mouse Donew-Move` grow brush window
 3. `Mouse up` set size of brush window
 4. `Mouse Down` initiate movement of brush window
 5. `Mouse Down-Move` move brush window
 
This is a little funky. Might think about after step 3, just having mouse movement on that view move the lasso around?
 
## Mouse and Key Combinations

 - `<Shift-1>` brushing


### View generated views

 - `<CTRL-mouse-down>` Generate alternative (new) view of selected observation(s) 
