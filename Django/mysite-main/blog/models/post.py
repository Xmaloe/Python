from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)  # Novo
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to="posts/", blank=True, null=True)  # Novo
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, help_text="Separar por vírgulas")  # Novo
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
