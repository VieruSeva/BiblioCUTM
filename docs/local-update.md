# Local update / Modificare locală

După preluarea prin `git pull --ff-only origin main` a commit-ului creat direct pe GitHub, această pagină a fost adăugată în copia locală BiblioCUTM la 5 octombrie 2026.

The local commit is transferred as a Git bundle to a standard GitHub Actions runner, which merges the exact commit and executes `git push origin main`. The original commit ID is preserved.

Verificarea finală include clonarea din GitHub și rularea celor 10 teste automate.
