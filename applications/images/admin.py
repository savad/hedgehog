from django.contrib import admin

from applications.images.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image', 'created']


admin.site.register(Image, ImageAdmin)
