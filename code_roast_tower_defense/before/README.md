source python-env/bin/activate
python TowerDefense.py
python mapEditor.py

Note to change the map, you must change the "self.map = "
line to the name of the map under the texts/mapTexts folder.

Note to change how the waves are generated, you must change the
"self.waveFile =" line to the name of the wave generator under
the texs/waveTexts folder

Note you can select a tower to sell, upgrade, or change its targetting,
but you must currently have 'None' selected on the side menu of towers

![gameplay](readme/capture.png)



I wrote this beauty originally in highschool, in 2015. This was my first
ever project in python, and my first time getting my hands dirty googling
everything I needed to know. So basically, the code is not quite the best
haha - but it works!

Note that this code was converted from python2 to python3, and somehow in
that transition, when PIL loads some of the images, they have a white background.

