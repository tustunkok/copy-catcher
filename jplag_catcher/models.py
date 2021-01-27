from django.db import models

# Create your models here.
class History(models.Model):
    LANGUAGE_CHOICES = [
        ('java19', 'Java 1.9'),
        ('java17', 'Java 1.7'),
        ('java15', 'Java 1.5'),
        ('java15dm', 'Java 1.5 DM'),
        ('java12', 'Java 1.2'),
        ('java11', 'Java 1.1'),
        ('python3', 'Python 3'),
        ('c/c++', 'C/C++'),
        ('c#-1.2', 'C# 1.2'),
        ('char', 'Char'),
        ('text', 'Text'),
        ('scheme', 'Scheme'),
    ]

    ip_address = models.CharField(null=False, max_length=15)
    prog_language = models.CharField(null=False, blank=False, max_length=8, choices=LANGUAGE_CHOICES)
    upload_time = models.DateTimeField(null=False, auto_now=True)
    submissions = models.FileField(upload_to='./', null=False, blank=False)

    def __str__(self):
        return self.ip_address + " - " + str(self.upload_time)
