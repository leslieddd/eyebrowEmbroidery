from django.db import models

class CustomerFace(models.Model):
    cust_name = models.CharField(max_length=200)
    cust_face = models.ImageField()

    def __str__(self):
        return self.cust_name

class PostSimFace(models.Model):
    postsim_name = models.CharField(max_length=200)
    postsim_face = models.ImageField()

    def __str__(self):
        return self.postsim_name


class EyeBrowFace(models.Model):
    eyebrow_name = models.CharField(max_length=200)
    eyebrow_face = models.ImageField()

    def __str__(self):
        return self.eyebrow_name