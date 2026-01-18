from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('mindspaceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
    ]

