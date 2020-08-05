from app import App
import tkinter as tk


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.title('Auto Crawler')
    root.geometry('600x400+700+300')
    root.resizable(False, False)

    root.mainloop()
