import turtle
import random

# ---------- НАСТРОЙКИ ----------
WIDTH, HEIGHT = 600, 600
MAX_COORD = 250

BG_COLORS = [
    "black", "navy", "maroon",
    "darkgreen", "midnightblue"
]

PEN_COLORS = [
    "red", "green", "blue", "yellow", "orange",
    "purple", "pink", "cyan", "magenta",
    "gold", "lime", "violet", "turquoise"
]


# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def move_to(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


# ---------- ФИГУРЫ ----------
def parallelogram(t, side):
    for i in range(4):
        t.forward(side)
        t.left(135 if i % 2 == 1 else 45)


def star(t, side):
    for _ in range(8):
        parallelogram(t, side)
        t.left(45)



def plus(t, length):
    for _ in range(8):
        t.forward(length)
        t.backward(length)
        t.left(45)


def spikes(t, length):
    for offset in (length // 2, 3*length // 4):
        t.penup()
        t.forward(offset)
        t.pendown()

        t.left(45)
        t.forward(length // 4)
        t.backward(length // 4)

        t.right(90)
        t.forward(length // 4)
        t.backward(length // 4)

        t.left(45)
        t.penup()
        t.backward(offset)
        t.pendown()


def snowflake(t, size, x, y):
    move_to(t, x, y)
    t.setheading(0)

    star(t, size // 4)
    plus(t, size)

    for i in range(8):
        move_to(t, x, y)
        t.setheading(45 * i)
        spikes(t, size)


# ---------- ОСНОВНАЯ ПРОГРАММА ----------
screen = turtle.Screen()

screen.setup(WIDTH, HEIGHT)
screen.bgcolor(random.choice(BG_COLORS))


n = int(input("Count of snowflakes: "))

placed = []


t = turtle.Turtle()
t.speed(0)
t.pensize(1)
for _ in range(n):
    
    t.color(random.choice(PEN_COLORS))
    size = random.randint(20, 70)

    while True:
        x = random.randint(-MAX_COORD, MAX_COORD)
        y = random.randint(-MAX_COORD, MAX_COORD)

        if all((x - px) ** 2 + (y - py) ** 2 > (size + ps) ** 2
                for px, py, ps in placed):
            break

    placed.append((x, y, size))
    snowflake(t, size, x, y)
    
