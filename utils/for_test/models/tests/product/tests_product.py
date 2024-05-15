from django.test import TestCase
from product import models
from ... product import (
    create_product_group,
    create_product,
    create_product_in_batch,
    create_product_item
)


class ProductTests(TestCase):
    def test_create_product_group_func_must_create_a_new_group(self) -> None:  # noqa: E501
        group = create_product_group()
        self.assertIsInstance(
            group,
            models.ProductGroup,
        )

    def test_create_product_func_must_create_a_new_product(self) -> None:
        product = create_product()
        self.assertIsInstance(
            product,
            models.Product,
        )

    def test_create_product_in_batch_func_must_create_a_list_of_product(self) -> None:  # noqa: E501
        products = create_product_in_batch(3)
        self.assertEqual(len(products), 3)
        self.assertIsInstance(products[0], models.Product)

    def test_create_product_item_func_must_create_a_new_product_item(self) -> None:  # noqa: E501
        _, item = create_product_item()
        self.assertIsInstance(item, models.ProductItem)
