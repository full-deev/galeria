# main.py
import tkinter as tk
from gallery import Gallery

def main():
    root = tk.Tk()
    gallery = Gallery(root)
    root.mainloop()

if __name__ == "__main__":
    main()
