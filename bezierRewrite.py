from pygame import *
class PointManager:
    def __init__(self):
        self.points = []
        self.eEpoints = []
        self.cPoints = []

    def getTotalPoints(self) -> list[Vector2]:
        return self.points
    
    def addEPoint(self, thing: Vector2) -> None:
        self.points.append(thing)
        self.eEpoints.append(thing)

    def addCPoint(self, thing: Vector2) -> None:
        self.points.append(thing)
        self.cPoints.append(thing)

    def deletePoint(self, point: Vector2) -> None:
        if point in self.points:
            thing = self.points.index(point)
            self.points.remove(thing)

    def deleteCPoint(self, point) -> None:
        if type(point) == Vector2:
            if point in self.points:
                thing = self.cPoints.index(point)
                self.points.remove(thing)
                self.deletePoint(point)

        elif type(point) == int:
            temp = self.cPoints.pop(point)
            self.deleteCPoint(temp)
            
        else:
            raise TypeError("wtf you put the wrong type here")
        
    def deleteEPoint(self, point) -> None:
        if type(point) == Vector2:
            if point in self.points:
                thing = self.eEpoints.index(point)
                self.points.remove(thing)
                self.deletePoint(point)

        elif type(point) == int:
            temp = self.eEpoints.pop(point)
            self.deleteCPoint(temp)
            
        else:
            raise TypeError("wtf you put the wrong type here")

"""
End of class body
"""

def bezierFunc(a: Vector2, b: Vector2, c: Vector2, d: Vector2, t: float) -> Vector2:
    quickThing = 1-t

    return Vector2(t**3*d.x + c.x * (t**2 * 3 * quickThing) + b.x * (3*t*quickThing**2) + a.x * quickThing**3, t**3*d.y + c.y * (t**2 * 3 * quickThing) + b.y * (3*t*quickThing**2) + a.y * quickThing**3)

# required init functions
init()
SCREEN = display.set_mode((500,500))
running = True
clock = time.Clock() # for frame rate

pm = PointManager()

pm.addEPoint(Vector2(100,100))
pm.addEPoint(Vector2(200,200))
pm.addCPoint(Vector2(159,100))
pm.addCPoint(Vector2(250,200))

# mouse stuff 
isMouseActive = False
currentMoving = 0

while running:

    # events (keys, events etc)
    for ev in event.get():
        if ev.type == QUIT:
            running = False

        # this sucks sorry
        if ev.type == MOUSEBUTTONDOWN:
            isMouseActive = not isMouseActive

            # if the mouse is active, this is how the selected point is found
            if (isMouseActive): 
                isMouseActive = False
                for t in range(len(pm.points)):
                    # fuck tuples :/
                    if abs(pm.points[t].x - mouse.get_pos()[0]) <= 5 and abs(pm.points[t].y - mouse.get_pos()[1]) <= 5:
                        currentMoving = t
                        isMouseActive = True
                        break

        # elif ev.type == KEYDOWN.K_SPACE:
            # pass

    #move point 
    if isMouseActive:
        pm.points[currentMoving].x = mouse.get_pos()[0]
        pm.points[currentMoving].y =  mouse.get_pos()[1]

    # bg
    SCREEN.fill("white")

    # drawing the points
    prevPoint = pm.points[0]

    for t in range(1, 100):
        for n in range(len(pm.eEpoints) - 1):
            temp = bezierFunc(pm.eEpoints[n], pm.cPoints[n], pm.cPoints[n+1], pm.eEpoints[n+1], t/100)
            draw.line(SCREEN, "black", prevPoint, temp)
            prevPoint = temp

    for i in range(len(pm.cPoints)):
        draw.line(SCREEN, "red", pm.cPoints[i], pm.eEpoints[i])
    # draw points
    for i in range(len(pm.points)):
        draw.circle(SCREEN, "black", pm.points[i], 5) 

    # refresh the screen
    display.flip()
    clock.tick(60)

quit()