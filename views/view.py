import Tkinter as tk
import numpy as np
import math

# interaction modes
BRUSHING = 1
LINKING = 2
PANNING = 3
TRAVELING = 4
ZOOMING = 5
NONE = 0

# selector geometry
RECTANGLE = 0
CIRCLE = 1
LINE = 2
POLYGON = 3

class Selector(object):
    """Widget for selecting objects on a view
    
    
    """
    def __init__(self, canvas):
        self.canvas = canvas

    def start(self, coords):
        pass

    def draw(self, coords):
        pass

    def move(self, coords):
        pass

    def delete(self):
        pass

    def findUnder(self):
        pass

    def findOverlapping(self):
        pass

    def findOutside(self):
        pass

class RectangleSelector(Selector):
    """ """
    def __init__(self, canvas):
        super(RectangleSelector, self).__init__(canvas)

    def start(self, coords):
        print coords

class CircleSelector(Selector):
    """ """
    def __init__(self, canvas):
        super(CircleSelector, self).__init__(canvas)

class LineSelector(Selector):
    """ """
    def __init__(self, canvas):
        super(LineSelector, self).__init__(canvas)

class PolygonSelector(Selector):
    """ """
    def __init__(self, canvas):
        super(PolygonSelector, self).__init__(canvas)


    def draw(self):
        """
        Trace out the perimeter of the polygon and snap starting and ending
        vertices to close.

        Mouse down-move traces the polygon, on mouse up snap
        """
        pass

selectors = {}
selectors[RECTANGLE] = RectangleSelector
selectors[CIRCLE] = CircleSelector
selectors[LINE] = LineSelector
selectors[POLYGON] = PolygonSelector

class LegendFrame(tk.Frame):
    """
    Container for Legend
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(fill='y', expand='no')
        width = 200
        height = self.parent.winfo_screenheight() / 2.
        self.canvas = tk.Canvas(self, bg='white', width = width, height =
                height)
        self.canvas.create_text(100, height/2., text='LEGEND')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky='ns')

class CanvasFrame(tk.Frame):
    """
    Container for Canvas
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self._title = 'CanvasFrame'
        #self.parent.title("CanvasView")
        self.pack(fill=tk.BOTH, expand = 1)
        height = self.parent.winfo_screenheight() / 2.
        width = self.parent.winfo_screenwidth() /2.
        length = height
        if width < height:
            length = width
        self.canvas = tk.Canvas(self, bg='white', width=length, height=length)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.canvas.create_line(0, 0, width, height, width = 5.0)
        self.canvas.create_line(0, height, width, 0, width = 5.0)
        self.config_events = 0

        # Event bindings
        self.canvas.bind('<Configure>', self.onConfigure)
        self.canvas.bind('<2>', self.popUpMenu) # for mac
        self.canvas.bind('<3>', self.popUpMenu)
        self.canvas.bind('<Shift-1>', self.setBrushingE)
        self.canvas.bind('l', self.setLinkingE)
        self.canvas.bind('n', self.setInteractionOffE)
        self.canvas.bind('z', self.setZoomingE)
        self.canvas.focus_set()
        self.makeMenu()

        # zooming
        self.zoom_history = []
        self.zoom_on = 0
        self._percent = 1.

    def title(self, title=None):
        if not title:
            return self._title
        else:
            self._title = title
            self.parent.title(self._title)

    def makeMenu(self):
        """
        Menu for the canvas
        """
        self.interaction_mode = tk.IntVar()
        self.selector_geometry = tk.IntVar()
        self.menu = tk.Menu(self.parent, tearoff=0)
        # interaction modes
        self.menu.add_separator()
        self.menu.add_command(label='Interaction')
        self.menu.add_separator()
        self.menu.add_radiobutton(label='Brush',
                variable=self.interaction_mode, value=BRUSHING,
                command=self.interaction_select)
        self.menu.add_radiobutton(label='Link',
                variable=self.interaction_mode, value=LINKING,
                command=self.interaction_select)
        self.menu.add_radiobutton(label='Pan',
                variable=self.interaction_mode, value=PANNING,
                command=self.interaction_select)
        self.menu.add_radiobutton(label='Zoom',
                variable=self.interaction_mode, value=ZOOMING,
                command=self.interaction_select)
        self.menu.add_radiobutton(label='None',
                variable=self.interaction_mode, value=NONE,
                command=self.interaction_select)
        # selector geometry
        self.menu.add_separator()
        self.menu.add_command(label='Selector')
        self.menu.add_separator()
        self.menu.add_radiobutton(label='Rectangle',
                variable=self.selector_geometry, value=RECTANGLE,
                command=self.selector_select)
        self.menu.add_radiobutton(label='Circle',
                variable=self.selector_geometry, value=CIRCLE,
                command=self.selector_select)
        self.menu.add_radiobutton(label='Line',
                variable=self.selector_geometry, value=LINE,
                command=self.selector_select)
        self.menu.add_radiobutton(label='Polygon',
                variable=self.selector_geometry, value=POLYGON,
                command=self.selector_select)
        # other
        self.menu.add_separator()
        self.menu.add_command(label='Reset', underline=0, command=self.redraw,
                accelerator='r')
        self.menu.add_separator()
        self.menu.add_command(label='Print')
        self.menu.add_command(label='Save')
        self.menu.add_separator()
        self.menu.add_command(label='Close', command=self.close)
        self.menu.add_command(label='Quit', command=self.quit)
    
    def close(self):
        self.parent.destroy()

    def quit(self):
        self.parent.master.destroy()

    def popUpMenu(self, event):
        self.current_mode = self.interaction_mode.get()
        self.menu.post(event.x_root, event.y_root)

    def setInteractionOffE(self, event):
        self.set_interaction_mode(NONE)

    def interaction_select(self):
        self.set_interaction_mode(self.interaction_mode.get())

    def setZoomingE(self, event):
        self.set_interaction_mode(ZOOMING)

    def setBrushingE(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        self.set_interaction_mode(BRUSHING)

    def setLinkingE(self, event):
        self.set_interaction_mode(LINKING)

    def set_interaction_mode(self, mode):
        print 'set interaciton_mode: ', mode
        if mode == BRUSHING:
            print 'brushing selected'
            self.interaction_mode.set(BRUSHING)
            self.currrent_mode = BRUSHING
            self.canvas.unbind('<1>')
            self.canvas.bind('<1>', self.startBrushing)
            self.canvas.unbind('<B1-Motion>')
            self.canvas.bind("<Motion>", self.moveBrush)
            self.canvas.bind('<B1-Motion>', self.sizeBrushWindow)
            self.canvas.unbind('<B1-ButtonRelease>')
            self.canvas.bind('<B1-ButtonRelease>', self.brushWindowStop)
            self.canvas.unbind('<Control-u>',)
            self.canvas.bind('<r>', self.redrawE)
            self.canvas.bind('<Escape>', self.handleEscE)
            self.zoom_on = 0
            self.brush_on = 1
            self.canvas.focus_set()
        elif mode == PANNING:
            self.interaction_mode.set(PANNING)
            self.current_mode = PANNING
            self.canvas.unbind('<1>')
            self.canvas.bind('<1>', self.startPanning)
            self.canvas.unbind('<B1-Motion>')
            self.canvas.bind('<B1-Motion>', self.panning)
        elif mode == LINKING:
            self.interaction_mode.set(LINKING)
            self.current_mode = LINKING
            self.canvas.unbind('<1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.bind('<r>', self.redrawE)
            self.canvas.focus_set()
        elif mode == ZOOMING:
            self.interaction_mode.set(ZOOMING)
            self.current_mode = ZOOMING
            self.canvas.unbind('<1>')
            self.canvas.bind('<1>', self.startZooming)
            self.canvas.unbind('<B1-Motion>')
            self.canvas.bind('<B1-Motion>', self.sizeZoomWindow)
            self.canvas.unbind('<B1-ButtonRelease>')
            self.canvas.bind('<B1-ButtonRelease>', self.zoomWindowStop)
            self.canvas.unbind('<Control-u>',)
            self.canvas.bind('<r>', self.redrawE)
            self.zoom_on = 1
            self.canvas.focus_set()
        elif mode == NONE:
            self.interaction_mode.set(NONE)
            self.canvas.unbind('<1>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.unbind('<B1-ButtonRelease>')
            print 'Interaction mode is NONE'

    def redrawE(self, event):
        self.redraw()

    def startPanning(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def panning(self, event):
        self.canvas.scan_dragto(event.x, event.y)

    def startBrushing(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasx(event.y)

    def sizeBrushWindow(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasx(event.y)

        if (x != self.start_x) and (y != self.start_y):
            try:
                self.canvas.delete(self.selector)
            except:
                pass # no selector exists
            #self.selector = self.canvas.create_rectangle(self.start_x,
            #        self.start_y, x, y, tag='selector')
            dx = x - self.start_x
            dy = y - self.start_y
            dx /= math.pi
            dy /= math.pi
            self.selector = self.canvas.create_oval(self.start_x-dx,
                    self.start_y-dy, x+dx, y+dy, tag='selector')
            self.update_idletasks()

    def brushWindowStop(self, event):
        selector_coords = self.canvas.coords('selector')
        print 'brush window rezied'

        # now set bindings to handle moving of brush window
        self.canvas.unbind('<1>')
        self.canvas.bind('<1>', self.startMoveBrush)
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind('<B1-Motion>', self.moveBrush)
        self.canvas.unbind('<B1-ButtonRelease>')

    def startMoveBrush(self, event):
        selector_coords = self.canvas.coords('selector')

    def moveBrush(self, event):
        selector_coords = self.canvas.coords('selector')
        if selector_coords:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasx(event.y)
            dx = x - selector_coords[2]
            dy = y - selector_coords[3]
            x0 = selector_coords[0] + dx
            y0 = selector_coords[1] + dy
            x1 = selector_coords[2] + dx
            y1 = selector_coords[3] + dy

            if (x != self.start_x) and (y != self.start_y):
                try:
                    self.canvas.delete(self.selector)
                except:
                    pass # no selector exists
                #self.selector = self.canvas.create_rectangle(x0, y0, x1, y1, tag='selector')
                self.selector = self.canvas.create_oval(x0, y0, x1, y1, tag='selector')
                self.update_idletasks()

    def handleEscE(self, event):
        try:
            self.canvas.delete(self.selector)
        except:
            pass # no selector exists

        # unset mouse bindings
        self.canvas.unbind('<1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<B1-ButtonRelease>')
        self.interaction_mode.set(NONE)

    def startZooming(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasx(event.y)

    def sizeZoomWindow(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasx(event.y)

        if (x != self.start_x) and (y != self.start_y):
            try:
                self.canvas.delete(self.selector)
            except:
                pass # no selector exists
            self.selector = self.canvas.create_rectangle(self.start_x,
                    self.start_y, x, y, tag='selector')
            self.update_idletasks()

    def zoomWindowStop(self, event):
        selector_coords = self.canvas.coords('selector')
        if selector_coords:
            x0, y0, x1, y1 = self.canvas.coords("selector")
            self.canvas.delete(self.selector)
            self.zoom(coords = (x0, y0, x1, y1))

    def zoom(self, percent=2.0, coords=None):
        Mx = self.width / 2.
        My = self.height / 2.

        if coords:
            x0, y0, x1, y1 = coords
            mx = (x0 + x1) / 2.
            my = (y0 + y1) / 2.
        else:
            my = Mx
            mx = My

        dx = Mx - mx
        dy = My - my

        self.zoom_history.append((percent, dx, dy))
        self.updatePercent(percent)

        self.canvas.move(tk.ALL, dx, dy)
        self.canvas.scale(tk.ALL, Mx, My, percent, percent)

    def updatePercent(self, percent):
        self._percent *= percent

    def onConfigure(self, event):
        print '(%d, %d)' %(event.width, event.height)
        print 'config_events: ', self.config_events
        #self.canvas.delete(tk.ALL)
        #self.canvas.create_line(0,0, event.width, event.height, width=5.0)
        self.width = event.width
        self.height = event.height
        self.redraw()
        self.config_events += 1

    def redraw(self):
        self.canvas.delete(tk.ALL)
        # buffer so we have some space between edge of parent window and our drawing
        # bounding box
        # bounding box is a square with sides having length equal to 
        # 1/2 * minimum [parent_width, parent_height]
        buff = (1 - 0.025) # use .975 of the window's min dimension
        if self.width < self.height:
            length = self.width
        else:
            length = self.height

        length *= buff
        self.x0 = self.width - length
        self.x0 /= 2
        self.x1 = self.x0 + length
        self.y0 = self.height - length
        self.y0 /= 2
        self.y1 = self.y0 + length

        # world coords for line
        wc_line = [ (100,100), (2000,2000) ]
        wc_line1 = [ (100,2000), (2000, 100) ]
        lines = np.array([ wc_line, wc_line1 ])
        xs = np.array([line[0] for line in lines])
        ys = np.array([line[1] for line in lines])
        min_x = xs.min()
        min_y = ys.min()
        max_x = xs.max()
        max_y = ys.max()

        width_world = max_x - min_x
        height_world = max_y - min_y
        sy = length * 1. / height_world
        sx = length * 1. / width_world

        x0 = self.x0
        y0 = self.y0 + (max_y - min_y) * sy 
        x1 = (max_x - min_x) * sx + self.x0
        y1 = self.y0 

        # first diagonal
        self.canvas.create_line(x0, y0, x1, y1, width=1.0)

        # second diagonal
        x0 = self.x0
        y0 = self.y0 
        x1 = (max_x - min_x) * sx + self.x0
        y1 = self.y0 + (max_y - min_x) * sy
        self.canvas.create_line(x0, y0, x1, y1, width=1.0)

        # left
        self.canvas.create_line(x0, y0, x0, y1, width=1.0)

        # right
        self.canvas.create_line(x1, y0, x1, y1, width=1.0)

        # top
        self.canvas.create_line(x0, y1, x1, y1, width=1.0)

        # bottom
        self.canvas.create_line(x0, y0, x1, y0, width=1.0)

        # create semi transparent square in the middle
        side = (x1-x0) / 10. # 1/10 of the canvas for the dimension 
        cx = (x1+x0) / 2.
        cy = (y1+y0) / 2.
        left = cx - side/2.
        right = cx + side/2.
        top = cy - side/2.
        bottom = cy + side/2.
        self.canvas.create_rectangle(left,bottom,right,top, fill="blue",
                stipple="gray12")
        self.canvas.create_rectangle(right,top,right+side, top-side,
                fill="yellow",
                stipple="gray12")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        # note that transparency isn't supported under Aqual (Mac OS X)

    def selector_select(self):
        self.set_selector_geometry(self.selector_geometry.get())

    def set_selector_geometry(self, mode):
        print 'set selector_geometry: ', mode
        self.selector_geometry.set(mode)
        self.selector_object = selectors[mode](self.canvas)

if __name__ == '__main__':

    root = tk.Tk()
    t1 = tk.Toplevel(root)
    view_1 = CanvasFrame(t1)
    view_1.title('View 1')
    view_2 = CanvasFrame(tk.Toplevel(root))
    view_2.title('View 2')
    root.title('STARS')
    #root.mainloop()
