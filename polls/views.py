import requests
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from utils.url import restify

from .models import Choice, Question, Comment
from .serializers import QuestionSerializer
from .forms import CommentForm

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
        # selected_choice.votes += 1
        # [9] Handle race condition on handling "vote" action
        selected_choice.votes += F('votes') + 1

        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# API
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    polls register comment on question
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('polls:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'polls/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    polls modify comment on question
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, 'There is no authority to modify')
        return redirect('polls:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('polls:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'polls/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    polls delete comment on question
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, 'There is no authority to delete')
        return redirect('polls:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('polls:detail', question_id=comment.question_id)