from turtle import Turtle, Screen, width
import turtle
import random

# set up field
screen = Screen()
screen.setup(width=800, height=600)
screen.bgpic('J:/Personal Projects/TurtleGame/assets/road.gif')

# global variables
y_position = [-260, -172, -85, 2, 85, 172, 260]
colors = ["white", "red", "blue", "pink", "yellow", "green", "black"]
ALIGN = "right"
FONT = ("Times New Roman", 28, "bold")

#drawing turtles
def draw():
    
    turtles = []    
    for index in range(0, 7):
        tur = Turtle(shape="turtle")
        tur.shapesize(2) # size of turtle shape
        tur.speed('fastest') # speed of drawing turtle shape
        tur.penup() # to remove those drawing lines
        tur.goto(x=-350, y=y_position[index]) #x for moving horizontal and y for moving vertically
        tur.color(colors[index])
        turtles.append(tur) # to address each turtle at a time
        
    return turtles

# play the game
def play():
    
    global screen
    
    shapes_turtles = draw()
    running = True
    user_choice = screen.textinput('Enter your bet:', prompt="Turtle's Color")
    if user_choice.lower() in colors:
        while running:
            for turtle in shapes_turtles:
                if turtle.xcor() > 330:
                    running = False
                    winner = turtle.pencolor()
                    if winner == user_choice:
                        turtle.write(f'You won! {winner} turtle is winner!', font=FONT, align=ALIGN)
                    else:
                        turtle.write(f'You lost! The {winner} turtle is winner!', font=FONT, align=ALIGN)
                random_spd = random.randint(0, 16)
                turtle.forward(random_spd)

def main(): # main execute
    
    process = True
    play()
    prompt_answer = ['yes', 'y', 'yeah', 'yah']
    
    # prompt user for playing again
    while process:
        user_choice = screen.textinput('End Game', prompt="Play Again Y or N: ")
        if user_choice.lower() in prompt_answer:
            screen.reset()
            screen.clear()
            screen.bgpic('J:/Personal Projects/TurtleGame/assets/road.gif')
            play()
            process = True
        else:
            process = False
            screen.reset()
            screen.clear()
            turtle.write(f'<<--See You Soon-->>', font=FONT, align="center")    

if __name__ == "__main__":
    main()
    screen.exitonclick() # to stop the program when we click on the screen