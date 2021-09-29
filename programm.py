##from kivy.uix.behaviors import button
import re
from kivy.uix.behaviors import button
from kivy.uix.widget import Widget
import  julia  
from PIL import Image
from kivy.app import App
from kivy.graphics import texture
from kivy.graphics import opengl
from kivy.graphics.texture import Texture
import kivy.graphics.instructions 
from kivy.graphics import Canvas,Rectangle
##from kivy.graphics.instructions import instructions

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image,AsyncImage
from kivy.uix.image import CoreImage
from kivy.uix.slider import Slider
from kivy.graphics.transformation import Matrix

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout

from kivy.logger import Logger
from kivy.resources import resource_find
from kivy.properties import AliasProperty
from kivy.uix.behaviors.drag import DragBehavior

from kivy.core.window import Window

Window.maximize()

pos = 0

class MyApp(App):
    def Sre_OnSliderValueChange(self,instance,value):
        self.Lre.text = "Re:" + str(value)
    def Sim_OnSliderValueChange(self,instance,value):
        self.Lim.text = "Im:" + str(value)
    def Sr_OnSliderValueChange(self,instance,value):
        self.Lr.text = "R:" + str(value)
    def Sn_OnSliderValueChange(self,instance,value):
        self.Ln.text = "N:" + str(value)
    def Sw_OnSliderValueChange(self,instance,value):
        self.Lw.text = "W:" + str(value)
    def Sh_OnSliderValueChange(self,instance,value):
        self.Lh.text = "H:" + str(value)
    def infoPanelPrint(self,value):
            self.Lpr.text = str(value)
    def render(self,instance):
        c = complex(
            float(str(self.Lre.text).split(':')[1]),
            float(str(self.Lim.text).split(':')[1]))
        r = int(str(str(self.Lr.text).split(':')[1].split('.')[0]))
        n = int(str(self.Ln.text).split(':')[1])
        w = int(str(self.Lw.text).split(':')[1])
        h = int(str(self.Lh.text).split(':')[1])
        print(c,r,n,w,h)
        self.texture = Texture.create(size = (h,w))
        self.texture.blit_buffer(
            julia.getArray(c,r,n,w,h).tobytes(),colorfmt = "rgb",bufferfmt = "ubyte")
        self.img.texture = self.texture
    def saveImage(self,instance):
        self.img.export_to_png("julia.jpg")
        
        
    def build(self):
        self.mB = BoxLayout(orientation = 'horizontal')

        self.mG = GridLayout(rows = 14,size_hint = (.4,1))

        self.pB = BoxLayout(orientation = 'vertical')

        self.Lre = Label(text = "Re:-0.7")
        self.Sre = Slider(min = -1,max = 1,value_track = 'true',step = 0.01,value = -0.7)
        self.Lim = Label(text = "Im:0.75")
        self.Sim = Slider(min = -1,max = 1,value_track = 'true',step = 0.01,value = 0.75)
        self.Lr = Label(text = "R:10")
        self.Sr = Slider(min = 0,max = 100,value_track = 'true',step = 1,value = 10)
        self.Ln = Label(text = "N:500")
        self.Sn = Slider(min = 1,max = 1000,value_track = 'true',step = 1,value = 500)
        self.Lw = Label(text = "W:500")
        self.Sw = Slider(min = 100,max = 10000,value_track = 'true',step = 50,value = 500)
        self.Lh = Label(text = "H:500")
        self.Sh = Slider(min = 100,max = 10000,value_track = 'true',step = 50,value = 500)

        self.rend = Button(text = "render",on_press = self.render)
        self.save = Button(text = "save",on_press = self.saveImage)

        self.array = julia.getArray().tobytes()
        self.texture = Texture.create(size = (500,500))
        self.texture.blit_buffer(self.array,colorfmt = "rgb",bufferfmt = "ubyte")
        self.img = Image(texture =self.texture,nocache = True,allow_stretch = True)
        self.scatt = ResizableDraggablePicture()
        self.scatt.add_widget(self.img)

        self.Lpr = Label(text = "Calculation completed")

        self.pB.add_widget(self.scatt)
        ##self.pB.add_widget(self.Lpr)



        self.mB.add_widget(self.pB)

        self.mB.add_widget(self.mG)
        
        self.Sre.bind(value=self.Sre_OnSliderValueChange)
        self.Sim.bind(value=self.Sim_OnSliderValueChange)
        self.Sr.bind(value=self.Sr_OnSliderValueChange)
        self.Sn.bind(value=self.Sn_OnSliderValueChange)
        self.Sw.bind(value=self.Sw_OnSliderValueChange)
        self.Sh.bind(value=self.Sh_OnSliderValueChange)

        self.mG.add_widget(self.rend)
        self.mG.add_widget(self.save)
        
        self.mG.add_widget(self.Lre)
        self.mG.add_widget(self.Lim)
        self.mG.add_widget(self.Lr)
        self.mG.add_widget(self.Ln)
        self.mG.add_widget(self.Lw)
        self.mG.add_widget(self.Lh)


        self.mG.add_widget(self.Sre)
        self.mG.add_widget(self.Sim)
        self.mG.add_widget(self.Sr)
        self.mG.add_widget(self.Sn)
        self.mG.add_widget(self.Sw)
        self.mG.add_widget(self.Sh)

        return self.mB
    
class ResizableDraggablePicture(DragBehavior,ScatterLayout):
    def __init__(self, **kwargs):
        super(ResizableDraggablePicture, self).__init__(**kwargs)
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
    def on_pos(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
    def on_size(self, *args):
        self.drag_rectangle = [self.x, self.y, self.width, self.height]
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            x = self.pos[0] / 10
            x = round(x, 0)
            x = x * 10
            y = self.pos[1] / 10
            y = round(y, 0)
            y = y * 10
            self.pos = x, y
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            factor = None
            if touch.button == 'scrolldown':
                if self.scale < self.scale_max:
                    factor = 1.1
            elif touch.button == 'scrollup':
                if self.scale > self.scale_min:
                    factor = 1 / 1.1
            if factor is not None:
                self.apply_transform(Matrix().scale(factor, factor, factor),
                             anchor=touch.pos)
        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos
    


if __name__ == "__main__":
    MyApp().run()
    


