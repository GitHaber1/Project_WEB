from django import forms
from .models import Category, TagPost, ScriptPost, Screenshots, Comment
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError


class AddPostForm(forms.ModelForm):
    cat_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')

    class Meta:
        model = ScriptPost
        fields = ['title', 'slug', 'content', 'about', 'is_published', 'cat_id', 'tags']
        labels = {'slug': 'URL'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина не должна превышать 50 символов')

        return title

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_")

        if not set(slug) <= allowed_chars:
            raise ValidationError("Слаг должен содержать только английские буквы, дефис и нижнее подчеркивание.")

        return slug


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'accept': 'image/*'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class AddPostFullForm(AddPostForm):
    screenshot = MultipleFileField(
        required=False,
        label='Скриншоты'
    )

    class Meta:
        model = ScriptPost
        fields = AddPostForm.Meta.fields + ['screenshot']


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-input'}
    ), label='Текст комментария')

    class Meta:
        model = Comment
        fields = ['text']
