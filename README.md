# reittihaku

Reittihaku-applikaatio (Solidabis koodihaaste, [nettisivu](https://koodihaaste.solidabis.com/))


# Käytetyt tekniikat

* Python, Flask, Javascript

Kehitetty Linux-käyttöjärjestelmää (Debian-based) käyttäen.


# Käyttäminen lokaalisti (Linux)

* Gitin kopioiminen:

`git clone https://github.com/tuolhutt/reittihaku.git`

* Requirements

`sudo pip3 install flask`

* Käynnistys

`cd reittihaku/cgi-bin/`

`python3 web.py local`


# Ratkaisusta

Ohjelma ratkaisee käynnistyessään iteroimalla kaikkien alku-/loppupysäkki-kombinaatioiden lyhimmät reitit. Lisäksi se ratkaisee jokaiselle reitille sellaisen linjastovalinnan, jotta vaihtoja tulee mahdollisimman vähän. Aikaa tämän lähtötilan selvittämiseen kuluu noin 10ms.
