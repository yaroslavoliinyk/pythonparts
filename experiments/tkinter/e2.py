import tkinter as tk

root = tk.Tk()

# Creates a 2x2 grid. 
for i in range(2):
    for j in range(2):
        frame = tk.Frame(root, height=100, width=100)
        # The sticky parameter is used to determine how the widget should fill the grid cell. 
        # 'nsew' means the widget will fill the entire cell.
        frame.grid(row=i, column=j, sticky='nsew')

        # Creates a label inside the frame to show which cell it is.
        label = tk.Label(frame, text=f"Row {i+1}\nColumn {j+1}")
        label.place(relx=0.5, rely=0.5, anchor='center')

root.mainloop()
