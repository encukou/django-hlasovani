from django.conf.urls import url
from voting import views

## Seznam adres které projekt obsahuje, a funkcí adresy obsluhují.
## Úvod do urlpatterns je v myfirstapp/urls.py.

urlpatterns = [
    ## Prázdná adresa (^ - začátek řetězce, $ - konec řetězce) se zpracuje
    ## funkcí "poll_list" z views.py.
    ## Tahle funkce vrací stránku se seznamem všech hlasování.
    url(r'^$', views.poll_list, name='poll_list'),

    ## Adresa jako "polls/123" se zpracuje funkcí "poll_detail" z views.py.
    ## Tahle funkce bere argument "pk" (proto ono "(?P<pk>" v regulárním
    ## výrazu), a vrátí stránku pro odpovídající hlasování.
    url(r'^polls/(?P<pk>\d+)$', views.poll_detail, name='poll_detail'),
]
