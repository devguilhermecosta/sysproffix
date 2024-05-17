from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.decorators import only_user_admin
from .. forms.register import ProductRegisterForm, ProductGroupRegisterForm
from .. models import Product, ProductItem


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class ProductListView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        products = Product.objects.all()

        return render(
            self.request,
            'product/pages/list.html',
            context={
                'products': products,
                'new_data_url': reverse('products:new'),
            }
        )


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class ProductCreateView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('new-product', None)
        form = ProductRegisterForm(session)

        return render(
            self.request,
            'product/pages/new.html',
            context={
                'form': form,
                'title': 'novo produto',
                'new_group_url': reverse('products:new_group'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['new-product'] = post
        form = ProductRegisterForm(post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Produto criado com sucesso',
            )

            del self.request.session['new-product']

            return redirect(reverse('products:list'))

        messages.error(
            self.request,
            'Existem erros no formulário'
        )

        return redirect(reverse('products:new'))


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class ProductDetailView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        product = get_object_or_404(Product, id=pk)
        session = self.request.session.get('product-details', None)
        form = ProductRegisterForm(instance=product, data=session)

        return render(
            self.request,
            'product/pages/details.html',
            context={
                'form': form,
                'button_value': 'salvar',
                'title': 'editar produto',
                'delete_message': 'Deseja realmente deletar este produto?',
                'new_group_url': reverse('products:new_group'),
                'delete_url': reverse('products:delete', args=(product.pk,))
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        product = get_object_or_404(Product, id=pk)
        post = self.request.POST
        self.request.session['product-details'] = post
        form = ProductRegisterForm(instance=product, data=post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Produto salvo com sucesso',
            )

            del self.request.session['product-details']

            return redirect(reverse('products:list'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('products:details', args=(product.pk,)))


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class ProductDeleteView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        product = get_object_or_404(Product, id=pk)

        product_item = ProductItem.objects.filter(product=product)

        if product_item.exists():
            messages.error(
                self.request,
                (
                    'Este produto possui movimentações, '
                    'por isso não pode ser deletado.'
                )
            )

            return redirect(reverse('products:details', args=(product.pk,)))

        product.delete()

        messages.success(
            self.request,
            'Produto deletado com sucesso',
        )

        return redirect(reverse('products:list'))
        # TODO criar um ProductItem para testar na prática a mensagem de erro


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class AddNewGroupView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('new-group', None)
        form = ProductGroupRegisterForm(session)

        return render(
            self.request,
            'product/pages/new_group.html',
            context={
                'form': form,
                'title': 'novo grupo',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['new-group'] = post
        form = ProductGroupRegisterForm(post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Grupo criado com sucesso',
            )

            del self.request.session['new-group']

            return redirect(reverse('products:new'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('products:new_group'))
