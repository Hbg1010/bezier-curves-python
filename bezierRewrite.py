from pygame import *

def bezierFunc(a: Vector2, b: Vector2, c: Vector2, d: Vector2, t: float) -> Vector2:
    quickThing = 1-t

    return Vector2(t**3*d.x + c.x * (t**2 * 3 * quickThing) + b.x * (3*t*quickThing**2) + a.x * quickThing**2, t**3*d.y + c.y * (t**2 * 3 * quickThing) + b.y * (3*t*quickThing**2) + a.y * quickThing**2)

# required init functions
init()
SCREEN = display.set_mode((500,500))
running = True
clock = time.Clock() # for frame rate

#points
clickPoses = []

# temp points
clickPoses.append(Vector2(100,100)) # e1
clickPoses.append(Vector2(159,100)) #c1
clickPoses.append(Vector2(250,200)) #c2
clickPoses.append(Vector2(200,200)) #e2

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
                for t in range(len(clickPoses)):
                    # fuck tuples :/
                    if abs(clickPoses[t].x - mouse.get_pos()[0]) <= 5 and abs(clickPoses[t].y - mouse.get_pos()[1]) <= 5:
                        currentMoving = t
                        isMouseActive = True
                        break

    #move point 
    if isMouseActive:
        clickPoses[currentMoving] = Vector2(mouse.get_pos()[0], mouse.get_pos()[1])

    # bg
    SCREEN.fill("white")

    # drawing the points
    prevPoint = clickPoses[0]

    for t in range(1, 100):
        temp = bezierFunc(clickPoses[0], clickPoses[1], clickPoses[2], clickPoses[3], t/100)
        draw.line(SCREEN, "black", prevPoint, temp)
        prevPoint = temp


    # draw points
    for i in range(len(clickPoses)):
        draw.circle(SCREEN, "black", clickPoses[i], 5) 

    # refresh the screen
    display.flip()
    clock.tick(60)

quit()