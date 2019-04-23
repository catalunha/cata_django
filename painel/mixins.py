import uuid
from django.db import models
from django.conf import settings
from mimetypes import guess_extension
from django.utils.timezone import now
from drf_extra_fields.fields import Base64FileField
from magic import Magic, MAGIC_MIME_TYPE

class TimedModelMixin(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)

    class Meta:
        abstract = True

class UserModelMixin(models.Model):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	class Meta:
		abstract = True
		ordering = ["usuario"]


class ArquivoBase64SerializerField(Base64FileField):
    ALLOW_ALL_TYPES = True

    def get_file_extension(self, filename, decoded_file):
        with Magic(flags=MAGIC_MIME_TYPE) as m:
            return guess_extension(m.id_buffer(decoded_file))
