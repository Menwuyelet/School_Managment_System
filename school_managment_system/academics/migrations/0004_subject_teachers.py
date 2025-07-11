# Generated by Django 5.1.7 on 2025-06-09 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_grade'),
        ('teachers', '0002_teacher_home_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ManyToManyField(related_name='subjects', to='teachers.teacher'),
        ),
    ]
