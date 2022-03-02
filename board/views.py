from pdb import post_mortem
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreeCommentForm, FreePostForm
from .models import AnonyPost,AnonyComment,FreePost,FreeComment
from django.db.models import Q


def home(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'GET':
        search = request.GET.get('keyword')
        if search:
            posts = AnonyPost.objects.filter(
            Q(title__icontains = search) | #제목
            Q(body__icontains = search) #내용
            )      
            #더하기 기능 annotate 이용하기
            posts2 = FreePost.objects.filter(
            Q(title__icontains = search) | #제목
            Q(body__icontains = search) #내용
            )      
                
            return render(request, 'anony.html', {'posts':posts})
    return render(request, 'index.html')

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
    # 에러??
    # post_detail.anonycomment_set.all().order_by('-anonycomment__date')

    comment_form = CommentForm()
    return render(request, 'anony_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

def anonydetail_edit(request, post_id):
    post = get_object_or_404(AnonyPost, pk=post_id)
    # 폼을 불러올 때 입력했던 내용을 포함시켜서 불러오려면 폼에 instance=order를 넣어준다.
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('anony')
    else:
        form = PostForm(instance=post)
    return render(request, 'anony_post_form.html', {'form':form})

def anonydetail_delete(request, post_id):
    delete_post = get_object_or_404(AnonyPost, pk=post_id)
    delete_post.delete()
    return redirect('anony')

def newcomment(request, post_id):
    filled_form = CommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(AnonyPost, pk=post_id)
        finished_form.save()
    return redirect('anonydetail', post_id)

def comment_delete(request, post_id, comment_id):
    delete_comment = get_object_or_404(AnonyComment, pk=comment_id)
    delete_comment.delete()
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

def freedetail_edit(request, post_id):
    post = get_object_or_404(FreePost, pk=post_id)
    # 폼을 불러올 때 입력했던 내용을 포함시켜서 불러오려면 폼에 instance=order를 넣어준다.
    if request.method == 'POST' or request.method == 'FILES':
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('free')
    else:
        form = PostForm(instance=post)
    return render(request, 'anony_post_form.html', {'form':form})

def freedetail_delete(request, post_id):
    delete_post = get_object_or_404(FreePost, pk=post_id)
    delete_post.delete()
    return redirect('free')

def newfreecomment(request, post_id):
    filled_form = FreeCommentForm(request.POST)
    if filled_form.is_valid():
        finished_form = filled_form.save(commit=False)
        finished_form.post = get_object_or_404(FreePost, pk=post_id)
        finished_form.save()
    return redirect('freedetail', post_id)

def freecomment_delete(request, post_id, comment_id):
    delete_comment = get_object_or_404(FreeComment, pk=comment_id)
    delete_comment.delete()
    return redirect('freedetail', post_id)