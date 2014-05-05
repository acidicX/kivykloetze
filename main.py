''' -------------------------------------
    KivyKloetze
    by Carsten Meier and Sina Busch
    -------------------------------------
    A small game for small children
    -------------------------------------
    Licensed under GPL v3
    https://www.gnu.org/licenses/gpl.html
    -------------------------------------
    Please read the README.md file for
    instructions.
    ------------------------------------- '''

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ReferenceListProperty, NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.config import Config

''' -------------------------------------
    Global variables
    ------------------------------------- '''

# global game object, "controller"
game = 0
# current level
level = 0
# puzze parts to solve in current level
parts = 0
# parts in all levels (also defines maximum level count)
partsArray = [5, 4]


''' -------------------------------------
    Shape
    -------------------------------------
    Class for all shapes, heir of Widget,
    contains most of the methods
    for level-based logic ("model")
    ------------------------------------- '''

  
class Shape(Widget):
    def __init__(self, **kwargs):
        super(Shape, self).__init__(**kwargs)
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

    # move stuff around on canvas
    def on_touch_move(self, touch):
        #print ('Shape::on_touch_move', self.shapeId, self.x, self.y, touch.x, touch.y)
        # is it defined as a tool (draggable element)?
        if self.shapeIsTool and self.shapeIsActive:
            # if yes, check if mouse inside element
            if self.collide_point(touch.x, touch.y):
                #print ('Shape::touch inside circle, move')
                self.center = (touch.x, touch.y)

    # collision check on_touch_up
    def on_touch_up(self, touch):
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


''' -------------------------------------
    < SHAPES >
    -------------------------------------
    All used shapes are defined here,
    but drawn in main kv file
    ------------------------------------- '''


# Circle mask, drawn by kv
class ShapeCircle(Shape):
    def __init__(self, **kwargs):
        super(ShapeCircle, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Circle tool, drawn by kv
class ShapeCircleTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeCircleTool, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Quad mask, drawn by kv
class ShapeQuad(Shape):
    def __init__(self, **kwargs):
        super(ShapeQuad, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Quad tool, drawn by kv
class ShapeQuadTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeQuadTool, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)
        
# Triangle mask, drawn by kv
class ShapeTriangle(Shape):
    def __init__(self, **kwargs):
        super(ShapeTriangle, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Triangle tool, drawn by kv
class ShapeTriangleTool(Shape):
    def __init__(self, **kwargs):
        super(ShapeTriangleTool, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Triangle mask, drawn by kv
class ShapePolygon(Shape):
    def __init__(self, **kwargs):
        super(ShapePolygon, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)


# Triangle tool, drawn by kv
class ShapePolygonTool(Shape):
    def __init__(self, **kwargs):
        super(ShapePolygonTool, self).__init__(**kwargs)
        self.size = (Window.height * 0.2, Window.height * 0.2)

  
''' -------------------------------------
    </ SHAPES >
    ------------------------------------- 
    
    -------------------------------------
    < ALL OTHER OBJECTS WITH GRAPHICS >
    -------------------------------------
    Also drawn in main kv file
    ------------------------------------- '''


# All levels are LevelObjects, defined in kv
class LevelObject(Widget):
    def __init__(self, **kwargs):
        super(LevelObject, self).__init__(**kwargs)
        self.size = Window.size


# LevelUpMessage, defined in kv
class LevelUpMessage(Widget):
    def __init__(self, **kwargs):
        super(LevelUpMessage, self).__init__(**kwargs)

 
# GameFinishedMessage, defined in kv
class GameFinishedMessage(Widget):
    def __init__(self, **kwargs):
        super(GameFinishedMessage, self).__init__(**kwargs)


# ToolBoxBar, defined in kv
class ToolBoxBar(Widget):
    def __init__(self, **kwargs):
        super(ToolBoxBar, self).__init__(**kwargs)
        self.size = Window.size
        
''' -------------------------------------
    </ ALL OTHER OBJECTS WITH GRAPHICS >
    -------------------------------------

    ------------------------------------
    KivyKloetze
    -------------------------------------
    Root canvas widget for the game,
    contains most of game logic
    (level loading, etc.)
    ------------------------------------- '''


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
            # print level up message
            self.levelUpMessage = LevelUpMessage()
            game.parent.add_widget(self.levelUpMessage)
            levelUpAni1 = Animation(opacity=1, duration=1)
            levelUpAni2 = Animation(opacity=0, duration=1)
            levelUpAni1.start(self.levelUpMessage)
            Clock.schedule_once(lambda dt: levelUpAni2.start(self.levelUpMessage), 4)
            # load next file in 5 seconds
            Clock.schedule_once(lambda dt: game.loadNextLevel(), 5)
        if level == 0:
            # app start
            game.loadNextLevel()
        if level == partsArray.__len__():
            # show game finished message and restart in 5 seconds
            self.gameFinishedMessage = GameFinishedMessage()
            game.parent.add_widget(self.gameFinishedMessage)
            gf1 = Animation(opacity=1, duration=1)
            gf2 = Animation(opacity=0, duration=1)
            gf1.start(self.gameFinishedMessage)
            Clock.schedule_once(lambda dt: gf2.start(self.gameFinishedMessage), 4)
            # load next file in 5 seconds
            Clock.schedule_once(lambda dt: game.loadNextLevel(), 5)
            Builder.unload_file('level'+str(level)+'.kv')
            level = 0

    def loadNextLevel(self):
        global level, parts
        if level is not 0:
            # remove levelUpMessage again
            game.parent.remove_widget(self.levelUpMessage)
            # remove old level
            game.remove_widget(self.levelObject)
            # unload old level file
            Builder.unload_file('level'+str(level)+'.kv')

        # increment level
        level += 1
        print('KivyKloetze::loadNextLevel::loading', level)

        # load new level file
        Builder.load_file('level'+str(level)+'.kv')
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
