from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Drink(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=128, default="guest")
    order_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(null=True, blank=True)
    total_drink = models.IntegerField(null=True, blank=True)
    drinks = models.ManyToManyField(
        Drink,
        through='OrderDrink',
        through_fields=('order', 'drink')
    )

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderDrink(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

