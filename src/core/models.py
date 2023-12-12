from django.db import models


class Secret(models.Model):
    secret_text = models.TextField()
    code_phrase = models.CharField(max_length=256)
    secret_key = models.CharField(max_length=256)
    is_revealed = models.BooleanField(default=False)

    def __str__(self):
        return self.secret_key
