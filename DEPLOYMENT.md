# SKYGUARD Production Deployment

Production domain:

```text
https://app.pejmoneglejmo.me/
```

The app is configured to run behind the Cloudflare proxy.

## Cloudflare

Create or verify this DNS record:

```text
Type: A
Name: app
Value: <your VPS public IP>
Proxy status: Proxied
TTL: Auto
```

In Cloudflare SSL/TLS:

```text
SSL/TLS encryption mode: Full (strict)
Always Use HTTPS: On
Automatic HTTPS Rewrites: On
```

## VPS Setup

On a fresh Ubuntu VPS:

```bash
apt update && apt upgrade -y
apt install -y git curl certbot
curl -fsSL https://get.docker.com | sh
git clone https://github.com/kb8482-svg/SKYGUARD.git
cd SKYGUARD
```

Before starting Docker production mode, request the first certificate while port `80` is free:

```bash
certbot certonly --standalone -d app.pejmoneglejmo.me
```

Then start the app:

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build
```

Production Compose uses [docker-compose.prod.yaml](/home/uporabnik/nuksvaje/SKYGUARD/docker-compose.prod.yaml):

- exposes Nginx on `80` and `443`
- mounts `/etc/letsencrypt`
- uses [api-gateway/nginx-production.conf](/home/uporabnik/nuksvaje/SKYGUARD/api-gateway/nginx-production.conf)
- keeps MinIO and Prometheus internal

## One-Command Deploy Script

After DNS points to the VPS:

```bash
DOMAIN=app.pejmoneglejmo.me ./deploy-vps.sh
```

## Certificate Renewal

Renew certificates on the VPS:

```bash
certbot renew
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml restart nginx_proxy
```

Optional cron entry:

```cron
0 3 * * * certbot renew --quiet && cd /root/SKYGUARD && docker compose -f docker-compose.yaml -f docker-compose.prod.yaml restart nginx_proxy
```

## Verification

```bash
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml ps
curl -I https://app.pejmoneglejmo.me/
curl https://app.pejmoneglejmo.me/weather/
```

Expected app URL:

```text
https://app.pejmoneglejmo.me/
```
