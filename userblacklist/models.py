from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from userblacklist.consts import STATUS_CHOICES


class BlackListUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return '%s  [%s] {%s} @ %s' % (self.id, self.user, self.status, self.created_at)

    def __repr__(self):
        return '%s  [%s] {%s} @ %s' % (self.id, self.user, self.status, self.created_at)

    @classmethod
    def add(cls, user, reason):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not isinstance(user, User):
            user = User.objects.get(pk=user)

        user.is_blocked = True
        obj = cls.objects.create(user=user, reason=reason, status=STATUS_CHOICES[0][0])
        user.save()
        return obj

    @classmethod
    def remove(cls, user, reason):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not isinstance(user, User):
            user = User.objects.get(pk=user)

        user.is_blocked = False
        obj = cls.objects.create(user=user, reason=reason, status=STATUS_CHOICES[1][0])
        user.save()
        return obj

    def as_json(self):
        return {
            'id': self.id,
            'reason': self.reason,
            'created_at': self.created_at,
            'status': self.status,
        }
