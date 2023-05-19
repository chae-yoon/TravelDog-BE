from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .serializers import UserCreateSerializer, UserLoginSerializer, UserSerializer, UserUpdateSerializer, UserPasswordUpdateSerializer
from django.shortcuts import get_object_or_404
import datetime
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate


# Create your views here.
User = get_user_model()

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def account(request):
    # 회원정보 확인
    if request.method == 'GET':
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        token = request.COOKIES.get('token')
        # 쿠키에 토큰이 있는 경우
        if token:
            payload = jwt_decode_handler(token)
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response({'isAuth': True, 'error': False, 'data': serializer.data, },status=status.HTTP_200_OK)
        return Response({"message": "로그인이 필요합니다.", 'isAuth': False, 'error': True}, status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        # 만약 username, password에 맞는 user가 존재하지 않는다면,
        if user is None:
            return Response(
                {"message": "해당 정보와 일치하는 유저가 없습니다.", 'loginSuccess': False,}, status=status.HTTP_400_BAD_REQUEST
            )
        
        user.last_login = datetime.datetime.now()
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response(
            {
                "user": UserLoginSerializer(user).data,
                "message": "login success",
                'loginSuccess': True,
                "token": token,
            },
            status=status.HTTP_200_OK
        )
        response.set_cookie("token", token, httponly=True)
        return response
   
    # 로그아웃 
    elif request.method == 'DELETE':
        response = Response({
            "message": "로그아웃 했습니다."
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('token')
        return response
    
    # 회원 정보 수정
    elif request.method == 'PUT':
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        token = request.COOKIES.get('token')
        if token:
            payload = jwt_decode_handler(token)
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserUpdateSerializer(instance=user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(status.HTTP_400_BAD_REQUEST)
        return Response({"message": "토근이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "가입 형식에 맞지 않습니다.", "registerSuccess": False }, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(username=serializer.validated_data['username']).first() is None:
            serializer.save()
            return Response({"message": "회원가입을 완료했습니다.", "registerSuccess": True, "notExistUsername": True}, status=status.HTTP_201_CREATED)
        return Response({"message": "중복된 아이디가 있습니다.", "registerSuccess": False, "notExistUsername": False}, status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
def profile(request, username):
    person = User.objects.get(username=username)
    serializer = UserSerializer(person)
    return Response(serializer.data)


@api_view(['POST'])
def password(request):
    if request.method == 'POST':
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        token = request.COOKIES.get('token')
        if token:
            payload = jwt_decode_handler(token)
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserPasswordUpdateSerializer(instance=user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                response = Response(
                    {
                        "user": UserLoginSerializer(user).data,
                        "message": "update success",
                        "token": token,
                    },
                    status=status.HTTP_200_OK
                )
                response.set_cookie("token", token, httponly=True)
                return response
        return Response({"message": "토근이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)