from django.contrib import admin
from applications.likes.models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created']


admin.site.register(Like, LikeAdmin)
