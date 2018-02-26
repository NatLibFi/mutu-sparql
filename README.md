MUTU
====

SPARQL-MUTU

Jenan komentorivityökalujen on oltava PATHissa jotta tämä toimii.

Linuxissa PATHiin laittaminen toimii kutakuinkin näin:

```
export JENA_HOME=/TIEDOSTOPOLKU/apache-jena
export PATH=$PATH:$JENA_HOME/bin
```

aja komennolla `python mututin.py puho.ttl yso-puho.ttl yso.ttl`
