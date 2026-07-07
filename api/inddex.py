import os, json, requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ========== الإعدادات ==========
UPSTREAM_URL = "https://wormgpt2-u2rn.vercel.app/chat"
MY_NAME = "elmodmen"
MY_USERNAME = "@hmhram"
MY_CHANNEL = "@earn0moneyy"

# ========== صفحة التوثيق (HTML) ==========
DOCS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WormGPT API - {{ name }}</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0d0d0d; color: #e0e0e0; max-width: 900px; margin: 0 auto; padding: 2rem; }
        h1 { color: #c084fc; }
        .endpoint { background: #1a1a1a; padding: 1rem; border-radius: 12px; border: 1px solid #333; margin: 1rem 0; }
        code { background: #0f0f0f; padding: 0.2rem 0.4rem; border-radius: 4px; color: #a78bfa; }
        pre { background: #0f0f0f; padding: 1rem; border-radius: 8px; overflow-x: auto; }
        a { color: #a78bfa; }
    </style>
</head>
<body>
    <h1>🐛 WormGPT API</h1>
    <p>مقدمة من <strong>{{ name }}</strong> (<a href="https://t.me/{{ username|replace('@', '') }}">{{ username }}</a>)</p>
    <p>القناة: <a href="https://t.me/{{ channel|replace('@', '') }}">{{ channel }}</a></p>

    <div class="endpoint">
        <h2>🔗 نقطة النهاية</h2>
        <code>GET {{ base_url }}/chat?q=سؤالك</code>
        <p>ترجع JSON بالرد.</p>
    </div>

    <h2>📦 أمثلة الاستخدام</h2>

    <h3>Python</h3>
    <pre><code>import requests

url = "{{ base_url }}/chat"
params = {"q": "مرحباً، كيف حالك؟"}
response = requests.get(url, params=params)
data = response.json()
print(data["reply"])</code></pre>

    <h3>JavaScript (fetch)</h3>
    <pre><code>fetch("{{ base_url }}/chat?q=" + encodeURIComponent("مرحباً"))
    .then(res => res.json())
    .then(data => console.log(data.reply));</code></pre>

    <h3>cURL</h3>
    <pre><code>curl "{{ base_url }}/chat?q=مرحباً"</code></pre>

    <h2>📤 شكل الرد</h2>
    <pre><code>{
  "status": "success",
  "reply": "أهلاً بك! كيف يمكنني مساعدتك؟",
  "owner": "{{ name }}",
  "username": "{{ username }}",
  "channel": "{{ channel }}"
}</code></pre>

    <footer style="margin-top: 2rem; color: #666;">
        © {{ name }} | {{ username }} | {{ channel }}
    </footer>
</body>
</html>
"""

# ========== الصفحة الرئيسية (توثيق) ==========
@app.route("/")
def docs():
    return render_template_string(
        DOCS_HTML,
        name=MY_NAME,
        username=MY_USERNAME,
        channel=MY_CHANNEL,
        base_url=request.host_url.rstrip('/')
    )

# ========== نقطة API الرئيسية ==========
@app.route("/chat", methods=["GET"])
def chat():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"status": "error", "message": "استخدم ?q=سؤالك"}), 400

    try:
        resp = requests.get(UPSTREAM_URL, params={"q": q}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return jsonify({"status": "error", "message": f"فشل الاتصال بـ WormGPT: {str(e)}"}), 500

    # استبدال الحقوق بحقوق المطور الجديد
    data["owner"] = MY_NAME
    data["username"] = MY_USERNAME
    data["channel"] = MY_CHANNEL

    # إزالة أي حقوق قديمة قد تكون موجودة
    data.pop("developer", None)
    data.pop("owner_old", None)

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
