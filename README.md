# SPARQL-MUTU

Vaatii Python 2.7:n ja rdflib-kirjaston (asenna: `pip install rdflib`). Ei toimi Python 3:ssa.

Jenan komentorivityökalujen on oltava PATHissa jotta tämä toimii.

Linuxissa PATHiin laittaminen toimii kutakuinkin näin:

    export JENA_HOME=/TIEDOSTOPOLKU/apache-jena
    export PATH=$PATH:$JENA_HOME/bin

Aja komennolla

    python mututin.py puho.ttl yso-puho.ttl yso.ttl >raportti.csv
