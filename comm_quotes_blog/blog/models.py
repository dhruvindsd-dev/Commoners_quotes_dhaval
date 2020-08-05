from django.db import models
import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Blog_db(models.Model):
    img_link = models.CharField(max_length=250, blank=True, null=True)
    img = models.ImageField(
        upload_to='images/', default=None, blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=350, null=False)
    subtitle = models.CharField(max_length=250, null=False)
    content = models.TextField(null=False)
    created_on = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=150, null=False)
    catagory = models.CharField(max_length=550, null=False)
    read_time = models.IntegerField(default=None, blank=True, null=True)

    def compressImage(self):
        uploadedImage = self.img
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=80)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(
            outputIoStream, 'ImageField', "%s.jpg" % f'article_{self.id}', 'image/jpeg', sys.getsizeof(outputIoStream), None)
        self.img = uploadedImage


class Submitted_articles(models.Model):
    name = models.CharField(max_length=100, null=False)
    number = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=254, null=False)
    content = models.TextField(null=False)
