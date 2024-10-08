from django.db import models

# Create your models here.


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=50)
#     image = models.ImageField(upload_to="category_images", blank=True)
#     parent_category = models.ForeignKey('self', null=True, blank=True,
#                                         related_name="children",
#                                         on_delete=models.SET_NULL,
#                                         default=None)
#     is_listed = models.BooleanField("This category is listed upon showing categories and on the sidebar",
#                                     default=True, blank=True)

#     def __str__(self):
#         return self.name


# class Exam(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, related_name='exams',
#                                  null=True,
#                                  on_delete=models.SET_NULL)
#     is_visible = models.BooleanField(default=True)
