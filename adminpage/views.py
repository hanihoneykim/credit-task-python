from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from projects.models import Project
from projects.serializers import TinyProjectSerializer


class AdminPage(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        all_projects = Project.objects.all()
        serializer = TinyProjectSerializer(
            all_projects,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class UnderReview(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # "under_review"인 프로젝트만 필터링
        projects = Project.objects.filter(is_approved="under_review")

        serializer = TinyProjectSerializer(projects, many=True)
        return Response(serializer.data)
