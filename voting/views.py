from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

from voting.models import Poll, Record, Vote


def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'voting/poll_list.html', {'polls': polls})


def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    error = ''
    if request.method == 'POST':
        title = request.POST.get('title')
        option_values = []
        for option in poll.options.all():
            if 'opt-{}'.format(option.pk) in request.POST:
                value = True
            else:
                value = False
            option_values.append((option, value))

        if title:
            with transaction.atomic():
                record = Record(poll=poll, title=title)
                record.save()
                for option, value in option_values:
                    vote = Vote(option=option, record=record, value=value)
                    vote.save()
            return redirect('poll_detail', pk=pk)
        else:
            error = 'Musíš zadat jméno.'
    else:
        option_values = []
        for option in poll.options.all():
            option_values.append((option, False))
    data = {
        'poll': poll,
        'error': error,
        'option_values': option_values,
    }
    print(option_values)
    return render(request, 'voting/poll_detail.html', data)
