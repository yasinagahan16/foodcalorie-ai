from PIL import Image
import json
import os
import sys
import time
import base64
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# Proxy sunucu adresi — Render'a deploy ettikten sonra buraya kendi URL'nizi yazın
API_URL = os.getenv("API_URL", "https://foodcalorie-server.onrender.com")


class FoodCaloriePredictor:
    def __init__(self, api_url: str = None):
        self.api_url = (api_url or API_URL).rstrip("/")
        print("✓ Model hazır\n")

    def predict(self, image_path: str, max_retries: int = 3) -> dict:
        """Görseli proxy sunucuya gönderip analiz ettir"""
        image = Image.open(image_path).convert("RGB")
        image.thumbnail((1024, 1024))

        # Base64'e çevir
        buf = BytesIO()
        image.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    f"{self.api_url}/analyze",
                    json={"image": b64},
                    timeout=120,
                )
                if resp.status_code == 429:
                    wait = (attempt + 1) * 15
                    print(f"⏳ Sunucu meşgul, {wait}s bekleniyor... (deneme {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    print(f"⏳ Sunucuya bağlanılamadı, tekrar deneniyor...")
                    time.sleep(5)
                else:
                    raise RuntimeError("Sunucuya bağlanılamadı. İnternet bağlantınızı kontrol edin.")
        raise RuntimeError("Maksimum deneme sayısına ulaşıldı.")

    def predict_and_display(self, image_path: str) -> dict:
        """Tahmin yap ve terminale güzel yazdır"""
        print(f"🖼  Görsel analiz ediliyor: {image_path}\n")
        
        result = self.predict(image_path)

        if not result.get("is_food", False):
            print("❌ Görselde yemek tespit edilemedi.")
            return result

        print(f"🍽  Yemek     : {result['food_name']} ({result['food_name_en']})")
        print(f"📝 Açıklama  : {result['description']}")
        print(f"📊 Güven     : %{result['confidence']}")
        print(f"⚖️  Porsiyon  : ~{result['estimated_portion_grams']}g")
        print(f"🔥 Kalori    : {result['calories_per_portion']} kcal")
        print()

        macros = result.get("macros", {})
        print("📊 Besin Değerleri:")
        print(f"   Protein : {macros.get('protein_g', '?')}g")
        print(f"   Karb.   : {macros.get('carbs_g', '?')}g")
        print(f"   Yağ     : {macros.get('fat_g', '?')}g")
        print(f"   Lif     : {macros.get('fiber_g', '?')}g")
        print()

        alts = result.get("alternatives", [])
        if alts:
            print("🔄 Alternatif Tahminler:")
            for a in alts:
                print(f"   - {a['food_name']} (%{a['confidence']})")
        
        if result.get("health_notes"):
            print(f"\n💡 {result['health_notes']}")

        return result


def main():
    if len(sys.argv) < 2:
        print("Kullanım: python predict.py <görsel_yolu>")
        print("Örnek:    python predict.py yemek.jpg")
        return

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"❌ Dosya bulunamadı: {image_path}")
        return

    predictor = FoodCaloriePredictor()
    result = predictor.predict_and_display(image_path)

    # Sonuçları JSON'a kaydet
    output_file = os.path.splitext(image_path)[0] + "_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Sonuçlar kaydedildi: {output_file}")


if __name__ == "__main__":
    main()
