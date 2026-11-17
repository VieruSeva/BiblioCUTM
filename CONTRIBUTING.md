# Colaborare în BiblioCUTM

Fiecare membru lucrează din propriul cont GitHub. Identitatea Git folosește numele și adresa asociată acelui cont. O singură persoană nu înlocuiește contribuția celorlalți membri.

## Fluxul unei sarcini

1. Alege un Issue și atribuie-l membrului responsabil.
2. Mută sarcina în In progress în GitHub Project.
3. Actualizează main prin git pull --ff-only origin main.
4. Creează o ramură cu git switch -c feature/numele-sarcinii.
5. Implementează modificarea și testele care verifică comportamentul cerut.
6. Rulează python3 -m unittest discover -s tests -v și git diff --check.
7. Publică ramura și deschide un Pull Request care include Closes #număr, explicația modificării și comenzile de verificare.
8. Un alt membru verifică diferențele, rulează testele și publică observații sau aprobarea. Autorul răspunde prin modificări pe aceeași ramură.
9. Integrează numai după verificarea colegului. Închide Issue-ul și mută-l în Done.
10. După finalizarea etapei, creează tag-ul și GitHub Release cu lista schimbărilor.

## Ce verifică persoana care face review

- Modificarea corespunde criteriilor din Issue.
- Cazurile de eroare nu modifică parțial datele.
- Testele acoperă rezultatul observabil și cazurile limită.
- Documentația descrie funcțiile care există în proiect.
- Nu sunt incluse parole, fișiere locale sau rezultate generate.

Pentru main se recomandă protecție cu cel puțin o aprobare, blocarea force push și rezolvarea discuțiilor înainte de merge. Regula trebuie configurată de un administrator în GitHub și verificată în interfață; acest document nu o activează.
