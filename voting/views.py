from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

from voting.models import Poll, Record, Vote

## Views – funkce, které vracejí webové odpovědi.
## Každá z těchto funkcí obsluhuje nějakou adresu (viz urls.py),
## bere jako argument "požadavek" od prohlížeče, a vrací odpověď – v našem
## případě webovou stránku vyrobenou ze šablony.


def poll_list(request):
    """Seznam všech hlasování"""
    ## Tahle funkce je celkem jednoduchá. Načte z databáze všechny
    ## hlasování:
    polls = Poll.objects.all()
    ## A pak je předá funkci "render", která zpracuje šablonu
    ## "voting/poll_list.html", do které vloží proměnnou
    ## "polls" nastavenou na seznam všech hlasování.
    return render(request, 'voting/poll_list.html', {'polls': polls})


def poll_detail(request, pk):
    """Jedno konkrétní hlasování"""
    ## Tahle funkce je složitější, protože zpracovává nejen dotazy na
    ## aktuální stav (GET), ale i požadavky na změnu stavu (POST) – u nás
    ## přidání nového záznamu.

    ## Nejdřív z databáze načteme hlasování zadané v adrese.
    ## Pokud neexistuje, vrátíme chybu 404 (stránka neexistuje).
    poll = get_object_or_404(Poll, pk=pk)
    ## Nastavíme proměnnou, do které dáme popis chyby, kdyby něco šlo špatně.
    error = ''
    ## A teď: Pokud chtěl uživatel změnit stav (POST), musíme mu zkusit
    ## vyhovět.
    if request.method == 'POST':
        ## S požadavkem POST by měly přijít informace z formuláře, které nám
        ## Django zpřístupní ve slovníku "request.POST".
        ## Očekáváme něco jako:
        ## {'title': 'Janča', 'opt-1': True, 'opt-3': True}
        ## t.j. 'title' obsahuje jméno, a 'opt-X', pokud ve slovníku je,
        ## znamená že uživatel hlasuje pro danou možnost.
        ## Vezměme si ze slovníku ono jméno.
        title = request.POST.get('title')
        ## Pak si naplníme seznam hlasů.
        option_values = []
        ## Pro každou možnost v tomto hlasování ...
        for option in poll.options.all():
            ## ... zjistíme, jestli je v POST datech příslušný záznam,
            if 'opt-{}'.format(option.pk) in request.POST:
                value = True
            else:
                value = False
            ## A seznam plníme dvojicemi (N-ticemi): (možnost, hodnota).
            ## ("append" bere jen jeden argument: append(a, b) by nefungovalo,
            ## závorky navíc znamenají, že metodě posíláme jednu dvojici.)
            option_values.append((option, value))

        ## Jméno musí být vyplněno ...
        if title:
            ## ... a jestli je, zapíšeme do databáze.
            ## ("with transaction.atomic" říká, že pokud se některý z příkazů
            ## v tomhle bloku nepovede, databáze zůstane netknutá.
            ## Je dobré to aspoň pro zápisy do databáze pooužívat.)
            with transaction.atomic():
                ## Vytvoříme nový záznam, a vložíme do databáze
                record = Record(poll=poll, title=title)
                record.save()
                ## A pro všechny dvojice (možnost, hodnota), které
                ## jsme si před chvílí připravili, vytvoříme a uložíme
                ## odpovídající hlas.
                for option, value in option_values:
                    vote = Vote(option=option, record=record, value=value)
                    vote.save()
            ## A potom řekneme prohlížeči, aby stránku načetl znova,
            ## tentokrát metodou GET.
            ## (To je proto, že kdyby uživatel stránku načtenou pomocí POST
            ## obnovil (F5), formulář by se odeslal znovu.)
            return redirect('poll_detail', pk=pk)
        else:
            ## Nebyla-li data správná, nastavíme chybovou hlášku.
            error = 'Musíš zadat jméno.'

            ## Formulář teď uživateli ukážeme znova, s chybovou hláškou,
            ## ale o údaje které vyplnil nepřijde – máme je v "option_values"
            ## a použijeme je při vytvéření stránky.
    else:
        ## Poslal-li uživatel požadavek GET, nastavíme si "option_values"
        ## na dvojice jako výše, jen budou všechny hlasy zatím prázdné.
        option_values = []
        for option in poll.options.all():
            option_values.append((option, False))

    ## Teď můžeme tvořit výslednou stránku. Napřed si pěkně připravíme
    ## informace pro šablonu...
    data = {
        'poll': poll,       ## Objekt "Hlasování" se všemi informacemi
        'error': error,     ## Případná chybová hláška

        ## Dvojice (možnost, hodnota) pro hlasovací formulář
        'option_values': option_values,
    }
    ## Informace předáme do šablony, a necháme Django vytvořit stránku.
    return render(request, 'voting/poll_detail.html', data)
