from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_p8.settings import AUTH_USER_MODEL

# Create your models here.

class Category(models.Model):
    """ Model representing category """

    category = models.CharField(max_length=200, help_text="Enter a category name")
    
    def __str__(self):
        return self.category
class Product(models.Model):
    """ Model representing product with nutrition score """

    product = models.CharField(max_length=200, null=False, blank=False)
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="related category"
    )
    brand=models.CharField(max_length=200, null=False, blank=False)
    score=models.CharField(max_length=1, null=False, blank=False)
    pic_url=models.CharField(max_length=500, null=False, blank=True)
    url=models.CharField(max_length=500, null=False, blank=True)
    energy=models.IntegerField(null=False, blank=False, default=0)
    carbo=models.DecimalField(decimal_places=3, max_digits=7, default=0)
    fat=models.DecimalField(decimal_places=3, max_digits=7, default=0)
    proteins=models.DecimalField(decimal_places=3, max_digits=7, default=0)
    sodium=models.DecimalField(decimal_places=3, max_digits=7, default=0)
    fiber=models.DecimalField(decimal_places=3, max_digits=7, default=0)
    
    def __str__(self):
        return self.product
    
class Favorite(models.Model):
    """ Model representing user's favorites """

    user_id=models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=False, blank=False)

    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, null=False, blank=False, related_name="replaced_id")
    
    replacement_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, null=False, blank=False, default=0, related_name="replacing_id")
    
    def __str__(self):
        return str(self.user_id) + "/" +  str(self.product_id) + " vs " +  str(self.replacement_id)
      
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['user_id', 'product_id', 'replacement_id'], name='unique_replacement')
        ]
