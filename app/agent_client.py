import os
import logging
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from azure.ai.agents.models import ListSortOrder

class AgentClient:
    def __init__(self):
        # Obtener variables de entorno
        self.endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        self.agent_id = os.getenv("AZURE_AGENT_ORCHESTRATOR_ID")
        self._client = None
        self._agent = None
        
        if not self.endpoint or not self.agent_id:
            raise ValueError("Faltan variables de entorno: AZURE_AI_PROJECT_ENDPOINT y AZURE_AGENT_ORCHESTRATOR_ID")
    
    @property
    def client(self):
        if self._client is None:
            # Usar AzureCliCredential que usa la sesión de la CLI de Azure
            self._client = AIProjectClient(
                credential=AzureCliCredential(),
                endpoint=self.endpoint
            )
        return self._client
    
    @property
    def agent(self):
        if self._agent is None:
            self._agent = self.client.agents.get_agent(self.agent_id)
            logging.info(f"Agente cargado: {self._agent.id}")
        return self._agent

    def ask_agent(self, message: str) -> str:
        try:
            # Crear un hilo
            thread = self.client.agents.threads.create()
            logging.info(f"Thread creado: {thread.id}")
            
            # Agregar mensaje del usuario
            self.client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )
            
            # Ejecutar el agente y esperar el resultado
            run = self.client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=self.agent.id
            )
            
            if run.status == "failed":
                error_msg = run.last_error if hasattr(run, 'last_error') else "Error desconocido"
                logging.error(f"Run failed: {error_msg}")
                return f"Error en la ejecución del agente: {error_msg}"
            
            # Obtener mensajes del hilo
            messages = self.client.agents.messages.list(
                thread_id=thread.id, 
                order=ListSortOrder.ASCENDING
            )
            
            # Buscar el último mensaje del asistente
            for msg in messages:
                if hasattr(msg, 'text_messages') and msg.text_messages:
                    if msg.role == "assistant":
                        # Obtener el último mensaje de texto
                        text_msg = msg.text_messages[-1]
                        if hasattr(text_msg, 'text') and hasattr(text_msg.text, 'value'):
                            return text_msg.text.value
            
            return "No se encontró respuesta del asistente."
        
        except Exception as e:
            logging.exception("Error en ask_agent")
            return f"Error al procesar la solicitud: {str(e)}"
