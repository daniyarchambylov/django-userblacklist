from django import forms
from django.utils.translation import ugettext as _

from .consts import STATUS_CHOICES
from .models import BlackListUser


status_message_error = _('Status value is invalid. Acceptable values are ["blocked", "unblocked"]')


class UserBlacklistForm(forms.Form):
    user = forms.IntegerField()
    status = forms.CharField()
    reason = forms.CharField()
    reporter = forms.IntegerField()

    def clean_status(self):
        status = self.cleaned_data.get('status')

        statuses = [x for x, y in STATUS_CHOICES]

        if status not in statuses:
            raise forms.ValidationError(status_message_error)

        return status

    def save(self):
        status = self.cleaned_data['status']
        if status == STATUS_CHOICES[0][0]:
            instance = BlackListUser.add(self.cleaned_data['user'], self.cleaned_data['reason'], self.cleaned_data['reporter'])
        elif status == STATUS_CHOICES[1][0]:
            instance = BlackListUser.remove(self.cleaned_data['user'], self.cleaned_data['reason'], self.cleaned_data['reporter'])
        else:
            raise ValueError(status_message_error)

        return instance.as_json()
