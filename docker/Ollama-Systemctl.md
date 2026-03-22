# Installation

curl -fsSL https://ollama.com/install.sh | sh

# ###########

# Stop ollama service
sudo systemctl stop ollama

# Verify it stopped
sudo ss -tlnp | grep 11434
# Should return nothing

# Check if override file was created correctly
cat /etc/systemd/system/ollama.service.d/override.conf


# ##
sudo mkdir -p /etc/systemd/system/ollama.service.d

sudo bash -c 'cat > /etc/systemd/system/ollama.service.d/override.conf << EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF'

# Verify it was written
cat /etc/systemd/system/ollama.service.d/override.conf

# Reload systemd and start
sudo systemctl daemon-reload
sudo systemctl start ollama
sleep 3

# Verify now on 0.0.0.0
sudo ss -tlnp | grep 11434

LISTEN 0  4096  0.0.0.0:11434  0.0.0.0:*

# test

bashcurl http://192.168.1.43:11434/api/tags
sudo docker exec agent-ai-api curl http://192.168.1.43:11434/api/tags