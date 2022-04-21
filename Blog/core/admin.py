from django.contrib import admin
from django.contrib.auth.models import User
from core.models import Post, Category
from users.models import Profile

# Register your models here.


class ProfileInLine(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'profile'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
