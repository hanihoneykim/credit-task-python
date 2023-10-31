from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from projects.serializers import PublicProjectSerializer, ProjectEditorSerializer
from projects.models import Project
from .serializers import PublicUserSerializer, PrivateUserSerializer
from .models import User


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        user_serializer = PublicUserSerializer(user)
        # 해당 사용자가 작성한 프로젝트 중 'approval'인 프로젝트 가져오기
        approved_projects = Project.objects.filter(user=user, is_approved="approval")
        project_serializer = PublicProjectSerializer(approved_projects, many=True)

        response_data = {
            "user_info": user_serializer.data,
            "approved_projects": project_serializer.data,
        }

        return Response(response_data)


class MyProjects(APIView):
    def get(self, request):
        user = request.user
        my_projects = Project.objects.filter(user=user)
        serializer = ProjectEditorSerializer(my_projects, many=True)
        return Response(serializer.data)


class Users(APIView):
    def post(self, request):
        """유저 생성"""
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
