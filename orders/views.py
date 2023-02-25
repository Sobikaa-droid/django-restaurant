from django.views.generic import ListView

from .models import Order


class OrdersView(ListView):
    context_object_name = 'orders'
    paginate_by = 12
    template_name = "orders/orders.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
