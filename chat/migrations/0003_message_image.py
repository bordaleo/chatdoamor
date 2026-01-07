# Generated manually

from django.db import migrations, models


def message_image_path(instance, filename):
    """Gera o caminho para salvar a imagem da mensagem"""
    return f'messages/{instance.sender.username}/{filename}'


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_options_message_is_read_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=message_image_path),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
