# gallery.py
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class Photo:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail((150, 150))  # Tamaño de miniatura

class Tag:
    def __init__(self, name):
        self.name = name

class Album:
    def __init__(self, name):
        self.name = name
        self.photos = []
        self.tags = []

    def add_photo(self, photo):
        self.photos.append(photo)

    def add_tag(self, tag):
        self.tags.append(tag)

class Gallery:
    def __init__(self, root):
        self.root = root
        self.root.title("Galería de Fotos")
        self.current_album = None

        # Crear widgets
        self.album_listbox = tk.Listbox(root)
        self.album_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.photo_canvas = tk.Canvas(root)
        self.photo_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones
        self.add_album_button = tk.Button(root, text="Añadir Álbum", command=self.add_album)
        self.add_album_button.pack(side=tk.TOP, fill=tk.X)

        self.load_photo_button = tk.Button(root, text="Cargar Foto", command=self.load_photo)
        self.load_photo_button.pack(side=tk.TOP, fill=tk.X)

        # Lista de álbumes
        self.albums = {}

        self.album_listbox.bind('<<ListboxSelect>>', self.load_album)

    def add_album(self):
        album_name = simpledialog.askstring("Nombre del Álbum", "Ingrese el nombre del álbum:")
        if album_name:
            album = Album(album_name)
            self.albums[album_name] = album
            self.album_listbox.insert(tk.END, album_name)

    def load_album(self, event):
        selection = self.album_listbox.curselection()
        if selection:
            album_name = self.album_listbox.get(selection[0])
            self.current_album = self.albums[album_name]
            self.show_photos()

    def load_photo(self):
        if not self.current_album:
            messagebox.showwarning("No hay Álbum Seleccionado", "Por favor seleccione un álbum primero.")
            return
        
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            photo = Photo(file_path)
            self.current_album.add_photo(photo)
            self.show_photos()

    def show_photos(self):
        if not self.current_album:
            return

        self.photo_canvas.delete("all")

        for i, photo in enumerate(self.current_album.photos):
            thumbnail = ImageTk.PhotoImage(photo.thumbnail)
            self.photo_canvas.create_image((i % 5) * 160 + 80, (i // 5) * 160 + 80, image=thumbnail)
            self.photo_canvas.image = thumbnail
