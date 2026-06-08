#!/bin/bash
# SKYGUARD VPS DEPLOYMENT SCRIPT
# Usage: ssh root@VPS_IP < deploy-vps.sh

echo "🚀 SKYGUARD VPS Deployment Script"
echo "===================================="

# 1. UPDATE SISTEM
echo "📦 Ažuriram sistem..."
apt update && apt upgrade -y
apt install -y curl git wget

# 2. INSTALIRAJ DOCKER
echo "🐳 Instaliram Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. INSTALIRAJ DOCKER COMPOSE
echo "📋 Instaliram Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 4. KLONIRAJ PROJEKT
echo "📥 Kloniram projekt sa GitHub..."
cd /root
git clone https://github.com/kb8482-svg/SKYGUARD.git
cd SKYGUARD

# 5. KREIRAJ .env FILE ZA PRODUCTION
echo "⚙️ Kreiram production environment..."
cat > .env.production << 'ENVFILE'
# SKYGUARD Production Config
DOMAIN=pejmoneglejmo.me
POSTGRES_USER=skyguard_user
POSTGRES_PASSWORD=$(openssl rand -base64 32)
POSTGRES_DB=skyguard_auth
MINIO_ROOT_USER=user-04
MINIO_ROOT_PASSWORD=thestrongestavajePass04
ENVFILE

# 6. KREIRAJ PRODUCTION DOCKER-COMPOSE
echo "🔧 Priprema docker-compose za production..."
# Production će koristiti existing docker-compose.yaml

# 7. POKRENITE SERVISE
echo "▶️  Pokrenjem servise..."
docker-compose up -d

# 8. ČEKAJ DA SE SERVISI PODIGUNJE
echo "⏳ Čekam servise (30 sekundi)..."
sleep 30

# 9. PROVJERA ZDRAVLJA
echo "🏥 Proverim zdravlje servisa..."
curl -s http://localhost:8000/ > /dev/null && echo "✅ API Gateway OK" || echo "❌ API Gateway problem"

# 10. SETUP SSL SA CERTBOT
echo "🔒 Postavljam SSL certifikat sa Let's Encrypt..."
apt install -y certbot python3-certbot-nginx

# NOTA: Trebate ručno pokrenuti:
# certbot certonly --standalone -d pejmoneglejmo.me -d www.pejmoneglejmo.me

echo ""
echo "═══════════════════════════════════════════════"
echo "✅ DEPLOYMENT GOTOV!"
echo "═══════════════════════════════════════════════"
echo ""
echo "🌐 Aplikacija je dostupna na:"
echo "   http://pejmoneglejmo.me:8000/"
echo ""
echo "📊 Min.io Console:"
echo "   http://pejmoneglejmo.me:9001/"
echo ""
echo "🔧 Sljedeći koraci:"
echo "   1. Dodaj DNS A record u Cloudflare"
echo "   2. Pokrenite SSL setup:"
echo "      certbot certonly --standalone -d pejmoneglejmo.me"
echo "   3. Ažuriraj nginx config sa SSL certifikatom"
echo ""
