from django.db import models


class Product(models.Model):
    title = models.CharField("Sarlavha", max_length=200)
    author = models.CharField("Muallif", max_length=200, blank=True)
    sku = models.CharField("SKU / ISBN", max_length=50, unique=True)
    purchase_price = models.DecimalField("Sotib olish narxi", max_digits=10, decimal_places=2)
    sale_price = models.DecimalField("Sotish narxi", max_digits=10, decimal_places=2)
    quantity = models.IntegerField("Miqdor", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def profit_per_item(self):
        return self.sale_price - self.purchase_price

    @property
    def total_profit(self):
        return self.profit_per_item * self.quantity

    @property
    def total_purchase_value(self):
        return self.purchase_price * self.quantity

    @property
    def total_sale_value(self):
        return self.sale_price * self.quantity

    def __str__(self):
        return f"{self.title} ({self.sku})"
