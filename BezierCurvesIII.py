"""
Al Nesky
May 30 2025

An attempt at making bezier curves cooperate
Using the power of TEAMWORK
and FRIENDSHIP

We are so doomed
"""

from graphics import *
WIN = GraphWin('such squiggles, such beauty', 500, 500, False)
WIN.setBackground(color_rgb(200, 200, 220))

RES = 100
ORANGE = color_rgb(200, 160, 90)

def bezierEq(a, b, c, d, t):
    i = (1 - t)
    return (t ** 3 * d) + c * ((t ** 2) * 3 * i) + b * (3 * t * i ** 2) + a * i ** 3



def undrawCurve(curve):
    for ln in curve:
        ln.undraw()



class myPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.shape = Circle(Point(x, y), 10)
        self.color = 'white'
        self.render()
    
    def render(self):
        self.shape.undraw()
        self.shape = Circle(Point(self.x, self.y), 10)
        self.shape.setFill(self.color)
        self.shape.draw(WIN)


    def clickedOn(self, click):
        dx, dy = click.getX() - self.x, click.getY() - self.y
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d <= 10: return True

class endPoint(myPoint):
    def __init__(self, x, y, control = None):
        self.control = control
        super().__init__(x, y)

    def createLine(self):
        if self.control == None: return None
        self.line = Line(Point(self.x, self.y), Point(self.control.x, self.control.y))
        self.line.setFill(ORANGE)
        self.line.draw(WIN)

class curvePoint(endPoint):
    def getOtherControl(self, control):
        dx, dy = self.x - control.x, self.y - control.y
        #circ = Circle(Point(self.x + dx, self.y + dy), 10)
        #circ.draw(WIN)
        return Point(self.x + dx, self.y + dy)


  
def generateCurve(pts):

    for i in range(len(pts) - 1):
        p1 = pts[i]
        p2 = pts[i + 1]

        if type(p1) == endPoint: c1 = p1.control
        else: c1 = p1.getOtherControl(p1.control)

        if type(p2) == endPoint: c2 = p2.control
        else: c2 = p2.control

        ########################
        xes, ys = [], []
        for _ in range(RES):
            t = _ / RES
            xes.append(bezierEq(p1.x, c1.x, c2.x, p2.x, t))
            ys.append(bezierEq(p1.y, c1.y, c2.y, p2.y, t))

            curve = []

        #draws lines between the given points on the curve
        for i in range(1, len(xes)):
            ln = Line(Point(xes[i], ys[i]), Point(xes[i - 1], ys[i - 1]))
            ln.draw(WIN)
            curve.append(ln)

    return curve



def main():
    pts = []
    curve = None
    clickedOnPt = None
    nextThing = 'linePoint'
    while True:
        key, click = WIN.checkKey(), WIN.checkMouse()
        if key == 'q' or key == 'Q':
            WIN.close()
            break

        if click:
            if clickedOnPt == None:
                for pt in pts:
                    if pt.clickedOn(click) == True: clickedOnPt = pt
            
            #if user clicks on preexisting point, move it to their next click
            if clickedOnPt != None:
                clickedOnPt.color = ORANGE
                clickedOnPt.render()

                click = WIN.getMouse()
                clickedOnPt.x, clickedOnPt.y = click.getX(), click.getY()
                clickedOnPt.color = 'white'
                clickedOnPt.render()
                clickedOnPt = None

                #redraw the curve
                undrawCurve(curve)
                try:
                    curve = generateCurve(pts)
                except: pass

            elif clickedOnPt == None:
                if nextThing == 'linePoint':
                    pts.append(endPoint(click.getX(), click.getY(), None))
                    if len(pts) > 2: pts[-2] = curvePoint(pts[-2].x, pts[-2].y, pts[-2].control)
                    nextThing = 'controlPoint'

                elif nextThing == 'controlPoint':
                    pts[-1].control = myPoint(click.getX(), click.getY())
                    if curve != None:
                        undrawCurve(curve)
                    if len(pts) > 1: curve = generateCurve(pts)
                    pts[-1].createLine()
                    nextThing = 'linePoint'

main()



