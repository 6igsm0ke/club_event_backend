from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.permissions import AllowAny 

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        errors = {
            "001": "Email is already in use",
            "002": "Email is required",
            "003": "Password is required",
            "004": "Invalid date format",
            "005": "Serilizer error",
            "999": "Something went wrong",
        }
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if CustomUser.objects.filter(email=email, is_active=True).exists():
                code = "001"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
           
            if not email:
                code = "002"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not password:
                code = "003"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (not serializer.is_valid()):
                code = '005'
                return Response(
                    {"error": errors[code], "description": serializer.errors, "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            CustomUser.objects.filter(email=email, is_active=False).delete()
            user = serializer.create(serializer.validated_data)

            return Response(
                {"message": "User created successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            code = "999"
            return Response(
                {"error": errors[code], "code": code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )