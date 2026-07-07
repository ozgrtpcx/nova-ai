import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Ücretsiz ChatGPT bağlantısı sağlayan kütüphaneyi içeri alıyoruz
import g4f

app = Flask(__name__)

# Hafıza yapımızı koruyoruz
USER_DATA = {
    "name": None,
    "role": "Geliştirici",
    "status": "Çevrim İçi (Ücretsiz ChatGPT Modu)"
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
    bot_response = ""

    # --- ÖNCEKİ ÇEVRİM DIŞI ÖZEL KOMUTLARIMIZI KORUYORUZ ---
    if "benim adım" in msg_lower or "benim ismim" in msg_lower:
        parts = user_message.split()
        if len(parts) > 2:
            extracted_name = " ".join(parts[2:])
            USER_DATA["name"] = extracted_name
            return jsonify({"response": f"Memnun oldum {extracted_name}! Hafızama kaydettim."})
            
    elif "ben kimim" in msg_lower or "profil" in msg_lower:
        if USER_DATA["name"]:
            return jsonify({"response": f"Sen benim geliştiricim olan *{USER_DATA['name']}* kişisisin!"})
        else:
            return jsonify({"response": "Şu an senin kim olduğunu bilmiyorum dostum. 'Benim adım ...' yazabilirsin."})

    elif msg_lower.startswith("topla") or msg_lower.startswith("çarp") or msg_lower.startswith("çıkar") or msg_lower.startswith("böl"):
        # Matematik motoru hızlıca lokalde çalışsın
        try:
            parts = msg_lower.split()
            islem = parts[0]
            sayi1 = float(parts[1])
            sayi2 = float(parts[2])
            if islem == "topla": return jsonify({"response": f"Hesapladım: {sayi1} + {sayi2} = *{sayi1 + sayi2}*"})
            elif islem == "çarp": return jsonify({"response": f"Hesapladım: {sayi1} × {sayi2} = *{sayi1 * sayi2}*"})
        except:
            pass

    # --- 🚀 EĞER ÖZEL KOMUT DEĞİLSE: ÜCRETSİZ CHATGPT'YE BAĞLANIYORUZ ---
    try:
        # Nova AI karakter tanımını mesaja gizlice ekliyoruz
        sistem_talimati = "Senin adın Nova AI. Kullanıcılara yardımcı olan kibar, zeki ve fütüristik bir yapay zeka asistanısın. Kısa ve net cevaplar ver."
        if USER_DATA["name"]:
            sistem_talimati += f" Kullanıcının adı {USER_DATA['name']}, ona ismiyle hitap edebilirsin."

        # g4f üzerinden ücretsiz ChatGPT (gpt-3.5-turbo veya varsayılan model) çağrısı yapıyoruz
        response = g4f.ChatCompletion.create(
            model=g4f.models.default, # En kararlı çalışan ücretsiz ChatGPT modelini otomatik seçer
            messages=[
                {"role": "system", "content": sistem_talimati},
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_response = response
        
    except Exception as e:
        print("ChatGPT Bağlantı Hatası:", str(e))
        bot_response = "Ücretsiz ChatGPT sunucularına şu an bağlanamadım. Lütfen internetini kontrol et veya biraz sonra tekrar dene."

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # host='0.0.0.0' yaparak yerel ağdaki telefonların da bağlanmasını sağlıyoruz
    app.run(host='0.0.0.0', debug=True, port=5000)