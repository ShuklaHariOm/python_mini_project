import turtle

wn = turtle.Screen()
wn.title("Pong in Python by Drashti Shah")
wn.bgcolor("yellow")
wn.setup(width=500, height=500)
wn.tracer(0)

# Score board
score_a = 0
score_b = 0

# paddle and ball
# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("red")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()  # paddle makes lines alond the path followed.This stops it.
paddle_a.goto(-220, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("red")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()  # paddle makes lines alond the path followed.This stops it.
paddle_b.goto(220, 0)

# ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("blue")
# ball.penup()       #paddle makes lines alond the path followed.This stops it.
ball.goto(0, 0)
ball.dx = 1.5
ball.dy = -2.25

# Pen/Turtle
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()  # we dont need lines to be shown
pen.hideturtle()
pen.goto(0, 200)
pen.write("Player A: -  Player B: - ", align="center", font=("Italic bold", 16))


# Function for movements
# For PaddleA
def paddle_a_up():
    y = paddle_a.ycor()
    y += 35
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 35
    paddle_a.sety(y)


# keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")

wn.listen()
wn.onkeypress(paddle_a_down, "s")


# For PaddleB
def paddle_b_up():
    y = paddle_b.ycor()
    y += 35
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 35
    paddle_b.sety(y)


# keyboard binding
wn.listen()
wn.onkeypress(paddle_b_up, "Up")

wn.listen()
wn.onkeypress(paddle_b_down, "Down")

# Main game loop!!!
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 240:
        ball.sety(240)
        ball.dy *= -1

    if ball.ycor() < -240:
        ball.sety(-240)
        ball.dy *= -1

    if ball.xcor() > 250:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A:{}  Player B:{} ".format(score_a, score_b), align="center", font=("Italic bold", 16))

    if ball.xcor() < -250:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A:{}  Player B:{} ".format(score_a, score_b), align="center", font=("Italic bold", 16))

    # paddle ball bounce
    if ball.xcor() > 200 and ball.ycor() < paddle_b.ycor() + 35 and ball.ycor() > paddle_b.ycor() - 35:
        ball.dx *= -1

    if ball.xcor() < -200 and ball.ycor() < paddle_a.ycor() + 35 and ball.ycor() > paddle_a.ycor() - 35:
        ball.dx *= -1
