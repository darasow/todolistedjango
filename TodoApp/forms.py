from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['nom', 'image', 'statut']
    def __init__(self, *warg, **kwarg):
        super(TodoForm, self).__init__(*warg, **kwarg)                                                              
        self.fields['nom'].widget.attrs['class'] = 'placeholder:italic col-span-2 md:col-span-1 placeholder:text-slate-400 block bg-white w-[100%] border border-slate-300 rounded-md py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm'
