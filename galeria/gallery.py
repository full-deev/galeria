from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class Photo:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail((150, 150)) # Tamaño de mi imagen

class Tag: # Puedo realizar un filtro por tag
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
        self.tags.append(tag) # Uso las propiedades de mi lista

class Gallery:
    def __init__(self, root):
        self.root = root
        self.root.title("Galeria de fotos By.milo")
        self.current_album = None

        # Creo opciones tipo Cinta - Ribbon
        self.ribbon = tk.Frame(root, bg="gray", height=40)
        self.ribbon.pack(side=tk.TOP, fill=tk.X)

        # Botones dentro de mi cinta ribbon
        self.add_album_button = tk.Button(
            self.ribbon, text="Nuevo Album", command=self.add_album
        )
        self.add_album_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_photo_button = tk.Button(
            self.ribbon, text="Subir Fotos", command=self.load_photo
        )
        self.load_photo_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.exit_button = tk.Button(
            self.ribbon, text="Salir", command=self.root.quit  # Salir
        )
        self.exit_button.pack(side=tk.RIGHT,padx=5, pady=5)

        # Creando widgets contenedores
        self.album_listbox = tk.Listbox(root)
        self.album_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.photo_canvas = tk.Canvas(root, bg="gray")
        self.photo_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Lista de álbumes
        self.albums = {}

        self.album_listbox.bind('<<ListboxSelect>>', self.load_album)

        # Lista para guardar una imagen luego de subir 
        self.imagen_refs = []

    def add_album(self):
        album_name = simpledialog.askstring("Nombre del álbum", "Ingrese el nombre del álbum:")
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
            messagebox.showwarning("No hay álbum", "Por favor agregue un nuevo álbum primero")
            return
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagen files", "*.jpg;*.jpeg;*.png")] # Extensiones permitidas
        )
        if file_path:
            photo = Photo(file_path)
            self.current_album.add_photo(photo)
            self.show_photos()

    def show_photos(self):
        if not self.current_album:
            return

        # Este linea me permite que cada
        # que creo un nuevo album
        # no ver la imagen de otro album
        self.photo_canvas.delete("all") 

        # Dimensiones del cuadro
        canvas_width = self.photo_canvas.winfo_width()
        canvas_height = self.photo_canvas.winfo_height()

        # Tamaño de las imagens y margen
        thumbnail_size = 150
        margin = 10

        # Conocer el número de columnas
        columns = (canvas_width - margin) // (thumbnail_size + margin)

        # Resetear limpiar las imagenes antiguas 
        self.imagen_refs.clear()

        # Mostrar imagenes en pequeñas
        for i, photo in enumerate(self.current_album.photos):
            row = i // columns
            column = i % columns

            x = margin + column * (thumbnail_size + margin)
            y = margin + row * (thumbnail_size + margin)

            thumbnail = ImageTk.PhotoImage(photo.thumbnail)
            self.photo_canvas.create_image(x, y, anchor=tk.NW, image=thumbnail)
            self.imagen_refs.append(thumbnail) # Guardar mi referencia de la imagen
            #self.photo_canvas.image = thumbnail