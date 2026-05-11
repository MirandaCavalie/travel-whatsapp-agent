# travel-whatsapp-agent

Servidor FastAPI que actua como un agente de WhatsApp para coordinar un viaje
grupal. Recibe mensajes via webhook de Twilio, los procesa con Claude
(Anthropic) usando como contexto los datos del viaje, y responde por WhatsApp.

Es un MVP: historial de conversacion en memoria (se pierde al reiniciar), sin
base de datos, datos del viaje en un archivo Python.

## Requisitos previos

1. **Cuenta de Twilio** con WhatsApp Sandbox habilitado:
   https://console.twilio.com → Messaging → Try it out → Send a WhatsApp message.
   De ahi obtienes `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` y el numero del
   sandbox (`whatsapp:+14155238886`).
2. **Cuenta de Anthropic** con una API key:
   https://console.anthropic.com → Settings → API Keys.
3. **Python 3.11+**.
4. **ngrok** (o equivalente) para exponer el servidor local a internet en dev:
   https://ngrok.com/download.

## Setup paso a paso

```powershell
# 1. Clonar
git clone <repo-url> travel-whatsapp-agent
cd travel-whatsapp-agent

# 2. Crear y activar venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# source .venv/bin/activate    # bash/zsh

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env         # PowerShell
# cp .env.example .env         # bash/zsh
# Edita .env con tus credenciales reales

# 5. Correr el servidor
uvicorn app.main:app --reload --port 8000
```

Health check: `curl http://localhost:8000/health` → `{"status":"ok"}`.

## Configurar el webhook de Twilio (sandbox)

1. Levanta tu servidor local en `http://localhost:8000`.
2. En otra terminal, expon el puerto con ngrok:
   ```bash
   ngrok http 8000
   ```
   Copia la URL `https://xxxx-xxxx.ngrok-free.app`.
3. (Opcional pero recomendado en prod) Pega esa URL en tu `.env` como
   `PUBLIC_BASE_URL=https://xxxx-xxxx.ngrok-free.app` y reinicia uvicorn.
   Sirve para que la validacion de firma de Twilio funcione detras del proxy.
4. En la consola de Twilio: Messaging → Try it out → Send a WhatsApp message
   → tab **Sandbox settings**.
5. En **When a message comes in** pega:
   `https://xxxx-xxxx.ngrok-free.app/webhook/whatsapp` (metodo `POST`).
6. Save.

## Probar con el sandbox

1. Une tu numero al sandbox: manda el codigo `join <palabra-asignada>` desde
   WhatsApp al `+1 415 523 8886`. Twilio te muestra la palabra exacta en la
   consola.
2. Escribe cualquier mensaje desde ese WhatsApp (ej: "donde nos quedamos?").
3. Deberias ver en los logs del servidor:
   `WhatsApp recibido from=whatsapp:+51... body='donde nos quedamos?'`
   y recibir la respuesta del agente en WhatsApp.

Tips de debugging:
- Si no responde, mira los logs de ngrok (`http://localhost:4040`) para ver
  si Twilio llego al webhook y con que payload.
- Errores 403 en logs = firma de Twilio invalida; revisa `PUBLIC_BASE_URL`.

## Pasar a produccion

1. **Registra un numero propio de WhatsApp Business** en Twilio (deja de usar
   el sandbox). Documentacion:
   https://www.twilio.com/docs/whatsapp/self-sign-up
2. Actualiza `TWILIO_WHATSAPP_NUMBER` en `.env` con tu numero registrado:
   `TWILIO_WHATSAPP_NUMBER=whatsapp:+51XXXXXXXXX`.
3. Despliega el servidor en un host con HTTPS estable (Fly.io, Railway,
   Render, Cloud Run, etc.). El servidor es un FastAPI standard:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Setea `ENVIRONMENT=production` y `PUBLIC_BASE_URL=https://tu-dominio` en
   las env vars del host. Con `ENVIRONMENT=production`, los requests sin
   firma valida de Twilio se rechazan con 403.
5. En la configuracion del numero en Twilio Console, apunta el webhook
   "When a message comes in" a `https://tu-dominio/webhook/whatsapp`.
6. Considera que el historial vive en memoria: si reinicias o escalas a
   varias instancias, se pierde / se desincroniza. Para algo mas serio,
   migra `_history` en `app/agent.py` a Redis o Postgres.

## Agregar los datos reales del viaje

Edita `app/trip_data.py`:

- `TRIP_DATA["general"]`: destino, fechas, moneda, zona horaria, tips.
- `TRIP_DATA["travelers"]`: una entrada por persona. **Importante:** el campo
  `phone` debe coincidir EXACTAMENTE con el numero desde el que esa persona
  envia WhatsApp (formato E.164 con `+`, sin espacios ni `whatsapp:`). Asi el
  agente sabe quien le habla.
- `TRIP_DATA["accommodation"]`: hotel/airbnb, direccion, fechas, confirmacion.
- `TRIP_DATA["activities"]`: lista de actividades (fecha, hora, lugar, notas).
- `TRIP_DATA["emergency"]`: contactos de emergencia, seguro.

Despues de editar, reinicia uvicorn (`--reload` lo hace solo si lo dejaste
corriendo). Todo cambio se refleja en el siguiente mensaje porque el system
prompt se construye en cada llamada.

## Estructura

```
travel-whatsapp-agent/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py
    ├── main.py        # FastAPI app + webhook
    ├── config.py      # Carga de env vars
    ├── whatsapp.py    # Envio via Twilio + chunking 1600 chars
    ├── agent.py       # System prompt + llamada a Claude + historial
    └── trip_data.py   # Datos del viaje (PLACEHOLDER, reemplazar)
```

## Endpoints

- `GET /health` → `{"status": "ok"}`.
- `POST /webhook/whatsapp` → recibe form-encoded de Twilio (`From`, `Body`, ...),
  procesa con el agente, responde TwiML.
