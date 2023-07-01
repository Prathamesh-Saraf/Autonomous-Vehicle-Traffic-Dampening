# Autonomous-Vehicle-Traffic-Dampening

Gradient based control of hexapod robot 'Daisy' using force feedback
Since the work is not published yet, I cannot share our code base for the controller. However, I have some plots and videos:

## Uneven terrain
<div  align="center">
<img src="./yuna_uneven_fb.gif" height="300" width="400" /> 
<img src="./yuna_uneven_nofb.gif" height="300" width="400" />
</div>
 Without gradient based control(left)                     with gradient based control (right)

## Smooth terrain

<div  align="center">
<img src="./yuna_nofb.gif" height="300" width="400" label="without fb" />
<img src="./yuna_fb.gif" height="300" width="400" />
</div>
 Without gradient based control(left)                     with gradient based control (right)
 
## Plots

<div  align="center">
<img src="./Yuna_openloop1.png" width="400" />
<img src="./Yuna_control.png" width="400" />
</div>
 Without gradient based control(left)                     with gradient based control (right)
 
 The graph should ideally be converge to 'zero' signifying equal workload distribution on each leg.
 
 ## All Videos
https://drive.google.com/drive/folders/16vyU0-7pZt6hR2acLCtNc61eJzKQQNqU?usp=sharing
