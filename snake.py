import numpy as np
import tkinter as tk

class Snake(object):
    
    def __init__(self,map):
        """
        Parameters:
        map: instance of the class Map

        Goal:

        Defining the left,right direction and upp/down direction. The position
        of the head and the score of the snake. Also create the first apple
        and the first body part(the head).

        """
        self.direction_ud=0
        self.direction_lr=1
        self.posX=0
        self.posY=0
        self.score=0
        self.body=np.array([[self.posX,self.posY]])
        map.create_body_part(self)
        map.map[self.posY,self.posX]=1
        map.add_apple()


    def move(self,map):

        """
        Parameters:
        map: instance of the class Map

        Goal:
        Restart game if the snake head touch the border of it's body,
        otherwise continue to move while updating the head and tail of the snake
        at each deplacement. Moreover add a body chunk if an apple is eaten.

        Every body part is kept in self.body and the snake on the map
        is kept in map.array
        """

        self.posY+=self.direction_ud
        self.posX+=self.direction_lr
        if(self.posX>=map.number_col or self.posY>=map.number_row or self.posX<0 or self.posY<0):
            lose()
        else:
            map_value=map.map[self.posY,self.posX]
            if(map_value==1):
                lose()
            elif(map_value==0):
                map.map[self.posY,self.posX]=1
                self.body=np.vstack((self.body,[self.posX,self.posY]))
                map.delete_body_part(self)
                map.create_body_part(self)
                map.map[self.body[0,1],self.body[0,0]]=0
                self.body=np.delete(self.body,0,0)
            elif(map_value==2):
                self.score+=1
                map.add_apple()
                map.map[self.posY,self.posX]=1
                self.body=np.vstack((self.body,[self.posX,self.posY]))
                map.create_body_part(self)
                t_canvas.delete("temp_text")
                t_canvas.create_text(300,40,text="current score : "+str(self.score),font=("Helvetica 25 bold"),tags="temp_text")




class Map(object):

    def __init__(self,row,col):
        """
        Parameters:
        row: number of rows wanted for the grid
        col: number of columns wanted for the grid


        Goal:

        Creating an array for the map and a grid of coordinates that translate the 
        indices of our array into cartesion coordinate. Mainly used 
        to render the body part of the snake and the apple.

        In the array different component of the map are represented by number
        0 for nothing
        1 for body part
        2 for apple

        """

        self.number_row=row
        self.number_col=col
        self.map=np.zeros((row,col))
        self.grid_Y=np.linspace(0,600,self.number_row+1)[0:self.number_row]
        self.grid_X=np.linspace(0,600,self.number_col+1)[0:self.number_col]


    def create_body_part(self,snake):
        """
        Parameters:
        snake: instance of the class Snake

        Goal: 
        Update the graphical representation of the snake by adding
        a body part.
        """
        canvas.create_rectangle(self.grid_X[snake.posX],self.grid_Y[snake.posY],self.grid_X[snake.posX]+600/self.number_col,self.grid_Y[snake.posY]+600/self.number_row,fill="blue")

    def delete_body_part(self,snake):  
        """
        Parameters:
        snake: instance of the class Snake

        Goal: 
        Update the graphical representation of the snake by removing
        a body part.

        Note:
        Could be fuse with the above function but I find it clearer this way
        """
        canvas.create_rectangle(self.grid_X[snake.body[0,0]],self.grid_Y[snake.body[0,1]],self.grid_X[snake.body[0,0]]+600/self.number_col,self.grid_Y[snake.body[0,1]]+600/self.number_row,fill="black")

    def add_apple(self):
        """
        Parameters:
        None

        Goal:
        Add an apple. To do that it get all the indices of the non zero components
        of the map array. Then select one at random and put an apple here.
        """
        indice=np.transpose(np.nonzero(self.map.T==0))
        self.rdm_pos=indice[np.random.randint(0,len(indice))]
        self.map[self.rdm_pos[1],self.rdm_pos[0]]=2
        canvas.create_rectangle(self.grid_X[self.rdm_pos[0]],self.grid_Y[self.rdm_pos[1]],self.grid_X[self.rdm_pos[0]]+600/self.number_col,self.grid_Y[self.rdm_pos[1]]+600/self.number_row,fill="red")



def playing():
    snake.move(map)
    root.after(100,playing)

def lose():
    """
    Parameters:
    None

    Goal:
    When the snake does an error the canvas is cleared. And 
    a new instance of snake and map are created as way to set the game back
    to zero.
    """
    global snake
    global map
    canvas.delete("all")
    t_canvas.delete("all")
    map=Map(15,15)
    snake=Snake(map)


def key(event):
    """
    Parameters:
    event: just a keyword for the tkinter event 

    Goal:
    Change the direction of the snake by modifying snake direction_lr/ud.
    The changement is done only if the right key is pressed when the snake
    has the right orientation. For example it cannot go the right if he is going to the left.
    It has to go down or up before.
    """
    key_pressed=event.keysym
    if(key_pressed=="Right" and snake.direction_lr==0):
        snake.direction_lr=1
        snake.direction_ud=0
    if(key_pressed=="Left" and snake.direction_lr==0):
        snake.direction_lr=-1
        snake.direction_ud=0
    if(key_pressed=="Up" and snake.direction_ud==0):
        snake.direction_ud=-1
        snake.direction_lr=0
    if(key_pressed=="Down" and snake.direction_ud==0):
        snake.direction_ud=1
        snake.direction_lr=0

root=tk.Tk()
root.geometry("600x700")

canvas=tk.Canvas(root,width=600,height=600,bg="black")
canvas.pack()
t_canvas=tk.Canvas(root,width=600,height=100,bg="yellow")
t_canvas.pack()

map=Map(15,15)
snake=Snake(map)

root.bind("<Key>",key)
playing()
root.mainloop()