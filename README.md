An example Django app. Comments are all in Czech.

Doporučuji instalovat a spouštět z virtuálního prostředí.
Návod na to, jak nainstalovat Python a nastavit virtuální prostředí, je na:
    http://pyladies.cz/v1/s001-install/instalace.html


Instalace:

    python -m pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser  # (zeptá se na nové přihlašovací údaje)

Spuštění:

    python manage.py runserver


# Co je tu k vidění?

Po celém projektu jsou rozesety komentáře s dvojitým dvojkřížkem (`##`).
Ty jsou od autora tohoto příkladu. Vlastní komentáře doporučuji psát
s jedním `#`.

`manage.py`: Spouští server, nebo jiné užitečné administrativní prográmky.

* Spuštění serveru: `python manage.py runserver`
* Vytvoření uživatele (administrátora): `python manage.py createsuperuser`
* Změna hesla: `python manage.py changepassword`
* Vytvoření migrací databáze: `python manage.py makemigrations` (viz voting/models.py)
* Spuštění migrací databáze: `python manage.py migrate` (viz voting/models.py)

`db.sqlite`: Databáze. Není součástí repozitáře. Smažeš-li ji, dá se
její struktura obnovit pomocí `python manage.py migrate`, ale pak musíš
znovu vytvořit uživatele (`python manage.py createsuperuser`) a dodat
informace (přes administrační rozhraní stránek).

`README.md`: Tento soubor

`LICENSE`: Říká že tenhle projekt můžeš používat. Hurá! Kdyžtak se napiš
do seznamu autorů (zkopíruj první řádek a do kopie dej své informace).

`requirements.txt`: Soubor se všemi balíčky, které je potřeba nainstalovat:
hlavně je to samotné Django.

## `myfirstapp`

Djangovský projekt – adresář, ve kterém je nastavení pro celou webovou
aplikaci.

`__init__.py`: Prázdný soubor, který z adresáře dělá Pythoní modul.

`settings.py`: Soubor s nastavením celého projektu.

`urls.py`: Nastavení toho, jaké adresy obsluhuje jaká funkce. A to pro celý
projekt; většinu práce deleguje na aplikaci `voting`.

`wsgi.py`: Vcelku nezajímavý kus kódu

## `voting`

Djangovská "aplikace" – modul, který obsahuje nějaký samostatný
kousek celkového projektu. V našem případě je to hlasování.
Podobné "aplikace" jsou zabudované v Djangu (např. administrační
rozhraní, systém uživatelů), nebo se dají stáhnout z intenetu
(např. přihlašování uživatelů, různé systémy komentářů, styly, a tak).

`__init__.py`: Další prázdný soubor, který z adresáře dělá Pythoní modul.

`apps.py`: Konfigurační soubor této aplikace

`models.py`: Definice struktury dat, která si tahle tahle aplikace ukládá

`urls.py`: Nastavení toho, jaké adresy obsluhuje jaká funkce.

`views.py`: Funkce, které obsluhují jednotlivé stránky.

`templates/`: Šablony s HTML kódem – obsah stránek.

`static/css/voting.css`: Soubor kaskádových stylů (CSS), říká jak budou různé
části naší stránky vypadat.

`migrations`: Automaticky generované programy pro změnu struktury databáze.
Vytváří se příkazem `python manage.py makemigrations`. A je dobré
je přidávat do Gitu.

`admin.py`: Konfigurace administračního rozhraní

`tests.py`: Testy. Zatím žádné.


