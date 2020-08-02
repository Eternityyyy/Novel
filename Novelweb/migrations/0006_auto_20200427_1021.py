# Generated by Django 3.0 on 2020-04-27 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Novelweb', '0005_author_income'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': '作者'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': '书籍'},
        ),
        migrations.AlterModelOptions(
            name='cashoutinfo',
            options={'verbose_name': '作者提现记录'},
        ),
        migrations.AlterModelOptions(
            name='chapter',
            options={'verbose_name': '章节'},
        ),
        migrations.AlterModelOptions(
            name='code',
            options={'verbose_name': '作者注册码'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '评论'},
        ),
        migrations.AlterModelOptions(
            name='orderinfo',
            options={'verbose_name': '用户充值账单'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户'},
        ),
        migrations.AlterField(
            model_name='code',
            name='code_num',
            field=models.CharField(max_length=10, verbose_name='注册码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_level',
            field=models.PositiveIntegerField(verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='用户名'),
        ),
    ]