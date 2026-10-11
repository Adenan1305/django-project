from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_userpoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_reward',
            field=models.BooleanField(default=False),
        ),
    ]
