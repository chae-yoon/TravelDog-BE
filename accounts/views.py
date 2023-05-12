from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from .serializers import UserCreateSerializer, UserLoginSerializer

# Create your views here.
User = get_user_model()

@api_view(['POST'])
def account(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "가입 형식에 맞지 않습니다."}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(username=serializer.validated_data['username']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "중복된 아이디가 있습니다."}, status=status.HTTP_409_CONFLICT)

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return Response(data={
            "message" : "Hello",
        })
    elif request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        # 만약 username에 맞는 user가 존재하지 않는다면,
        if user is None:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우,
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user가 맞다면,
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user) # refresh 토큰 생성
            refresh_token = str(token) # refresh 토큰 문자열화
            access_token = str(token.access_token) # access 토큰 문자열화
            response = Response(
                {
                    "user": UserLoginSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        response = Response({
        "message": "로그아웃 했습니다."
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('refresh_token')

    return response