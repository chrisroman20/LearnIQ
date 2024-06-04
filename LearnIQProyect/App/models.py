from django.db import models

# Create your models here.
class LearningStyles(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='LearningStyles/%Y/%m/%d', blank=True, null=True)

    def getImage(self):
        if self.image:
            return self.image.url
        return 'LearningStyles/default-img.jpg'