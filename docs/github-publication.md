# GitHub publication / Publicarea pe GitHub

Repository public: https://github.com/VieruSeva/BiblioCUTM

Istoricul original, toate cele 8 ramuri și tag-ul adnotat `v1.0.0` au fost publicate. Prima publicare a reușit în rularea GitHub Actions 37365286775, după verificarea celor 10 teste.

## Execution environments / Medii de execuție

Git, commit-urile, ramurile, conflictul și modificarea locală sunt realizate în mediul de lucru. Publicarea autentificată este executată de un runner standard GitHub Actions, folosind istoricul Git exact transferat prin bundle. Commit-urile originale nu sunt recreate.

```sh
git push origin --all
git push origin --tags
```

Fișierul `docs/remote-update.md` a fost creat direct pe GitHub în commit-ul `be7efddae033a185a1f98c3719f86feece1ab536`. Copia locală a preluat efectiv modificarea:

```sh
git pull --ff-only origin main
```

Ulterior, `docs/local-update.md` și documentația publicării au fost actualizate local și înregistrate într-un commit. Runner-ul publică acest commit prin `git push origin main`.

## Reproduce / Reproducere

```sh
git clone https://github.com/VieruSeva/BiblioCUTM.git BiblioCUTM-GitHub-clone
cd BiblioCUTM-GitHub-clone
git log --oneline --graph --decorate --all
git branch -a
git tag --list
python3 -m unittest discover -s tests -v
```

Raportul final și jurnalul de execuție documentează comenzile efective și ID-urile commit-urilor.
