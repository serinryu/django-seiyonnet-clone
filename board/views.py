from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, FreeCommentForm, FreePostForm
from .models import AnonyPost,AnonyComment,FreePost,FreeComment
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Max

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

    # post_detail = post_detail.annotate(order_comment=Max('anonycomment__date')).order_by('-order_comment')

    #post_detail = AnonyPost.objects.get(pk=post_id).order_by('-anonycomment__date')

    #post_detail = AnonyPost.objects.filter(pk=post_id).order_by('-anonycomment__date')

    #위 코드는 에러가 나는 게 맞다. 생각해보자. 우리는 pk=post_id 값인 post 를 제대로 넘겨줘야 한다. 만약 뒤에서 order_by 를 작성하게 되면 댓글생성시기에 따라서 "post"의 순서를 바꾸라는 의미다. 따라서 '엥? 내가 받아야 하는 것은 pk=post_id 인 post 하나인데 왜 순서 바꾸라고 하지?' 하고 에러가 뜨는 것! 즉, 우리는 post 안의 "댓글"순서를 바꿔주고 싶은 것이므로 models.py 의 anonycomment 에 애초에 처음부터 ordering 을 설정해주면, 확실하게 "댓글"의 순서를 바꿔줄 수 있겠다.
    
    comment_form = CommentForm()
    return render(request, 'anony_detail.html', {'post_detail':post_detail, 'comment_form': comment_form})

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

def anonydetail_delete(request, post_id):
    delete_post = get_object_or_404(AnonyPost, pk=post_id)
    delete_post.delete()
    return redirect('anony')

def newcomment(request, post_id):
    if request.method == 'POST':
        filled_form = CommentForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.post = get_object_or_404(AnonyPost, pk=post_id)
            finished_form.author = request.user #댓글 작성자
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
    paginator = Paginator(posts, 5)
    pagnum = request.GET.get('page')
    posts = paginator.get_page(pagnum)
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
    return render(request, 'free_post_form.html', {'form':form})

def freedetail_delete(request, post_id):
    delete_post = get_object_or_404(FreePost, pk=post_id)
    delete_post.delete()
    return redirect('free')

def newfreecomment(request, post_id):
    if request.method == 'POST':
        filled_form = FreeCommentForm(request.POST)
        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.post = get_object_or_404(FreePost, pk=post_id)
            finished_form.author = request.user #댓글 작성자
            finished_form.save()
        return redirect('freedetail', post_id)

def freecomment_delete(request, post_id, comment_id):
    delete_comment = get_object_or_404(FreeComment, pk=comment_id)
    delete_comment.delete()
    return redirect('freedetail', post_id)