from django import forms
from .models import Profile, AnonyPost, AnonyComment, FreePost, FreeComment

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

#익명게시물 폼
class PostForm(forms.ModelForm):
    class Meta:
        model = AnonyPost
        fields = ['title', 'body', 'image']
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "글 제목을 입력해주세요",
            'rows': 20
        }

        self.fields['body'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "글 제목을 입력해주세요",
            'rows': 20,
            'cols' : 100
        }

#익명댓글 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = AnonyComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "댓글을 입력해주세요",
            'rows': 3,
            'cols': 150
        }

#자유게시물 폼
class FreePostForm(forms.ModelForm):
    class Meta:
        model = FreePost
        fields = ['title', 'body', 'image']

    def __init__(self, *args, **kwargs):
        super(FreePostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "글 제목을 입력해주세요",
            'rows': 20
        }

        self.fields['body'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "글 제목을 입력해주세요",
            'rows': 20,
            'cols' : 100
        }

#자유댓글 폼
class FreeCommentForm(forms.ModelForm):
    class Meta:
        model = FreeComment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(FreeCommentForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "댓글을 입력해주세요",
            'rows': 3,
            'cols': 150
        }