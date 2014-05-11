#KivyKlötze
=============
by [Carsten](https://github.com/acidicX) ([Web](http://condime.de)) and Sina

Licensed under GPL v3

https://www.gnu.org/licenses/gpl.html

For the audio sources and respective licenses, see snd/sources.md

=============
##A small game for small children

This game was created for the Kivy App Contest 2014.

It aims to educate small children (up to age six) by training their motor skills
and their ability to recognize shapes.

Our goals for the game were:

* keep it simple and easy to use
* adding new level should be easy
* running on every device (mouse and touch inputs) and every screen size

This was our first ever App in Python (and Kivy).

=============
###How to start the game

The code is not packaged, so we still need to start the app with:

> $ python2 main.py -f --size 0x0

The "-f --size 0x0" parameters are necessary because (for some reason)
nothing else works to get a correct (!) fullscreen output, at least on linux. This seems to be a Kivy issue.

An android.txt file is included, so you can start it with the Kivy Launcher.
Just put all the contents into:

> /storage/sdcard0/kivy/KivyKloetze/

Note that audio files did not play on our Android test device (HTC Desire X, Android 4.1 with Kivy Launcher). This could be another Kivy issue since it works fine on linux and Windows.

=============
###How to add new levels

####Structure

The game consists of required and optional files.

**Required files:**
* level files
* level artwork

**Optional files:**
* level gimmicks
* level up sounds

All **level** files are stored in the 'lvl' directory. They are numbered consecutively - level1.kv, level2.kv ...

All **artwork** is stored in the 'img' directory, followed by the level number subdirectory. The background for the first level ist stored in 'img/1/bg.jpg', for example.

All **sounds** (level up sounds) are stored in the 'snd' directory. They need to be ogg/vorbis files and have to be named 'levelnumber.ogg' - so for the first level, the filename should be '1.ogg'.

####Creating a new level

First, there is one restriction that you have to keep in mind while
designing/adding new levels. Due to screen space, visibility and touch restrictions only six unique shapes (dragable elements) can be added. If you want to overcome that restriction, you need to add more ShapeNumber and ShapeNumberTool classes in the main.py.

We strongly recommend to stick with six tough. Otherwise you would have to decrease the size of all shapes, which will result in bad touch usability on small screens.

Ok, let's get started. Apart from the level files written in kivy language, there is no need to modify any actual program code.

**Objects inside a level file**

TODO