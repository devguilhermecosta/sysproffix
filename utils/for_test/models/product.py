from product import models
from . hospital import create_hospital


def create_product_group(name: str = 'group') -> models.ProductGroup:
    new_group = models.ProductGroup.objects.create(
        name=name
    )
    new_group.save()
    return new_group


def create_product(code: str = '123',
                   name: str = 'product',
                   **kwargs,
                   ) -> models.Product:
    new_product = models.Product.objects.create(
        group=kwargs.get('group', create_product_group()),
        code=code,
        name=name,
    )
    new_product.save()
    return new_product


def create_product_in_batch(num_of_products: int) -> list[models.Product]:
    group = create_product_group(name='group test')
    product_list = []

    for i in range(num_of_products):
        product = create_product(name=f'product-{i}', group=group)
        product_list.append(product)

    return product_list


def create_product_item() -> tuple[models.Product, models.ProductItem]:
    hospital = create_hospital()  # create a hospital and a stock
    product = create_product()

    new_item = models.ProductItem.objects.create(
        stock=hospital.stock,
        product=product,
        lot='123',
    )
    new_item.save()
    return product, new_item
