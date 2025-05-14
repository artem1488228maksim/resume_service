from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Resume(models.Model):
    user_id = models.BigIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата создания")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    title = models.CharField(max_length=255, verbose_name=_("Заголовок резюме"))
    first_name = models.CharField(max_length=150, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=150, verbose_name=_("Фамилия"))
    email = models.EmailField(verbose_name=_("Электронная почта"))
    phone_number = PhoneNumberField(
        region="BY", blank=True, verbose_name=_("Номер телефона")
    )
    profession = models.CharField(max_length=255, verbose_name=_("Профессия"))
    qualification_category = models.CharField(
        max_length=100, blank=True, verbose_name=_("Категория квалификации")
    )
    experience_years = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Опыт работы (в годах)")
    )
    work_experience = models.TextField(blank=True, verbose_name=_("Опыт работы"))
    education = models.TextField(blank=True, verbose_name=_("Образование"))
    skills = models.TextField(blank=True, verbose_name=_("Навыки"))
    additional_info = models.TextField(
        blank=True, verbose_name=_("Дополнительная информация")
    )
    portfolio_link = models.URLField(blank=True, verbose_name=_("Ссылка на портфолио"))
    status = models.CharField(
        max_length=50,
        choices=(
            ("draft", _("Черновик")),
            ("published", _("Опубликовано")),
            ("archived", _("Архивировано")),
        ),
        default="draft",
        verbose_name=_("Статус"),
    )

    class Meta:
        verbose_name = _("Резюме")
        verbose_name_plural = _("Резюме")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user_id"])]

    def __str__(self):
        return f"{self.title} ({self.first_name} {self.last_name})"
