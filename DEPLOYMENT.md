# 🚀 SKYGUARD Production Deployment Guide

## 📋 Preduvjeti

- Cloudflare račun (imaš ✅)
- Domena `pejmoneglejmo.me` (imaš ✅)
- VPS server (preporuka: DigitalOcean, Linode, Hetzner)
- SSH pristup na server

---

## ⚡ QUICK DEPLOYMENT (15 minuta)

### 1️⃣ **Kreiraj DigitalOcean Droplet**

```bash
1. Idi na https://www.digitalocean.com/
2. Klikni "Create" → "Droplet"
3. Odaberi:
   - Region: Frankfurt (ili najbliži)
   - OS: Ubuntu 22.04 LTS
   - Size: $6/mj
   - Authentication: SSH Key
4. Klikni "Create"
5. Sačuvaj IP adresu (npr: 165.227.1.1)
```

### 2️⃣ **Cloudflare DNS Konfiguracija**

Idi na Cloudflare dashboard (`pejmoneglejmo.me`):

```
DNS → Dodaj A Record:
┌─────────────────────────────────────┐
│ Type: A                             │
│ Name: pejmoneglejmo.me              │
│ Value: 165.227.1.1 (tvoja IP)       │
│ TTL: Auto                           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Type: A                             │
│ Name: www                           │
│ Value: 165.227.1.1                  │
│ TTL: Auto                           │
└─────────────────────────────────────┘

SSL/TLS → Edge Certificates:
✅ Always Use HTTPS
✅ Full Mode (ili Flexible ako problem)
```

### 3️⃣ **SSH Deploy Script**

Logiraj se na server i pokreni:

```bash
# SSH na server
ssh root@165.227.1.1

# Kopija i pokreni deploy script
curl -O https://raw.githubusercontent.com/kb8482-svg/SKYGUARD/main/deploy-vps.sh
chmod +x deploy-vps.sh
./deploy-vps.sh
```

Ili ručno:

```bash
# UPDATE SISTEM
apt update && apt upgrade -y
apt install -y curl git docker.io

# INSTALIRAJ DOCKER COMPOSE
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# KLONIRAJ PROJEKT
cd /root
git clone https://github.com/kb8482-svg/SKYGUARD.git
cd SKYGUARD

# POKRENITE SERVISE
docker-compose up -d

# ČEKAJ 30 SEKUNDI
sleep 30

# PROVJERA ZDRAVLJA
curl http://localhost:8000/
```

### 4️⃣ **SSL Certifikat sa Let's Encrypt**

```bash
# INSTALIRAJ CERTBOT
apt install -y certbot python3-certbot-nginx

# KREIRAJ CERTIFIKAT
certbot certonly --standalone -d pejmoneglejmo.me -d www.pejmoneglejmo.me

# Sačuvaj putanju certifikata - trebat će ti za nginx config
# Obično: /etc/letsencrypt/live/pejmoneglejmo.me/
```

### 5️⃣ **Update Nginx Config sa SSL**

```bash
# Kopija production config
cp api-gateway/nginx-production.conf /etc/nginx/conf.d/default.conf

# Test nginx config
nginx -t

# Reload nginx
systemctl restart nginx
```

### 6️⃣ **Update Docker-Compose**

Dodaj u `docker-compose.yaml`:

```yaml
nginx_proxy:
  image: nginx:latest
  container_name: nginx_proxy
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./api-gateway/nginx-production.conf:/etc/nginx/conf.d/default.conf:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro
  depends_on:
    - frontend
    - user-service
    - weather-service
    - storage-service
  restart: unless-stopped
```

---

## ✅ **Provjera Deploymenta**

```bash
# 1. Provjera ako su servisi pokrenuti
docker-compose ps

# 2. Test API-ja
curl https://pejmoneglejmo.me/auth/
curl https://pejmoneglejmo.me/weather/
curl https://pejmoneglejmo.me/storage/

# 3. Provjera SSL certifikata
curl -vI https://pejmoneglejmo.me/

# 4. Logovi ako nešto ne radi
docker-compose logs -f nginx_proxy
docker-compose logs -f frontend
```

---

## 🔒 **Security Best Practices**

### 1. Firewall

```bash
# UFW na VPS-u
ufw enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw status
```

### 2. Environment Variables

Ne drži lozinke u docker-compose.yaml! Koristi `.env`:

```bash
# .env file
POSTGRES_PASSWORD=secure_password_123
MINIO_ROOT_PASSWORD=secure_password_456
```

### 3. Redoviti Backups

```bash
# Backup baza podataka
docker-compose exec postgres-db pg_dump skyguard_auth > backup.sql
docker-compose exec mongo-db mongodump --out backup
```

### 4. SSL Auto-Renewal

```bash
# Certbot automatski renew (cron job)
certbot renew --quiet --no-eff-email
```

---

## 📊 **Monitoring i Logging**

### Prometheus Dashboard
```
https://pejmoneglejmo.me/prometheus/
```

### Logovi
```bash
# Follow svi logovi
docker-compose logs -f

# Specifični service
docker-compose logs -f weather-service
```

---

## 🆘 **Troubleshooting**

### Port 80/443 zauzeti?
```bash
# Pronađi koji proces koristi port
lsof -i :80
lsof -i :443

# Kill proces
kill -9 <PID>
```

### SSL Certifikat nije validan?
```bash
# Provjera certifikata
ssl-cert-check -c /etc/letsencrypt/live/pejmoneglejmo.me/cert.pem

# Renew
certbot renew --force-renewal
```

### Servisi se pada?
```bash
# Provjera resursa
docker stats

# Restart servisa
docker-compose restart weather-service

# Čitav reset
docker-compose down -v
docker-compose up -d --build
```

---

## 📈 **Upgrade & Skaliranje**

Kada aplikacija raste:

1. **Veći Droplet** - Idi sa $6 na $12 ili više
2. **Load Balancer** - Cloudflare Pages ili własny LB
3. **CDN** - Cloudflare CDN za statične datoteke
4. **Database** - Managed PostgreSQL + MongoDB
5. **Kubernetes** - Za enterprise deployment

---

## 🎯 **Sljedeći Koraci**

1. ✅ Kreiraj DigitalOcean Droplet
2. ✅ Konfiguruj Cloudflare DNS
3. ✅ Pokreni deploy script
4. ✅ Setup SSL sa Certbot
5. ✅ Update nginx config
6. ✅ Restart Docker servise
7. ✅ Test https://pejmoneglejmo.me/

---

## 📞 **Support**

Ako nešto ne radi:

```bash
# 1. Provjera health check-a
curl -v https://pejmoneglejmo.me/

# 2. Logovi nginx-a
docker-compose logs nginx_proxy

# 3. Restart sve
docker-compose restart

# 4. Rebuild ako trebas
docker-compose up -d --build
```

---

**Gotovo! 🚀 Aplikacija je na Production Server!**
