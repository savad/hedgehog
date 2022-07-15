from django.contrib import admin

from applications.followers.models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created']


admin.site.register(Follow, FollowAdmin)
