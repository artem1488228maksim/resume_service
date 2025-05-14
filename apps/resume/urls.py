from django.urls import path

from resume.views import ResumeAPIView, ResumeDetailAPIView

urlpatterns = [
    path(
        "users/<int:user_id>/resumes/",
        ResumeAPIView.as_view(),
        name="user-resumes-list",
    ),
    path(
        "users/<int:user_id>/resumes/<int:resume_id>/",
        ResumeDetailAPIView.as_view(),
        name="user-resume-detail",
    ),
]
