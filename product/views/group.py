from typing import Any
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from utils.views import OnlyAdminBaseView, OnlyAdminListView
from product.models import ProductGroup, Product
from product.forms.register import ProductGroupRegisterForm


class ProductGourpListView(OnlyAdminListView):
    model = ProductGroup
    context_object_name = 'groups'
    template_name = 'product/pages/groups.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['new_data_url'] = reverse('products:group_register')
        return ctx


class ProductGroupDetailView(OnlyAdminBaseView):
    def get(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        group = get_object_or_404(ProductGroup, pk=pk)
        session = self.request.session.get('group-edit', None)
        form = ProductGroupRegisterForm(instance=group, data=session)

        return render(
            request=self.request,
            template_name='product/pages/new_group.html',
            context={
                'group': group,
                'title': 'editar grupo',
                'form': form,
                'url': reverse('products:group_edit', args=(group.pk,)),
                'button_value': 'salvar',
                'delete_url': reverse('products:group_delete', args=(group.pk,)),  # noqa: E501
                'delete_message': 'Deseja realmente deletar este grupo de produtos?',  # noqa: E501
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        group = get_object_or_404(ProductGroup, pk=pk)
        post = self.request.POST
        self.request.session['group-edit'] = post
        form = ProductGroupRegisterForm(instance=group, data=post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Grupo salvo com sucesso',
            )

            del self.request.session['group-edit']

            return redirect(reverse('products:group_list'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('products:group_edit', args=(group.pk,)))


class ProductGroupRegisterView(OnlyAdminBaseView):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('product-group-register', None)
        form = ProductGroupRegisterForm(session)

        return render(
            request=self.request,
            template_name='product/pages/new_group.html',
            context={
                'form': form,
                'title': 'novo grupo',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['product-group-register'] = post
        form = ProductGroupRegisterForm(data=post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Grupo criado com sucesso',
            )

            del self.request.session['product-group-register']

            return redirect(reverse('products:group_list'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('products:group_register'))


class ProductGroupDeleteView(OnlyAdminBaseView):
    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        group = get_object_or_404(ProductGroup, pk=pk)
        products = Product.objects.filter(group=group)

        if products.exists():
            messages.error(
                self.request,
                'Você não pode deletar este grupo, pois existem '
                'produtos ativos e vinculados a ele',
            )
        else:
            group.delete()

            messages.success(
                self.request,
                'Grupo deletado com sucesso',
            )

        return redirect(reverse('products:group_list'))
