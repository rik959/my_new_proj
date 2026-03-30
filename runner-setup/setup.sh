#!/bin/bash
set -e

echo "============================================"
echo " 💚 Love Pipeline — Full Setup Script"
echo " WSL Ubuntu | registry.eberrik.local:5000"
echo "============================================"
echo ""

# =============================================
# STEP 1: Local Docker Registry Setup
# =============================================
echo "📦 STEP 1: Setting up local secured Docker registry..."

REGISTRY_DIR=~/local-registry
mkdir -p $REGISTRY_DIR/auth $REGISTRY_DIR/data

# Install htpasswd if not present
if ! command -v htpasswd &> /dev/null; then
    echo "  Installing apache2-utils..."
    sudo apt-get update -qq && sudo apt-get install -y -qq apache2-utils
fi

# Create registry credentials
if [ ! -f "$REGISTRY_DIR/auth/registry.password" ]; then
    echo ""
    echo "  🔐 Create your registry password:"
    htpasswd -Bc $REGISTRY_DIR/auth/registry.password eberrik
    echo "  ✅ Credentials created for user: eberrik"
else
    echo "  ✅ Credentials already exist."
fi

# =============================================
# STEP 2: /etc/hosts entry
# =============================================
echo ""
echo "🌐 STEP 2: Configuring FQDN..."

if ! grep -q "registry.eberrik.local" /etc/hosts; then
    echo "127.0.0.1  registry.eberrik.local" | sudo tee -a /etc/hosts
    echo "  ✅ Added registry.eberrik.local to /etc/hosts"
else
    echo "  ✅ registry.eberrik.local already in /etc/hosts"
fi

# =============================================
# STEP 3: Docker insecure registry config
# =============================================
echo ""
echo "🐳 STEP 3: Configuring Docker for HTTP registry..."

DAEMON_JSON="/etc/docker/daemon.json"
DESIRED='{"insecure-registries":["registry.eberrik.local:5000"]}'

if [ -f "$DAEMON_JSON" ]; then
    if grep -q "registry.eberrik.local" "$DAEMON_JSON"; then
        echo "  ✅ Docker already configured for insecure registry."
    else
        echo "  ⚠️  $DAEMON_JSON exists but missing registry entry."
        echo "  Please manually add \"registry.eberrik.local:5000\" to insecure-registries."
        echo "  Current content:"
        cat "$DAEMON_JSON"
    fi
else
    echo "$DESIRED" | sudo tee "$DAEMON_JSON"
    echo "  ✅ Created $DAEMON_JSON"
    echo "  Restarting Docker..."
    sudo systemctl restart docker
    echo "  ✅ Docker restarted."
fi

# =============================================
# STEP 4: Start the Registry Container
# =============================================
echo ""
echo "🗄️ STEP 4: Starting Docker registry..."

cat > $REGISTRY_DIR/docker-compose.yml << 'EOF'
services:
  registry:
    image: registry:2
    container_name: eberrik_registry
    restart: always
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: "Eberrik Private Registry"
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/registry.password
    volumes:
      - ./data:/var/lib/registry
      - ./auth:/auth
EOF

cd $REGISTRY_DIR
docker compose up -d
echo "  ✅ Registry running at registry.eberrik.local:5000"

# Test login
echo ""
echo "  🔐 Testing registry login..."
echo "  (Enter the password you just created)"
docker login registry.eberrik.local:5000 -u eberrik

# =============================================
# STEP 5: Install GitHub Actions Runner
# =============================================
echo ""
echo "🏃 STEP 5: Installing GitHub Actions self-hosted runner..."

RUNNER_DIR=~/actions-runner
RUNNER_VERSION="2.321.0"

if [ -d "$RUNNER_DIR" ] && [ -f "$RUNNER_DIR/run.sh" ]; then
    echo "  ✅ Runner already installed at $RUNNER_DIR"
else
    mkdir -p $RUNNER_DIR && cd $RUNNER_DIR

    echo "  ⬇️  Downloading runner v${RUNNER_VERSION}..."
    curl -sO -L "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"

    echo "  📦 Extracting..."
    tar xzf actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
    rm -f actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

    echo "  ✅ Runner extracted to $RUNNER_DIR"
fi

# =============================================
# STEP 6: Windows Port Forwarding Reminder
# =============================================
echo ""
echo "============================================"
echo " ✅ SETUP COMPLETE!"
echo "============================================"
echo ""
echo " Registry:  registry.eberrik.local:5000"
echo " Username:  eberrik"
echo " Protocol:  HTTP (insecure-registries configured)"
echo ""
echo "============================================"
echo " NEXT STEPS:"
echo "============================================"
echo ""
echo " 1. CONFIGURE THE RUNNER:"
echo "    cd ~/actions-runner"
echo "    ./config.sh --url https://github.com/YOUR_USER/YOUR_REPO \\"
echo "                --token YOUR_TOKEN \\"
echo "                --name love-server \\"
echo "                --labels self-hosted"
echo ""
echo " 2. START THE RUNNER:"
echo "    cd ~/actions-runner && ./run.sh"
echo ""
echo "    OR install as a service (auto-start):"
echo "    sudo ./svc.sh install"
echo "    sudo ./svc.sh start"
echo ""
echo " 3. SET GITHUB SECRETS (repo → Settings → Secrets):"
echo "    DOCKER_USERNAME  = eberrik"
echo "    DOCKER_PASSWORD  = (your registry password)"
echo ""
echo " 4. WINDOWS HOSTS FILE (Run Notepad as Admin):"
echo "    Add to C:\Windows\System32\drivers\etc\hosts:"
echo "    127.0.0.1  registry.eberrik.local"
echo ""
echo " 5. WINDOWS PORT FORWARDING (PowerShell as Admin):"
echo "    netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8501 connectaddress=127.0.0.1 connectport=8501"
echo ""
echo " 6. WINDOWS FIREWALL (PowerShell as Admin):"
echo "    New-NetFirewallRule -DisplayName 'Love Pipeline' -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow"
echo ""
echo " 7. PUSH TO GITHUB:"
echo "    git add . && git commit -m 'deploy: love-pipeline v1.0 💚' && git push"
echo ""
echo "============================================"
echo " 💚 Happy Anniversary, eberrik!"
echo "============================================"
