# BiblioCUTM

Prototip educațional pentru laboratorul 2 AMPS, pe baza proiectului din laboratorul 1.
Obiectivul laboratorului este gestionarea versiunilor cu Git și GitHub.
Acest prototip Python rulează local, cu date în memorie. Nu reprezintă MVP-ul web complet.

## Run

Python 3.10 sau mai nou. Nu sunt necesare biblioteci externe.

```sh
python3 -m bibliocutm.demo
python3 -m unittest discover -s tests -v
```

## Project scope

Catalog, rezervări de 48 de ore, împrumuturi de 14 zile, limita de 3 angajamente,
returnări, raport CSV și verificarea rolurilor sunt demonstrate prin funcții locale.
Autentificarea, stocarea persistentă, interfața web și controlul concurenței
rămân componente ale proiectului specificat în laboratorul 1.
