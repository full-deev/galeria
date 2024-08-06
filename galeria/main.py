# main.py
import tkinter as tk
from galeria import Galeria

def main():
    root = tk.Tk()
    gallery = Galeria(root)
    root.mainloop()

# Esta condicion me permite ejecutar mi funcion main()
# siempre y cuando se este ejecutando el archivo main.py
# con estop
if __name__ == "__main__":
    main()
