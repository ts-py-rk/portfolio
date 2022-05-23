from .models import Active
from .models import Operation
from django.forms import ModelForm, TextInput, Select

class OperationForm(ModelForm):
    class Meta:
        model = Operation
        fields = ['tiker', 'pozition', 'quantity', 'price']
        widgets = {
            'tiker': TextInput(attrs={
                'class': 'class_1',
                'placeholder': 'Тикер',
            }),
            'pozition': Select(attrs={
                'class': 'class_2',
                'placeholder': 'Позиция',
            }),
            'quantity': TextInput(attrs={
                'class': 'class_3',
                'placeholder': 'Введите количество',
            }),
            # 'price': TextInput(attrs={
            #     'class': 'class_4',
            #     'placeholder': 'Цена',
            # }),

        }
