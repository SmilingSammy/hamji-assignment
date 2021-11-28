from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from rest_framework import viewsets
from ..serializers import QuestionSerializer

from ..models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# def index(request):
#     # input parameter
#     page = request.GET.get('page', '1')  # page
#     # select
#     # latest_question_list = Question.objects.order_by('pub_date')
#     latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
#     # paging
#     paginator = Paginator(latest_question_list, 5)  # show 5 question per page
#     page_obj = paginator.get_page(page)
#
#     context = {'latest_question_list': page_obj}
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     """
#     poll print question detail
#     """
#     question = get_object_or_404(Question, pk=question_id)
#     # question = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
