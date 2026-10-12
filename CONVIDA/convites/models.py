from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Convite(models.Model):

    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado'),
    ]

    TIPO_EVENTO_CHOICES = [
        ('casamento', 'Casamento'),
        ('aniversario', 'Aniversário'),
        ('batizado', 'Batizado'),
        ('formatura', 'Formatura'),
        ('noivado', 'Noivado'),
        ('cha', 'Chá'),
        ('outro', 'Outro'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='convites'
    )

    titulo = models.CharField(
        max_length=200,
        verbose_name='Título do convite'
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )

    tipo_evento = models.CharField(
        max_length=30,
        choices=TIPO_EVENTO_CHOICES,
        default='outro'
    )

    template = models.CharField(
        max_length=100,
        default='minimal-blue'
    )

    data_evento = models.DateField(
        null=True,
        blank=True
    )

    hora_evento = models.TimeField(
        null=True,
        blank=True
    )

    local_evento = models.CharField(
        max_length=255,
        blank=True
    )

    descricao = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            contador = 1

            while Convite.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{contador}'
                contador += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

