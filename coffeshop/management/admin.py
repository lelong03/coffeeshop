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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "total_drink", "total_price")

    inlines = [OrderDrinkInline]
    # def save_model(self, request, obj, form, change):
    #     super(OrderAdmin, self).save_model(request, obj, form, change)

