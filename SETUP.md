# 🛡️ SKYGUARD Setup - Lokalna Konfiguracija

## 📋 Provjera Statusne Servisa

```bash
cd /home/uporabnik/nuksvaje/SKYGUARD
docker-compose ps
```

### Očekivani Status:
- ✅ postgres-db (Up)
- ✅ mongo-db (Up)
- ✅ minio (Up)
- ✅ user-service (Up)
- ✅ weather-service (Up)
- ✅ storage-service (Up)
- ✅ frontend (Up)
- ✅ nginx_proxy (Up)

## 🌐 Pristup Aplikaciji

### Frontend - Nadzorna Plošča
```
http://localhost:8000/
```

### API Endpoints (kroz nginx proxy):
- **Auth Service:** http://localhost:8000/auth/
- **Weather Service:** http://localhost:8000/weather/
- **Storage Service:** http://localhost:8000/storage/

### Min.io Console (S3 Upravljanje)
```
http://localhost:9001/
Username: user-04
Password: thestrongestavajePass04
```

### Prometheus (Monitoring)
```
http://localhost:9090/
```

## 🔌 API Primjeri

### 1. Registracija Korisnika
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass123"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass123"}'
```

Response će sadržavati JWT token koji se koristi za autentifikaciju.

### 3. Provjera Vremenske Prognoze
```bash
curl http://localhost:8000/weather/
```

### 4. Upload Slike na Min.io
```bash
curl -X POST http://localhost:8000/storage/upload/ \
  -F "file=@/path/to/image.jpg"
```

## 🏗️ Arhitektura Servisa

### Frontend (Nginx - Port 3000 interno, 8000 javno)
- Nadzorna plošča sa HTML/CSS/JavaScript
- Omogućava registraciju, login, upload datoteka, provjeru vremenske prognoze

### User Service (Node.js/Express - Port 5001)
- POST /auth/register - Registracija
- POST /auth/login - Login sa JWT tokenima
- PostgreSQL baza za korisnike

### Weather Service (Python/FastAPI - Port 5002)
- GET /weather/ - Dohvaćanje vremenske prognoze
- Koristi Open-Meteo API (besplatan, bez API ključa)
- MongoDB za cachiranje

### Storage Service (Python/FastAPI - Port 5003)
- POST /upload/ - Upload datoteka na Min.io
- GET /image/{id} - Dohvaćanje slike
- Koristi boto3 za S3 API

### API Gateway (Nginx - Port 8000)
- Proxy za sve servise
- Omogućava pristup iz brsera bez CORS problema

## 📊 Baze Podataka

### PostgreSQL (localhost:5432)
```
Username: skyguard_user
Password: password123
Database: skyguard_auth
```

### MongoDB (localhost:27017)
```
Nema autentifikacije
Database: skyguard_weather
```

### Min.io S3 (localhost:9000)
```
Access Key: user-04
Secret Key: thestrongestavajePass04
Bucket: skyguard
```

## 🔄 Pokretanje & Zaustavljanje

### Pokrenuti sve servise
```bash
docker-compose up -d
```

### Zaustaviti sve servise
```bash
docker-compose down
```

### Revidiati logove
```bash
docker-compose logs -f [service-name]
```

### Ponovno izgraditi images
```bash
docker-compose up -d --build
```

## ⚙️ Konfiguracije

### nginx.conf
- Lokacija: `./api-gateway/nginx.conf`
- Proxy konfiguracija za sve servise
- Server name: localhost, 127.0.0.1, pejmoneglejmo.me

### docker-compose.yaml
- Definiše sve servise
- Volume mounting za baze podataka
- Network - svi servici na istoj mreži

### Dockerfile-ovi
- `user-service/Dockerfile` - Node.js
- `weather-service/Dockerfile` - Python
- `storage-service/Dockerfile` - Python
- `frontend/Dockerfile` - Nginx

## 🚨 Troubleshooting

### Port već korišten
```bash
# Pronađite proces koji koristi port 8000
lsof -i :8000

# Zaustavite kontejner
docker-compose down
```

### Baza podataka se ne podignuće
```bash
# Očistite volume
docker-compose down -v

# Ponovno pokrenite
docker-compose up -d
```

### Service se rušti
```bash
# Provjerite logove
docker-compose logs service-name

# Ponovno pokrenite service
docker-compose restart service-name
```

## 📝 CI/CD Pipeline

GitHub Actions automatski:
1. Gradi Docker slike za sve servise
2. Testira docker-compose konfiguraciju
3. Provjerava da li API gateway reagira

Workflow je u: `.github/workflows/docker-build.yml`

## ✨ Što je Ispravljeno

1. ✅ Storage Service - Dodano `requirements.txt` sa boto3
2. ✅ Frontend - Implementiran `uploadFile()` sa HTTP error handling
3. ✅ CI/CD Pipeline - Kreirane GitHub Actions workflow datoteke
4. ✅ Docker Compose - Poboljšana startup order konfiguracija
5. ✅ Nginx Proxy - Svi rute funkcioniraju pravilno
6. ✅ Min.io - Integrirano sa Storage Service (S3 API)

## 📊 Testirane Rute

Svi API endpoints su testirani i funkcionalni:
- Frontend HTML ✅
- `/auth/register` ✅
- `/auth/login` ✅
- `/weather/` ✅
- `/storage/` ✅

## 🎯 Sljedeći Koraci

1. Konfiguracija DNS-a za domenu `pejmoneglejmo.me`
2. SSL certifikat (Let's Encrypt)
3. Deployment na production server
4. Monitoring sa Prometheom i Grafanom
5. Centralizirano logiranje sa ELK stackom

---

**Projekt je uspješno konfiguriran za lokalno testiranje!** 🎉
