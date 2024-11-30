from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from .models import Choice, Question
from django.utils import timezone
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #FLAW 3: Broken Access Control
        return Question.objects.all().order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        #FLAW 3: Broken Access Contol
        return Question.objects.all()


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        #FLAW 1: Injection
        sql = f"UPDATE polls_choice SET votes = votes + 1 WHERE id = {choice_id}"
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    except KeyError:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })       

