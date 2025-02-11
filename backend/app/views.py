from django.shortcuts import render
from rest_framework.views import APIView
from .models import React
from .serializer import ReactSerializer
from rest_framework.response import Response

class ReactView(APIView):
    def get(self, request):
        output = [{"employee": obj.employee, "department": obj.department} 
                  for obj in React.objects.all()]
        return Response(output)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
