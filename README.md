<p align="center">
  <img src="https://i.imgur.com/4f6GpJ2.png" alt="OLX Bot Logo" height="120"/>
</p>

# 🤖 OLX Bot – Alerta de Ofertas no Telegram

Um bot em **Python + Selenium** que monitora **novos anúncios na OLX** com base em palavras-chave personalizadas e envia **alertas em tempo real para o Telegram**. Ideal para quem quer aproveitar promoções, encontrar itens raros ou automatizar buscas por produtos específicos.

---

### 🚀 Funcionalidades

- 🔍 Busca automática por produtos com base em palavras-chave  
- 🧠 Sistema inteligente de prioridade por relevância  
- 🗃️ Armazena anúncios já vistos (evita alertas duplicados)  
- 💬 Envia alertas diretamente para o seu Telegram  
- 🔧 Totalmente personalizável para outros sites ou categorias  

---

### 📸 Exemplo de Alerta no Telegram

<p align="center">
  <img src="https://i.imgur.com/g6LKqC5.png" alt="Exemplo de alerta no Telegram" width="600"/>
</p>

---

### 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.10+  
- 🕷️ Selenium WebDriver  
- 📡 Telegram Bot API  
- 📝 JSON para persistência de dados  

---

### ⚙️ Como Usar

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/seu-usuario/olx-bot.git

2. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    

3. **Configure o token e o chat ID do Telegram**
   ```bash
   TELEGRAM_TOKEN = 'Seu_Token_Aqui'
   CHAT_ID = 'Seu_Chat_ID_Aqui'

2. **Mude URL's**
   ```bash
   SEARCH_URLS = [
    'https://www.olx.com.br/brasil?q=ps5',
    ]

4.  **Adicione Palavras Complementares (Também tenha no Titulo) nos Filtros **
    ```bash
    PALAVRAS_JOGO     = ['jogos', 'jogo', 'cartucho', 'fita', 'card game']
    PALAVRAS_CONJUNTO = ['+ jogo', '+ jogos']

6. **Adicione o que quer procurar no Loop For e em Definir Prioridade**
   ```bash
   if 'play station' not in titulo_lower and 'ps5' not in titulo_lower:
   continue

   # define prioridade
   if titulo_lower.startswith('play station') or titulo_lower.startswith('playstation'):
   prioridade = 1

7. **Execute o bot:**
   ```bash
   pyhon app.py

---

### 🙌 Contribuições

Contribuições são sempre bem-vindas!
Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias.

---

📩 Contato
Linkedin: https://www.linkedin.com/in/felipe-martins-duarte/
