## Konfigurační soubor djangovské aplikace.
## My tu nemáme moc co říct: appka se jmenuje "voting",
## všechno ostatní ať se doplní automaticky.

from django.apps import AppConfig


class VotingConfig(AppConfig):
    name = 'voting'
