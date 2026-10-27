
from django.db import models
from django.utils import timezone

from convites.models import Convite, Presente


class Convidado(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('recusado', 'Não vai participar'),
    ]

    convite = models.ForeignKey(
        Convite,
        on_delete=models.CASCADE,
        related_name='convidados',
    )

    nome = models.CharField(
        max_length=150,
        verbose_name='Nome completo',
    )

    email = models.EmailField(
        blank=True,
        verbose_name='Email',
    )

    telefone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Telefone',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    numero_acompanhantes = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Número de acompanhantes',
    )

    mensagem = models.TextField(
        blank=True,
        verbose_name='Mensagem do convidado',
    )

    confirmado_em = models.DateTimeField(
        null=True,
        blank=True,
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
    )

    
    GRAU_PARENTESCO_CHOICES = [
        ('familia', 'Familiar'),
        ('amigo', 'Amigo/a'),
        ('colega', 'Colega de trabalho'),
        ('conhecido', 'Conhecido/a'),
        ('outro', 'Outro'),
    ]

    grau_parentesco = models.CharField(
        max_length=20,
        choices=GRAU_PARENTESCO_CHOICES,
        default='outro',
        verbose_name='Grau de parentesco ou relação',
    )


    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['convite', 'email'],
                condition=~models.Q(email=''),
                name='unico_email_por_convite',
            ),
        ]

    def save(self, *args, **kwargs):
        if self.status in ('confirmado', 'recusado'):
            if self.confirmado_em is None:
                self.confirmado_em = timezone.now()
        else:
            self.confirmado_em = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} — {self.convite.titulo}'



class ReservaPresente(models.Model):
    STATUS_CHOICES = [
        ('reservado', 'Reservado'),
        ('cancelado', 'Cancelado'),
    ]

    presente = models.ForeignKey(
        Presente,
        on_delete=models.CASCADE,
        related_name='reservas',
    )

    convidado = models.ForeignKey(
        Convidado,
        on_delete=models.SET_NULL,
        related_name='reservas_presentes',
        null=True,
        blank=True,
    )

    nome_reservante = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nome de quem reservou',
    )

    telefone_reservante = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Telefone de quem reservou',
    )

    email_reservante = models.EmailField(
        blank=True,
        verbose_name='E-mail de quem reservou',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='reservado',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        constraints = [
            models.UniqueConstraint(
                fields=['presente', 'convidado'],
                condition=models.Q(
                    status='reservado',
                    convidado__isnull=False,
                ),
                name='reserva_ativa_unica_por_convidado',
            ),
            models.UniqueConstraint(
                fields=['presente', 'telefone_reservante'],
                condition=(
                    models.Q(status='reservado')
                    & ~models.Q(telefone_reservante='')
                ),
                name='reserva_ativa_unica_por_telefone',
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.presente_id
            and self.convidado_id
            and self.presente.convite_id != self.convidado.convite_id
        ):
            raise ValidationError(
                'O presente e o convidado devem pertencer ao mesmo convite.'
            )

    def __str__(self):
        nome = self.nome_reservante

        if not nome and self.convidado_id:
            nome = self.convidado.nome

        return f'{self.presente.nome} — {nome or "Reserva"}'
