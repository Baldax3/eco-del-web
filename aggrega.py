import feedparser
import os
import requests
import json
from datetime import datetime

FEED_URL = "https://mediaset.it"
OUTPUT_DIR = "content/posts"
API_KEY = os.environ.get("GEMINI_API_KEY")

def chiedi_a_gemini(promt_testo):
    url = f"https://googleapis.com{API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": promt_testo}]}]}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()['candidates']['content']['parts']['text'].strip()
    except:
        return None

def avvia_giornale():
    feed = feedparser.parse(FEED_URL)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for index, entry in enumerate(feed.entries[:5]):
        titolo_originale = entry.title
        descrizione_originale = entry.summary if 'summary' in entry else ""
        link_fonte = entry.link
        
        promt_titolo = f"Riscrivi questo titolo di giornale in modo unico e accattivante, senza virgolette: {titolo_originale}"
        promt_testo = f"Riscrivi questa notizia creando un riassunto giornalistico originale di 4 righe in italiano: {descrizione_originale}"
        
        nuovo_titolo = chiedi_a_gemini(promt_titolo) or titolo_originale
        nuovo_testo = chiedi_a_gemini(promt_testo) or descrizione_originale
        data_corrente = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00")
        
        file_contenuto = f"""---
title: "{nuovo_titolo}"
date: {data_corrente}
draft: true
---

{nuovo_testo}

*Fonte della notizia originale:* [Leggi su ANSA]({link_fonte})
"""
        with open(f"{OUTPUT_DIR}/notizia_{index}.md", "w", encoding="utf-8") as f:
            f.write(file_contenuto)

if __name__ == "__main__":
    avvia_giornale()
