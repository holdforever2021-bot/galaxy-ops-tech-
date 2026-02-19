#!/bin/bash

###############################################################################
# Galaxy Ops Tech Demo Deployment
###############################################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVER="174.138.54.167"
USER="root"
PORT="5001"
REMOTE_DIR="/root/galaxy-ops-tech"
LOCAL_DIR="/Users/ankurjoshi/Documents/trading-system-build/galaxy-ops-tech"
EXPECT_SCRIPT="/Users/ankurjoshi/Documents/trading-system-build/.credentials/ssh_deploy_fixed.exp"
PASSWORD_FILE="/Users/ankurjoshi/Documents/trading-system-build/.credentials/ssh_password.txt"

echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        🚀 DEPLOYING GALAXY OPS TECH DEMO TO SERVER        ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Server: $SERVER"
echo "Port: $PORT"
echo ""

# Step 1: Sync files
echo -e "${YELLOW}[1/3]${NC} Syncing files to server..."

$EXPECT_SCRIPT $PASSWORD_FILE rsync -avz --progress \
    --exclude='venv/' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git/' \
    --exclude='*.log' \
    "$LOCAL_DIR/" "$USER@$SERVER:$REMOTE_DIR/"

echo -e "${GREEN}✓${NC} Files synced"

# Step 2: Install dependencies and setup service
echo -e "${YELLOW}[2/3]${NC} Installing dependencies..."

$EXPECT_SCRIPT $PASSWORD_FILE ssh $USER@$SERVER "cd $REMOTE_DIR && pip3 install --break-system-packages -r requirements.txt"

# Create systemd service
cat > /tmp/galaxy-ops-tech.service << 'EOF'
[Unit]
Description=Galaxy Ops Tech Demo
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/galaxy-ops-tech
Environment="FLASK_ENV=production"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/usr/bin/gunicorn --bind 0.0.0.0:5001 --chdir /root/galaxy-ops-tech app:app --workers 2 --timeout 60
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

$EXPECT_SCRIPT $PASSWORD_FILE scp /tmp/galaxy-ops-tech.service $USER@$SERVER:/etc/systemd/system/

$EXPECT_SCRIPT $PASSWORD_FILE ssh $USER@$SERVER "systemctl daemon-reload && systemctl enable galaxy-ops-tech"

echo -e "${GREEN}✓${NC} Service configured"

# Step 3: Start service
echo -e "${YELLOW}[3/3]${NC} Starting service..."

$EXPECT_SCRIPT $PASSWORD_FILE ssh $USER@$SERVER "ufw allow $PORT && systemctl restart galaxy-ops-tech && sleep 5 && systemctl status galaxy-ops-tech --no-pager"

echo -e "${GREEN}✓${NC} Service started"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✅ DEPLOYMENT SUCCESSFUL!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}🎯 Galaxy Ops Tech Demo URL:${NC} http://$SERVER:$PORT"
echo ""
echo -e "${GREEN}📝 Management Commands:${NC}"
echo "   Status:  ssh root@$SERVER 'systemctl status galaxy-ops-tech'"
echo "   Logs:    ssh root@$SERVER 'journalctl -u galaxy-ops-tech -f'"
echo "   Restart: ssh root@$SERVER 'systemctl restart galaxy-ops-tech'"
echo ""
