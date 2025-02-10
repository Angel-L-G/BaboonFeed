# Generated by Django 5.1.6 on 2025-02-10 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files')),
                ('type', models.CharField(choices=[('audio', 'Audio'), ('image', 'Image'), ('video', 'Video')], max_length=5, null=True)),
            ],
        ),
    ]
