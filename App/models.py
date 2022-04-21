from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your models here.
User = get_user_model()


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']

    def __str__(self):
        return f"{self.first_person} {self.second_person}"


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='chatmessages_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'


User.add_to_class('following',
                  models.ManyToManyField('self', through=Thread, related_name='followers', symmetrical=False))
