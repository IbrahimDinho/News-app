from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from headLine.models import UserProfile,Article,Category


class BaseForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class ArticleForm(forms.Form):
    article_title = forms.CharField(max_length=100, required=True)
    article_summary = forms.CharField(max_length=200, required=True)
    article_body = forms.CharField(max_length=2000, required=True)
    class Meta:
        model = Article
        fields = ('article_title', 'article_summary','article_body')

class CategoryForm(forms.Form):
    category_name = forms.CharField(max_length=50, required=True)
    category_description = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Category
        fields = ('category_name', 'category_description')
    

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}
    ), required=True)
    profile_photo = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'profile_photo',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())

    class Meta:
        fields = ('username', 'password')


class ModifyProfilePhotoForm(forms.Form):
    profile_photo = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(ModifyProfilePhotoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Div(Div(Field('profile_photo'), css_class="col-11"),
                Div(

                    Div(

                        Div(
                            Submit(name="photoChange", css_class='btn btn-primary', value='Submit'), css_class='col-3'),
                        Div(
                            Submit(name="photoDelete", css_class='btn btn-danger', value='Delete'), css_class='col-3'),
                        css_class="row  justify-content-around")
                    , css_class="row justify-content-center")))
        self.helper.form_method = 'POST'


class PreferenceForm(forms.Form):
    selected_categories = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        selected = kwargs.pop('selected', None)
        super(PreferenceForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['selected_categories'].choices = choices
        if selected:
            self.fields['selected_categories'].initial = selected

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Div(Field('selected_categories', css_class="w-100"), css_class="col-11"), css_class="row"),
            Div(Div(Submit(name="preference", css_class='btn-primary', value='Submit'), css_class="col-auto"),
                css_class="row justify-content-center m-4")

        )
        self.helper.form_method = 'POST'
