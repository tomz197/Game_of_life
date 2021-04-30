from tkinter import *
from math import floor

CanvasW, CanvasH = 400, 400


def rgb(value):
    return "#%02x%02x%02x" % value


def paint(event):
    global numOfElements, elements, grid
    if event.x >= 400 or event.x < 0 or event.y >= 400 or event.y < 0:
        return
    x, y = floor(event.x/40), floor(event.y/40)

    if grid[y*10+x] == 0:
        grid[y*10+x] = 1


def check():
    global grid, newGrid
    for i in range(10):
        for j in range(10):
            x = 0
            # -------------------------------------Check neighbour cells
            if i != 0:
                if grid[(i-1)*10 + j-1] == 1:
                    x += 1
                if grid[(i-1)*10 + j] == 1:
                    x += 1
                if j != 9:
                    if grid[(i-1)*10 + j+1] == 1:
                        x += 1
            if grid[i*10 + j-1] == 1:
                x += 1
            if j != 9:
                if grid[i*10 + j+1] == 1:
                    x += 1
                if i != 9:
                    if grid[(i+1)*10 + j+1] == 1:
                        x += 1
            if i != 9 and j != 0:
                if grid[(i+1)*10 + j-1] == 1:
                    x += 1
            if i != 9:
                if grid[(i+1)*10 + j] == 1:
                    x += 1
            # --------------------------------------Decide to live/die/born
            if x == 2 and grid[i*10+j] == 1:
                newGrid[i*10+j] = 1
            elif x == 3:
                newGrid[i*10+j] = 1
            else:
                newGrid[i*10+j] = 0


def pause():
    global paused, pauseButton
    if paused:
        paused = False
        pauseButton.configure(text="Pause")
    else:
        paused = True
        pauseButton.configure(text="Play")


def reset():
    global grid, newGrid, paused
    grid = [0]*100
    newGrid = [0]*100
    if not paused:
        pause()


def main():
    global speed
    canvas.delete("all")

    if not paused:
        check()

    for i in range(10):
        for j in range(10):
            if not paused:
                grid[i*10+j] = newGrid[i*10+j]
            if grid[i*10+j] != 0:
                canvas.create_rectangle(
                    j*40, i*40, j*40+40, i*40+40, fill=rgb((240, 240, 240)))
    if playSpeed.get() != "":
        if int(playSpeed.get()) != speed:
            speed = int(playSpeed.get())
    if not paused:
        canvas.after(speed, main)
    else:
        canvas.after(10, main)


grid = [0]*100
newGrid = [0]*100
paused = True
window = Tk()
speed = 200
window.configure(bg=rgb((15, 15, 15)), width=400, height=500)
window.title("Simulation")
canvas = Canvas(window, width=CanvasW, height=CanvasH, bg=rgb((30, 30, 30)))
pauseButton = Button(window, text="Play", font="Arial 10 bold", bd=0, width=10,
                     fg=rgb((0, 0, 0)), command=pause)
resetButton = Button(window, text="RESET", font="Arial 10 bold", bd=0, width=10,
                     fg=rgb((0, 0, 0)), command=reset)
playSpeed = Entry(window, width=10, font="Arial 10", bd=0, justify='center')
playSpeed.insert(END, "200")

canvas.grid(row=0, column=0, columnspan=3)
playSpeed.grid(row=1, column=0)
pauseButton.grid(row=1, column=1)
resetButton.grid(row=1, column=2)

main()

canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", paint)

canvas.mainloop()
