from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemetadata',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='アップロードファイル'),
        ),
    ]
