# Telegram AI Bot

Bot de Telegram con inteligencia artificial usando la API de Claude (Anthropic). Mantiene contexto de conversación por usuario y responde en el idioma del usuario.

## Características

-  Conversación natural con memoria de contexto
-  Responde en el idioma del usuario automáticamente
-  Resumen de conversación con IA
-  Comando para limpiar el historial
-  Indicador de "escribiendo..." mientras procesa

## Estructura del proyecto

```
telegram-ai-bot/
├── src/
│   ├── bot.py          # Lógica principal del bot de Telegram
│   └── ai_client.py    # Cliente para la API de Claude
├── tests/
│   └── test_ai_client.py
├── .env.example        # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

##  Instalación paso a paso

### 1. Cloná el repositorio

```bash
git clone https://github.com/tu-usuario/telegram-ai-bot.git
cd telegram-ai-bot
```

### 2. Creá un entorno virtual

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalá las dependencias

```bash
pip install -r requirements.txt
```

### 4. Obtené tus credenciales

**Token de Telegram:**
1. Abrí Telegram y buscá `@BotFather`
2. Enviá `/newbot`
3. Seguí las instrucciones y copiá el token

**API Key de Anthropic:**
1. Entrá a [console.anthropic.com](https://console.anthropic.com)
2. Creá una cuenta y generá una API key

### 5. Configurá las variables de entorno

```bash
cp .env.example .env
```

Editá `.env` con tus credenciales:

```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
ANTHROPIC_API_KEY=tu_api_key_de_anthropic
```

### 6. Ejecutá el bot

```bash
python src/bot.py
```

##  Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `/start` | Mensaje de bienvenida |
| `/help` | Muestra ayuda |
| `/clear` | Limpia el historial de conversación |
| `/history` | Genera un resumen de la conversación |

##  Tests

```bash
python -m pytest tests/
```

##  Personalización

Para cambiar la personalidad del bot, editá `SYSTEM_PROMPT` en `src/ai_client.py`:

```python
SYSTEM_PROMPT = """Sos un asistente experto en Python que ayuda a programadores...
```

##  Tecnologías usadas

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — SDK de Telegram
- [Anthropic Python SDK](https://github.com/anthropic-ai/anthropic-sdk-python) — API de Claude
- [python-dotenv](https://github.com/theskumar/python-dotenv) — manejo de variables de entorno

## 📄 Licencia

MIT
