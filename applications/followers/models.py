from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django_extensions.db import fields

from applications.accounts.models import User


class Follow(models.Model):
    """
    Model for recording follower and following users details
    """
    following = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    def __str__(self):
        return f"{self.follower.email} >> {self.following.email}"

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        unique_together = ('following', 'follower',)

    def edit_follower_following_count(self, func_type=None):
        """
        Profile update with func_type variable for
        following_count,follower_count field.
        @:param func_type: str
        @:return: add or minus follow instance count
        """
        following_profile = User.objects.get(id=self.following.id)
        follower_profile = User.objects.get(id=self.follower.id)
        value = 1 if func_type == 'add' else -1
        following_profile.followers_count += value
        following_profile.save()
        follower_profile.following_count += value
        follower_profile.save()


@receiver(post_save, sender=Follow, dispatch_uid="follow_add_count")
def follow_post_save(sender, instance, created, **kwargs):
    if created:
        instance.edit_follower_following_count(func_type='add')


@receiver(post_delete, sender=Follow, dispatch_uid="follow_delete_count")
def follow_post_delete(sender, instance, **kwargs):
    instance.edit_follower_following_count(func_type='delete')
