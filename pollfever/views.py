from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from .models import Question

from django.db.models import F

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {
    'latest_question_list': latest_question_list,
  }
  return render(request, 'pollfever/index.html', context)

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'pollfever/detail.html', { 'question': question })

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'pollfever/results.html', { 'question': question })

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])

  except (KeyError, Choice.DoesNotExist):
    return render(request, 'pollfever/detail.html', { 
      'question': question, 
      'error_message': "You need to select a choice", 
    })
  else:
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('pollfever:results', args=(question.id,)))
