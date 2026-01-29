from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .utils.pop_permission import ProofOfPossessionPermission
from rest_framework.permissions import IsAuthenticated


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SecureDataView(APIView):
    permission_classes = [IsAuthenticated, ProofOfPossessionPermission]

    def get(self, request):
        return HttpResponse({"data": "PoP protected data"})
