"""
Video ve Ses Düzenleme Aracı
Desteklenen Formatlar: mp4, avi, mov, mkv, mp3, wav, flac, aac, m4a
"""

import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    # MoviePy 2.x için import
    from moviepy import (
        VideoFileClip, 
        AudioFileClip, 
        concatenate_videoclips, 
        concatenate_audioclips
    )
except ImportError:
    try:
        # MoviePy 1.x için fallback
        from moviepy.editor import (
            VideoFileClip, 
            AudioFileClip, 
            concatenate_videoclips, 
            concatenate_audioclips
        )
    except ImportError as e:
        print(f"MoviePy import hatası: {e}")
        print("Lütfen 'pip install moviepy' komutunu çalıştırın.")
        sys.exit(1)


class MediaEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video & Ses Düzenleme Aracı")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")
        
        self.selected_files = []
        self.output_path = ""
        
        # Desteklenen formatlar
        self.video_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
        self.audio_formats = ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']
        
        self.setup_ui()
    
    def setup_ui(self):
        # Başlık
        title = tk.Label(
            self.root, 
            text="🎬 Video & Ses Düzenleme Aracı", 
            font=("Segoe UI", 20, "bold"),
            bg="#1e1e1e", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # Dosya Seçim Butonu
        btn_select = tk.Button(
            self.root,
            text="📁 Dosya Seç (Multiple)",
            font=("Segoe UI", 12),
            bg="#007acc",
            fg="white",
            padx=20,
            pady=10,
            command=self.select_files,
            cursor="hand2"
        )
        btn_select.pack(pady=10)
        
        # Seçilen dosyalar listesi
        self.file_listbox = tk.Listbox(
            self.root,
            font=("Consolas", 10),
            bg="#252526",
            fg="#d4d4d4",
            selectbackground="#094771",
            height=8
        )
        self.file_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # İşlem seçim paneli
        operations_frame = tk.LabelFrame(
            self.root,
            text="İşlem Seç",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e1e",
            fg="#ffffff",
            padx=10,
            pady=10
        )
        operations_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        # İşlem butonları
        operations = [
            ("🔗 Video Birleştir", self.merge_videos),
            ("🎵 Ses Birleştir", self.merge_audios),
            ("✂️ Video Kes", self.trim_video),
            ("✂️🎵 Ses Kes", self.trim_audio),
            ("🔇 Ses Çıkar (Video → Audio)", self.extract_audio),
            ("🔊 Ses Seviyesi Ayarla", self.adjust_volume),
            ("🔄 Format Dönüştür", self.convert_format),
            ("🎬 Ses + Video Birleştir", self.combine_audio_video)
        ]
        
        btn_row = 0
        btn_col = 0
        for text, command in operations:
            btn = tk.Button(
                operations_frame,
                text=text,
                font=("Segoe UI", 10),
                bg="#323233",
                fg="white",
                padx=15,
                pady=8,
                command=command,
                cursor="hand2"
            )
            btn.grid(row=btn_row, column=btn_col, padx=5, pady=5, sticky="ew")
            btn_col += 1
            if btn_col > 1:
                btn_col = 0
                btn_row += 1
        
        # Grid ayarları
        operations_frame.grid_columnconfigure(0, weight=1)
        operations_frame.grid_columnconfigure(1, weight=1)
    
    def select_files(self):
        """Kullanıcıdan dosyaları seç"""
        filetypes = [
            ("Tüm Medya Dosyaları", "*.mp4 *.avi *.mov *.mkv *.mp3 *.wav *.flac *.aac *.m4a"),
            ("Video Dosyaları", "*.mp4 *.avi *.mov *.mkv *.webm"),
            ("Ses Dosyaları", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg"),
            ("Tüm Dosyalar", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Dosya Seçin (Multiple seçim için Ctrl tuşunu kullanın)",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
    
    def update_file_list(self):
        """Seçilen dosyaları listede göster"""
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = Path(file).name
            self.file_listbox.insert(tk.END, f"✓ {filename}")
    
    def get_output_path(self, default_name, extension):
        """Çıktı dosyası için yol al"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=extension,
            initialfile=default_name,
            filetypes=[("Output", f"*{extension}"), ("Tüm Dosyalar", "*.*")]
        )
        return filepath
    
    def merge_videos(self):
        """Birden fazla videoyu birleştir"""
        if len(self.selected_files) < 2:
            messagebox.showwarning("Uyarı", "En az 2 video dosyası seçmelisiniz!")
            return
        
        try:
            output = self.get_output_path("merged_video", ".mp4")
            if not output:
                return
            
            clips = [VideoFileClip(f) for f in self.selected_files]
            final = concatenate_videoclips(clips, method="compose")
            final.write_videofile(output, codec="libx264", audio_codec="aac")
            
            # Temizlik
            for clip in clips:
                clip.close()
            final.close()
            
            messagebox.showinfo("Başarılı", f"Video birleştirildi:\n{output}")
        except Exception as e:
            messagebox.showerror("Hata", f"Video birleştirilemedi:\n{str(e)}")
    
    def merge_audios(self):
        """Birden fazla sesi birleştir"""
        if len(self.selected_files) < 2:
            messagebox.showwarning("Uyarı", "En az 2 ses dosyası seçmelisiniz!")
            return
        
        try:
            output = self.get_output_path("merged_audio", ".mp3")
            if not output:
                return
            
            clips = [AudioFileClip(f) for f in self.selected_files]
            final = concatenate_audioclips(clips)
            final.write_audiofile(output)
            
            # Temizlik
            for clip in clips:
                clip.close()
            final.close()
            
            messagebox.showinfo("Başarılı", f"Ses birleştirildi:\n{output}")
        except Exception as e:
            messagebox.showerror("Hata", f"Ses birleştirilemedi:\n{str(e)}")
    
    def trim_video(self):
        """Video kesme işlemi"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Dosya seçmelisiniz!")
            return
        
        # Kullanıcıdan süre al
        dialog = tk.Toplevel(self.root)
        dialog.title("Video Kes")
        dialog.geometry("300x200")
        dialog.configure(bg="#1e1e1e")
        
        tk.Label(dialog, text="Başlangıç (saniye):", bg="#1e1e1e", fg="white").pack(pady=5)
        entry_start = tk.Entry(dialog)
        entry_start.pack(pady=5)
        entry_start.insert(0, "0")
        
        tk.Label(dialog, text="Bitiş (saniye):", bg="#1e1e1e", fg="white").pack(pady=5)
        entry_end = tk.Entry(dialog)
        entry_end.pack(pady=5)
        entry_end.insert(0, "10")
        
        def process_trim():
            try:
                start = float(entry_start.get())
                end = float(entry_end.get())
                
                output = self.get_output_path("trimmed_video", ".mp4")
                if not output:
                    return
                
                clip = VideoFileClip(self.selected_files[0])
                trimmed = clip.subclip(start, end)
                trimmed.write_videofile(output, codec="libx264", audio_codec="aac")
                
                clip.close()
                trimmed.close()
                dialog.destroy()
                
                messagebox.showinfo("Başarılı", f"Video kesildi:\n{output}")
            except Exception as e:
                messagebox.showerror("Hata", f"Video kesilemedi:\n{str(e)}")
        
        tk.Button(dialog, text="Kes", command=process_trim, bg="#007acc", fg="white").pack(pady=10)
    
    def trim_audio(self):
        """Ses kesme işlemi"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Ses dosyası seçmelisiniz!")
            return
        
        # Kullanıcıdan süre al
        dialog = tk.Toplevel(self.root)
        dialog.title("Ses Kes")
        dialog.geometry("300x200")
        dialog.configure(bg="#1e1e1e")
        
        tk.Label(dialog, text="Başlangıç (saniye):", bg="#1e1e1e", fg="white").pack(pady=5)
        entry_start = tk.Entry(dialog)
        entry_start.pack(pady=5)
        entry_start.insert(0, "0")
        
        tk.Label(dialog, text="Bitiş (saniye):", bg="#1e1e1e", fg="white").pack(pady=5)
        entry_end = tk.Entry(dialog)
        entry_end.pack(pady=5)
        entry_end.insert(0, "10")
        
        def process_trim():
            try:
                start = float(entry_start.get())
                end = float(entry_end.get())
                
                output = self.get_output_path("trimmed_audio", ".mp3")
                if not output:
                    return
                
                clip = AudioFileClip(self.selected_files[0])
                trimmed = clip.subclip(start, end)
                trimmed.write_audiofile(output)
                
                clip.close()
                trimmed.close()
                dialog.destroy()
                
                messagebox.showinfo("Başarılı", f"Ses kesildi:\n{output}")
            except Exception as e:
                messagebox.showerror("Hata", f"Ses kesilemedi:\n{str(e)}")
        
        tk.Button(dialog, text="Kes", command=process_trim, bg="#007acc", fg="white").pack(pady=10)
    
    def extract_audio(self):
        """Videodan sesi çıkar"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Video dosyası seçmelisiniz!")
            return
        
        try:
            output = self.get_output_path("extracted_audio", ".mp3")
            if not output:
                return
            
            video = VideoFileClip(self.selected_files[0])
            audio = video.audio
            audio.write_audiofile(output)
            
            video.close()
            audio.close()
            
            messagebox.showinfo("Başarılı", f"Ses çıkarıldı:\n{output}")
        except Exception as e:
            messagebox.showerror("Hata", f"Ses çıkarılamadı:\n{str(e)}")
    
    def adjust_volume(self):
        """Ses seviyesini ayarla"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Dosya seçmelisiniz!")
            return
        
        # Kullanıcıdan volume faktörü al
        dialog = tk.Toplevel(self.root)
        dialog.title("Ses Seviyesi Ayarla")
        dialog.geometry("300x150")
        dialog.configure(bg="#1e1e1e")
        
        tk.Label(dialog, text="Ses Katı (1.0 = normal, 2.0 = 2x):", bg="#1e1e1e", fg="white").pack(pady=10)
        entry_vol = tk.Entry(dialog)
        entry_vol.pack(pady=5)
        entry_vol.insert(0, "1.5")
        
        def process_volume():
            try:
                factor = float(entry_vol.get())
                
                file_path = self.selected_files[0]
                ext = Path(file_path).suffix
                
                if ext in self.video_formats:
                    output = self.get_output_path("volume_adjusted_video", ".mp4")
                    if not output:
                        return
                    
                    video = VideoFileClip(file_path)
                    adjusted = video.volumex(factor)
                    adjusted.write_videofile(output, codec="libx264", audio_codec="aac")
                    video.close()
                    adjusted.close()
                else:
                    output = self.get_output_path("volume_adjusted_audio", ".mp3")
                    if not output:
                        return
                    
                    audio = AudioFileClip(file_path)
                    adjusted = audio.volumex(factor)
                    adjusted.write_audiofile(output)
                    audio.close()
                    adjusted.close()
                
                dialog.destroy()
                messagebox.showinfo("Başarılı", f"Ses seviyesi ayarlandı:\n{output}")
            except Exception as e:
                messagebox.showerror("Hata", f"Ses ayarlanamadı:\n{str(e)}")
        
        tk.Button(dialog, text="Uygula", command=process_volume, bg="#007acc", fg="white").pack(pady=10)
    
    def convert_format(self):
        """Format dönüştürme"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Dosya seçmelisiniz!")
            return
        
        # Format seçim dialog'u
        dialog = tk.Toplevel(self.root)
        dialog.title("Format Dönüştür")
        dialog.geometry("300x200")
        dialog.configure(bg="#1e1e1e")
        
        tk.Label(dialog, text="Hedef Format Seçin:", bg="#1e1e1e", fg="white").pack(pady=10)
        
        format_var = tk.StringVar(value=".mp4")
        formats = [".mp4", ".avi", ".mov", ".mkv", ".mp3", ".wav", ".flac"]
        
        for fmt in formats:
            tk.Radiobutton(
                dialog, 
                text=fmt, 
                variable=format_var, 
                value=fmt,
                bg="#1e1e1e",
                fg="white",
                selectcolor="#007acc"
            ).pack()
        
        def process_convert():
            try:
                target_format = format_var.get()
                output = self.get_output_path("converted_file", target_format)
                if not output:
                    return
                
                file_path = self.selected_files[0]
                ext = Path(file_path).suffix
                
                if ext in self.video_formats and target_format in self.video_formats:
                    # Video → Video
                    clip = VideoFileClip(file_path)
                    clip.write_videofile(output, codec="libx264", audio_codec="aac")
                    clip.close()
                elif ext in self.video_formats and target_format in self.audio_formats:
                    # Video → Audio
                    video = VideoFileClip(file_path)
                    audio = video.audio
                    audio.write_audiofile(output)
                    video.close()
                    audio.close()
                elif ext in self.audio_formats and target_format in self.audio_formats:
                    # Audio → Audio
                    audio = AudioFileClip(file_path)
                    audio.write_audiofile(output)
                    audio.close()
                else:
                    messagebox.showerror("Hata", "Bu format dönüşümü desteklenmiyor!")
                    return
                
                dialog.destroy()
                messagebox.showinfo("Başarılı", f"Format dönüştürüldü:\n{output}")
            except Exception as e:
                messagebox.showerror("Hata", f"Format dönüştürülemedi:\n{str(e)}")
        
        tk.Button(dialog, text="Dönüştür", command=process_convert, bg="#007acc", fg="white").pack(pady=10)
    
    def combine_audio_video(self):
        """Ses ve videoyu birleştir"""
        if len(self.selected_files) != 2:
            messagebox.showwarning("Uyarı", "1 video ve 1 ses dosyası seçmelisiniz!")
            return
        
        try:
            # Hangi dosya video hangi ses?
            video_file = None
            audio_file = None
            
            for file in self.selected_files:
                ext = Path(file).suffix
                if ext in self.video_formats:
                    video_file = file
                elif ext in self.audio_formats:
                    audio_file = file
            
            if not video_file or not audio_file:
                messagebox.showerror("Hata", "Bir video ve bir ses dosyası seçmelisiniz!")
                return
            
            output = self.get_output_path("combined_video", ".mp4")
            if not output:
                return
            
            video = VideoFileClip(video_file)
            audio = AudioFileClip(audio_file)
            
            final = video.set_audio(audio)
            final.write_videofile(output, codec="libx264", audio_codec="aac")
            
            video.close()
            audio.close()
            final.close()
            
            messagebox.showinfo("Başarılı", f"Video ve ses birleştirildi:\n{output}")
        except Exception as e:
            messagebox.showerror("Hata", f"Birleştirme başarısız:\n{str(e)}")


def main():
    root = tk.Tk()
    app = MediaEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
