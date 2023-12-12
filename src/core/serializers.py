from .models import Secret
from rest_framework import serializers


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ["secret_text", "code_phrase"]
        