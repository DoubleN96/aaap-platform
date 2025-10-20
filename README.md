# 🤖 Stratomai Agents

> **Plataforma de Agentes IA para Automatización Empresarial**

Transforma tareas repetitivas en automatizaciones inteligentes mediante lenguaje natural. Sin código, sin complicaciones.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org/)

---

## ✨ Características Principales

- 🤖 **Agentes IA Personalizados** - Crea asistentes especializados (Email, CRM, Calendar, Analytics)
- 💬 **Lenguaje Natural** - Describe lo que necesitas y déjalo ejecutarse automáticamente
- 🔗 **Integraciones Empresariales** - Gmail, Outlook, Slack, HubSpot, Google Calendar
- ⚡ **Tiempo Real** - Seguimiento de tareas en tiempo real
- 📊 **Analytics Inteligente** - Métricas de productividad y ahorro de tiempo
- 🔒 **Seguridad Enterprise** - OAuth 2.0, RLS, cifrado end-to-end
- 🐳 **Deploy Fácil** - Docker Compose + Coolify en minutos

## 🚀 Quick Start

```bash
git clone https://github.com/DoubleN96/stratomai-agents.git
cd stratomai-agents
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```

Acceder a: http://localhost:3000

## 📖 Documentación

- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Guía completa de deployment
- [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) - Instrucciones paso a paso

## 🛠️ Stack

- **Frontend**: Next.js 15, TypeScript, Tailwind, Shadcn/ui
- **Backend**: Next.js API Routes, Python FastAPI  
- **AI**: OpenAI GPT-4, Anthropic Claude, LangChain
- **Database**: Supabase (PostgreSQL), Redis
- **DevOps**: Docker, Coolify, n8n

## 📊 API Endpoints

### Tasks
- `POST /api/tasks` - Crear tarea en lenguaje natural
- `GET /api/tasks` - Listar tareas
- `GET /api/tasks/:id` - Detalles de tarea

### Agents
- `POST /api/agents` - Crear agente IA
- `GET /api/agents` - Listar agentes

Ver documentación completa en `http://localhost:8000/docs` (AI Engine)

## 🤝 Contribuir

Seguimos [Conventional Commits](https://www.conventionalcommits.org/).

1. Fork del proyecto
2. Crea tu branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'feat: add feature'`)
4. Push (`git push origin feature/amazing`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

**Hecho con ❤️ por el equipo de Stratomai**
