# Reittihaku-applikaatio

Tekijä: Tuomo Huttu

Päiväys: 11.4.2020

Ratkaisuni Solidabis koodihaasteeseen ([nettisivu](https://koodihaaste.solidabis.com/))


# Käytetyt tekniikat

* Python, Flask, Javascript

Kehitetty Linux-käyttöjärjestelmää (Debian-based) käyttäen.


# Testaaminen lokaalisti (Linux)

* Gitin kopioiminen

`git clone https://github.com/tuolhutt/reittihaku.git`

* Käynnistys

`cd reittihaku/cgi-bin/`

`python3 web.py local`

* Avaaminen selaimessa

osoite: http://127.0.0.1:5000/


# Ratkaisusta

Ohjelma ratkaisee (ensimmäisen yhteyden alussa) iteroimalla kaikkien alku-/loppupysäkki-kombinaatioiden nopeimmat reitit. Lisäksi se ratkaisee jokaiselle reitille sellaisen linjastovalinnan, jotta vaihtoja tulee mahdollisimman vähän. Aikaa näiden selvittämiseen kuluu noin 10ms.
