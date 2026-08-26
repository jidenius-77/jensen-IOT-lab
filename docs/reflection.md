# Reflektionsdokument – obligatorisk leverabel

1. ***Varför ska sensorerna kommunicera med ett API i stället för direkt med PostgreSQL?*** - 
Sensorerna bör kommunicera med ett API eftersom API:t fungerar som ett lager mellan sensorerna och databasen. Där kan inkommande data valideras och kontrolleras innan den sparas. Sensorerna behöver då inte känna till hur databasen är uppbyggd eller ha direkt tillgång till PostgreSQL. Det gör också lösningen säkrare och enklare att förändra.

2. ***Varför ska felaktig sensordata stoppas innan den sparas?*** - 
Felaktig data bör stoppas innan den sparas för att databasen inte ska fyllas med ogiltiga mätvärden. I laborationen valideras bland annat deviceId, temperatur, luftfuktighet och batterinivå. Simulatorn skickar ibland medvetet felaktig data från sensor-003, vilket gjorde det möjligt att kontrollera att API:t returnerade HTTP 400 och inte sparade mätningen.

3. ***Varför passar PostgreSQL för historiska mätvärden?*** - 
PostgreSQL passar bra för historiska mätvärden eftersom informationen lagras beständigt och kan sökas med SQL. I laborationen kunde jag till exempel räkna antalet mätningar, beräkna medeltemperaturen och hämta mätningar från de senaste 24 timmarna. Med Docker-volymen finns datan även kvar när containrarna stoppas och startar upp igen.

4. ***Vad händer med lösningen om Redis försvinner?*** - 
Redis innehåller bara cache för den senaste mätningen, medan den beständiga datan finns i PostgreSQL. Om innehållet i Redis töms kan den senaste mätningen hämtas från PostgreSQL och sedan cachelagras igen.

5. ***Vad händer med lösningen om PostgreSQL försvinner?*** - 
Om PostgreSQL försvinner påverkas lösningen betydligt mer eftersom PostgreSQL är den beständiga datakällan. Nya mätningar kan inte sparas och historiska mätningar kan inte hämtas. Redis kan fortfarande innehålla vissa redan cachelagrade senaste mätningar, men det ersätter inte databasen och innehåller inte hela historiken.

6. ***Varför används Docker Compose lokalt?*** - 
Docker Compose används för att enkelt kunna starta alla delar av lösningen tillsammans. I projektet består den lokala miljön av API, simulator, PostgreSQL och Redis. Med ett kommando kan hela miljön byggas och startas på samma sätt, vilket gör utveckling och testning enklare och minskar skillnader mellan olika datorer.

7. ***Vad automatiserar din CI-pipeline?*** - 
CI-pipelinen i GitHub Actions körs vid push eller pull request. Den installerar projektets beroenden, kör pytest-testerna och bygger API:ts Docker-image. På så sätt upptäcks fel automatiskt och kan kontrollera att projektet fortfarande fungerar efter kodändringar.

8. ***Vad observerade du när du tog bort en Kubernetes Pod?*** - 
När jag tog bort en av de tre Podarna skapade Kubernetes automatiskt en ny Pod. Antalet repliker gick därför tillbaka till det antal som var definierat i Deployment. Det visade hur Kubernetes använder self-healing för att försöka hålla systemet i det önskade tillståndet som var tre.

9. ***Varför kan flera repliker ge högre tillgänglighet?*** - 
Med flera repliker finns det flera Podar som kan hantera trafiken. Om en Pod slutar fungera finns de andra fortfarande kvar och kan fortsätta ta emot anrop medan Kubernetes skapar en ersättare. Det minskar risken att hela API:t blir otillgängligt på grund av att en Pod går ner.

10. ***När hade Kubernetes varit overkill för en lösning?*** - 
Kubernetes kan vara overkill för en liten lösning med få användare och några få tjänster. För ett mindre projekt som endast ska köras på en dator kan Docker Compose vara betydligt enklare att konfigurera och underhålla. Kubernetes blir mer användbart när det finns större behov av skalning, hög tillgänglighet, self-healing och hantering av många containrar.
