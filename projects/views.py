from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from . import serializers
from categories.models import Category
from .models import Project


class ProjectEditor(APIView):
    """프로젝트 신청 페이지 view"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.ProjectEditorSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("카테고리가 필요합니다.")
            try:
                category = Category.objects.get(pk=category_pk)
            except Category.DoesNotExist:
                raise ParseError("카테고리를 찾을 수 없습니다.")
            try:
                with transaction.atomic():
                    project = serializer.save(
                        user=request.user,
                        category=category,
                    )
                    serializer = serializers.ProjectEditorSerializer(
                        project,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception as e:
                raise ParseError("잘못된 요청입니다.")
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProjectEditorDetail(APIView):
    """관리자만 접근 가능한 신청된 프로젝트 detail view"""

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = serializers.ProjectEditorSerializer(
            project,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        """관리자는 is_approved 만 변경 가능합니다."""

        project = self.get_object(pk)

        # is_approved 필드만 수정
        is_approved = request.data.get("is_approved", None)
        if is_approved:
            project.is_approved = is_approved
            project.save(update_fields=["is_approved"])
            return Response({"is_approved": project.is_approved})
        else:
            raise ParseError("is_approved 항목만 수정 가능합니다.")
