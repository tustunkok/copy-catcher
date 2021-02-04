from django import forms
from captcha.fields import CaptchaField
from jplag_catcher import models

class SubmissionForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = models.History
        fields = ['prog_language', 'submissions']
