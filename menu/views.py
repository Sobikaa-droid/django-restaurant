from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin

from .models import Food
from cart.forms import AmountForm


class MenuView(ListView):
    queryset = Food.objects.prefetch_related("categories").all()
    context_object_name = 'foods'
    paginate_by = 8
    template_name = "menu/menu.html"


class FoodDetailView(DetailView, ModelFormMixin):
    model = Food
    form_class = AmountForm
    template_name = "menu/food_detail.html"


# def food_detail(request, pk):
#     food_object = get_object_or_404(Food, pk=pk)
#     form = AmountForm
#
#     context = {
#         'food': food_object,
#         'form': form,
#     }
#
#     return render(request, 'menu/food_detail.html', context)
