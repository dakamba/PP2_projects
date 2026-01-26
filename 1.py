import turtle
import time
delay = 0.2

wn = turtle.Screen()
wn.title("SNake Game")
wn.bgcolor('Green')
wn.setup(width=600, height=600)
wn.tracer(0)

head = turtle.Turtle()
head.speed(4)
head.shape('square')
head.color('black')
head.penup()
head.goto(0, 0)
head.direction = 'Stop'

#Function
def move():
    if head.direction == 'Up':
        y = head.ycor()
        head.sety(y+20)
    if head.direction == 'Down':
        y = head.ycor()
        head.sety(y-20)
    if head.direction == 'Left':
        x = head.xcor()
        head.setx(x-20)
    if head.direction == 'Right':
        x = head.xcor()
        head.setx(x+20)
def go_up():
    head.direction = 'Up'
def go_down():
    head.direction = 'Down'
def go_left():
    head.direction = 'Left'
def go_right():
    head.direction = 'Right'
    
#Keyboard listen
wn.listen()
wn.onkey(go_up, 'Up')
wn.onkey(go_down, 'Down')
wn.onkey(go_left, 'Left')
wn.onkey(go_right, 'Right')
while True:
    wn.update()
    move()
    time.sleep(delay)
    
wn.mainloop()