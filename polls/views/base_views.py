from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from rest_framework import viewsets
from ..serializers import QuestionSerializer

from ..models import Question, Choice

def index(request):
    # input parameter
    page = request.GET.get('page', '1')  # page
    # select
    latest_question_list = Question.objects.order_by('pub_date')
    # paging
    paginator = Paginator(latest_question_list, 5)  # show 5 question per page
    page_obj = paginator.get_page(page)

    context = {'latest_question_list': page_obj}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    """
    poll print question detail
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)

def result(request, question_id):
    """
    poll result
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, "polls/results.html", context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += F('votes') + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# API
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
