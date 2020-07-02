from django.db import models
from django.contrib.auth.models import User
from django.utils.text  import slugify
from django.conf import settings

Question_GENRE_CHOICES = (
    ("T", "Technology"),
    ("S", "Science"),
    ("G", "Grammer"),
    ("M", "Maths"),
    ("C", "Chemistry"),
    ("B", "Bio"),
    ("P", "Psychology"),
)

class Question(models.Model):
    author    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre     = models.CharField(choices = Question_GENRE_CHOICES, max_length=1)
    question  = models.TextField()
    created   = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug      = models.SlugField()
    question_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="question_liked_by")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('q_detail', args=[str(self.slug)])

class Answer(models.Model):
    author    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer    = models.TextField(help_text="Enter your answer here !!!")
    question  = models.ForeignKey(Question, on_delete=models.CASCADE)
    created   = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated   = models.DateTimeField(auto_now=True,     auto_now_add=False)
    answer_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="answer_liked_by")

    def __str__(self):
        return self.answer

class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ('created',)


    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("users must have an emial address")
        if not username :
            raise ValueError("users must have an username")
        user  = self.model(
                email=self.normalize_email(email),
                username=username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    email                = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username             = models.CharField(max_length=30,unique=True)
    date_joined          = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login           = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin             = models.BooleanField(default=False)
    is_active            = models.BooleanField(default=True)
    is_staff             = models.BooleanField(default=False)
    is_superuser         = models.BooleanField(default=False)
    bio        = models.CharField(max_length=250)
    profession = models.CharField(max_length=250)
    following = models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label ):
        return True



