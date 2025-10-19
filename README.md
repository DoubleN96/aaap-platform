# AAAP Platform - AI Agent Automation Platform

> Automatiza tareas empresariales con agentes IA mediante lenguaje natural

## 🚀 Descripción

AAAP (AI Agent Automation Platform) es una plataforma SaaS completa que permite a usuarios crear y gestionar agentes de IA que automatizan tareas mediante instrucciones en lenguaje natural.

## 🛠️ Stack Tecnológico

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Shadcn/ui
- **Backend**: Next.js API Routes, Python FastAPI
- **AI**: OpenAI GPT-4, Anthropic Claude, LangChain  
- **Database**: Supabase (PostgreSQL), Redis
- **Deployment**: Docker, Coolify, n8n

## 📦 Estructura

```
aaap-platform/
├── app/                 # Next.js App Router
├── components/          # Componentes React
├── lib/                 # Utilidades
├── ai-engine/          # Microservicio Python IA
├── migrations/         # SQL Migrations
└── docker-compose.yml  # Docker orchestration
```

## 🚀 Quickstart

### Desarrollo Local

```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Run development servers
npm run dev:all
```

### Docker Deployment

```bash
docker-compose up -d
```

## 📖 Documentación Completa

Ver archivos en el repositorio:
- `DEPLOYMENT_GUIDE.md` - Guía completa de deployment
- `migrations/001_initial_schema.sql` - Esquema de base de datos
- API Routes en `app/api/`

## 🔐 Configuración Requerida

Variables de entorno necesarias:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `OPENAI_API_KEY` o `ANTHROPIC_API_KEY`
- Ver `.env.example` para la lista completa

## 📊 Features

- 🤖 Agentes IA personalizados (Email, CRM, Scheduler)
- 💬 Procesamiento de lenguaje natural
- 🔗 Integraciones (Gmail, Slack, HubSpot, etc.)
- 📊 Analytics y métricas
- 🔒 Seguridad (OAuth, RLS, auditoría)

## 🚀 Deployment con Coolify

1. Crear repositorio en GitHub
2. Configurar proyecto en Coolify
3. Conectar al repositorio
4. Configurar variables de entorno
5. Deploy automático

## 📝 Licencia

MIT License

## 🔗 Links

- Repository: https://github.com/DoubleN96/aaap-platform
- Issues: https://github.com/DoubleN96/aaap-platform/issues

---

**Hecho con ❤️ usando Next.js, Python y mucha IA**
