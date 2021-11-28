from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


from ..forms import CommentForm
from ..models import Question, Comment

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
        messages.success(request, 'Delete comment success')
    return redirect('polls:detail', question_id=comment.question_id)


# def post_detail(request, slug):
#     post = Post.objects.get(slug=slug)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             reply_obj = None
#             try:
#                 reply_id = int(request.POST.get('reply_id'))
#             except:
#                 reply_id = None
#             if reply_id:
#                 reply_obj = Comment.objects.get(id=reply_id)
#
#             author = form.cleaned_data['author']
#             comment = form.cleaned_data['comment']
#             if reply_obj:
#                Comment(author=author,comment_field=comment, reply=reply_obj, post=post).save()
#             else:
#                 Comment(author=author,comment_field=comment, post=post).save()
#             return redirect(reverse('post_detail', args=[post.slug]))
#     else:
#         form = CommentForm()
#     comments = Comment.objects.filter(post=post, reply=None).order_by('-create_date')
#     context = {
#         'post':post,
#         'form':form,
#         'comments':comments
#     }
#     return render(request, 'post_detail.html', context)