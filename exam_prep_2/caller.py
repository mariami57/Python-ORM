import os
import pydoc

import django
from django.db.models import Q, Count, F, Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
# Create queries within functions
def populate_db():
    profile1 = Profile.objects.create(
        full_name="Adam Smith",
        email="adam.smith@example.com",
        phone_number="123456789",
        address="123 Main St, Springfield",
        is_active=True
    )

    profile2 = Profile.objects.create(
        full_name="Susan James",
        email="susan.james@example.com",
        phone_number="987654321",
        address="456 Elm St, Metropolis",
        is_active=True
    )

    product1 = Product.objects.create(
        name="Desk M",
        description="A medium-sized office desk",
        price=150.00,
        in_stock=10,
        is_available=True

    )

    product2 = Product.objects.create(
        name="Display DL",
        description="A 24-inch HD display",
        price=200.0,
        in_stock=5,
        is_available=True

    )

    product3 = Product.objects.create(
        name="Printer Br PM",
        description="A high-speed printer",
        price=300.0,
        in_stock=3,
        is_available=True

    )

    order1 = Order.objects.create(
        profile=profile1,
        total_price=350.00,
        is_completed= False
    )
    order1.products.add(product1,product2)

    order2 = Order.objects.create(
        profile=profile1,
        total_price=300.00,
        is_completed= True
    )
    order2.products.add(product3)

    order3 = Order.objects.create(
        profile=profile1,
        total_price=650.00,
        is_completed= False
    )
    order3.products.add(product1, product2, product3)

    order4 = Order.objects.create(
        profile=profile2,
        total_price=550.00,
        is_completed= False
    )
    order4.products.add(product1, product3)

def get_profiles(search_string=None):
    if search_string is None:
        return ''

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)).order_by('full_name')

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.customer_orders.count()}"
        for p in profiles
    )

def get_loyal_profiles():
    loyal_profiles = Profile.objects.get_regular_customers()

    if not loyal_profiles:
        return ''

    return '\n'.join(f"Profile: {lp.full_name}, orders: {lp.orders_count}" for lp in loyal_profiles)


def get_last_sold_products():
    latest_order = Order.objects.prefetch_related('products').order_by('products__name').last()

    if latest_order is None or not latest_order.products.exists():
        return ''

    product_names = [p.name for p in latest_order.products.all()]

    return f"Last sold products: {', '.join(product_names)}"


def get_top_products() -> str:
    top_products = Product.objects.annotate(
        orders_count=Count('order'),
    ).filter(
        orders_count__gt=0,
    ).order_by(
        '-orders_count',
        'name',
    )[:5]

    if not top_products.exists():
        return ""

    return "Top products:\n" + "\n".join(
        f"{p.name}, sold {p.orders_count} times"
        for p in top_products
    )


def apply_discounts() -> str:
    updated_orders_count: int = Order.objects.annotate(
        products_count=Count('products'),
    ).filter(
        products_count__gt=2,
        is_completed=False,
    ).update(
        total_price=F('total_price') * 0.90,
    )

    return f"Discount applied to {updated_orders_count} orders."


def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False,
    ).order_by(
        'creation_date'
    ).first()

    if order is None:
        return ""


    Product.objects.filter(order=order).update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"
