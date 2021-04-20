from django.contrib import admin
from .models import Category, Drink, Order, OrderDrink

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Drink)
# admin.site.register(Order)


class DrinkInline(admin.StackedInline):
    model = Drink


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "drink_count")
    inlines = [DrinkInline]

    def drink_count(self, obj):
        return obj.drink_set.count()

    def save_model(self, request, obj, form, change):
        super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")


class OrderDrinkInline(admin.TabularInline):
    model = OrderDrink
    fields = ("drink", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "customer_name", "order_by", "total_drink", "total_price")
    fields = ("customer_name",)
    inlines = [OrderDrinkInline]

    def total_drink(self, obj):
        drink_count = 0
        for order_drink in obj.orderdrink_set.all():
            drink_count += order_drink.quantity
        return drink_count

    def total_price(self, obj):
        total = 0
        for order_drink in obj.orderdrink_set.all():
            total += order_drink.total_price
        return total

    def save_model(self, request, obj, form, change):
        obj.order_by = request.user
        super().save_model(request, obj, form, change)

