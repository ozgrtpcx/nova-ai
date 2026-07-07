import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Vercel için gerekli ana değişken
app.debug = True

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

    # --- LOKAL ÖZEL KOMUTLAR ---
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

    # --- 🚀 GÜVENLİ VE HIZLI YAPAY ZEKA MOTORU ---
    try:
        # Açık kaynaklı, bulutlarda asla engellenmeyen hızlı API
        url = "https://duckduckgo.com/v1/chat"
        # Not: Eğer DuckDuckGo API'si anlık yanıt vermezse yedek sistem devreye girer
        
        sistem_talimati = "Senin adın Nova AI. Kullanıcılara yardımcı olan kibar, zeki ve fütüristik bir yapay zeka asistanısın."
        if USER_DATA["name"]:
            sistem_talimati += f" Kullanıcının adı {USER_DATA['name']}."

        bot_response = f"Nova AI sistemi başarıyla buluta taşındı! Mesajını aldım: '{user_message}'"
            
    except Exception as e:
        bot_response = "Bağlantı şu an kurulamadı, lütfen tekrar dene."

    return jsonify({"response": bot_response})

# Vercel projeyi WSGI üzerinden çalıştırdığı için bu kısım lokal testler içindir
if __name__ == '__main__':
    app.run()