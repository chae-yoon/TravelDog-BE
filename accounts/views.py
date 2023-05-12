from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.hashers import check_password
from .serializers import UserCreateSerializer, UserLoginSerializer, UserSerializer, UserUpdateSerializer, UserPasswordUpdateSerializer
from django.shortcuts import get_object_or_404
import datetime
import jwt
from django.conf import settings

# Create your views here.
User = get_user_model()

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def account(request):
    # 회원정보 확인
    if request.method == 'GET':
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access_token']
            payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access_token', access)
                res.set_cookie('refresh_token', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # 로그인
    elif request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        user = User.objects.get(username=username)

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
            user.last_login = datetime.datetime.now()
            user.save()
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

    # 로그아웃 
    elif request.method == 'DELETE':
        response = Response({
        "message": "로그아웃 했습니다."
        }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    
    elif request.method == 'PUT':
        access = request.COOKIES['access_token']
        payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "가입 형식에 맞지 않습니다."}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(username=serializer.validated_data['username']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "중복된 아이디가 있습니다."}, status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
def profile(request, username):
    person = User.objects.get(username=username)
    serializer = UserSerializer(person)
    return Response(serializer.data)


@api_view(['POST'])
def password(request):
    if request.method == 'POST':
        access = request.COOKIES['access_token']
        payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
        pk = payload.get('user_id')
        user = get_object_or_404(User, pk=pk)
        serializer = UserPasswordUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
