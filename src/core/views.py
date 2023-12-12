from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Secret
from .serializers import SecretSerializer
from .utils import get_note_id
    
class SecretCreateAPIView(generics.CreateAPIView):
    serializer_class = SecretSerializer

    def perform_create(self, serializer):
        secret_text = serializer.validated_data['secret_text']
        code_phrase = serializer.validated_data['code_phrase']
        secret_key = get_note_id(secret_text, code_phrase)
        serializer.save(secret_key=secret_key)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'secret_key': serializer.instance.secret_key}, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SecretRetrieveAPIview(generics.RetrieveAPIView):
    serializer_class = SecretSerializer
    queryset = Secret.objects.all()
    lookup_field = 'secret_key'
    
    def retrieve(self, request, *args, **kwargs):
        secret_key = self.kwargs.get('secret_key')
        secret = self.queryset.filter(secret_key=secret_key).first()
        code_phrase = request.GET.get('code_phrase', '')
        
        if secret.is_revealed:
            return Response({'error': 'Secret has already been revealed'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if secret.code_phrase != code_phrase:
            return Response({'error': 'Invalid code phrase'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        secret.is_revealed = True
        secret.save()
        return Response({'secret_text': secret.secret_text}, 
                        status=status.HTTP_200_OK)
