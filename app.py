import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from predict import FoodCaloriePredictor
import threading
import os
import sys
import requests
from io import BytesIO

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FoodCalorieApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FoodCalorie AI")
        self.geometry("900x680")
        self.minsize(800, 600)
        self.predictor = FoodCaloriePredictor()
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header, text="🍽  FoodCalorie AI",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Fotoğrafını çek, kalorisini öğren",
            font=ctk.CTkFont(size=13), text_color="gray",
        ).pack(side="left", padx=(12, 0), pady=(6, 0))

        # Ana içerik — sol ve sağ panel
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # ──── SOL PANEL: Görsel Yükleme ────
        left = ctk.CTkFrame(content, corner_radius=12)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        ctk.CTkLabel(left, text="📸 Görsel", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

        # Görsel önizleme
        self.image_frame = ctk.CTkFrame(left, width=360, height=280, corner_radius=8, fg_color=("gray90", "gray17"))
        self.image_frame.pack(padx=15, pady=5)
        self.image_frame.pack_propagate(False)

        self.image_label = ctk.CTkLabel(self.image_frame, text="Görsel buraya yüklenecek\n\n📁 Dosya Seç veya 🔗 URL Gir", text_color="gray")
        self.image_label.pack(expand=True)

        # Butonlar
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(8, 4))

        ctk.CTkButton(btn_frame, text="📁 Dosya Seç", command=self._pick_file, height=36).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(btn_frame, text="📋 Yapıştır", command=self._paste_image, height=36, fg_color="#555", hover_color="#666").pack(side="left", expand=True, fill="x", padx=(4, 0))

        # URL girişi
        url_frame = ctk.CTkFrame(left, fg_color="transparent")
        url_frame.pack(fill="x", padx=15, pady=(4, 8))

        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="Görsel URL'si yapıştırın...", height=36)
        self.url_entry.pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(url_frame, text="🔗", width=44, height=36, command=self._load_url).pack(side="right")

        # ANALİZ BUTONU
        self.analyze_btn = ctk.CTkButton(
            left, text="🔍  Analiz Et", font=ctk.CTkFont(size=15, weight="bold"),
            height=44, command=self._analyze, fg_color="#2563eb", hover_color="#1d4ed8",
        )
        self.analyze_btn.pack(fill="x", padx=15, pady=(4, 15))

        # ──── SAĞ PANEL: Sonuçlar ────
        right = ctk.CTkFrame(content, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        ctk.CTkLabel(right, text="📊 Sonuçlar", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

        self.result_box = ctk.CTkTextbox(right, font=ctk.CTkFont(size=13), state="disabled", wrap="word")
        self.result_box.pack(fill="both", expand=True, padx=12, pady=(5, 12))

        # ──── DURUM ÇUBUĞU ────
        self.status_label = ctk.CTkLabel(self, text="Hazır", font=ctk.CTkFont(size=11), text_color="gray")
        self.status_label.pack(pady=(0, 8))

        # Dahili durum
        self._current_image_path = None

    # ──── Dosya Seçme ────
    def _pick_file(self):
        path = filedialog.askopenfilename(filetypes=[
            ("Görseller", "*.jpg *.jpeg *.png *.webp *.bmp"),
            ("Tüm dosyalar", "*.*"),
        ])
        if path:
            self._load_image(path)

    # ──── URL'den Yükleme ────
    def _load_url(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        self._set_status("URL'den indiriliyor...")
        threading.Thread(target=self._download_url, args=(url,), daemon=True).start()

    def _download_url(self, url):
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            temp_path = os.path.join(os.path.dirname(__file__), "uploads", "temp_url.jpg")
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            img.save(temp_path, "JPEG", quality=95)
            self.after(0, lambda: self._load_image(temp_path))
        except Exception as e:
            self.after(0, lambda: self._set_status(f"❌ URL hatası: {e}"))

    # ──── Panodan Yapıştır ────
    def _paste_image(self):
        try:
            from PIL import ImageGrab
            img = ImageGrab.grabclipboard()
            if img:
                temp_path = os.path.join(os.path.dirname(__file__), "uploads", "temp_paste.jpg")
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                img.convert("RGB").save(temp_path, "JPEG", quality=95)
                self._load_image(temp_path)
            else:
                # Panoda metin (URL) olabilir
                text = self.clipboard_get()
                if text.startswith(("http://", "https://")):
                    self.url_entry.delete(0, "end")
                    self.url_entry.insert(0, text)
                    self._load_url()
                else:
                    self._set_status("⚠ Panoda görsel veya URL bulunamadı")
        except Exception:
            self._set_status("⚠ Panoda görsel bulunamadı")

    # ──── Görseli Yükle & Önizleme ────
    def _load_image(self, path):
        self._current_image_path = path
        try:
            img = Image.open(path).convert("RGB")
            # Önizleme boyutu
            img.thumbnail((350, 270))
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo
            self._set_status(f"✓ Görsel yüklendi: {os.path.basename(path)}")
        except Exception as e:
            self._set_status(f"❌ Görsel açılamadı: {e}")

    # ──── Analiz ────
    def _analyze(self):
        if not self._current_image_path:
            self._set_status("⚠ Önce bir görsel yükleyin")
            return

        self.analyze_btn.configure(state="disabled", text="⏳ Analiz ediliyor...")
        self._set_status("Yapay zeka analiz ediyor...")
        self._clear_results()
        threading.Thread(target=self._run_prediction, daemon=True).start()

    def _run_prediction(self):
        try:
            result = self.predictor.predict(self._current_image_path)
            self.after(0, lambda: self._show_results(result))
        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))

    # ──── Sonuçları Göster ────
    def _show_results(self, r):
        self.analyze_btn.configure(state="normal", text="🔍  Analiz Et")

        if not r.get("is_food", False):
            self._write_result("❌ Görselde yemek tespit edilemedi.")
            self._set_status("Tamamlandı — yemek bulunamadı")
            return

        lines = []
        lines.append(f"🍽  {r['food_name']}  ({r.get('food_name_en', '')})")
        lines.append(f"{'─' * 42}")
        lines.append(f"📝  {r.get('description', '')}")
        lines.append("")
        lines.append(f"📊  Güven        %{r.get('confidence', '?')}")
        lines.append(f"⚖️   Porsiyon     ~{r.get('estimated_portion_grams', '?')}g")
        lines.append(f"🔥  Kalori       {r.get('calories_per_portion', '?')} kcal")
        lines.append("")

        macros = r.get("macros", {})
        lines.append(f"{'─' * 42}")
        lines.append("📊  Besin Değerleri")
        lines.append(f"    Protein      {macros.get('protein_g', '?')}g")
        lines.append(f"    Karbonhidrat {macros.get('carbs_g', '?')}g")
        lines.append(f"    Yağ          {macros.get('fat_g', '?')}g")
        lines.append(f"    Lif          {macros.get('fiber_g', '?')}g")

        alts = r.get("alternatives", [])
        if alts:
            lines.append("")
            lines.append(f"{'─' * 42}")
            lines.append("🔄  Alternatif Tahminler")
            for a in alts:
                lines.append(f"    • {a['food_name']}  (%{a.get('confidence', '?')})")

        notes = r.get("health_notes")
        if notes:
            lines.append("")
            lines.append(f"{'─' * 42}")
            lines.append(f"💡  {notes}")

        self._write_result("\n".join(lines))
        self._set_status(f"✅ {r['food_name']} — {r.get('calories_per_portion', '?')} kcal")

    def _show_error(self, msg):
        self.analyze_btn.configure(state="normal", text="🔍  Analiz Et")
        self._write_result(f"❌ Hata: {msg}")
        self._set_status("Hata oluştu")

    # ──── Yardımcılar ────
    def _write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def _clear_results(self):
        self._write_result("")

    def _set_status(self, text):
        self.status_label.configure(text=text)


if __name__ == "__main__":
    app = FoodCalorieApp()
    app.mainloop()
