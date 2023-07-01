from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True)
    other_social_media = models.URLField(blank=True)

class Post(models.Model):
    #createduser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='createduser',blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    # Add fields for likes, comments, and shares here
    def total_likes(self):
        return self.likes.count() 
    def __str__(self):
        return self.id

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by f"{self.author.username}" on {self.post.text}' 

class Connection(models.Model):

    currentuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='usercurrent',null=True,blank=True)
    connectuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='connectuser',null=True,blank=True)   