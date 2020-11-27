from tkinter import Tk, Canvas
from random import randint

# Globals
Game_speed = 75
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True
IS_WIN = False

# Helper functions

def create_apple():
    # Creates an apple to be eaten
    global apple
    posx = SEG_SIZE * randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    apple = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="#ff8243")


def main():
    #Handles game process
    global IN_GAME, IS_WIN, Game_speed
    if IN_GAME:
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Win condition
        if len(s.segments)-3 > 999:
            IS_WIN = True
            IN_GAME = False
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
            c.delete(score)
        # Eating apples
        elif head_coords == c.coords(apple):
            #for i in range(1000):
            s.add_segment()
            c.itemconfigure(score, text="{score}".format(score = len(s.segments)-3))
            c.delete(apple)
            create_apple()
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
                    c.delete(score)
        root.after(int(Game_speed-(len(s.segments)-2)/10), main)
    # IS_WIN -> stop game and print congratulations
    elif IS_WIN:
        set_state(win_text, 'normal')
        set_state(restart_text, 'normal')
    # Not IN_GAME -> stop game and print message
    else:
        c.itemconfigure(score_text,text="Your score is {score}".format(score=len(s.segments)-3))
        set_state(restart_text, 'normal')
        set_state(score_text, 'normal')
        set_state(game_over_text, 'normal')


class Segment(object):
    """ Single snake segment """
    def __init__(self, x, y, color="yellow"):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill=str(color))


class Snake(object):
    #Simple Snake class
    def __init__(self, segments):
        self.seg_cnt=3;
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = (self.mapping["Right"])
        self.last_key = "Right"
    def move(self):
        #Moves the snake with the specified vector
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        #Adds segment to the snake
        for i in range(1):
            self.seg_cnt = self.seg_cnt + 1
            last_seg = c.coords(self.segments[0].instance)
            x = last_seg[2] - SEG_SIZE
            y = last_seg[3] - SEG_SIZE
            self.segments.insert(0, Segment(x, y, "#00cc85"))

    def change_direction(self, event):
        #Changes direction of snake
        if event.keysym in self.mapping:
            if event.keysym == "Up" and self.last_key != "Down" and self.last_key != "Up":
                self.vector = self.mapping[event.keysym]
            if event.keysym == "Down" and self.last_key != "Up" and self.last_key != "Down":
                self.vector = self.mapping[event.keysym]
            if event.keysym == "Left" and self.last_key != "Right" and self.last_key != "Left":
                self.vector = self.mapping[event.keysym]
            if event.keysym == "Right" and self.last_key != "Left" and self.last_key != "Right":
                self.vector = self.mapping[event.keysym]
            self.last_key = str(event.keysym)
    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    if event.keysym == "space":
        global IN_GAME
        global IS_WIN
        global Game_speed
        Game_speed = 75
        s.reset_snake()
        IN_GAME = True
        IS_WIN = False
        c.delete(apple)
        c.itemconfigure(win_text, state='hidden')
        c.itemconfigure(restart_text, state='hidden')
        c.itemconfigure(score_text, state='hidden')
        c.itemconfigure(game_over_text, state='hidden')
        c.delete(score)
        start_game()
    elif event.keysym == "Escape":
        root.destroy()


def start_game():
    global s
    create_apple()
    s = create_snake()
    global score;
    score = c.create_text(WIDTH-50, HEIGHT/25, 
                            text=len(s.segments)-3,
                            font='Arial 20',
                            fill='black')
    # Reaction on keypress
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(SEG_SIZE, SEG_SIZE,"#00cc85"),
                Segment(SEG_SIZE*2, SEG_SIZE, "#00cc85"),
                Segment(SEG_SIZE*3, SEG_SIZE,"#009b76")]
    return Snake(segments)


# Setting up window
root = Tk()
root.title("Snake_Game")
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#71bc66")
c.grid()

# catch keypressing
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/2-75,
                            text="GAME OVER!",
                            font='Arial 50',
                            fill='red',
                            state='hidden')
score_text = c.create_text(WIDTH/2, HEIGHT/2+15,
                            text="Your score is: 0",
                            font='Arial 30',
                            fill='white',
                            state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                            font='Arial 30',
                            fill='white',
                            text="Press space to restart or escape to exit",
                            state='hidden')
win_text = c.create_text(WIDTH/2, HEIGHT/2,
                            font='Arial 50',
                            fill='red',
                            text="YOU IS_WIN!!!",
                            state='hidden')

root.bind_all("<KeyPress>", clicked)
start_game()
root.mainloop()