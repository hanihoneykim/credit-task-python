from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from . import serializers
from categories.models import Category
from .models import Project
from users.models import User
import boto3


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

    def patch(self, request, pk):
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


class ProjectList(APIView):
    def get(self, request):
        # "under_review"인 프로젝트만 필터링
        projects = Project.objects.filter(is_approved="approval")

        serializer = serializers.PublicProjectSerializer(projects, many=True)
        return Response(serializer.data)


class S3Uploads(APIView):
    def post(self, request):
        try:
            photo = request.FILES.get("photo")
            user = request.user  # 현재 로그인한 사용자를 가져옵니다.
            title = request.data.get("title")
            description = request.data.get("description")
            category_id = request.data.get("category")

            try:
                category = Category.objects.get(pk=category_id)  # 카테고리를 찾습니다.
            except Category.DoesNotExist:
                return Response({"ERROR": "Category not found"}, status=HTTP_400_BAD_REQUEST)

            s3r = boto3.resource(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            key = f"{user}/{photo.name}"
            s3r.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=key, Body=photo, ContentType="image/jpeg"
            )
            photo_url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{key}"

            project = Project.objects.create(
                title=title,
                description=description,
                user=user,
                photo_url=photo_url,
                category=category,  # Category 모델의 인스턴스를 할당합니다.
            )

            # 처리 완료 후 응답
            return Response({"MESSAGE": "SUCCESS"}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"ERROR": str(e)}, status=HTTP_400_BAD_REQUEST)
