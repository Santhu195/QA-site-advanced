from django.db import models
from django.utils.text import slugify

class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100, null = True)
    question_text = models.TextField(max_length=50000, null = True)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.TextField(max_length=20, null = True)
    slug = models.SlugField(max_length=40, null = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question_title)
        super(Question, self).save(*args, **kwargs)

class Answer(models.Model):
    aid = models.AutoField(primary_key=True)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=50000)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.TextField(max_length=20)
