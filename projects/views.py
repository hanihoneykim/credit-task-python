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
                # is_approved는 false로 자동 생성
                # is_approved = request.data.get("is_approved", False)

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
        pass

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass
