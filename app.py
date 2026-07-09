import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
app.debug = True

# 🔑 API anahtarın eksiksiz ve doğrudan koda gömülü durumdadır
GEMINI_API_KEY = "AQ.Ab8RN6KSKrVnTPfjxuhSZmciunYY-d_JlK2gXqOeqLCqV_W2Gg"
genai.configure(api_key=GEMINI_API_KEY)

DATA_FILE = "nova_memory.json"

def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except:
            pass
    return {"name": "Özgür", "role": "Geliştirici"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    user_data = load_user_data()
    
    # 🗓️ Sistem saatini ve gün adını hatasız bir şekilde alıyoruz
    simdiki_zaman = datetime.now()
    tarih_saat_str = simdiki_zaman.strftime("%d.%m.%Y %H:%M:%S")
    
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    bugun_hangi_gun = gunler[simdiki_zaman.weekday()]  # 🛠️ Boşluk hatası düzeltildi!

    # 🤖 Yapay zekanın her zaman gerçekçi ve doğru bilgiyi vermesini sağlayan sistem talimatı
    sistem_talimati = (
        f"Senin adın Nova AI. Kullanıcılara yardımcı olan son derece zeki, "
        f"samimi, gerçekçi ve fütüristik bir yapay zeka asistanısın. Kısa, net ve doğru cevaplar ver. "
        f"Konuştuğun kullanıcının adı {user_data.get('name', 'Özgür')}. Ona ismiyle hitap et. "
        f"KRİTİK GERÇEK ZAMAN BİLGİSİ: Şu anki kesin tarih ve saat: {tarih_saat_str}. Bugün günlerden: {bugun_hangi_gun}. "
        f"Kullanıcı sana saati, tarihi veya günlerden ne olduğunu sorarsa, asla şaşırmadan veya tahminde bulunmadan direkt buradaki net zaman bilgisini temel alarak kesin doğruları söyleyeceksin."
    )

    # Arka planda hiçbir try-except engeli veya hata filtresi olmadan mesajı doğrudan modele aktarıyoruz
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash',
        system_instruction=sistem_talimati
    )
    
    response = model.generate_content(user_message)
    
    return jsonify({"response": response.text.strip()})

if __name__ == '__main__':
    app.run(port=5001)