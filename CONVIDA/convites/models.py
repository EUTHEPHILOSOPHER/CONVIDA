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

    musica = models.FileField(
        upload_to='musicas_convites/',
        blank=True,
        null=True,
        verbose_name='Música do convite',
    )

    reproduzir_musica = models.BooleanField(
        default=True,
        verbose_name='Disponibilizar música no convite',
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


class Presente(models.Model):
    convite = models.ForeignKey(
        Convite,
        on_delete=models.CASCADE,
        related_name='presentes',
    )

    nome = models.CharField(
        max_length=200,
        verbose_name='Nome do presente',
    )

    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição',
    )

    imagem = models.ImageField(
        upload_to='presentes/',
        blank=True,
        null=True,
        verbose_name='Fotografia do presente',
    )

    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantidade desejada',
    )

    link_compra = models.URLField(
        blank=True,
        verbose_name='Link de compra',
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name='Disponível na lista',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade__gte=1),
                name='presente_quantidade_minima_1',
            ),
        ]

    def __str__(self):
        return f'{self.nome} — {self.convite.titulo}'


class LocalEvento(models.Model):
    convite = models.ForeignKey(
        Convite,
        on_delete=models.CASCADE,
        related_name='locais',
        verbose_name='Convite',
    )

    nome = models.CharField(
        max_length=200,
        verbose_name='Nome do local',
    )

    atividade = models.CharField(
        max_length=200,
        verbose_name='Atividade',
    )

    data = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data',
    )

    hora = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Hora',
    )

    localizacao = models.CharField(
        max_length=255,
        verbose_name='Endereço ou localização',
    )

    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem de apresentação',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'hora', 'id']
        verbose_name = 'Local do evento'
        verbose_name_plural = 'Locais do evento'

    def __str__(self):
        return f'{self.nome} — {self.convite.titulo}'
