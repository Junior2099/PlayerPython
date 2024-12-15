import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import subprocess
import threading

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("400x350")
        self.root.config(bg="#2E2E2E")
        self.root.resizable(False, False)

        # Inicializar o mixer do pygame
        mixer.init()

        # Variáveis
        self.file_path = None
        self.is_playing = False
        self.total_length = 0

        # Labels e Widgets
        self.label = tk.Label(self.root, text="Selecione um arquivo", font=("Arial", 14), fg="white", bg="#2E2E2E")
        self.label.pack(pady=20)

        self.play_button = tk.Button(self.root, text="Play", font=("Arial", 12), command=self.toggle_play, width=10)
        self.play_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", font=("Arial", 12), command=self.stop, width=10)
        self.stop_button.pack(pady=5)

        self.volume_label = tk.Label(self.root, text="Volume", font=("Arial", 12), fg="white", bg="#2E2E2E")
        self.volume_label.pack(pady=5)

        self.volume_scale = tk.Scale(self.root, from_=0, to=1, orient="horizontal", resolution=0.01, command=self.adjust_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load", font=("Arial", 12), command=self.open_file, width=10)
        self.load_button.pack(pady=20)

    def open_file(self):
        """Abrir arquivo de áudio (MP3, WAV)"""
        self.file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Áudio", "*.mp3;*.wav;*.ogg;*.flac")])
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            display_name = file_name if len(file_name) <= 30 else file_name[:30] + "..."
            self.label.config(text=display_name)  # Exibe o nome do arquivo ou uma versão truncada

            # Obter o tempo total do áudio
            if self.file_path.lower().endswith(".mp3"):
                audio = MP3(self.file_path)
                self.total_length = audio.info.length
            elif self.file_path.lower().endswith(".wav"):
                audio = self.get_audio_duration(self.file_path)
                self.total_length = audio
            else:
                # Para outros formatos como FLAC, OGG, etc
                self.total_length = self.get_audio_duration(self.file_path)

    def get_audio_duration(self, file_path):
        """Usar FFmpeg para obter a duração do arquivo de áudio"""
        result = subprocess.run(['ffmpeg', '-i', file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = result.stderr.decode('utf-8')
        
        # Procurar a linha que contém a duração
        for line in output.split('\n'):
            if "Duration" in line:
                duration_str = line.split(",")[0].split("Duration:")[1].strip()
                hours, minutes, seconds = duration_str.split(":")
                total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
                return total_seconds
        return 0

    def toggle_play(self):
        """Alternar entre play e pause"""
        if self.is_playing:
            mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            if self.file_path:
                if self.file_path.lower().endswith(".mp3") or self.file_path.lower().endswith(".wav"):
                    mixer.music.load(self.file_path)
                    mixer.music.play()
                else:
                    # Usar FFmpeg para converter e tocar outros formatos em segundo plano
                    threading.Thread(target=self.convert_and_play, args=(self.file_path,)).start()
                self.play_button.config(text="Pause")
        self.is_playing = not self.is_playing

    def convert_and_play(self, file_path):
        """Converter e tocar o áudio em formato WAV"""
        output_wav = "temp.wav"
        # Usar FFmpeg para converter para WAV
        try:
            result = subprocess.run(['ffmpeg', '-i', file_path, '-ar', '44100', '-ac', '2', '-sample_fmt', 's16', output_wav], check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # Se a conversão for bem-sucedida
            mixer.music.load(output_wav)  # Carregar o áudio convertido
            mixer.music.play()
        except subprocess.CalledProcessError as e:
            print("Erro na conversão com FFmpeg:", e.stderr.decode())
            # Exibir uma mensagem de erro para o usuário
            self.label.config(text="Erro na conversão do arquivo!")

    def stop(self):
        """Parar a música"""
        mixer.music.stop()
        self.is_playing = False
        self.play_button.config(text="Play")

    def adjust_volume(self, val):
        """Ajustar o volume"""
        mixer.music.set_volume(float(val))

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Player(root)
    root.mainloop()
