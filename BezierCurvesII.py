"""
Al Nesky
May 23 2025

A demo for how we acquired such wild curves
"""

from graphics import *
WIN = GraphWin('Lines doing a good job of being curves for once', 500, 500, False)
WIN.setBackground('white')

class myPoint:
    def __init__(self, center, num):
        self.x, self.y, self.text = center.getX(), center.getY(), Text(Point(center.getX(), center.getY() - 10), 'P' + str(num));
        self.circ = Circle(center, 7)

    def draw(self):
        self.text.draw(WIN)
        self.circ.draw(WIN)

    def undraw(self):
        self.text.undraw()
        self.circ.undraw()

##########################################################################

def distAlongLine(p1, p2, dist):
    point = Point((p2.x - p1.x) * dist + p1.x, (p2.y - p1.y) * dist + p1.y)
    return point

def makeLines(pts, t):
    howManyPts = 1
    objs = []
    #identify how to get t / 1 of the way along each line
    depth1 = [distAlongLine(pts[0], pts[1], t),
              distAlongLine(pts[1], pts[2], t),
              distAlongLine(pts[2], pts[3], t)]
    for i in range(3): 
        objs.append(myPoint(depth1[i], howManyPts))
        howManyPts += 1
        objs[-1].draw()
    #WIN.getMouse()
    for i in range(2):
        objs.append(Line(depth1[i], depth1[i + 1]))
        objs[-1].draw(WIN)

    #WIN.getMouse()

    #same thing with depth 2!
    depth2 = [distAlongLine(depth1[0], depth1[1], t),
              distAlongLine(depth1[1], depth1[2], t)]

    for i in range(2): 
        objs.append(myPoint(depth2[i], howManyPts))
        howManyPts += 1
        objs[-1].draw()

    #WIN.getMouse()

    objs.append(Line(depth2[0], depth2[1]))
    objs[-1].draw(WIN)

    depth3 = distAlongLine(depth2[0], depth2[1], t)
    objs.append(myPoint(depth3, howManyPts))
    howManyPts += 1
    objs[-1].draw()

    return objs



def main():
    pts = []
    for i in range(4):
        pts.append(WIN.getMouse())
        pts[-1].draw(WIN)

    lines = []    

    for i in range(3):
        lines.append(Line(pts[i], pts[i + 1]))
        lines[-1].draw(WIN)
        
    t = 0.6

    objs = makeLines(pts, t)

    while True:
        if WIN.checkMouse():
            WIN.close()
            break

        key = WIN.checkKey()
        if key == 'Right':
            t += 0.05
        elif key == 'Left':
            t -= 0.05

        if key == 'Right' or key == 'Left': 
            for obj in objs: obj.undraw()
            objs = makeLines(pts, t) 

main()
        