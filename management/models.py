from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    drink_count = models.IntegerField()

    def __str__(self):
        return self.name


class Drink(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField('created at')
    updated_at = models.DateTimeField('updated at')

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=128)
    order_by = models.IntegerField()
    created_at = models.DateTimeField()
    total_price = models.FloatField()
    total_drink = models.IntegerField()
    drinks = models.ManyToManyField(
        Drink,
        through='OrderDrink',
        through_fields=('order', 'drink')
    )

    def __str__(self):
        return self.order_number


class OrderDrink(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

