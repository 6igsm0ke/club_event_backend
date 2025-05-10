from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .utils import *
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


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
            user = serializer.save()

            return Response(
                {"message": "Verify email sent"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            code = "999"
            return Response(
                {"error": errors[code], "code": code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method == "PATCH":
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerificationView(APIView):
    def get(self, request, token_id):
        errors = {
            "001": "Invalid token is provided",
            "002": "Token has already been used",
            "999": "Something went wrong",
        }
        try:
            is_valid, token = Token.check_and_get_token(token_id, 0)
            if is_valid:
                user = token.user
                user.is_active = True
                user.save()

                token.is_used = True
                token.save()

                return Response(
                    {"message": "Email confirmed! Now you can log in."},
                    status=status.HTTP_200_OK,
                )
            if not is_valid:
                code = "001"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if token.is_used:
                code = "002"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            code = "999"
            return Response(
                {"error": errors[code], "code": code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class PasswordResetView(APIView):
    def post(self, request, token_id=None):
        errors = {
            "001": "Token is valid but password not provided",
            "002": "New password is same as previous",
            "003": "User with this email not found",
            "004": "Invalid token is provided",
            "005": "Token has already been used",
            "006": "Email is required",
            "999": "Something went wrong",
        }
        try:
            if token_id is None:
                # Handle password reset request (send email)
                email = request.data.get("email")
                try:
                    user = CustomUser.objects.get(email=email)
                    if email:
                        send_password_reset_email(user)
                        return Response(
                            {"message": "Password reset email sent!"},
                            status=status.HTTP_200_OK,
                        )
                    else:
                        code = "006"
                        return Response(
                            {"error": errors[code], "code": code},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except CustomUser.DoesNotExist:
                    code = "003"
                    return Response(
                        {"error": errors[code], "code": code},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                serializer = ResetPasswordSerializer(data=request.data)
                if serializer.is_valid():
                    is_valid, token = Token.check_and_get_token(token_id, 1)

                    if not is_valid:
                        code = "004"
                        return Response(
                            {"error": errors[code], "code": code},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if token.is_used:
                        code = "005"
                        return Response(
                            {"error": errors[code], "code": code},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                    if is_valid:
                        user = token.user
                        new_password = serializer.validated_data["password"]
                        if not new_password:
                            code = "001"
                            return Response(
                                {"error": errors[code], "code": code},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                        if user.check_password(new_password):
                            code = "002"
                            return Response(
                                {"error": errors[code], "code": code},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                        else:
                            user.set_password(new_password)
                            user.save()

                            token.is_used = True
                            token.save()
                        return Response(
                            {"message": "Password reset successfully!"},
                            status=status.HTTP_200_OK,
                        )

        except Exception:
            code = "999"
            return Response(
                {"error": errors[code], "code": code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )