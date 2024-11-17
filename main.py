import os
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import queue
import yt_dlp


def download_and_convert():
    video_url = entry_url.get()
    output_path = r"D:\Programas_Carlos\Converter_Mp3\Descargas"
    progress_queue = queue.Queue()  # Cola para actualizar progreso

    def update_progress():
        """Actualizar la barra de progreso desde la cola"""
        try:
            while True:
                progress = progress_queue.get_nowait()
                progress_var.set(progress)
                root.update_idletasks()
        except queue.Empty:
            root.after(100, update_progress)

    def download_thread():
        try:
            # Crear el directorio de salida si no existe
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Variable para almacenar el nombre del archivo
            downloaded_file_name = None

            # Configuración de yt-dlp
            def on_progress(d):
                """Hook para actualizar progreso"""
                nonlocal downloaded_file_name
                if d['status'] == 'downloading':
                    downloaded_file_name = d.get('filename', downloaded_file_name)
                    try:
                        downloaded = float(d.get('_percent_str', '0.00').replace('%', '').strip())
                        progress_queue.put(downloaded)
                    except ValueError:
                        pass  # Ignorar errores de conversión

            ydl_opts = {
                'format': 'bestaudio/best',  # Descargar solo el mejor audio
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Nombre del archivo
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Extraer el audio
                    'preferredcodec': 'mp3',  # Guardar como MP3
                    'preferredquality': '192',  # Calidad del audio
                }],
                'noprogress': False,  # Activar progreso detallado
                'progress_hooks': [on_progress],  # Hook para actualizar progreso
                'nocolor': True,  # Desactivar códigos de colores ANSI
            }

            # Descargar el video/audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            messagebox.showinfo("Éxito", "Descarga y conversión completadas")

            update_treeview(downloaded_file_name, "Descargado")
            progress_var.set(0)  # Reinicia la barra de progreso

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    # Ejecutar la descarga en un hilo separado
    threading.Thread(target=download_thread).start()
    update_progress()  # Inicia el bucle de progreso


def update_treeview(filename, status):
    """Agrega una entrada al Treeview con el nombre del archivo y el estado"""
    file_name = os.path.basename(filename) if filename else "Desconocido"
    treeview.insert("", "end", values=(file_name, status))


# Crear ventana principal
root = tk.Tk()
root.title("Descargador de audio MP3 desde YouTube")

# Ajustar tamaño de la ventana
root.geometry("1000x550")
root.configure(bg="#BEC8C9")

# Crear elementos de la interfaz
label_url = tk.Label(root, text="Introduce el enlace del video:", font=("Arial", 20), bg="#BEC8C9")
label_url.pack(pady=20)

entry_url = tk.Entry(root, width=50, font=("Arial", 16))
entry_url.pack(pady=10)

button_download = tk.Button(root, text="Descargar y Convertir", command=download_and_convert, font=("Arial", 20))
button_download.pack(pady=20)

# Configurar el estilo de la barra de progreso con color verde
style = ttk.Style(root)
style.theme_use('default')
style.configure(
    "TProgressbar",
    thickness=30,
    troughcolor="white",  # Color del fondo de la barra
    background="green"    # Color de la barra de progreso
)

# Crear barra de progreso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=500, style="TProgressbar")
progress_bar.pack(pady=20, padx=20)

# Crear Treeview
treeview = ttk.Treeview(root, columns=("Name", "Status"), height=10, show="headings")
treeview.heading("Name", text="Nombre del archivo")
treeview.heading("Status", text="Estado")
treeview.pack(pady=20)

# Ejecutar el bucle principal de la ventana
root.mainloop()
