1. Totalt antal mätningar
Räknar alla rader i tabellen measurements.
Resultat från första mätningen 2026-08-20 count 1242 (1 row).
SELECT COUNT(*)
FROM measurements;


2. Medeltemperatur med AVG
Beräknar den genomsnittliga temperaturen för alla mätningar.
Resultat från första mätningen 2026-08-20 avg 21.3837363344051447 (1 row).
SELECT AVG(temperature)
FROM measurements;


3. Mätningar från de senaste 24 timmarna
Hämtar alla mätningar som skapats under de senaste 24 timmarna.
Resultat från första mätningen 2026-08-20: 1682 | sensor-001 |       21.83 |    64.98 |      40 | 2026-08-20 12:21:40.968081
                                           1683 | sensor-002 |       20.71 |    47.33 |      72 | 2026-08-20 12:21:41.002116
                                           1684 | sensor-003 |       23.44 |    44.69 |      72 | 2026-08-20 12:21:41.029542
(969 rows).
SELECT *
FROM measurements
WHERE created_at >= NOW() - INTERVAL '24 hours';