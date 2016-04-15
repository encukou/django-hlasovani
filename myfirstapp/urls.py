"""myfirstapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

## Seznam adres které projekt obsahuje, a funkcí adresy obsluhují.
## Protože je to pro celý projekt, není tu toho moc – jen delegace na
## jednotlivé aplikace.

## Napřed pár importů:

from django.conf.urls import include, url
from django.contrib import admin

## A pak veledůležitý "urlpatterns": seznam záznamů "url".
## Každý záznam má dvě části:
## 1. Regulární výraz, který určuje pro jaké adresy tenhle záznam platí.
##
## 2. Funkce, která odpovídající adresy obsluhuje. V tomto případě to není
##    jedna funkce, ale "include", který adresy posílá na další roztřídění:
##    když adresa začíná "admin/", je součást administračního rozhraní;
##    jinak se aplikují urlpatterns v modulu 'voting.urls'.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('voting.urls')),
]
