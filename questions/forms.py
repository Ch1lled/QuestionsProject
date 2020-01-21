from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tag_list = forms.CharField()
    class Meta:
        model = Question
        fields = ('title', 'text')
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)

class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title', )
        