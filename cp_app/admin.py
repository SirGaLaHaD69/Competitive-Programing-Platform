from django.contrib import admin
from .models import Tag,UserProfileInfo,Problem,Author
# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)

admin.site.register(Problem)
admin.site.register(UserProfileInfo)
