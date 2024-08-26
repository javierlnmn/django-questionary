from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            default_pfp_number = (self.id % 4) if (self.id % 4) != 0 else 4
            return static(f'images/default_pfp_{default_pfp_number}.png')

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'