# Jensen IoT Platform – studentguide

Detta starter-repository hör till uppgiftsunderlaget **Labb för DDM**. Uppgiftsunderlaget beskriver syfte, milstolpar, bedömning, deadline och inlämning. Repositoryt innehåller de praktiska instruktionerna, startkoden och övningarna.

## Hitta rätt

- [docs/lab-guide.md](docs/lab-guide.md) – steg-för-steg-instruktioner för alla fyra milstolpar
- [docs/architecture.md](docs/architecture.md) – instruktion och mall för arkitekturdiagrammet
- [docs/reflection.md](docs/reflection.md) – obligatoriska reflektionsfrågor
- `api/` – Flask-API, databas- och cachekod samt tester
- `simulator/` – tre simulerade IoT-sensorer
- `database/init.sql` – databastabeller och startdata
- `k8s/` – färdiga manifest för den introducerande Kubernetes-övningen

## Verktyg som behövs

Installera innan du börjar:

1. Git och ett GitHub-konto.
2. Docker Desktop (Windows/macOS) eller Docker Engine med Docker Compose-plugin (Linux).
3. En valfri kodeditor, exempelvis Visual Studio Code.
4. Inför milstolpe 3: `kubectl` och Minikube.

Python behöver inte installeras lokalt för grunduppgifterna; Python och beroenden finns i containrarna. Kontrollera installationerna i PowerShell, Terminal eller ett Linux-skal:

```text
git --version
docker --version
docker compose version
kubectl version --client
minikube version
```

> Windows: använd PowerShell och kör Docker Desktop innan Docker-kommandona. Kommandona i guiden är desamma på Windows, macOS och Linux. Där ett kommando skiljer sig anges det uttryckligen.

## Start här – första 10 minuterna

### 1. Skapa och klona din fork

Skapa en fork av kursens starter-repository på GitHub. Kopiera URL:en till **din fork** och kör:

```text
git clone <URL-TILL-DIN-FORK>
cd <REPOSITORY-MAPP>
```

Kontrollera att du står i repositoryts rot, alltså mappen som innehåller `docker-compose.yml`. Alla Docker Compose-kommandon i guiden ska köras därifrån.

### 2. Kontrollera Docker

Starta Docker Desktop på Windows/macOS eller Docker Engine på Linux. Kontrollera sedan installationen:

```text
docker info
docker compose version
```

Båda kommandona ska fungera utan fel. Ingen `.env`-fil eller lokal Python-installation behövs; projektet har fungerande standardvärden och kör Python i containern.

### 3. Bygg och starta miljön

```text
docker compose up --build -d
docker compose ps
```

`docker compose ps` ska visa tjänsterna `api`, `simulator`, `db` och `redis`. Databasen ska efter en kort stund visa `healthy`. Om någon tjänst fortfarande startar, vänta några sekunder och kör statuskommandot igen.

### 4. Kontrollera API:t

Öppna följande adresser:

- <http://localhost:5001> – enkel startsida
- <http://localhost:5001/health> – ska visa `"status": "ok"`
- <http://localhost:5001/devices> – ska visa tre sensorer
- <http://localhost:5001/measurements> – ska visa en tom lista `[]`, ***Men nu efter implentering visar sparade mätningar.***

Den tomma listan är förväntad. Simulatorns giltiga data tas emot men sparas inte förrän du har implementerat lagringen i milstolpe 1.
***Men eftersom milstolpe 1 nu är färdig är det inte längre en tom lista utan tidigare mätningar.***

### 5. Följ simulatorn

```text
docker compose logs -f simulator
```

Från början returnerar API:t status `202` för giltiga mätningar. `sensor-003` skickar ibland avsiktligt felaktig data och ska då få `400`. Det är förväntat. Avsluta den löpande loggvisningen med `Ctrl+C`; tjänsterna fortsätter att köras i bakgrunden.
***Men eftersom milstolpe 1 nu är färdig retunerar `201` för giltiga mätningar.***

### 6. Ändra och testa koden

Du kommer främst att arbeta i:

- `api/app.py` – endpoints och HTTP-statuskoder
- `api/db.py` – PostgreSQL-frågor
- `api/cache.py` – Redis-cache
- `api/validation.py` – valideringsregler
- `api/tests/` – automatiserade tester

Källkoden kopieras in i Docker-imagen. Bygg därför om efter kodändringar och kör testerna:

```text
docker compose up --build -d
docker compose exec api python -m pytest -q
```

Visa API-loggen om något går fel:

```text
docker compose logs --tail=100 api
```

### 7. Stoppa miljön

```text
docker compose down
```

Databasen sparas i en Docker-volym och finns kvar till nästa start. Använd endast följande kommando om du avsiktligt vill radera all lokal databasdata för labben:

```text
docker compose down -v
```

Fortsätt nu till [docs/lab-guide.md](docs/lab-guide.md) och genomför milstolparna i ordning.

## Om starten misslyckas

- Kontrollera att Docker Desktop/Docker Engine körs med `docker info`.
- Kör kommandot från repositoryts rot.
- Om port `5001` används av ett annat program: stoppa programmet eller starta med en annan port. PowerShell: `$env:API_PORT=5002; docker compose up --build`. macOS/Linux: `API_PORT=5002 docker compose up --build`.
- Visa status med `docker compose ps` och loggar med `docker compose logs api db redis simulator`.
- Om en kodändring inte syns, kontrollera att du har kört `docker compose up --build -d` efter ändringen.



# Slutrapport – Genomförda milstolpar

## Sammanfattning

Projektet har utvecklats från starterkod till en fungerande IoT-plattform med ett Flask-baserat REST API, PostgreSQL, Redis, Docker Compose, CI och Kubernetes.

## Milstolpe 1 – REST API och PostgreSQL

De obligatoriska REST-endpoints har implementerats för att ta emot, validera, lagra och hämta sensordata.

Implementationen omfattar:

* validering av inkommande mätningar
* kontroll av att sensorn finns
* lagring av mätningar i PostgreSQL
* hämtning av de senaste mätningarna
* hämtning av historik per sensor
* relevanta HTTP-statuskoder

Giltiga mätningar returnerar **HTTP 201** och ogiltiga mätningar eller okända sensorer returnerar **HTTP 400**.

## Milstolpe 2 – Docker och Redis-cache

PostgreSQL används som beständig lagring och data finns kvar efter att Docker-containrarna stoppas och startas igen.

Redis används som cache för den senaste mätningen per sensor.

Vid anrop till:

```text
GET /devices/{id}/latest
```

läser API:t först från Redis. Vid cache miss hämtas den senaste mätningen från PostgreSQL och sparas därefter i Redis.

När en ny mätning sparas uppdateras även motsvarande cachepost i Redis.

PostgreSQL är den beständiga datakällan. Om Redis töms kan den senaste mätningen hämtas från PostgreSQL och därefter cachelagras i Redis igen.

## Milstolpe 3 – CI och Kubernetes

En GitHub Actions-workflow har konfigurerats för att köra projektets tester och bygga API:ts Docker-image.

Kubernetes-delen har genomförts i Minikube. API:t har distribuerats med Kubernetes Deployment och Service.

Följande har verifierats:

* tre repliker av API:t
* self-healing genom att en Pod raderades och ersattes automatiskt
* scaling från tre till fem repliker och tillbaka till tre

## Milstolpe 4 – Dokumentation och reflektion

Projektets dokumentation har färdigställts i samband med inlämningen.

Följande dokument ingår:

* [Arkitekturdokumentation](docs/architecture.md)
* [Reflektionsdokument](docs/reflection.md)
* [SQL-frågor](docs/sql-queries.sql)

## Verifiering och tester

Projektet byggs och startas med:

```bash
docker compose up --build -d
```

Tjänsternas status kan kontrolleras med:

```bash
docker compose ps
```

Automatiserade tester körs med:

```bash
docker compose exec api python -m pytest -q
```

Simulatorn används för att verifiera att giltiga mätningar returnerar **201** och att avsiktligt felaktiga mätningar returnerar **400**.

## SQL-frågor

De tre obligatoriska SQL-frågorna finns i [docs/sql-queries.sql](docs/sql-queries.sql).

Frågorna omfattar:

1. Totalt antal mätningar med `COUNT`
2. Medeltemperatur med `AVG`
3. Mätningar från de senaste 24 timmarna

## PostgreSQL och Redis

PostgreSQL används för permanent lagring av sensordata.

Redis används som cache för den senaste mätningen per sensor.

Vid en cache miss hämtas informationen från PostgreSQL och läggs därefter tillbaka i Redis. Detta innebär att Redis kan tömmas utan att den underliggande sensordatan försvinner.

## Kubernetes

API:t har distribuerats i Minikube med Kubernetes Deployment och Service.

Self-healing verifierades genom att en Pod raderades och ersattes automatiskt av Kubernetes.

Scaling verifierades genom att antalet repliker ändrades från tre till fem och därefter tillbaka till tre.

## CI

Projektet innehåller en GitHub Actions-workflow som kör testerna och bygger API:ts Docker-image.

Den senaste CI-körningen har verifierats som grön.

## Dokumentation

Projektets dokumentation finns i:

* [docs/architecture.md](docs/architecture.md)
* [docs/reflection.md](docs/reflection.md)
* [docs/sql-queries.sql](docs/sql-queries.sql)

## Kända begränsningar

Fördjupningsfunktionen `/statistics` är inte implementerad eftersom den var frivillig och tidsbegräningar fanns.

Kubernetes-demon omfattar endast REST API:t. PostgreSQL, Redis och simulatorn körs lokalt med Docker Compose enligt laborationens avgränsning.

## Slutlig verifiering

Följande delar har verifierats innan inlämning:

* REST API fungerar
* PostgreSQL lagrar mätningar
* Redis-cache fungerar
* Docker Compose-miljön fungerar
* SQL-frågorna är genomförda och dokumenterade
* Automatiserade tester är genomförda
* CI-körningen är grön
* Kubernetes self-healing är genomförd
* Kubernetes scaling är genomförd
* Dokumentationen är färdig
* Reflektionsfrågorna är besvarade