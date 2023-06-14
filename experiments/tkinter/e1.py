import tkinter as tk

root = tk.Tk()

frame1 = tk.Frame(root, bd=5, relief="sunken", background="blue")
frame1.pack(side="left", fill="both", expand=True)

label1 = tk.Label(frame1, text="I'm in Frame 1", background="blue", fg="white")
label1.pack()

frame2 = tk.Frame(root, bd=5, relief="sunken", background="red")
frame2.pack(side="left", fill="both", expand=True)

label2 = tk.Label(frame2, text="I'm in Frame 2", background="red", fg="white")
label2.pack()

root.mainloop()
