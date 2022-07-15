from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django_extensions.db import fields

from applications.accounts.models import User
from applications.images.models import Image


class Like(models.Model):
    """
    Model for saving Like data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    def __str__(self):
        return f'{self.user.email} liked'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('user', 'image',)

    def edit_like_count(self, func_type=None):
        """
        Image update with func_type variable for like field.
        @:param func_type: str
        @:return: add or delete like count.
        """
        value = 1 if func_type == 'add' else -1
        self.image.likes += value
        self.image.save()


@receiver(post_save, sender=Like, dispatch_uid="like_add_count")
def follow_post_save(sender, instance, created, **kwargs):
    if created:
        instance.edit_like_count(func_type='add')


@receiver(post_delete, sender=Like, dispatch_uid="like_delete_count")
def follow_post_delete(sender, instance, **kwargs):
    instance.edit_like_count(func_type='delete')
