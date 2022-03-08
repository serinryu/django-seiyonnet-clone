from django.contrib import admin
from .models import Profile, AnonyPost,AnonyComment,FreePost,FreeComment

admin.site.register(Profile)
admin.site.register(AnonyPost)
admin.site.register(AnonyComment)
admin.site.register(FreePost)
admin.site.register(FreeComment)