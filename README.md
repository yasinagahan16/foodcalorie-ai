# 🍽 FoodCalorie AI

Yemek fotoğrafını yükle, yapay zeka kalorisini söylesin.

Görsel tabanlı yapay zeka modeli kullanarak fotoğraftaki yemeği tanır ve **kalori**, **besin değerleri**, **porsiyon tahmini** gibi detaylı bilgileri saniyeler içinde sunar.

---

## ✨ Neler Yapabilir?

- 🔍 **Yemek Tanıma** — Türk ve dünya mutfağından binlerce yemeği fotoğraftan tanır
- 🔥 **Kalori Tahmini** — Porsiyon bazlı gerçekçi kalori hesabı
- 📊 **Besin Değerleri** — Protein, karbonhidrat, yağ ve lif detayı
- 🔄 **Alternatif Tahminler** — Benzer yemek önerileri ve güven yüzdeleri
- 💡 **Sağlık Notları** — Yemek hakkında kısa beslenme tavsiyeleri
- 🖥 **Masaüstü Uygulama** — Dosya seç, URL yapıştır veya panodan aktar

## 📸 Nasıl Çalışır?

1. Yemek fotoğrafını yükleyin (dosya, URL veya panodan)
2. Yapay zeka görseli analiz eder
3. Yemek adı, kalori, besin değerleri ve porsiyon tahmini gelir

## 🚀 Kurulum

### Hızlı Kurulum (Windows)

1. Repoyu indirin veya klonlayın
2. **`setup.bat`** dosyasına çift tıklayın — gerisini otomatik halleder

### Manuel Kurulum

```bash
git clone https://github.com/yasinagahan16/foodcalorie-ai.git
cd foodcalorie-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 📖 Kullanım

### Masaüstü Uygulama

```
python app.py
```

Açılan pencereden:
- **Dosya Seç** ile bilgisayardan görsel seçin
- **Yapıştır** ile panodaki görseli yapıştırın
- **URL** alanına görsel linki girin
- **Analiz Et** butonuna tıklayın

### Komut Satırı

```
predict.bat yemek.jpg
```

### Örnek Çıktı

```
🍽  Yemek     : İskender Kebap (Iskender Kebab)
📊 Güven     : %98
⚖️  Porsiyon  : ~400g
🔥 Kalori    : 1050 kcal

📊 Besin Değerleri:
   Protein : 55g
   Karb.   : 55g
   Yağ     : 65g
   Lif     : 4g

🔄 Alternatif Tahminler:
   - Porsiyon Döner (%90)
   - Et Döner (%85)

💡 Yüksek protein kaynağı. Porsiyon kontrolü önemlidir.
```

### JSON Yanıt Formatı

Her analiz sonucu aşağıdaki formatta döner:

```json
{
  "food_name": "İskender Kebap",
  "food_name_en": "Iskender Kebab",
  "description": "Döner etinin pide üzerine doğranıp domates sosu ve tereyağı ile servis edildiği geleneksel bir Türk yemeğidir.",
  "estimated_portion_grams": 400,
  "calories_per_portion": 1050,
  "macros": {
    "protein_g": 55,
    "carbs_g": 55,
    "fat_g": 65,
    "fiber_g": 4
  },
  "confidence": 98,
  "is_food": true,
  "alternatives": [
    { "food_name": "Porsiyon Döner", "confidence": 90 },
    { "food_name": "Et Döner", "confidence": 85 }
  ],
  "health_notes": "Yüksek protein kaynağı. Porsiyon kontrolü önemlidir."
}
```

## 🛠 Gereksinimler

- Python 3.10+
- İnternet bağlantısı

## 📝 Lisans

MIT
