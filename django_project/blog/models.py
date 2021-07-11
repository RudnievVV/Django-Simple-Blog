from django.db import models
from django.urls import reverse
from django.utils import timezone


class BaseModel(models.Model):
    user_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=254, null=False)
    home_page = models.URLField(max_length=200, blank=True)
    title = models.CharField(max_length=50)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    user_ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)
    user_agent_info = models.CharField(max_length=150)

    class Meta:
        ordering = ('-created_at', )
        abstract = True

    def __str__(self):
        return f"{self.user_name} - {self.title}"


class Post(BaseModel):
    def get_absolute_url(self):
        reverse('post', args=[self.id])


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    children_comments = models.ForeignKey('self', related_name='children', null=True, on_delete=models.CASCADE)
    related_to_comment_id = models.IntegerField(default=0)