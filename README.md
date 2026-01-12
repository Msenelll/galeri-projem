# 🎬 Video & Ses Düzenleme Aracı

Python tabanlı, GUI destekli video ve ses düzenleme aracı.

## ✨ Özellikler

- 📁 **Multiple Dosya Seçimi**: Birden fazla dosyayı aynı anda seçin
- 🔗 **Video Birleştirme**: Birden fazla videoyu tek bir videoda birleştirin
- 🎵 **Ses Birleştirme**: Ses dosyalarını birleştirin
- ✂️ **Video Kesme**: Videoları istediğiniz sürede kesin
- ✂️🎵 **Ses Kesme**: Ses dosyalarını istediğiniz sürede kesin
- 🔇 **Ses Çıkarma**: Videolardan ses dosyası çıkarın
- 🔊 **Ses Seviyesi Ayarlama**: Ses seviyesini artırın veya azaltın
- 🔄 **Format Dönüştürme**: Video ve ses formatları arasında dönüşüm yapın
- 🎬 **Ses + Video Birleştirme**: Ayrı ses ve video dosyalarını birleştirin

## 📦 Desteklenen Formatlar

### Video Formatları
- MP4, AVI, MOV, MKV, WEBM, FLV

### Ses Formatları
- MP3, WAV, FLAC, AAC, M4A, OGG

## 🚀 Kurulum

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Programı çalıştırın:
```bash
python video_editor.py
```

## 📖 Kullanım

1. **Dosya Seç** butonuna tıklayın
2. İstediğiniz dosyaları seçin (Ctrl tuşu ile multiple seçim)
3. Yapmak istediğiniz işlemi seçin
4. İşlem tamamlandığında dosyayı kaydedin

## 🛠️ Teknolojiler

- **Python 3.x**
- **MoviePy**: Video/ses işleme
- **Tkinter**: GUI arayüzü
- **FFmpeg**: Video codec desteği (otomatik indirilir)

## 📝 Notlar

- İlk çalıştırmada FFmpeg otomatik olarak indirilecektir
- Büyük dosyalarda işlem süresi uzun olabilir
- İşlem sırasında program donmuş gibi görünebilir, lütfen bekleyin

## 🎯 Örnek İşlemler

### Video Birleştirme
1. 2 veya daha fazla video seçin
2. "Video Birleştir" butonuna tıklayın
3. Çıktı dosyası adını belirleyin

### Video Kesme
1. Bir video seçin
2. "Video Kes" butonuna tıklayın
3. Başlangıç ve bitiş sürelerini girin (saniye cinsinden)

### Ses Çıkarma
1. Bir video seçin
2. "Ses Çıkar" butonuna tıklayın
3. MP3 dosyası olarak kaydedin

### Ses Kesme
1. Bir ses dosyası seçin
2. "Ses Kes" butonuna tıklayın
3. Başlangıç ve bitiş sürelerini girin (saniye cinsinden)
4. MP3 dosyası olarak kaydedin

## 📄 Lisans

Bu proje açık kaynaklıdır ve özgürce kullanılabilir.
