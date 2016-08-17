from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    auth_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sources = models.ManyToManyField('Source')

    STATUSES = (
        ('pending', 'Pending'),
        ('check-failed', 'Check failed'),
        ('expired', 'Expired'),
        ('soon-to-expire', 'Soon to expire'),
        ('good', 'Look\'s good')
    )
    status = models.CharField(max_length=255, choices=STATUSES, default='pending')

    expiration_date = models.DateTimeField(null=True, blank=True)
    registrar = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    last_seen = models.DateTimeField()
    last_checked = models.DateTimeField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
