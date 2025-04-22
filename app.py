import json
import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

print("""
     .-~~^-.
   .'  O    \\
  (_____,    \\
   `----.     \\
         \\     \\
          \\     \\
           \\     `.             _ _
            \\       ~- _ _ - ~       ~ - .
             \\                              ~-.
              \\                                `.
               \\    /               /       \\    \\
                `. |         }     |         }    \\
                  `|        /      |        /       \\
                   |       /       |       /          \\
                   |      /`- _ _ _|      /.- ~ ^-.     \\
                   |     /         |     /          `.    \\
                   |     |         |     |             -.   ` . _ _ _ _ _ _
                   |_____|         |_____|                ~ . _ _ _ _ _ _ _ >
""")

# Créditos
print("\nFeito por Felipe Martins")
print("GitHub: https://github.com/FelipeMartinsDuarte")

# ───── CONFIGURAÇÃO TELEGRAM ─────
TELEGRAM_TOKEN = 'Coloque_seu_TOKEN_AQUI'
CHAT_ID        = 'Coloque_seu_CHAT_ID_AQUI'
SEEN_FILE      = 'seen.json'
SEEN_LIMIT     = 150
SEEN_KEEP      = 50

# ───── URLS DE BUSCA ─────
SEARCH_URLS = [
    'SuaUrlAqui',
    'SuaUrlAqui',
    'SuaUrlAqui',
    'SuaUrlAqui',
    'SuaUrlAqui',
]

PALAVRAS_JOGO     = ['Seu', 'Conjunto', 'de', 'Palavras']
PALAVRAS_CONJUNTO = ['+ Escreva', '+ aqui', '+ O que tem']

# ───── FUNÇÕES AUXILIARES ─────
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r', encoding='utf-8') as f:
            return list(json.load(f))
    return []

def save_seen(seen):
    if len(seen) > SEEN_LIMIT:
        seen = seen[-SEEN_KEEP:]
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)
    return seen

def send_telegram(msg):
    api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'disable_web_page_preview': True,
        'parse_mode': 'Markdown'
    }
    r = requests.post(api_url, data=payload)
    r.raise_for_status()

# ───── SCRAPER ─────
def scrape_ads(url):
    chrome_options = Options()
    for arg in ['--lang=pt-BR', '--window-size=1920,1080', '--incognito']:
        chrome_options.add_argument(arg)
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    coletados = set()
    itens = []

    anuncios = driver.find_elements(By.CSS_SELECTOR, 'a.olx-ad-card__title-link')
    for anuncio in anuncios:
        try:
            titulo = anuncio.find_element(By.CSS_SELECTOR, 'h2').text.strip()
            titulo_lower = titulo.lower()
            if 'seuproduto' not in titulo_lower and 'seu produto' not in titulo_lower:
                continue

            link = anuncio.get_attribute('href')
            container = anuncio.find_element(By.XPATH, './../..')
            preco = container.find_element(By.CSS_SELECTOR, 'h3.olx-ad-card__price').text.strip()
            preco_float = float(preco.replace('R$', '').replace('.', '').replace(',', '.').strip())

            chave = (titulo, preco_float)
            if chave in coletados:
                continue
            coletados.add(chave)

            if titulo_lower.startswith('seuproduto') or titulo_lower.startswith('seu produto'):
                prioridade = 1
            elif any(p in titulo_lower for p in PALAVRAS_CONJUNTO):
                prioridade = 2
            elif any(p in titulo_lower for p in PALAVRAS_JOGO):
                prioridade = 4
            else:
                prioridade = 3

            itens.append((prioridade, preco_float, titulo, preco, link))
        except:
            continue

    driver.quit()
    return sorted(itens, key=lambda x: (x[0], x[1]))

# ───── FLUXO PRINCIPAL ─────
def main():
    seen = load_seen()
    seen_set = set(seen)
    novos = []

    for url in SEARCH_URLS:
        for _, _, titulo, preco, link in scrape_ads(url):
            if link not in seen_set:
                seen.append(link)
                seen_set.add(link)
                novos.append((titulo, preco, link))

    if novos:
        for titulo, preco, link in novos:
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            msg = (
                "🚨 *Nova Oferta Detectada!*\n"
                f"📅 *Data:* {now.split()[0]}   🕑 *Hora:* {now.split()[1]}\n\n"
                f"*{titulo}*\n"
                f"{preco}\n"
                f"{link}"
            )
            send_telegram(msg)
        seen = save_seen(seen)
        print(f"Enviadas {len(novos)} novas notificações.")
    else:
        print("Nenhum anúncio novo encontrado.")

    print(f"\nQuantidade de Anúncios Encontrados: {len(novos)}")

    print("""
               __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|
    """)

    print("\nFeito por Felipe Martins")
    print("GitHub: https://github.com/FelipeMartinsDuarte")

if __name__ == '__main__':
    main()
