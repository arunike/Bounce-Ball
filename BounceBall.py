## Imports
import tkinter as tkinter
import tkinter.messagebox as mb
import random, time

## Ball class definition
class Ball():
    def __init__(self, canvas, paddle, score, color, init_x = 100, init_y = 100): ## Constructor for Ball class
        ## Initialize the Ball class attributes
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.color = color

        self.id = canvas.create_oval(10, 10, 30, 30, fill = self.color) ## Create the ball
        self.canvas.move(self.id, init_x, init_y) ## Move the ball to the initial position

        starts = [-3, -2, -1, 1, 2, 3] ## List of possible ball speeds

        random.shuffle(starts) ## Shuffle the list

        ## Set the ball speed
        self.x = starts[0]
        self.y = -3

        ## Get the canvas height and width
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    ## Draw method for Ball class
    def draw(self):
        self.canvas.move(self.id, self.x, self.y) ## Move the ball
        position = self.canvas.coords(self.id) ## Get the ball position

        if position[1] <= 0: ## If the ball hits the top of the canvas
            self.y = 3
        if position[3] >= self.canvas_height: ## If the ball hits the bottom of the canvas
            self.hit_bottom = True
        if self.hit_paddle(position) == True: ## If the ball hits the paddle
            self.y = -3
        if position[0] <= 0: ## If the ball hits the left side of the canvas
            self.x = 3
        if position[2] >= self.canvas_width: ## If the ball hits the right side of the canvas
            self.x = -3

    ## Hit paddle method for Ball class
    def hit_paddle(self, position):
        paddle_position = self.canvas.coords(self.paddle.id) ## Get the paddle position
        print ('paddle_position:', paddle_position[0], paddle_position[1], paddle_position[2], paddle_position[3])

        if position[2] >= paddle_position[0] and position[0] <= paddle_position[2]: ## If the ball hits the paddle
            if position[3] >= paddle_position[1] and position[3] <= paddle_position[3]: ## If the ball hits the paddle
                self.x += self.paddle.x
                colors = ['red', 'green']

                random.shuffle(colors) ## Shuffle the list

                ## Set the ball attributes
                self.color = colors[0]
                self.canvas.itemconfig(self.id, fill = colors[0])
                self.score.hit(ball_color = self.color)
                self.canvas.itemconfig(self.paddle.id, fill = self.color)
                self.adjust_paddle(paddle_position)

                return True

        return False

    ## Adjust paddle method for Ball class
    def adjust_paddle(self, paddle_position):
        ## Set the paddle attributes
        paddle_grow_length = 30
        paddle_width = paddle_position[2] - paddle_position[0]

        if self.color == 'red': ## If the ball is red
            if paddle_width > 30: ## If the paddle is greater than 30
                if paddle_position[2] >= self.canvas_width:
                    paddle_position[2] = paddle_position[2] - paddle_grow_length
                else: ## If the paddle is less than 30
                    paddle_position[0] = paddle_position[0] + paddle_grow_length
        elif self.color == 'green': ## If the ball is green
            if paddle_width < 300: ## If the paddle is less than 300
                if paddle_position[2] >= self.canvas_width:
                    paddle_position[0] = paddle_position[0] - paddle_grow_length
                else: ## If the paddle is greater than 300
                    paddle_position[2]=paddle_position[2]+paddle_grow_length

## Paddle class definition
class Paddle: 
    def __init__(self, canvas, color): ## Constructor for Paddle class
        ## Initialize the Paddle class attributes
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.id = canvas.create_rectangle(0, 0, 180, 15, fill = color)
        self.canvas.move(self.id, 200, self.canvas_height * 0.75)
        self.x = 0
        self.started = False
        self.continue_game = False

        ## Bind the paddle to the keyboard
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Enter>', self.continue_game)
        self.canvas.bind_all('<Button-1>', self.start_game)
        self.canvas.bind_all('<space>', self.pause_game)

    ## Turn left method for Paddle class
    def turn_left(self, event):
        position = self.canvas.coords(self.id)

        if position[0] <= 0: ## If the paddle hits the left side of the canvas
            self.x = 0
        else: ## If the paddle does not hit the left side of the canvas
            self.x = -3

    ## Turn right method for Paddle class
    def turn_right(self, event): 
        position = self.canvas.coords(self.id)

        if position[2] >= self.canvas_width: ## If the paddle hits the right side of the canvas
            self.x = 0
        else: ## If the paddle does not hit the right side of the canvas
            self.x = 3

    ## Start game method for Paddle class
    def start_game(self, evt): 
        self.started = True

    ## Pause game method for Paddle class
    def pause_game(self, evt):
        if self.started: ## If the game is started
            self.started = False
        else: ## If the game is not started
            self.started = True

    ## Draw method for Paddle class
    def draw(self): 
        self.canvas.move(self.id, self.x, 0)
        position = self.canvas.coords(self.id)

        if position[0] <= 0: ## If the paddle hits the left side of the canvas
            self.x = 0
        elif position[2] >= self.canvas_width: ## If the paddle hits the right side of the canvas
            self.x = 0

## Score class definition
class Score():
    def __init__(self, canvas, color): ## Constructor for Score class
        ## Initialize the Score class attributes
        self.score = 0
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.id = canvas.create_text(self.canvas_width - 150, 10,text = 'score:0',fill = color, font = (None, 18, "bold"))
        self.note = canvas.create_text(self.canvas_width - 70, 10, text = '--', fill = 'red', font = (None, 18, "bold"))

    ## Hit method for Score class
    def hit(self,ball_color='grey'):
        self.score += 1
        self.canvas.itemconfig(self.id, text = 'score:{}'.format(self.score))

        if ball_color == 'red': ## If the ball is red
            self.canvas.itemconfig(self.note,text='{}-'.format('W'), fill = 'red')
        elif ball_color == 'green': ## If the ball is green
            self.canvas.itemconfig(self.note,text='{}+'.format('W'), fill = 'green')
        else: ## If the ball is grey
            self.canvas.itemconfig(self.note,text='--', fill = 'grey')

## Main function to run the program
def main(): 
    tk = tkinter.Tk() ## Create the main window

    ## Create the quit button
    def callback():
        if mb.askokcancel("Quit", "Do you really wish to quit?"):
            tk.destroy()
            
    tk.protocol("WM_DELETE_WINDOW", callback) ## Bind the quit button to the main window

    ## Initialize the canvas dimensions
    canvas_width = 600
    canvas_hight = 500

    tk.title("Ball Game") ## Set the title of the main window
    tk.wm_attributes("-topmost", 1) ## Set the main window to the topmost

    canvas = tkinter.Canvas(tk, width = canvas_width, height = canvas_hight, bd = 0, highlightthickness = 0, bg = '#FFFFFF') ## Create the canvas
    canvas.pack() ## Pack the canvas

    tk.update() ## Update the main window

    score = Score(canvas, 'red') ## Create the score object
    paddle = Paddle(canvas, "red") ## Create the paddle object
    ball = Ball(canvas,paddle,score, "grey") ## Create the ball object

    game_over_text = canvas.create_text(canvas_width / 2, canvas_hight / 2, text = 'Game over', state = 'hidden', fill = 'red', font = (None, 18, "bold")) ## Create the game over text
    introduce = 'Welcome to Ball Game:\nClick Any Key--Start\nStop--Enter\nContinue-Enter\n' ## Create the game start text
    game_start_text = canvas.create_text(canvas_width / 2, canvas_hight / 2, text = introduce, state = 'normal', fill = 'magenta', font = (None, 18, "bold")) ## Create the game start text

    while True: ## Main loop
        if (ball.hit_bottom == False) and ball.paddle.started: ## If the ball has not hit the bottom of the canvas and the game is started
            canvas.itemconfig(game_start_text, state = 'hidden')
            ball.draw()
            paddle.draw()
        if ball.hit_bottom == True: ## If the ball has hit the bottom of the canvas
            time.sleep(0.1)
            canvas.itemconfig(game_over_text, state = 'normal')

        tk.update_idletasks() ## Update the main window
        tk.update() ## Update the main window

        time.sleep(0.01) ## Sleep for 0.01 seconds

if __name__=='__main__':
    main()