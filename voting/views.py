from django.shortcuts import render

from voting import models

def poll_list(request):
    polls = models.Poll.objects.all()
    return render(request, 'voting/poll_list.html', {'polls': polls})
