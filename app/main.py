from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from .models import ChatRequest, ChatResponse
from .agent_client import AgentClient
import logging

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(title="Agente Orquestador API")

# Servir archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Instancia del cliente (inicialización lazy)
agent_client = AgentClient()

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # El cliente se conecta solo cuando se necesita
        respuesta = agent_client.ask_agent(request.message)
        return ChatResponse(response=respuesta)
    except ValueError as e:
        logging.error(f"Error de configuración: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logging.exception("Error procesando la consulta")
        raise HTTPException(status_code=500, detail=str(e))
