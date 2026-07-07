import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

USER_DATA = {
    "name": None,
    "role": "Geliştirici",
    "status": "Çevrim İçi (Nova AI Bulut Modu)"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global USER_DATA
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "Boş mesaj gönderilemez."}), 400
    
    msg_lower = user_message.lower()

    # --- LOKAL ÖZEL KOMUTLARIMIZ ---
    if "benim adım" in msg_lower or "benim ismim" in msg_lower:
        parts = user_message.split()
        if len(parts) > 2:
            USER_DATA["name"] = " ".join(parts[2:])
            return jsonify({"response": f"Memnun oldum {USER_DATA['name']}! Hafızama kaydettim."})
            
    elif "ben kimim" in msg_lower or "profil" in msg_lower:
        if USER_DATA["name"]:
            return jsonify({"response": f"Sen benim geliştiricim olan *{USER_DATA['name']}* kişisisin!"})
        else:
            return jsonify({"response": "Şu an senin kim olduğunu bilmiyorum dostum. 'Benim adım ...' yazabilirsin."})

    # --- 🚀 BULUT DOSTU ÜCRETSİZ CHATGPT API BAĞLANTI MOTORU ---
    try:
        # Sunucularda takılmayan, açık kaynaklı ücretsiz yapay zeka tüneli
        url = "https://chateverywhere.app/api/chat/"
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        sistem_talimati = "Senin adın Nova AI. Kullanıcılara yardımcı olan kibar, zeki ve fütüristik bir yapay zeka asistanısın. Kısa cevaplar ver."
        if USER_DATA["name"]:
            sistem_talimati += f" Kullanıcının adı {USER_DATA['name']}, ona ismiyle hitap et."

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": sistem_talimati},
                {"role": "user", "content": user_message}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            bot_response = response.text
        else:
            bot_response = "Nova AI şu an yoğun, lütfen tekrar dener misin?"
            
    except Exception as e:
        print("Bağlantı Hatası:", str(e))
        bot_response = "Bağlantı şu an kurulamadı, lütfen internetini kontrol et."

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)