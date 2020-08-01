from django.db.models import Q
from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# Create your views here.

class SearchView(ListView):
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q', None )
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.all()