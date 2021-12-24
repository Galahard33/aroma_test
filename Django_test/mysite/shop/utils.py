from django.db import models


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_prise'), models.Count('product'))
    if cart_data.get('total_prise__sum'):
        cart.total_prise = cart_data.get('total_prise__sum')
    else:
        cart.total_prise = 0
    cart.total_product = cart_data['product__count']
    cart.save()