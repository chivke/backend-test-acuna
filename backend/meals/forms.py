from django import forms

from backend.meals.models import MenuModel, PlateModel, MealModel


class MenuForm(forms.ModelForm):
    '''
    Form to edit menus
    '''
    date = forms.DateField(
        label='Date of menu',
        widget=forms.SelectDateWidget)

    class Meta:
        model = MenuModel
        fields = ['date', 'plates']


class PlateForm(forms.ModelForm):
    '''
    Form to edit plate
    '''
    short_desc = forms.CharField(
        label='Short description of plate',
        required=True)
    description = forms.CharField(
        label='Description of plate',
        widget=forms.Textarea,
        required=False)

    class Meta:
        model = PlateModel
        fields = ['short_desc', 'description']


class MenuPreferenceForm(forms.ModelForm):
    '''
    Form to serialize meals
    '''

    class Meta:
        model = MealModel
        fields = ['plate', 'customization']
