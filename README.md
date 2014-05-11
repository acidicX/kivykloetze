#KivyKlötze
by [Carsten](https://github.com/acidicX) ([web profile](http://condime.de/cm)) and Sina

Licensed under GPL v3

https://www.gnu.org/licenses/gpl.html

For the audio sources and respective licenses, see snd/sources.md

=============
###A small game for small children

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

Note that audio files did not play on our Android test device (HTC Desire X, Android 4.1 with Kivy Launcher). This could be another Kivy issue since audio works fine on linux and Windows.

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

All **level** files are written in [Kivy language](http://kivy.org/docs/api-kivy.lang.html) and stored in the 'lvl' directory. They are numbered consecutively - level1.kv, level2.kv ...

All **artwork** is stored in the 'img' directory, followed by the level number subdirectory. The background for the first level ist stored in 'img/1/bg.jpg', for example. Artwork can be in all formats Kivy can handle.

All **sounds** (level up sounds) are stored in the 'snd' directory. They need to be ogg/vorbis files and have to be named 'levelnumber.ogg' - so for the first level, the filename should be '1.ogg'.

####Creating a new level

**Objects inside a level file**

* Masks (= Shapes, up to 6 individual, unlimited in total)
* Tools (= Shapes, up to 6 individual, unlimited in total)
* Level Object with Background (1x)
* Toolbox Bar (1x)
* Level Up Gimmicks (unlimited)

First, there is one restriction that you have to keep in mind while
designing/adding new levels. Due to screen space, visibility and touch restrictions only six **individual** shapes (dragable elements) can be added. **In total, you can add more than six shapes if you add multiples of one individual shape**, e.g. three times ShapeOne. If you want to overcome that restriction, look at the end of this readme. 

Ok, let's get started. Apart from the level files written in Kivy language, there is no need to modify any actual program code in order to add new levels. We will now explain how to create a new level file by using the included 'level4.kv' file as an example.

At the top of the level#.kv file, the masks and shapes have to be described. In this case, we have four masks (ShapeOne, ShapeTwo, ...) and therefore also four tools (ShapeOneTool, ShapeTwoTool, ...). The only thing you need to define yourself is the artwork - edit the 'source' lines for each shape
> source: 'img/4/mask_blume1.png' <
to match it to your new level artwork, e.g. 'img/6/mask_quad1.png' for a level6.kv file.

Now it will get a bit more tricky, we need to define the LevelObject
> \<LevelObject\>: <
which basically contains all object placements and further artwork descriptions.

First, give the level a new background by changing the source line of the rectangle on the canvas of LevelObject:
> <LevelObject>:
>    canvas:
>        Rectangle:
>            size: self.size
>            source: 'img/6/mynewlevel6background.jpg'

After that, we need to leave the ToolBoxBar element in place (it's the grey transparent bar where all tool shapes lie on):
>    ToolBoxBar:
>        isToolBoxBar: True

Then we add all masks and tools to the canvas.
**Mask properties**:
* shapeId (required, must be the number of the element, ShapeOne = 1)
* shapeIsActive (required, must be True)
* shapeIsTool (required, must be False - because it's a mask)
* center (required, positioning of the mask on the canvas)

**Tool properties**:
* shapeId (required, must be the number of the element, ShapeFourTool = 4)
* shapeIsActive (required, must be True for the first element in stack, False for every element beneath the first)
* shapeIsTool (required, must be True - because it's a tool)
* shapeToolNo (optional, used only if tools are stacked, incremented with every stacked element)
* shapeCenter (required, must be an exact copy of center)
* center (required, positioning of the mask on the canvas)

Corresponding masks and tools must **always** have the same shapeId!
In order to add multiple masks and tools of the same class (e.g. ShapeFour and ShapeFourTool in level4.kv), the tools can be stacked inside the toolbox. Therefore, the first tool with
> shapeToolNo: 1
must be active,
> shapeIsActive: True
but all following (stacked) tools must be inactive, e.g.
>    ShapeFourTool:
>        shapeId: 4
>        shapeIsActive: False
>        shapeIsTool: True
>        shapeToolNo: 2

If you want to add level up gimmicks (optional), you can just include them after the tools. There is no limit for level up gimmicks. They will be faded in once the level is completed. You can set the size, center and source of all gimmicks.

> LevelUpGimmick:
>        **size**: root.height * 0.2, root.height * 0.2
>        **center**: 0 + root.width * 0.9, root.height * 0.8
>        opacity: 0
>        isGimmick: True
>        canvas:
>            Color:
>                rgb: 1, 1, 1
>            Rectangle:
>                pos: self.pos
>                size: self.size
>                **source**: 'img/4/biene.png'

Last but not least, you can add a level up sound to your level. Just place a soundfile 'levelnumber.ogg' as an [ogg/vorbis](http://www.vorbis.com/) file in the 'snd' directory, e.g. '6.ogg'. **It should not be longer than 5 seconds.**

=============
###Six unique (individual) shapes restriction

This restriction is in place for a reason. We **strongly recommend** to stick with six shapes. Otherwise you would have to decrease the size of all shapes, which will result in bad touch usability on small screens.

If you still want to add more individual shapes to a level, you just need to add more ShapeNumber and ShapeNumberTool classes in the main.py.