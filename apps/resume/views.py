from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from resume.models import Resume
from resume.serializers import ResumeSerializer


class ResumeAPIView(APIView):
    serializer_class = ResumeSerializer

    @extend_schema(
        operation_id="resume-list",
        summary="List/Create resumes",
        description="Get all resumes for user or create new resume",
    )
    def get(self, request, user_id):
        resumes = Resume.objects.filter(user_id=user_id)
        if not resumes.exists():
            return Response(
                {"message": "У данного пользователя отсутствуют резюме"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(resumes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Create resume", description="Create new resume for user")
    def post(self, request, user_id):
        data = request.data.copy()
        data["user_id"] = user_id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResumeDetailAPIView(APIView):
    serializer_class = ResumeSerializer

    def get_object(self, user_id, resume_id):
        try:
            return Resume.objects.get(id=resume_id, user_id=user_id)
        except Resume.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve resume",
        description="Get specific resume details",
        operation_id="resume-detail",
    )
    def get(self, request, user_id, resume_id):
        resume = self.get_object(user_id, resume_id)
        serializer = self.serializer_class(resume)
        return Response(serializer.data)

    @extend_schema(summary="Update resume", description="Update existing resume")
    def patch(self, request, user_id, resume_id):
        resume = self.get_object(user_id, resume_id)
        if resume.status == "archived":
            return Response(
                {"error": "Архивные резюме нельзя изменять"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(resume, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Delete resume", description="Delete existing resume")
    def delete(self, request, user_id, resume_id):
        resume = self.get_object(user_id, resume_id)
        if resume.status == "archived":
            return Response(
                {"error": "Архивные резюме нельзя удалять"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
