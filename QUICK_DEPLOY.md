# 🚀 Guía Rápida de Despliegue - Stratomai Agents

## Estado Actual

- ✅ Código completo y funcional en `/root/stratomai-agents/`
- ✅ Git inicializado con todos los commits
- ⏳ Pendiente: Subir a GitHub y desplegar en Coolify

## 🎯 Opción 1: Despliegue Directo desde Servidor (RECOMENDADO)

Ya que el código está completo en el servidor, puedes desplegarlo directamente en Coolify sin GitHub:

### Paso 1: Crear Servicio en Coolify

1. Accede a Coolify: **http://46.224.16.135:8000**

2. Click en **"New Resource"** → **"New Application"**

3. Selecciona **"Deploy from Source"** → **"Local Directory"**

4. Configuración:
   ```
   Name: stratomai-agents
   Source Directory: /root/stratomai-agents
   Build Pack: Docker Compose
   ```

### Paso 2: Configurar Variables de Entorno

Copia TODAS estas variables en la sección **Environment Variables** de Coolify:

```env
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://stratomai-agents.stratomai.com
NEXT_PUBLIC_AI_ENGINE_URL=https://stratomai-agents.stratomai.com/ai
NEXT_PUBLIC_SUPABASE_URL=https://pdzefcjfbbofgokwcpwo.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkemVmY2pmYmJvZmdva3djcHdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY5Nzg0MzksImV4cCI6MjA1MjU1NDQzOX0.PlTFWfF99FJx0jggdMfQa63DK87G-3VJ9RAuTZw8UDY
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkemVmY2pmYmJvZmdva3djcHdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjk3ODQzOSwiZXhwIjoyMDUyNTU0NDM5fQ.Crc9CtNbxRd5JHX1b5rnD1U4bNmFwTCzM3J0uoSDy-w
DATABASE_URL=postgresql://postgres.pdzefcjfbbofgokwcpwo:[TU-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
ANTHROPIC_API_KEY=sk-ant-api03-Smy3GQLOFj3j5E-CJDz6kCk6NsLfUQqXx_lD3Fo4pXSN7DQmjkT4H7_8tYPPKKy0pF2j9qBKv21uqhQUKNB3kQ-YJV9MAAA
N8N_BASE_URL=https://n8n.stratomai.com
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OGJkNjYwZi0xNDU0LTQyMmEtOTg2MC03YTg4Y2ExZjdlNmYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwNzcwNDgwfQ.zbBMlbSpDuqhaVl69C6_msIBxAcMM5v8G0Rg0xj6BaI
REDIS_URL=redis://redis:6379
ENCRYPTION_KEY=stratomai_agents_encryption_key_2025
JWT_SECRET=stratomai_agents_jwt_secret_2025_production
```

**IMPORTANTE**: Reemplaza `[TU-PASSWORD]` en DATABASE_URL con la contraseña real de Supabase.

### Paso 3: Configurar Dominio

En la sección **Domains**:
- Domain: `stratomai-agents.stratomai.com`
- ✅ Enable SSL (Let's Encrypt)

### Paso 4: Desplegar

1. Click en **"Deploy"**
2. Espera 5-10 minutos mientras Coolify:
   - Construye las imágenes Docker
   - Levanta los 3 servicios (web, ai-engine, redis)
   - Configura SSL
3. Monitorea los logs en tiempo real

### Paso 5: Ejecutar Migraciones de Base de Datos

1. Ve a **Supabase Dashboard**: https://supabase.com/dashboard/project/pdzefcjfbbofgokwcpwo
2. Click en **SQL Editor**
3. Ejecuta **en orden**:
   - El contenido de `/root/stratomai-agents/migrations/001_initial_schema.sql`
   - El contenido de `/root/stratomai-agents/migrations/002_seed_data.sql`

### Paso 6: Verificar

Accede a:
- 🌐 Frontend: https://stratomai-agents.stratomai.com
- 🔧 AI Engine: https://stratomai-agents.stratomai.com/ai/health
- 📡 API: https://stratomai-agents.stratomai.com/api/tasks

---

## 🎯 Opción 2: Despliegue desde GitHub

Si prefieres usar GitHub (más profesional):

### Paso 1: Configurar Autenticación GitHub

```bash
# Opción A: SSH (Recomendado)
ssh-keygen -t ed25519 -C "tu@email.com"
cat ~/.ssh/id_ed25519.pub
# Copia la clave y agrégala en GitHub → Settings → SSH Keys

# Opción B: GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
gh auth login
```

### Paso 2: Push a GitHub

```bash
cd /root/stratomai-agents

# Si usaste SSH:
git remote set-url origin git@github.com:DoubleN96/aaap-platform.git

# Push
git push -u origin main
```

### Paso 3: Crear Servicio en Coolify

1. Coolify → **New Resource** → **New Application**
2. Selecciona **"Deploy from Git"**
3. Configuración:
   ```
   Repository: https://github.com/DoubleN96/aaap-platform
   Branch: main
   Build Pack: Docker Compose
   ```
4. Continúa con los pasos de variables de entorno del Método 1

---

## 🐛 Troubleshooting

### Error: "Docker build failed"

```bash
cd /root/stratomai-agents
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

### Error: "Cannot connect to Supabase"

1. Verifica que DATABASE_URL tenga la contraseña correcta
2. Ve a Supabase Dashboard → Settings → Database
3. Copia la connection string completa

### Error: "Port 3000 already in use"

```bash
# Encuentra qué proceso usa el puerto
sudo lsof -i :3000
# Mata el proceso
sudo kill -9 <PID>
# O cambia el puerto en docker-compose.yml
```

---

## ✅ Checklist de Deployment

- [ ] Coolify servicio creado
- [ ] Variables de entorno configuradas (incluyendo DATABASE_URL con password)
- [ ] Dominio configurado con SSL
- [ ] Deployment iniciado
- [ ] Migraciones SQL ejecutadas en Supabase
- [ ] Frontend accesible
- [ ] AI Engine health check OK
- [ ] API funcionando

---

## 📞 Comandos Útiles

```bash
# Ver logs en Coolify
# (Desde la UI de Coolify, sección Logs)

# O si tienes acceso SSH al servidor:
ssh root@46.224.16.135
docker ps | grep stratomai
docker logs -f stratomai-agents-web
docker logs -f stratomai-agents-ai-engine

# Reiniciar servicios
docker-compose restart

# Reconstruir todo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎉 ¡Listo!

Una vez completados todos los pasos, tu aplicación estará publicada y funcionando en:

**https://stratomai-agents.stratomai.com**

¡Disfruta de Stratomai Agents! 🚀
