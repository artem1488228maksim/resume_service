from rest_framework import serializers

from resume.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "user_id")

    def validate_user_id(self, value):
        if value < 0:
            raise serializers.ValidationError("Нельзя отрицательный id")
        return value

    def validate_experience_years(self, value):
        if value > 50:
            raise serializers.ValidationError("Опыт работы не может быть больше 50 лет")
        return value

    def validate_status(self, value):
        if (
            value == "archived"
            and self.instance
            and self.instance.status != "published"
        ):
            raise serializers.ValidationError(
                "Можно архивировать только опубликованные резюме"
            )
        return value

    def create(self, validated_data, **kwargs):
        status = validated_data["status"]
        if status == "archived":
            raise serializers.ValidationError(
                "Нельзя при создании указать архивный статус"
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if (
            "user_id" in validated_data
            and validated_data["user_id"] != instance.user_id
        ):
            raise serializers.ValidationError(
                {"user_id": "Нельзя изменять ID пользователя"}
            )
        if "status" in validated_data:
            if (
                self.instance.status == "published"
                and validated_data["status"] == "draft"
            ):
                raise serializers.ValidationError(
                    "Нельзя сменить опубликованный статус на черновик"
                )
        return super().update(instance, validated_data)
