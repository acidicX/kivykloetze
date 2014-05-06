''' ---------------------------------------
    KivyKloetze
    by Carsten Meier and Sina Busch
    ---------------------------------------
    https://github.com/acidicX/kivykloetze
    ---------------------------------------
    A small game for small children
    ---------------------------------------
    Licensed under GPL v3
    https://www.gnu.org/licenses/gpl.html
    ---------------------------------------
    Please read the README.md file for
    instructions.
    --------------------------------------- '''

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ReferenceListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

''' ---------------------------------------
    Global variables
    --------------------------------------- '''

# global game object, "controller"
game = 0
# current level
level = 0
# puzze parts to solve in current level
parts = 0
# parts in all levels (also defines maximum level count)
partsArray = [2, 3, 5, 6, 6]
# contains reference for shape function on_touch_move
selectedElement = 0
# contains reference for level up gimmick
levelUpGimmick = 0


''' ---------------------------------------
    Shape
    ---------------------------------------
    Class for all shapes, heir of Widget,
    contains most of the methods
    for level-based logic ("model")
    --------------------------------------- '''


class Shape(Widget):
    def __init__(self, **kwargs):
        super(Shape, self).__init__(**kwargs)
        # set size
        self.size = (Window.height * 0.2, Window.height * 0.2)
        # shapeId can be: circle, quad, ...
        shapeId = StringProperty(None)
        # defines if shape is currently active
        shapeIsActive = BooleanProperty(None)
        # defines if shape is a tool or a mask
        shapeIsTool = BooleanProperty(None)
        # count of tools with the same shape
        shapeToolNo = NumericProperty(None)
        # if tool, save default shape center
        shapeCenter = ReferenceListProperty(None)

    # move selector on_touch_down TODO
    def on_touch_down(self, touch):
        global selectedElement
        # is it defined as an active tool (draggable element)?
        if self.shapeIsTool and self.shapeIsActive:
            # if yes, check if mouse inside element
            if self.collide_point(touch.x, touch.y):
                # if yes, set reference for on_touch_move
                selectedElement = self

    # move stuff around on canvas
    def on_touch_move(self, touch):
        # if an element reference has been set
        if selectedElement:
            # move element on canvas to touch coordinates
            selectedElement.center = (touch.x, touch.y)

    # collision check on_touch_up
    def on_touch_up(self, touch):
        global selectedElement
        # delete reference for on_touch_move
        selectedElement = 0

        # only check tools, not masks
        if self.shapeIsTool and self.shapeIsActive:
            # array of masks
            maskArray = []
            # if collision has been detected, true
            collisionFound = False
            # correct colliding element
            collidingElement = 0

            # check tool against other children
            for c in self.parent.children:
                # filter - only shape elements!
                if hasattr(c, 'shapeIsTool'):
                    # we only want active masks with the same shapeId as our tool
                    if c.shapeIsTool is False and c.shapeIsActive is True and c.shapeId == self.shapeId:
                        # filter other (still disabled) tools
                        if hasattr(c, 'shapeToolNo') is False:
                            # add to array
                            maskArray.append(c)

            # check for collision with all filtered shapes
            for c in maskArray:
                # if center distance is close enough (collision detection)
                if Vector(self.center).distance(c.center) < (Window.width / 25):
                    collisionFound = True
                    collidingElement = c

            if collisionFound:
                # execute collide function
                self.collide(collidingElement, maskArray.__len__())
                print('Shape::on_touch_up::found collision', maskArray.__len__())
            else:
                # element not colliding or not close enough to center, reset tool to default center
                print('Shape::on_touch_up::no collision found, reset tool to default center')
                self.reset_to_default_center()

    # reset the tool to default center
    def reset_to_default_center(self):
        self.center = self.shapeCenter

    # check if element collides when dropped
    def collide(self, otherWidget, numberOfMasks):
        # center tool on mask
        print ('Shape::collide::center tool on mask')
        self.center = otherWidget.center
        # if multiple tools inside level, set next one active
        if hasattr(self, 'shapeToolNo'):
            if self.shapeToolNo < numberOfMasks:
                print ('Shape::collide::more than one mask with same shape, set next tool active')
                for c in self.parent.children:
                    # filter - only shape elements!
                    if hasattr(c, 'shapeToolNo'):
                        # we only want inactive tools with the same shapeId as our tool
                        if c.shapeIsActive is False and c.shapeId == self.shapeId:
                            # we also only want the next element!
                            if c.shapeToolNo == self.shapeToolNo + 1:
                                print ('Shape::collide::new tool active')
                                c.shapeIsActive = True

        # set shape and mask inactive
        self.shapeIsActive = False
        otherWidget.shapeIsActive = False
        # trigger puzzle part counter
        print('Shape::collide::call game.puzzlePartDone()')
        game.puzzlePartDone()


''' ---------------------------------------
    < SHAPES >
    ---------------------------------------
    All four shapes are defined here,
    but drawn in <lvl/level#.kv> file
    --------------------------------------- '''


# First mask, drawn by kv
class ShapeOne(Shape):
    def __init__(self, **kwargs):
        super(ShapeOne, self).__init__(**kwargs)


# First tool, drawn by kv
class ShapeOneTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeOneTool, self).__init__(**kwargs)


# Second mask, drawn by kv
class ShapeTwo(Shape):
    def __init__(self, **kwargs):
        super(ShapeTwo, self).__init__(**kwargs)


# Second tool, drawn by kv
class ShapeTwoTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeTwoTool, self).__init__(**kwargs)


# Third mask, drawn by kv
class ShapeThree(Shape):
    def __init__(self, **kwargs):
        super(ShapeThree, self).__init__(**kwargs)


# Third tool, drawn by kv
class ShapeThreeTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeThreeTool, self).__init__(**kwargs)


# Fourth mask, drawn by kv
class ShapeFour(Shape):
    def __init__(self, **kwargs):
        super(ShapeFour, self).__init__(**kwargs)


# Fourth tool, drawn by kv
class ShapeFourTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeFourTool, self).__init__(**kwargs)


# Fifth mask, drawn by kv
class ShapeFive(Shape):
    def __init__(self, **kwargs):
        super(ShapeFive, self).__init__(**kwargs)


# Fifth tool, drawn by kv
class ShapeFiveTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeFiveTool, self).__init__(**kwargs)


# Sixth mask, drawn by kv
class ShapeSix(Shape):
    def __init__(self, **kwargs):
        super(ShapeSix, self).__init__(**kwargs)


# Sixth tool, drawn by kv
class ShapeSixTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeSixTool, self).__init__(**kwargs)

''' ---------------------------------------
    </ SHAPES >
    ---------------------------------------

    ---------------------------------------
    < ALL OTHER OBJECTS WITH GRAPHICS >
    ---------------------------------------
    Drawn in <kivykloetze.kv> and/or
    <lvl/level#.kv> file
    --------------------------------------- '''


# All levels are LevelObjects, defined in kv
class LevelObject(Widget):
    def __init__(self, **kwargs):
        super(LevelObject, self).__init__(**kwargs)
        self.size = Window.size


# SplashScreen, defined in kv
class SplashScreen(Widget):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.size = Window.size


# All levels are LevelObjects, defined in kv
class LevelUpGimmick(Widget):
    def __init__(self, **kwargs):
        super(LevelUpGimmick, self).__init__(**kwargs)
        # indicator for level up gimmick
        isGimmick = BooleanProperty(None)


# GameFinishedMessage, defined in kv
class GameFinishedMessage(Widget):
    def __init__(self, **kwargs):
        super(GameFinishedMessage, self).__init__(**kwargs)


# ToolBoxBar, defined in kv
class ToolBoxBar(Widget):
    def __init__(self, **kwargs):
        super(ToolBoxBar, self).__init__(**kwargs)
        self.size = Window.size
        # indicator for toolboxbar
        isToolBoxBar = BooleanProperty(None)

''' ---------------------------------------
    </ ALL OTHER OBJECTS WITH GRAPHICS >
    ---------------------------------------

    ------------------------------------
    KivyKloetze
    ---------------------------------------
    Root canvas widget for the game,
    contains most of game logic -
    level loading, etc. ("controller")
    --------------------------------------- '''


class KivyKloetze(Widget):
    def __init__(self, **kwargs):
        super(KivyKloetze, self).__init__(**kwargs)

    # count puzzle parts and check for next level
    def puzzlePartDone(self):
        global parts
        # substract one part
        parts -= 1
        # if parts are empty, load next level
        if parts == 0:
            print('KivyKloetze::puzzlePartDone::parts empty, start next level')
            game.nextLevel()

    # load next level and set up stage
    def nextLevel(self):
        global level
        if level is not 0 and level < partsArray.__len__():
            self.levelUp()
            # load next file in 5 seconds
            Clock.schedule_once(lambda dt: game.loadNextLevel(), 5)

        if level == 0:
            # app start, show splash screen
            self.splashScreen = SplashScreen()
            game.add_widget(self.splashScreen)
            splashAni1 = Animation(opacity=1, duration=1)
            splashAni1.start(self.splashScreen)
            splashAni2 = Animation(opacity=0, duration=1)
            Clock.schedule_once(lambda dt: splashAni2.start(self.splashScreen), 6)
            Clock.schedule_once(lambda dt: game.remove_widget(self.splashScreen), 7)
            # load first level in 5s
            Clock.schedule_once(lambda dt: game.loadNextLevel(), 7)

        if level == partsArray.__len__():
            self.levelUp()
            # show game finished message and restart in 5 seconds
            self.gameFinishedMessage = GameFinishedMessage()
            game.parent.add_widget(self.gameFinishedMessage)
            gf1 = Animation(opacity=1, duration=1)
            gf2 = Animation(opacity=0, duration=1)
            gf1.start(self.gameFinishedMessage)
            Clock.schedule_once(lambda dt: gf2.start(self.gameFinishedMessage), 10)
            # load next file in 5 seconds
            Clock.schedule_once(lambda dt: game.loadNextLevel(), 11)
            Builder.unload_file('lvl/level'+str(level)+'.kv')
            level = 0

    def levelUp(self):
        # hide ToolBoxBar
        for c in self.levelObject.children:
            # filter - only toolboxbar
            if hasattr(c, 'isToolBoxBar'):
                # fade in
                hideToolBoxBarAni = Animation(opacity=0, duration=1)
                hideToolBoxBarAni.start(c)

        # play level sound
        levelUpSound = SoundLoader.load('snd/' + str(level) + '.ogg')
        if levelUpSound:
            print("KivyKloetze::playLevelUpSound::play sound %s" % levelUpSound.source)
            levelUpSound.play()

        # show level up gimmicks
        for c in self.levelObject.children:
            # filter - only gimmicks
            if hasattr(c, 'isGimmick'):
                # fade in
                levelUpGimmickAni = Animation(opacity=1, duration=1)
                levelUpGimmickAni.start(c)

    def loadNextLevel(self):
        global level, parts
        if level is not 0:
            # remove old level
            game.remove_widget(self.levelObject)
            # unload old level file
            Builder.unload_file('lvl/level'+str(level)+'.kv')

        # increment level
        level += 1
        print('KivyKloetze::loadNextLevel::loading', level)

        # load new level file
        Builder.load_file('lvl/level'+str(level)+'.kv')
        Builder.sync()

        # add new level object to game stage
        self.levelObject = LevelObject()
        game.add_widget(self.levelObject)

        # correct parts count
        parts = partsArray[level-1]


# Startup routine
class KivyKloetzeApp(App):
    def build(self):
        global game
        game = KivyKloetze()
        game.size = Window.size
        print ('KivyKloetzeApp::start')
        game.nextLevel()
        return game


if __name__ == "__main__":
    Config.set('graphics', 'fullscreen', 'auto')
    KivyKloetzeApp().run()
