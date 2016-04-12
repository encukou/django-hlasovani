from django.shortcuts import render

def poll_list(request):
    return render(request, 'voting/poll_list.html', {})
