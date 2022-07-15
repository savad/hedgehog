from django.db import models

from django_extensions.db import fields

from applications.accounts.models import User


class Image(models.Model):
    """
    Model for saving image feeds
    """
    user = models.ForeignKey(User, related_name='user_image', on_delete=models.CASCADE)
    image = models.ImageField('Image', upload_to='images/%Y/%m/%d/', max_length=1000)
    image_caption = models.CharField(max_length=100)
    published = models.BooleanField('Published?', default=False)
    likes = models.PositiveIntegerField(default=0)
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    def __str__(self):
        return f"{self.image_caption}"

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ('-created', )
