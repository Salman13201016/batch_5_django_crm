from django.db import models

# Create your models here.
#oop = design pattern of coding

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    sort_order = models.CharField(unique=True)


class CourseDetails(models.Model):

    category_id_fk = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    course_title = models.CharField(max_length=200)

    course_description = models.TextField()

    course_image = models.ImageField(
        upload_to='course_images/',
        blank=True,
        null=True
    )

    actual_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )


    course_prerequisite = models.TextField(
        blank=True,
        null=True
    )

    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
