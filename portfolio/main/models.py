from django.utils import timezone
from django.db import models


class Operation(models.Model):
    tiker = models.CharField('Тикер', max_length=15)
    LONG = 'купил'
    SHORT = 'продал'
    POZITION_CHOICES = [(LONG, 'Купил'), (SHORT, 'Продал')]
    pozition = models.CharField(
        verbose_name='Тип позиции',
        max_length=6,
        choices=POZITION_CHOICES,
        default=LONG,
    )
    quantity = models.FloatField(verbose_name='Количество', null=True)
    price = models.FloatField(verbose_name='Цена', null=True)
    comission_stavka = 0.001

    @property
    def comission(self):
        if self.pozition != 'купил':
            return round((self.summa()) * (self.comission_stavka), 2) * -1
        else:
            return round((self.summa()) * (self.comission_stavka), 2)

    @property
    def quantity_real(self):
        if self.pozition == 'купил':
            return self.quantity
        else:
            return self.quantity * (-1)

    def summa(self):
        return round((self.quantity_real) * (self.price), 2)

    def __str__(self):
        if self.tiker == None:
            return 'tiker is NULL'
        return self.tiker

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class Active(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.DO_NOTHING)
    tikers = list(set(Operation.objects.all()))
    middle = models.FloatField(verbose_name='Средняя', null=True, default=0)
    volume = models.FloatField(verbose_name='Объем', null=True, default=0)
    in_pozition = models.FloatField(verbose_name='В позиции', null=True, default=0)

    def __str__(self):
        if self.tikers == None:
            return 'tiker is NULL'
        return str(self.tikers)

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'