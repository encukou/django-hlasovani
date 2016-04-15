## Modely určují strukturu databáze: jaké druhy informací se
## do databáze budou ukládat.
## Všechny informace, které se mají "zapamatovat" mezi jednotlivými
## načteními stránek, musí být v databázi.
##
## Djangovská databáze je tzv. "relační". V praxi to znamená, že
## se skládá s tabulek, které mají je pevně daný počet a názvy sloupců,
## a druh informací které se do každého sloupce dají dát (např. čísla,
## řetězce, odkazy na řádky z jiných tabulek.)
## Změny téhle struktury sloupců jsou složité: po provedení změn v tomhle
## souboru je potřeba spustit `python manage.py makemigrations`, což vytvoří
## program který umí změnit samotnou databázi, výsledný soubor pak nejíp
## dát do Gitu, a pak aplikovat pomocí `python manage.py migrate`.
##
## Samotná webová aplikace strukturu databáze měnit nemůže (resp. neměla by :).
## Takže když by to vypadalo, že potřebuješ třeba takovouhle tabulku
## pro hlasování o termínu:
##
## Jméno | 9. 4. | 16. 4. | 23. 4. |
## ---------------------------------
## Janča |  jo   |   ne   |   jo   |
## Verča |  ne   |   jo   |   jo   |
##
## ... kde je potřeba mít pro každé hlasování jiné sloupce, a ještě se možná
## budou v průběhu hlasování sloupce přidávat a ubírat, tak je potřeba
## přidat další tabulku:
##
## Záznamy          Možnosti            Hlasy
## ----------       --------            ------
##
## č. | Jméno       č. | Datum          č. člověka | č. možnosti | hodnota
## ----------       -----------         ----------------------------------
## 1  | Janča       1  | 9. 4.          1 (Janča)  | 1 (9. 4.)   | jo
## 2  | Verča       2  | 16. 4.         1 (Janča)  | 2 (16. 4.)  | ne
##                  3  | 23. 4.         1 (Janča)  | 3 (23. 4.)  | jo
##                                      2 (Verča)  | 1 (9. 4.)   | ne
##                                      2 (Verča)  | 2 (16. 4.)  | jo
##                                      2 (Verča)  | 3 (23. 4.)  | jo
##
## Každý řádek tabulky má svoje číslo, a ostatní tabulky můžou přes toto
## číslo na určitý řádek "odkazovat" (neboli tvořit "relaci" -- odtud
## relační databáze).
## Mimochodem, číslo řádku se v Djangu jmenuje "pk" (z angl. "primary key").
##
## A s takovouhle strukturu májí i naše modely. Jen ještě přidáváme
## tabulku hlasování.
##
## A každá tabulka je definovaná jako třída se speciálním atributem
## pro každý sloupec.
## S jednotlivými řádky se pak v Djangu dá pracovat jako s objekty této
## třídy.

from django.db import models


class Poll(models.Model):
    """Tabulka hlasování"""
    ## Každé hlasování má své vlastní jméno.
    ## Je to řetězec (CharField) s max. délkou 200 znaků.
    title = models.CharField(max_length=200)

    ## Protože model je "jen" třída, můžeme nadefinovat, jak
    ## se "převádí na řetězec". Django výsledek použije jako
    ## název objektu, např. v administračním rozhraní.
    def __str__(self):
        return self.title


class Record(models.Model):
    """Tabulka "Záznamy" -- sady hlasů, které patří jednomu hlasujícímu"""
    ## Každý záznam patří k nějakému hlasování; tady řekneme, že to tak
    ## má být.
    ## Sloupec "poll" v databázi bude obsahovat čísla řádků v tabulce "Poll".
    ## A když načteme některý řádek tabulky Record, výsledný objekt bude
    ## mít atribut "poll" přímo s objektem třídy Poll, který přísluší danému
    ## hlasování.
    ## Navíc ještě:
    ## - díky "related_name" bude mít každý objekt třídy Poll atribut
    ##   "records", přes který se dá dostat k jednotlivým záznamům
    ## - díky "on_delete" se při smazání hlasování smažou i všechny
    ##   související záznamy.
    poll = models.ForeignKey(Poll,
                             related_name='records',
                             on_delete=models.CASCADE)
    ## Jo, a každý záznam má název; zase je to řetězec.
    title = models.CharField(max_length=200)

    ## Opět: převod na řetězec = jméno objektu
    def __str__(self):
        return self.title

    ## A navíc tady nadefinujeme ještě metodu, která vrátí
    ## seznam všech hlasů v tomhle záznamu, v pořadí odpovídajícím
    ## pořadí možností.
    ## (Čteš-li komentáře zvrchu dolů, doporučuji tuhle funkci
    ## přeskočit a vrátit se k ní později.)
    def vote_values(self):
        ## Budeme postupně plnit seznam.
        result = []
        ## Projdeme všechny Možnosti našeho hlasování
        for option in self.poll.options.all():
            try:
                ## Pro každou možnost zkusíme z databáze vyzvednout
                ## odpovídající Hlas.
                vote = Vote.objects.get(option=option, record=self)
            except Vote.DoesNotExist:
                ## Pokud takový hlas neexistuje, Django vyhodí výjimku
                ## "Vote.DoesNotExist". Do seznamu dáme hodnotu "None",
                ## a tak zaznamenáme že tady žádný hlas není.
                ## (To se může stát třeba když se přidá možnost do
                ## už probíhajícího hlasování.)
                result.append(None)
            else:
                ## Když hlas existuje, dáme do seznamu jeho hodnotu.
                result.append(vote.value)
        ## A nakonec seznam vrátíme – to je docela důležité...
        return result

    ## Navíc tu ještě přidáme nějaké nastavení.
    ## Speciální nastavení se v Djangu dělá zajímavým způsobem:
    ## uvnitř v modelu nadefinujeme třídu jménem Meta,
    ## a nastavení uděláme v ní.
    ## Dokumentace k nastavení je kdyžtak tady:
    ##   https://docs.djangoproject.com/en/1.9/ref/models/options/
    class Meta:
        ## Záznamy budou mít pevně určené pořadí v rámci hlasování.
        order_with_respect_to = 'poll'


class Option(models.Model):
    """Tabulka "Možnosti" -- pro co je v daném hlasování možné hlasovat"""
    ## Podobně jako u Záznamů, u Možnosti jsou vázané na určité hlasování.
    poll = models.ForeignKey(Poll,
                             related_name='options',
                             on_delete=models.CASCADE)
    ## A taky mají název. A __str__.
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    ## A nastavení – aspoň tady je něco nového :)
    class Meta:
        order_with_respect_to = 'poll'
        ## Možnosti v rámci jednoho hlasování musí mít různá jména.
        ## Nebo-li, v databázi nemůžou být dvě možnosti se stejným
        ## "poll" i "title".
        unique_together = [('poll', 'title')]


class Vote(models.Model):
    """Tabulka "Hlasy" -- jednotlivé ano/ne"""
    ## Každý hlas náleží nějakému záznamu a nějaké možnosti
    ## (Ideálně takovým, které oba náleží stejnému hlasování,
    ## ale to na úrovni databáze nebudeme kontrolovat.)
    record = models.ForeignKey('voting.Record',
                               related_name='votes',
                               on_delete=models.CASCADE)
    option = models.ForeignKey('voting.Option',
                               related_name='votes',
                               on_delete=models.CASCADE)
    ## A každý hlas má nějakou hodnotu: ano nebo ne, True nebo False.
    ## Proto BooleanField.
    value = models.BooleanField()

    ## Převádnění na řetězec; např. "False on 9. 4. by Verča"
    def __str__(self):
        return '{} on {} by {}'.format(self.value, self.option.title,
                                       self.record.title)

    ## A možnosti: vždy max. jeden Hlas pro každou kombinaci
    ## Záznam/Možnost
    class Meta:
        unique_together = [('record', 'option')]
