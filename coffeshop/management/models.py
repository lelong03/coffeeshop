from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


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
    customer_name = models.CharField(max_length=128, default="guest")
    order_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    drinks = models.ManyToManyField(
        Drink,
        through='OrderDrink',
        through_fields=('order', 'drink')
    )

    def __str__(self):
        return f'{self.id} - {self.customer_name}'


class OrderDrink(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    item_price = models.FloatField(null=True)
    total_price = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.drink is not None:
            self.item_price = self.drink.price
            self.total_price = self.item_price * self.quantity
        super().save(force_insert, force_update, using, update_fields)

