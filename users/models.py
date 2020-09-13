from django.db import models
from django.contrib.auth.models import User
from PIL import Image

specialization_choices = (
    ('', 'Select Specialization'),
    ('BA', 'BA'),
    ('BASC', 'BASC'),
    ('BCOM', 'BCOM'),
    ('BSC', 'BSC'),
    ('other', 'other'),
)

year_choices = (
    ('', 'Select Year'),
    ('1st year', '1st year'),
    ('2nd year', '2nd year'),
    ('3rd year', '3rd year'),
    ('4th year', '4th year'),
    ('5th year', '5th year'),
    ('other', 'other'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    specialization = models.CharField(
        max_length=10, choices=specialization_choices, default='select')
    year = models.CharField(
        max_length=10, choices=year_choices, default='select')

    def __str__(self):
        return f'{self.user.username} Profile'
