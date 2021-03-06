# Generated by Django 3.0 on 2020-01-18 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('question_title', models.CharField(max_length=100, null=True)),
                ('question_text', models.TextField(max_length=50000, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.TextField(max_length=20, null=True)),
                ('slug', models.SlugField(max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.TextField(max_length=50000)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.TextField(max_length=20)),
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QAsite.Question')),
            ],
        ),
    ]
