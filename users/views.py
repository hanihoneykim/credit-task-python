from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from projects.serializers import PublicProjectSerializer, ProjectEditorSerializer
from projects.models import Project
from .serializers import PublicUserSerializer
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
