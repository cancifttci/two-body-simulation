VERSIONS
------------------------------------------------------
Python 3.9.5
gcc 8.1.0 (Windows, unicode) - 64-bit
keyboard 0.13.5
pygame 2.0.1


PLEASE INSTALL REQUIREMENTS BEFORE THE TEST
>pip/pip3 install -r requirements.txt

------------------------------------------------------
INSTRUCTIONS

1-Run two_body_simulation.py
2-Enter parameters

(Example Input)
Two Body Movement Calculator
Select calculation method(euler|runge-kutta):runge-kutta
Select Mass Ratio:0.5
Select Eccentricity:0.5
Select Step Size:0.01
Select Total Time:10000


3-data.txt generated in directory.

(Example Output)
+Calculation Started...
-Method: runge-kutta
-Mass Ratio: 0.5
-Eccentricity: 0.5
-Total Time: 10000
-Step Size: 0.01
+Calculation Finished. (13 seconds)
+Export Started...
+Export Finished. (4 seconds)
+1000000 state exported -> data.txt

4-Run the two_body_animation.py (Before the start you can set the dataset name (Make sure name is correct!) and simulation speed with simulator object parameters)

SIMULATION CONTROLS
"SPACE": Start/Stop
"R": Rewind the simulation (It works if simulation is stopped!!!)
"Q": Exit from simulation

!!!Sometimes the simulation may start late due to lack of optimization. Please wait :) !!!  


TEAM MEMBERS 
-------------
İbrahim Baran Oral - 250201048
Tunahan Atalay     - 250201047
Can Çiftçi         - 270201080
Gizem Sarsınlar    - 250206061