from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
from PIL import Image as _Image
from io import BytesIO
import sys
# Create your models here.


class Image(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    name = models.TextField(default='')
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return str(self.unique_id)

    def save(self):
        img = _Image.open(self.image)

        # transform image here
        output = BytesIO()

        im = img.resize((400, 400))

        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, 'ImageField', str(self.unique_id) + "%s.jpg" % self.image.name.split(
            '.')[0], 'image/jpeg', sys.getsizeof(output), None)
        self.name = "%s.jpg" % self.image.name.split(
            '.')[0]

        super(Image, self).save()
