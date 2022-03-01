from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreeCommentForm, FreePostForm
from .models import AnonyPost,AnonyComment,FreePost,FreeComment

def home(request):
    # posts = Post.objects.all()
    posts = AnonyPost.objects.filter().order_by('-date')
    return render(request, 'index.html', {'posts':posts})


###
# 익명게시판
###

def anony(request):
    posts = AnonyPost.objects.filter().order_by('-date')
    return render(request, 'anony.html', {'posts':posts})

def anonypostcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('anony')
    else:
        form = PostForm()
    return render(request, 'anony_post_form.html', {'form':form})

def anonydetail(request, post_id):
    post_detail = get_object_or_404(AnonyPost, pk=post_id)
    comment_form = CommentForm()
    return render(request, 'anony_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

def newcomment(request, post_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(AnonyPost, pk=post_id)
        finished_form.save()
    return redirect('anonydetail', post_id)

###
# 자유게시판
###

def free(request):
    posts = FreePost.objects.filter().order_by('-date')
    return render(request, 'free.html', {'posts':posts})

def freepostcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = FreePostForm(request.POST, request.FILES)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.author = request.user  # user 추가!
            unfinished.save()
            return redirect('free')
    else:
        form = FreePostForm()
    return render(request, 'free_post_form.html', {'form':form})


def freedetail(request, post_id):
    post_detail = get_object_or_404(FreePost, pk=post_id)
    comment_form = FreeCommentForm()
    return render(request, 'free_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})


def newfreecomment(request, post_id):
    filled_form = FreeCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(FreePost, pk=post_id)
        finished_form.save()
    return redirect('freedetail', post_id)
