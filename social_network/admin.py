from django.contrib import admin

# Register your models here.
from .models import CustomUser,Profile,Post,Comment,Connection

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Connection)

