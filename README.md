# ⚽ Football Stats Analyzer

Análisis de estadísticas de fútbol en tiempo real con comparación de cuotas de casas de apuestas.

## 🚀 Stack Tecnológico
- **Backend:** FastAPI + Python 3.11
- **Frontend:** React + Vite
- **Datos:** TheStatsAPI (estadísticas reales + odds en vivo)
- **CI/CD:** GitHub Actions
- **Deploy:** Docker + GitHub Container Registry

## 📊 Métricas Analizadas
- Corners, Remates (totales/al arco), Goles, Tarjetas
- Ambos Anotan (BTTS), xG (Expected Goals)
- Posesión, Pases, Entradas, Paradas
- Cuotas: 1X2, BTTS, Total Goles, Corners, Asian Handicap

## 🔧 Configuración desde Móvil (sin terminal)

### 1. Crear repo en GitHub
- Abre GitHub Mobile → New Repository
- Nombre: `football-stats-analyzer`
- Público o Privado

### 2. Subir archivos
- Ve a la web de GitHub en tu navegador móvil
- En cada carpeta, usa "Add file" → "Create new file"
- Pega el contenido de cada archivo mostrado arriba

### 3. Configurar Secrets
- Settings → Secrets and variables → Actions
- Agrega: `THESTATSAPI_KEY` (obtenida en thestatsapi.com)

### 4. Activar Actions
- Ve a Actions tab → Enable Actions
- Los workflows se ejecutarán automáticamente en cada push

### 5. Deploy
- Conecta Render/Railway/Fly.io a tu repo
- O descarga las imágenes Docker desde GitHub Packages

## 🏃 Ejecución local (opcional)
```bash
docker-compose up --build
