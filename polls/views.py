import requests
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets
from django.db.models import F

from utils.url import restify

from .models import Choice, Question
from .serializers import QuestionSerializer


# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"
#     def get_queryset(self):
#         """Return the last five published questions."""
#         response = requests.get(restify("/questions/"))
#         questions = response.json()
#
#         return questions[:5]

def index(request):
    # input parameter
    page = request.GET.get('page', '1')  # page
    # select
    latest_question_list = Question.objects.order_by('-pub_date')
    # paging
    paginator = Paginator(latest_question_list, 5)  # show 5 question per page
    page_obj = paginator.get_page(page)

    context = {'latest_question_list': page_obj}
    return render(request, "polls/index.html", context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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
        # selected_choice.votes += 1
        # [9] Handle race condition on handling "vote" action
        selected_choice.votes += F('votes') + 1

        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# API
# ===


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
