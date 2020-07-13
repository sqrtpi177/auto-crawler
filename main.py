import app
import tkinter as tk


def on_closing():
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = app.App(root)
    root.title('Auto Crawler')
    root.geometry('600x400+700+300')

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
