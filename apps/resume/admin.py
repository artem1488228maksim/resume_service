from django.contrib import admin
from resume.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
