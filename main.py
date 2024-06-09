import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
from mutagen.id3 import ID3, APIC, TIT2, TPE1
import tkinter as tk
from tkinter import messagebox

def download_and_convert():
    video_url = entry_url.get()
    output_path = r"D:\Programas_Carlos\Converter_Mp3\Descargas"  # Ruta específica deseada para almacenar las descargas
    
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4').first()
        if not stream:
            raise Exception("No hay streams disponibles para este video.")
        
        filepath = os.path.join(output_path, "video.mp4")
        stream.download(output_path=output_path, filename="video.mp4")
        
        video = VideoFileClip(filepath)
        audio = video.audio
        audio_filename = os.path.join(output_path, "audio.mp3")
        audio.write_audiofile(audio_filename)
        video.close()
        audio.close()
        
        title = yt.title
        artist = yt.author
        
        audio_file = ID3(audio_filename)
        audio_file.add(TIT2(encoding=3, text=title))
        audio_file.add(TPE1(encoding=3, text=artist))
        audio_file.save()
        
        new_audio_filename = os.path.join(output_path, f"{artist} - {title}.mp3")
        os.rename(audio_filename, new_audio_filename)
        
        # Eliminar el archivo MP4 después de la conversión
        os.remove(filepath)
        
        messagebox.showinfo("Información", "Descarga y conversión completadas correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear ventana principal
root = tk.Tk()
root.title("Descargador de audio mp3 desde YouTube")

# Ajustar tamaño de la ventana
root.geometry("1000x550")

# Cambiar el color de fondo de la ventana
root.configure(bg="#BEC8C9")

# Crear elementos de la interfaz
label_url = tk.Label(root, text="Introduce el enlace del video:", font=("Arial", 20), bg="#BEC8C9")
label_url.pack(pady=20)

entry_url = tk.Entry(root, width=50, font=("Arial", 16))
entry_url.pack(pady=10)

button_download = tk.Button(root, text="Descargar y Convertir", command=download_and_convert, font=("Arial", 20))
button_download.pack(pady=20)

# Ejecutar el bucle principal de la ventana
root.mainloop()
