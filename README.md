# NUKS-Vaje, Projekt
testni repo za vaje
 #
Cloud-native end-to-end encrypted chat aplikacija, razvita v okviru predmeta NUKS. Projekt sledi zahtevam predmeta: mikrostoritve, Docker Compose, API gateway, relacijska + nerelacijska baza, centralizirano logiranje, CI/CD in uporaba S3 API.

# 1 Povzetek ideje
Projekt NUKS 2026:
  * Vremenski načrtovalec dogodkov ali  » SKY GUARD«

<img width="666" height="444" alt="image" src="https://github.com/user-attachments/assets/3458d113-a33a-41d0-8eda-d342d7e440ac" />


## 1.2 OPIS IDEJE
** SkyGuard - Vremenski Načrtovalec 
Moj projekt spletne aplikacije (cloud native app) za načrtovanje dogodkov na prostem glede na vremensko napoved. 
Uporabnikom omogoča iskanje lokacij, spremljanje vremena v realnem času ( mogoče prejemanje personaliziranih opozoril, če vreme ogroža njihove načrtovane aktivnosti).

** CILJ : (za uporabnika) Aplikacija avtomatizira preverjanje vremenskih pogojev za specifične lokacije in čase dogodkov ter uporabnika opozori na morebitne neugodne razmere. 
** Arhitekturna zasnova sistema
Sistem je zasnovan na sodobni arhitekturi mikrostoritev, ki so med seboj neodvisne in povezane preko centralne vstopne točke.


<img width="836" height="558" alt="image" src="https://github.com/user-attachments/assets/059f6f98-2cbe-4d8e-ad8c-626870921cbf" />

* * Frontend (Uporabniški vmesnik): Razvit v tehnologiji WEBapp (React), omogoča dostop preko spletnih in mobilnih naprav.
* * API Gateway (Nginx): Služi kot varnostni in usmerjevalni sloj (proxy), ki vse zahtevke uporabnika varno posreduje ustreznim storitvam v ozadju.
* * Mikrostoritve:
o	User & Event Service (Go/Node.js): Upravlja z avtentikacijo uporabnikov in poslovno logiko dogodkov.
o	Weather Service (Python/FastAPI): Skrbi za komunikacijo z zunanjim OpenWeather API-jem in analizo vremenskih podatkov.
o	Storage & S3 Service (Node.js): Upravlja z datotekami in slikami preko S3 protokola.

## 1.3 Tehnološki sklad in podatkovni sloj
Aplikacija uporablja hibridni model shranjevanja podatkov, kar zagotavlja hitrost in integriteto:
•	Relacijska baza (PostgreSQL): Shranjevanje strukturiranih podatkov o uporabnikih, njihovih profilih in podrobnostih dogodkov.
•	Nerelacijska baza (MongoDB): Deluje kot predpomnilnik (cache) za vremenske podatke, kar zmanjšuje odvisnost od zunanjega API-ja in povečuje odzivnost sistema.
•	Objektna shramba (Min.io): S3-združljiva shramba za trajno shranjevanje slik dogodkov in sistemskih dnevnikov (logov).

## 1.4 Razvojni proces in nadzor (Observability)
Projekt sledi standardom sodobnega inženirstva programske opreme:

•	CI/CD (GitHub Actions): Celoten postopek gradnje Docker slik in objave aplikacije je avtomatiziran.
•	Centralizirano logiranje in metriki: Za spremljanje stanja sistema se uporabljata Prometheus (metriki) in Grafana (vizualizacija logov), kar omogoča hiter odziv na morebitne napake.

# 2 API klici in plan segnemtcije storitev
## 2.1 Koraki : Plan segnemtacije mikrostoritev

  * User & Event service
  * Weather service
  * Storage
 
 /frontend (React aplikacija)   


/user-event-service (Go/Node.js)   


/weather-service (Python/FastAPI)   


/storage-service (Node.js)   


/nginx (API Gateway)

## 2.2 API dokumentacija
### User & Event service

+ ``POST /auth/register `` Registracija novega uporabnika,  
+ ``POST /auth/login`` Prijava uporabnika in pridobitev žetona,  
+ ``GET /events`` Seznam vseh načrtovanih dogodkov uporabnika,
+ ``POST /events`` Ustvarjanje novega dogodka (lokacija, čas),
+ ``DELETE /events/{id} `` Brisanje načrtovanega dogodka.

### Weather service

 
+ ``GET /weather/current`` Seznam vseh načrtovanih dogodkov uporabnika,
+ ``GET /weather/forecast`` Vremenska napoved za čas dogodka
+ `GET /weather/alerts ` Pridobivanje opozoril.

### Storage & S3 Service

+ ``POST /storage/upload `` Nalaganje slik dogodkov v Min.io. 
+ ``GET /storage/image/{id}`` Pridobivanje povezave do slike.

 ###  Media Service (Port 8004)

### 2.3 API Gateway (Port 8000 + NGINX 80/443)
**Frontend:** NGINX | **Backend:** FastAPI (Python)


