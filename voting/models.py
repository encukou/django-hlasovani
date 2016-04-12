from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Record(models.Model):
    poll = models.ForeignKey(Poll,
                             related_name='records',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def vote_values(self):
        result = []
        for option in self.poll.options.all():
            try:
                vote = Vote.objects.get(option=option, record=self)
            except Vote.DoesNotExist:
                result.append(None)
            else:
                result.append(vote.value)
        return result

    class Meta:
        order_with_respect_to = 'poll'


class Option(models.Model):
    poll = models.ForeignKey(Poll,
                             related_name='options',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'poll'
        unique_together = [('poll', 'title')]


class Vote(models.Model):
    record = models.ForeignKey('voting.Record',
                               related_name='votes',
                               on_delete=models.CASCADE)
    option = models.ForeignKey('voting.Option',
                               related_name='votes',
                               on_delete=models.CASCADE)
    value = models.BooleanField()

    def __str__(self):
        return '{} on {} by {}'.format(self.value, self.option.title,
                                       self.record.title)

    class Meta:
        unique_together = [('record', 'option')]
