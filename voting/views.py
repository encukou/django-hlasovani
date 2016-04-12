from django.shortcuts import render, get_object_or_404

from voting.models import Poll


def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'voting/poll_list.html', {'polls': polls})


def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    return render(request, 'voting/poll_detail.html', {'poll': poll})
