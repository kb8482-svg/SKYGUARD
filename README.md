# NUKS-vajetestrepo
testni repo za vaje
 #
Cloud-native end-to-end encrypted chat aplikacija, razvita v okviru predmeta NUKS. Projekt sledi zahtevam predmeta: mikrostoritve, Docker Compose, API gateway, relacijska + nerelacijska baza, centralizirano logiranje, CI/CD in uporaba S3 API.

# 1 Povzetek ideje
Projekt NUKS 2026:
  * Vremenski načrtovalec dogodkov ali  » SKY GUARD«

<img width="666" height="444" alt="image" src="https://github.com/user-attachments/assets/3458d113-a33a-41d0-8eda-d342d7e440ac" />

skica2
<img width="836" height="558" alt="image" src="https://github.com/user-attachments/assets/059f6f98-2cbe-4d8e-ad8c-626870921cbf" />

* (1)	OPIS IDEJE
 (SkyGuard - Vremenski Načrtovalec) 
Moj projekt spletne aplikacije (cloud native app) za načrtovanje dogodkov na prostem glede na vremensko napoved. Uporabnikom omogoča iskanje lokacij, spremljanje vremena v realnem času ( mogoče prejemanje personaliziranih opozoril, če vreme ogroža njihove načrtovane aktivnosti) .
CILJ : (za uporabnika) Aplikacija avtomatizira preverjanje vremenskih pogojev za specifične lokacije in čase dogodkov ter uporabnika opozori na morebitne neugodne razmere. 
(2)	Arhitekturna zasnova sistema
Sistem je zasnovan na sodobni arhitekturi mikrostoritev, ki so med seboj neodvisne in povezane preko centralne vstopne točke.
•	Frontend (Uporabniški vmesnik): Razvit v tehnologiji WEBapp (React), omogoča dostop preko spletnih in mobilnih naprav.
•	API Gateway (Nginx): Služi kot varnostni in usmerjevalni sloj (proxy), ki vse zahtevke uporabnika varno posreduje ustreznim storitvam v ozadju.
•	Mikrostoritve:
o	User & Event Service (Go/Node.js): Upravlja z avtentikacijo uporabnikov in poslovno logiko dogodkov.
o	Weather Service (Python/FastAPI): Skrbi za komunikacijo z zunanjim OpenWeather API-jem in analizo vremenskih podatkov.
o	Storage & S3 Service (Node.js): Upravlja z datotekami in slikami preko S3 protokola.
3. Tehnološki sklad in podatkovni sloj
Aplikacija uporablja hibridni model shranjevanja podatkov, kar zagotavlja hitrost in integriteto:
•	Relacijska baza (PostgreSQL): Shranjevanje strukturiranih podatkov o uporabnikih, njihovih profilih in podrobnostih dogodkov.
•	Nerelacijska baza (MongoDB): Deluje kot predpomnilnik (cache) za vremenske podatke, kar zmanjšuje odvisnost od zunanjega API-ja in povečuje odzivnost sistema.
•	Objektna shramba (Min.io): S3-združljiva shramba za trajno shranjevanje slik dogodkov in sistemskih dnevnikov (logov).
4. Razvojni proces in nadzor (Observability)
Projekt sledi standardom sodobnega inženirstva programske opreme:
•	CI/CD (GitHub Actions): Celoten postopek gradnje Docker slik in objave aplikacije je avtomatiziran.
•	Centralizirano logiranje in metriki: Za spremljanje stanja sistema se uporabljata Prometheus (metriki) in Grafana (vizualizacija logov), kar omogoča hiter odziv na morebitne napake.
