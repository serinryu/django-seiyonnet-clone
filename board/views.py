from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreeCommentForm, FreePostForm
from .models import Profile,AnonyPost,AnonyComment,FreePost,FreeComment
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Max
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'GET':
        search = request.GET.get('keyword')
        if search:
            posts1 = AnonyPost.objects.filter(
            Q(title__icontains = search) | #제목
            Q(body__icontains = search) #내용
            )      
            posts2 = FreePost.objects.filter(
            Q(title__icontains = search) | #제목
            Q(body__icontains = search) #내용
            )      
            posts = posts1.union(posts2) #검색 결과  합치기 
            return render(request, 'search.html', {'posts':posts})
    return render(request, 'index.html')

def profile(request, user_id):
    userprofile = get_object_or_404(Profile, pk=user_id)
    return render(request, 'profile.html', {'userprofile':userprofile})
    

###
# 익명게시판
###

def anony(request):
    posts = AnonyPost.objects.filter().order_by('-date')
    paginator = Paginator(posts, 5)
    pagnum = request.GET.get('page')
    posts = paginator.get_page(pagnum)
    return render(request, 'anony.html', {'posts':posts})

def anonypostcreate(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.author = request.user  # user 추가!
            unfinished.save()
            form.save()
            return redirect('anony')
    else:
        form = PostForm()
    return render(request, 'anony_post_form.html', {'form':form})

def anonydetail(request, post_id):
    post_detail = get_object_or_404(AnonyPost, pk=post_id)
    comment_form = CommentForm()
    return render(request, 'anony_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

@login_required
def anonydetail_edit(request, post_id):
    post = get_object_or_404(AnonyPost, pk=post_id)
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('anony')
    else:
        form = PostForm(instance=post)
    return render(request, 'anony_post_form.html', {'form':form})

@login_required
def anonydetail_delete(request, post_id):
    delete_post = get_object_or_404(AnonyPost, pk=post_id)
    delete_post.delete()
    return redirect('anony')

@login_required
def newcomment(request, post_id):
    if request.method == 'POST':
        filled_form = CommentForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.post = get_object_or_404(AnonyPost, pk=post_id)
            finished_form.author = request.user #댓글 작성자
            finished_form.save()
        return redirect('anonydetail', post_id)

@login_required
def comment_delete(request, post_id, comment_id):
    delete_comment = get_object_or_404(AnonyComment, pk=comment_id)
    delete_comment.delete()
    return redirect('anonydetail', post_id)

@login_required
def anony_like(request, post_id):
    post = get_object_or_404(AnonyPost, id=post_id)
    user = request.user
    profile = Profile.objects.get(id=user.id)
    check_like_post = profile.like_anonyposts.filter(id=post_id)
    if check_like_post.exists():
        profile.like_anonyposts.remove(post)
        post.like_count -= 1
        post.save()
    else:
        profile.like_anonyposts.add(post)
        post.like_count += 1
        post.save()
    return redirect('anonydetail', post_id)

###
# 자유게시판
###

def free(request):
    posts = FreePost.objects.filter().order_by('-date')
    paginator = Paginator(posts, 5)
    pagnum = request.GET.get('page')
    posts = paginator.get_page(pagnum)
    return render(request, 'free.html', {'posts':posts})

@login_required
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

@login_required
def freedetail_edit(request, post_id):
    post = get_object_or_404(FreePost, pk=post_id)
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('free')
    else:
        form = PostForm(instance=post)
    return render(request, 'free_post_form.html', {'form':form})

@login_required
def freedetail_delete(request, post_id):
    delete_post = get_object_or_404(FreePost, pk=post_id)
    delete_post.delete()
    return redirect('free')

@login_required
def newfreecomment(request, post_id):
    if request.method == 'POST':
        filled_form = FreeCommentForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.post = get_object_or_404(FreePost, pk=post_id)
            finished_form.author = request.user #댓글 작성자
            finished_form.save()
        return redirect('freedetail', post_id)

@login_required
def freecomment_delete(request, post_id, comment_id):
    delete_comment = get_object_or_404(FreeComment, pk=comment_id)
    delete_comment.delete()
    return redirect('freedetail', post_id)

@login_required
def free_like(request, post_id):
    post = get_object_or_404(FreePost, id=post_id)
    user = request.user
    profile = Profile.objects.get(id=user.id)
    check_like_post = profile.like_freeposts.filter(id=post_id)
    if check_like_post.exists():
        profile.like_freeposts.remove(post)
        post.like_count -= 1
        post.save()
    else:
        profile.like_freeposts.add(post)
        post.like_count += 1
        post.save()
    return redirect('freedetail', post_id)