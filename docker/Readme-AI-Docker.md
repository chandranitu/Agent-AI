mkdir -p ~/Agent-AI/docker/{api/routers,gui,data/uploads/{bills,orders,reports},nginx}
cd ~/Agent-AI/docker

# Copy API files from original Agent-AI
cp ~/Agent-AI/api/main.py          ~/Agent-AI/docker/api/
cp ~/Agent-AI/api/config.py        ~/Agent-AI/docker/api/
cp ~/Agent-AI/requirements.txt ~/Agent-AI/docker/api/
cp ~/Agent-AI/api/routers/db_router.py   ~/Agent-AI/docker/api/routers/
cp ~/Agent-AI/api/routers/file_router.py ~/Agent-AI/docker/api/routers/
cp ~/Agent-AI/api/routers/agent_router.py ~/Agent-AI/docker/api/routers/
touch ~/Agent-AI/docker/api/routers/__init__.py

# Copy GUI
cp ~/Agent-AI/gui/index.html ~/Agent-AI/docker/gui/

cat > ~/Agent-AI/docker/Dockerfile << 'EOF'


cat > ~/Agent-AI/docker/nginx/default.conf << 'EOF'

cat > ~/Agent-AI/docker/api/config.py << 'EOF'

cat > ~/Agent-AI/docker/api/main.py << 'EOF'

cat > ~/Agent-AI/docker/docker-compose.yml << 'EOF'

cat > ~/Agent-AI/docker/init.sql << 'EOF'

# Change API base URL — nginx proxies /api/ to fastapi container
sed -i "s|const API = 'http://localhost:8000'|const API = ''|g" \
    ~/Agent-AI/docker/gui/index.html

cd ~/Agent-AI/docker

# Make sure Ollama is running on host first
ollama serve &
sleep 5

# Build and start all containers
sudo docker compose up --build -d

#start
sudo docker compose up -d

# Watch logs
sudo docker compose logs -f

# Check all containers are running
sudo docker compose ps

# Check API health
curl http://localhost:8000/api/health

# Check DB connected
curl http://localhost:8000/api/db/schema

# Check files visible
curl http://localhost:8000/api/files/list

# Open GUI
xdg-open http://localhost:8080

cd ~/Agent-AI/docker
sudo docker compose restart nginx

------------------

#troubleshoot
Cannot connect to Ollama at http://host.docker.internal:11434. Please start Ollama: ollama serve and pull a model: ollama pull llama3.2:latest

hostname -I | awk '{print $1}'

change OLLAMA_BASE_URL in docker-compose.yml

sudo docker compose up -d --force-recreate fastapi

sudo docker exec agent-ai-api curl http://172.18.0.3:11434/api/tags


#ollama

# Stop Ollama
pkill ollama
sleep 2

# Start with 0.0.0.0 binding
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
sleep 3

# Verify it is now listening on all interfaces
curl http://127.0.0.1:11434/api/tags
curl http://192.168.1.43:11434/api/tags

#container
# Connect to PostgreSQL inside container
sudo docker exec -it agent-ai-postgres psql -U postgres -d reports_db

# Copy your existing order files to the mounted folder
sudo docker cp . agent-ai-api:/app/data/uploads/orders/

# Verify container side — should show same files instantly
sudo docker exec agent-ai-api ls -lh /app/data/uploads/orders/



