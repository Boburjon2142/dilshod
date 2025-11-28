import csv
from decimal import Decimal

from django.db.models import Count, DecimalField, F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductForm
from .models import Product


def _aggregate_totals(queryset):
    totals = queryset.aggregate(
        total_products=Count("id"),
        total_quantity=Sum("quantity"),
        total_purchase_value=Sum(
            F("purchase_price") * F("quantity"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        total_sale_value=Sum(
            F("sale_price") * F("quantity"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
        total_profit=Sum(
            (F("sale_price") - F("purchase_price")) * F("quantity"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        ),
    )
    defaults = {
        "total_products": 0,
        "total_quantity": 0,
        "total_purchase_value": Decimal("0.00"),
        "total_sale_value": Decimal("0.00"),
        "total_profit": Decimal("0.00"),
    }
    return {key: totals.get(key) or defaults[key] for key in defaults}


def _format_currency(value: Decimal) -> str:
    return f"{value:,.2f} so‘m"


def product_list(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(sku__icontains=query)
        )
    totals = _aggregate_totals(products)
    context = {
        "products": products,
        "query": query,
        "totals": totals,
    }
    return render(request, "store/product_list.html", context)


def product_export_csv(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(sku__icontains=query)
        )
    totals = _aggregate_totals(products)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Sarlavha",
            "Muallif",
            "SKU",
            "Sotib olish narxi",
            "Sotish narxi",
            "Miqdor",
            "Foyda / dona",
            "Jami foyda",
        ]
    )

    for product in products:
        writer.writerow(
            [
                product.title,
                product.author,
                product.sku,
                f"{product.purchase_price:.2f}",
                f"{product.sale_price:.2f}",
                product.quantity,
                f"{product.profit_per_item:.2f}",
                f"{product.total_profit:.2f}",
            ]
        )

    writer.writerow([])
    writer.writerow(
        [
            "Jami",
            "",
            "",
            f"{totals['total_purchase_value']:.2f}",
            f"{totals['total_sale_value']:.2f}",
            totals["total_quantity"],
            "",
            f"{totals['total_profit']:.2f}",
        ]
    )

    return response


def product_export_txt(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(sku__icontains=query)
        )
    totals = _aggregate_totals(products)

    lines = []
    lines.append("Mahsulotlar ro'yxati")
    if query:
        lines.append(f"Qidiruv: {query}")
    lines.append("")
    lines.append(
        " | ".join(
            [
                "Sarlavha",
                "Muallif",
                "SKU",
                "Sotib olish narxi",
                "Sotish narxi",
                "Miqdor",
                "Foyda/dona",
                "Jami foyda",
            ]
        )
    )
    lines.append("-" * 120)
    for p in products:
        lines.append(
            " | ".join(
                [
                    p.title,
                    p.author or "—",
                    p.sku,
                    _format_currency(p.purchase_price),
                    _format_currency(p.sale_price),
                    str(p.quantity),
                    _format_currency(p.profit_per_item),
                    _format_currency(p.total_profit),
                ]
            )
        )
    lines.append("")
    lines.append("Umumiylar:")
    lines.append(f"- Jami mahsulotlar: {totals['total_products']}")
    lines.append(f"- Jami miqdor: {totals['total_quantity']}")
    lines.append(f"- Jami sotib olish qiymati: {_format_currency(totals['total_purchase_value'])}")
    lines.append(f"- Jami sotish qiymati: {_format_currency(totals['total_sale_value'])}")
    lines.append(f"- Jami foyda: {_format_currency(totals['total_profit'])}")

    response = HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="products.txt"'
    return response


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "store/product_form.html", {"form": form, "is_edit": False})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "store/product_form.html",
        {"form": form, "is_edit": True, "product": product},
    )


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(
        request, "store/product_confirm_delete.html", {"product": product}
    )
