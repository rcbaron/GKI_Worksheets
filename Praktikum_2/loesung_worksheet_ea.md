# Lokale Suche und GA

## EA.01: Modellierung von GA

## Landkarten-Färbe-Problem

### Ziel:
- Jedem Land auf der Landkarte eine bestimmte Farbe zuweisen.
- Nebeneinander liegende Länder sollen nicht die gleiche Farbe haben
- Die kleinste mögliche Menge an individuellen Farben

### Kodierung:
- Ein Vektor mit reellen Zahlen [0 bis n] Bei dem der Index die Länder sind und die Zahlen die Farben repräsentieren
- [1, 0, 2, 0, 1, 2] -> Index: Länder, Werte: Farben

### Fitness:
1 - (Anzahl Konflikte / maximale Konflikte)

### Crossover:
Schneidet Vektor zweier Elternteile durch und Vertauscht diese

Elternteil1 -> [1, 0, 2, 0, 1, 2], Elternteil2 -> [2, 1, 0, 1, 2, 1], Kind1 -> [1, 0, 2, 1, 2, 1], Kind2 -> [2, 1, 0, 0, 1, 2]

### Mutation:

Wählt eine Zufällige Farbe eines Individuum und vertauscht die Farbe mit einer anderen aus der vorhandenen Menge an Farben


## N - Queens - Problem

### Ziel:
- Ein Feld aus N * N Zellen mit N Damen die sich gegenseitig nicht schlagen können.

### Kodierung:
- Ein Vektor mit reellen Zahlen [0 bis n] Bei dem der Index die Spalte auf der sich die Dame befindet und die Zahl repräsentiert die Zeile der Dame

### Fitness:

1 - (Anzahl der Konflikte / maximale Konflikte)

Konflikte berechnen sich durch: n*(n-1)/2

### Crossover:
Geordnete Crossover:
- Schneidet einen Teilbereich eines Elternteils zu und fügt es in ein neues Individuum, der rest wird aus dem Teilbereich des zweiten Elternteils aufgefüllt.

### Mutation:

Wählt zufällig zwei Spalten aus und Vertauscht die beiden miteinander.



## EA.02: Implementierung:

[Implementierung](https://github.com/rcbaron/GKI_Worksheets/blob/main/Praktikum_2/genetischer_algorithmus/main.py)

<img width="1380" height="1146" alt="image" src="https://github.com/user-attachments/assets/9a26030f-3a84-497d-98f3-dd291187aee2" />

Ausgewertet wurden die Operatoren für das Crossover, Generationen und Populationsgrößen über 100 Durchläufe 
die die Success Rate - SR (Erfolgrate) und Average Evaluation to Solution - AES (Durchschnittliche Generationen bis zur Lösung) angeben.



## EA.03: Anwendungen:

## 1) Randal Olson – “Here’s Waldo” 
Randal Olson hat mit einem genetischen Algorithmus (GA) die optimale 
Suchstrategie für „Wo ist Waldo?“ berechnet. 
Dazu hat er die möglichen Waldo-Positionen (insgesamt 68) als Punkte auf einer 
Karte genommen und wollte die Reihenfolge finden, in der man Waldo am 
schnellsten finden würde (eine Art Travelling Salesman Problem).

### Kodierung: 
Jedes Individuum ist eine Permutation dieser 68 Punkte, also eine Reihenfolge, in 
der die Positionen besucht werden sollen. 
→ Chromosom = Liste von Indizes, z. B. [17, 4, 1, 12, ...]. 

### Fitnessfunktion: 
Bewertet wird die Gesamtlänge des Weges. Je kürzer der Weg, desto besser die 
Fitness. 

(Man kann die Fitness auch als 1 / Distanz oder als negative Distanz ausdrücken.) 

Mutation: Zwei Positionen werden vertauscht oder ein Teil der Liste wird umgedreht. 
Crossover: Kombination von zwei Routen (z. B. Order Crossover). 
Selektion: Die besten Individuen werden bevorzugt weitergegeben. 

### Ziel: 
Der GA findet eine möglichst kurze Route, also eine gute Suchstrategie für Waldo. 


## 2) Evolution Simulator (MinuteLabs) 
Der Evolution Simulator zeigt, wie einfache künstliche Lebewesen sich durch 
Mutation und Selektion an ihre Umgebung anpassen. 
Es ist also ein visueller, vereinfachter Evolutionsalgorithmus. 

### Kodierung: 
Jedes Lebewesen hat eine Datenstruktur mit Parametern wie: - - - - 
Größe 
Geschwindigkeit 
Sichtweite (wie weit er Nahrung sieht) 
evtl. Farbe oder Energie 
Diese Werte sind meist Fließkommazahlen (z. B. size = 0.8, speed = 1.2). 

### Fitnessfunktion: 
Es gibt keine mathematische Funktion, sondern es ergibt sich aus dem Verhalten: - 
Wer überlebt, weil er Nahrung findet 

Wer sich fortpflanzt, somit Erfolg hat und seine Gene weitergibt. -> Fitness = Überlebens- und Reproduktionsrate. 

Mutation: Kleine zufällige Änderungen an den Genwerten (z. B. Geschwindigkeit ± 0.1). 

Reproduktion: Erfolgreiche Individuen erzeugen neue Lebewesen mit leicht veränderten Genen. 

Selektion: Nur Lebewesen, die überleben, vermehren sich → natürliche Selektion. 

## 3) American Fuzzy Lop (AFL) 
AFL ist ein Software-Testing-Tool, das mit einer Art genetischem Algorithmus neue 
Programm-Inputs erzeugt, um Bugs und Abstürze zu finden. 
Man kann sich jedes Input-File als ein „Individuum“ vorstellen. 

### Kodierung: 
Individuum = Input-Datei (Byte-Array), das an das Programm gegeben wird. 

### Fitnessfunktion: 
AFL misst, wie „interessant“ ein Input ist: -> Wie viel neue Programmpfade (Coverage) dieser Input auslöst. - - - 
Neue Pfade = hohe Fitness 
Alte, bekannte Pfade = niedrige Fitness 
Crashes oder Hangs werden zusätzlich gespeichert 
Operatoren: 
AFL benutzt viele Mutationsarten: - - - - - 
Bit- und Byte-Flips 
Bytes einfügen/löschen 
Werte verändern 
„Splicing“ = Teile von zwei Inputs kombinieren 
Randomisierte „Havoc“-Mutationen 
Danach werden die Inputs, die neue Coverage bringen, bevorzugt 
weiterverwendet. 

## 4) Weitere Anwendungen von Evolutionären Algorithmen (EA/GA) 

### Robotik: 
Evolutionäre Algorithmen werden genutzt, um Bewegungen oder sogar Körperformen 
von Robotern zu optimieren. 
Beispiel: Virtuelle Kreaturen (Karl Sims) ->Fitness misst, wie weit sich der Roboter 
bewegen kann. 

### Neuroevolution (NEAT): 
Bei der NEAT werden neuronale Netze automatisch durch Evolution verbessert. -> Sowohl die Verbindungen (Topologie) als auch die Gewichte werden verändert, 
Fitness = wie gut das Netz eine Aufgabe löst. 
Technische Optimierung (z. B. Aerodynamik): 
GA sucht nach der besten Form oder Materialkombination, z. B. für Flugzeugflügel 
oder Motoren. -> Fitness = maximale Leistung oder minimale Kosten. 

### Scheduling und Logistik: 
GA wird verwendet, um optimale Reihenfolgen oder Zuweisungen zu finden (z. B. 
Produktionsplanung, Routenplanung). -> Fitness = minimale Zeit, Kosten oder Wartezeiten. 
Kunst und Design (z. B. Artbreeder): 
Bilder, Musik oder 3D-Modelle werden evolutionär verändert. -> Fitness = ästhetische Bewertung (oft durch den Benutzer gewählt). 

### Finanzoptimierung: 
GA hilft, Anlagestrategien oder Portfolios zu optimieren. -> Fitness = hohes Gewinn-Risiko-Verhältnis. 
Software-Fuzzing (AFL, AFL++): 
Evolutionäre Algorithmen erzeugen neue Testeingaben für Programme, um Fehler zu 
finden. ->Fitness = wie viele neue Programmpfade ein Testeingang erreicht.


