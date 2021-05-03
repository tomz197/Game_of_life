from tkinter import *
from random import randint
from math import floor

CanvasW, CanvasH = 800, 800
blocksPW = 40


def rgb(value):
    return "#%02x%02x%02x" % value


def paint(event):
    global elements, grid
    if event.x >= CanvasW or event.x < 0 or event.y >= CanvasH or event.y < 0:
        return
    x, y = floor(event.x/20), floor(event.y/20)

    if grid[y*blocksPW+x] == 0:
        grid[y*blocksPW+x] = 1


def delete(event):
    if event.x >= CanvasW or event.x < 0 or event.y >= CanvasH or event.y < 0:
        return
    x, y = floor(event.x/20), floor(event.y/20)
    grid[y*blocksPW+x] = 0


def check():
    global grid, newGrid
    newGrid = [0]*blocksPW*blocksPW
    for y in range(blocksPW):
        for x in range(blocksPW):
            sum = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    col = (x+j+blocksPW) % blocksPW
                    row = (y+i+blocksPW) % blocksPW
                    if grid[row*blocksPW+col] == 1:
                        sum += 1
            sum -= grid[y*blocksPW+x]
            if sum == 3 and grid[y*blocksPW+x] == 0:
                newGrid[y*blocksPW+x] = 1
            elif grid[y*blocksPW+x] == 1 and (sum < 2 or sum > 3):
                newGrid[y*blocksPW+x] = 0
            else:
                newGrid[y*blocksPW+x] = grid[y*blocksPW+x]


def pause():
    global paused, pauseButton
    if paused:
        check()
        paused = False
        pauseButton.configure(text="Pause")
    else:
        paused = True
        pauseButton.configure(text="Play")


def reset():
    global grid, newGrid, paused
    x = blocksPW * blocksPW
    grid = [0]*x
    newGrid = [0]*x
    if not paused:
        pause()


def setRandom():
    global grid, paused
    if not paused:
        pause()
    for i in range(blocksPW):
        for j in range(blocksPW):
            grid[i*blocksPW+j] = randint(0, 1)


def main():
    global speed, grid, newGrid
    canvas.delete("all")

    for i in range(blocksPW):
        for j in range(blocksPW):
            if grid[i*blocksPW+j] != 0:
                canvas.create_rectangle(
                    j*20, i*20, j*20+20, i*20+20, fill=rgb((240, 240, 240)))

    if not paused:
        check()
        grid = newGrid

    if playSpeed.get() != "":
        if int(playSpeed.get()) != speed and int(playSpeed.get()) != 0:
            speed = int(playSpeed.get())
    if not paused:
        canvas.after(speed, main)
    else:
        canvas.after(10, main)


x = blocksPW * blocksPW
grid = [0]*x
newGrid = [0]*x
paused = True
speed = 100

window = Tk()
window.configure(bg=rgb((15, 15, 15)), width=400, height=500)
window.title("Game of life")

canvas = Canvas(window, width=CanvasW, height=CanvasH, bg=rgb((30, 30, 30)))
pauseButton = Button(window, text="Play", font="Arial 10 bold", bd=0, width=10,
                     fg=rgb((0, 0, 0)), command=pause)
resetButton = Button(window, text="RESET", font="Arial 10 bold", bd=0, width=10,
                     fg=rgb((0, 0, 0)), command=reset)
randomButton = Button(window, text="Random", font="Arial 10 bold", bd=0, width=10,
                      fg=rgb((0, 0, 0)), command=setRandom)
playSpeed = Entry(window, width=10, font="Arial 10", bd=0, justify='center')
playSpeed.insert(END, "100")

canvas.grid(row=0, column=0, columnspan=4)
playSpeed.grid(row=1, column=0)
pauseButton.grid(row=1, column=1)
resetButton.grid(row=1, column=2)
randomButton.grid(row=1, column=3)

main()

canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", paint)
canvas.bind("<B3-Motion>", delete)
canvas.bind("<Button-3>", delete)

canvas.mainloop()
