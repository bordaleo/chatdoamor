from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def message_image_path(instance, filename):
    """Gera o caminho para salvar a imagem da mensagem"""
    return f"messages/{instance.sender.username}/{filename}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=message_image_path, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver', '-timestamp']),
        ]

    def __str__(self):
        preview = (self.content or '').strip()
        if preview:
            preview = preview[:30]
        elif self.image:
            preview = '[imagem]'
        else:
            preview = '[vazio]'
        return f'{self.sender} -> {self.receiver}: {preview}'
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])


class UserPresence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='presence')
    is_online = models.BooleanField(default=False, db_index=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User presence'
        verbose_name_plural = 'User presence'

    def __str__(self):
        return f'{self.user.username} - {"online" if self.is_online else "offline"}'