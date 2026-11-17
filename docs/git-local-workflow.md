# Flux local Git pentru BiblioCUTM

Datele locale din .env.local, jurnalele, fișierele temporare și build/ sunt ignorate.
Fișierele .env.example pot fi urmărite dacă nu conțin date sensibile.

Funcționalitatea reader_history returnează împrumuturile unui singur cititor.
Ordinea este cronologică, apoi după identificator. Un cititor inexistent produce ValueError.
Este o funcție a prototipului local, fără autentificare web.
