import tkinter as tk

root = tk.Tk()

# Create a button
button = tk.Button(root, text="Button")
# Place the button in the grid
button.grid(row=0, column=0, sticky='e')

root.mainloop()
