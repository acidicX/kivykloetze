KivyKlötze
=============
by [Carsten](https://github.com/acidicX) and [Sina]()

Licensed under GPL v3

https://www.gnu.org/licenses/gpl.html

For the audio sources and respective licenses, see snd/sources.md

=============
A small game for small children

This game was created for the Kivy App Contest 2014.

It aims to educate small children (up to age six) by training their motor skills
and their ability to recognize shapes.

Our goals for the game were:

* keep it simple and easy to use
* adding new level should be easy
* running on every device (mouse and touch inputs) and every screen size

This was our first ever App in Python (and Kivy).

=============
How to start:

The code is not packaged, so we still need to start the app with:

> $ python2 main.py -f --size 0x0

The "-f --size 0x0" parameters are necessary because (for some reason)
nothing else works to get a correct fullscreen output, at least on linux.

An android.txt file is included, so you can start it with the Kivy Launcher.
Just put all the contents into:

> /storage/sdcard0/kivy/KivyKloetze/

=============
How to add new levels:

First, there is one restriction that you have to keep in mind while
designing/adding new levels. Due to screen space, visibility and touch restrictions
only six unique shapes can be added. If you want to overcome that restriction,
you need to add more ShapeNumber and ShapeNumberTool classes in the main.py.

We strongly recommend to stick with six tough. Otherwise you would have to decrease the
size of all shapes, which will result in bad touch usability on small screens.

*TODO*