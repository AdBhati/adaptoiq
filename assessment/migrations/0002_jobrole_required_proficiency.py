# Generated by Django 5.1.7 on 2025-03-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrole',
            name='required_proficiency',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='null', max_length=20),
            preserve_default=False,
        ),
    ]
