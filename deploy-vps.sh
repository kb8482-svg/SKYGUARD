#!/bin/bash
set -euo pipefail

# SKYGUARD VPS DEPLOYMENT SCRIPT
# Usage: DOMAIN=app.pejmoneglejmo.me ./deploy-vps.sh

DOMAIN="${DOMAIN:-app.pejmoneglejmo.me}"
REPO_URL="${REPO_URL:-https://github.com/kb8482-svg/SKYGUARD.git}"
APP_DIR="${APP_DIR:-/root/SKYGUARD}"

echo "SKYGUARD VPS Deployment"
echo "Domain: ${DOMAIN}"

echo "Updating system packages..."
apt update && apt upgrade -y
apt install -y curl git wget openssl certbot

if ! command -v docker >/dev/null 2>&1; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
fi

if [ ! -d "${APP_DIR}" ]; then
  echo "Cloning project..."
  git clone "${REPO_URL}" "${APP_DIR}"
fi

cd "${APP_DIR}"

echo "Creating production environment file..."
POSTGRES_PASSWORD="$(openssl rand -base64 32)"
cat > .env.production << ENVFILE
DOMAIN=${DOMAIN}
POSTGRES_USER=skyguard_user
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=skyguard_auth
MINIO_ROOT_USER=user-04
MINIO_ROOT_PASSWORD=thestrongestavajePass04
ENVFILE

echo "Requesting Let's Encrypt certificate..."
echo "Cloudflare DNS for ${DOMAIN} must point to this VPS before this step."
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  certbot certonly --standalone -d "${DOMAIN}" --agree-tos --register-unsafely-without-email --non-interactive
fi

echo "Starting SKYGUARD production stack..."
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build

echo "Waiting for services..."
sleep 30

echo "Checking HTTPS..."
curl -s "https://${DOMAIN}/" > /dev/null && echo "HTTPS OK" || echo "HTTPS check failed"

echo ""
echo "Deployment complete."
echo "App: https://${DOMAIN}/"
echo ""
echo "Cloudflare settings:"
echo "  SSL/TLS encryption mode: Full (strict)"
echo "  Always Use HTTPS: On"
echo ""
echo "Renewal:"
echo "  certbot renew && cd ${APP_DIR} && docker compose -f docker-compose.yaml -f docker-compose.prod.yaml restart nginx_proxy"
