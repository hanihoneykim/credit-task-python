# Generated by Django 4.2.6 on 2023-10-30 08:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="",
                max_length=10,
                verbose_name="성별",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(
                default="",
                help_text="사용하실 별명을 입력해주세요",
                max_length=100,
                verbose_name="별명",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="date_joined",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                default="", max_length=254, unique=True, verbose_name="이메일"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(editable=False, max_length=150, verbose_name="이름"),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(editable=False, max_length=150, verbose_name="성"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="15자 이내로 만들어주세요. 영어 소문자, 특수문자 (_) 사용 가능.",
                max_length=15,
                unique=True,
                verbose_name="ID",
            ),
        ),
    ]