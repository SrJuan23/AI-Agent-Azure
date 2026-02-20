# Sistema de Salud Colombia - Asistente Virtual

Asistente virtual del sistema de salud colombiano, construido con FastAPI y Azure AI Agents.

## Características

- Interfaz de chat interactiva
- Integración con Azure AI Agents para procesamiento de lenguaje natural
- Frontend responsivo con diseño del Ministerio de Salud de Colombia
- Manejo de sesiones para mantener contexto de conversación

## Requisitos

- Python 3.10+
- Azure CLI (para autenticación)
- Cuenta de Azure AI Project configurada

## Instalación

1. **Clonar el repositorio:**
```bash
git clone <repo-url>
cd AI-Agent-Duck-Hunter-Game
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
```

3. **Activar el entorno virtual:**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno:**

Crea un archivo `.env` con las siguientes variables:
```env
AZURE_AI_PROJECT_ENDPOINT=https://tu-endpoint.azure.com/api/projects/tu-proyecto
AZURE_AGENT_ORCHESTRATOR_ID=asst_xxxxxxxxxxxx
```

## Configuración de Azure

### Opción 1: Usar Azure CLI (Recomendado)

1. Instala Azure CLI: https://docs.microsoft.com/es-es/cli/azure/install-azure-cli

2. Inicia sesión:
```bash
az login
```

3. Configura las variables de entorno en `.env`

### Opción 2: Usar Service Principal

```env
AZURE_TENANT_ID=tu-tenant-id
AZURE_CLIENT_ID=tu-client-id
AZURE_CLIENT_SECRET=tu-client-secret
```

## Uso

1. **Iniciar el servidor:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

2. **Acceder a la aplicación:**

Abre tu navegador en: http://localhost:8001

## Estructura del Proyecto

```
AI-Agent-Duck-Hunter-Game/
├── app/
│   ├── __init__.py
│   ├── agent_client.py    # Cliente del agente de Azure
│   ├── main.py           # Aplicación FastAPI
│   ├── models.py         # Modelos Pydantic
│   └── static/
│       └── index.html    # Frontend
├── data/
│   ├── analytics_data.json
│   └── faq_knowledge_base.json
├── .env                  # Variables de entorno (no subir)
├── .gitignore
├── requirements.txt
└── README.md
```

## Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `AZURE_AI_PROJECT_ENDPOINT` | Endpoint del proyecto de Azure AI | Sí |
| `AZURE_AGENT_ORCHESTRATOR_ID` | ID del agente orquestador | Sí |
| `AZURE_TENANT_ID` | Tenant de Azure AD (para Service Principal) | No |
| `AZURE_CLIENT_ID` | Client ID (para Service Principal) | No |
| `AZURE_CLIENT_SECRET` | Client Secret (para Service Principal) | No |

## Troubleshooting

### Error de autenticación

Si aparece `DefaultAzureCredential failed to retrieve a token`:

1. Verifica que hayas iniciado sesión con `az login`
2. O configura las variables de entorno con credenciales de Service Principal
3. Verifica que el tenant ID sea válido

### Error al iniciar el servidor

- Asegúrate de que el puerto 8001 no esté en uso
- Verifica que las variables de entorno estén configuradas correctamente

## Licencia

MIT License
