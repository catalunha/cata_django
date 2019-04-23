from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

class VersaoAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, formt=None):
        """
        Retorna versão atual da api
        """
        
        return Response(settings.API_VERSION)
