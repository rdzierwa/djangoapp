from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm
from django.views.generic import ListView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Warehouse
from .forms import WarehouseForm
from django.views import generic
import logging
logger = logging.getLogger(__name__)

class WarehouseCreateView(generic.CreateView):
    form_class = WarehouseForm
    template_name = 'add_warehouse.html'
    success_url = '/'  # Możesz zmienić na odpowiednią wartość
    
    def form_valid(self, form):
        warehouse = form.save(commit=False)
        warehouse.save()  # zapisuje magazyn
        warehouse.users.set(form.cleaned_data['users'])  # przypisuje użytkowników do magazynu
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        logger.info(form.fields['users'].queryset)  # Zaloguj queryset dla użytkowników
        return form


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.method in permissions.SAFE_METHODS


class ProductListView(LoginRequiredMixin, ListView):
    login_url = 'authenticate/login/'  # ustaw URL dla strony logowania

    model = Product
    template_name = 'list_products.html'
    context_object_name = 'products'
    paginate_by = 2
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.company:
            return Product.objects.filter(company=self.request.company)
        else:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = context['page_obj'].number
        context['max_page'] = context['paginator'].num_pages
        return context


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(warehouses__users=self.request.user)

    
    def perform_create(self, serializer):
        if self.request.user.has_perm('productapp.add_product'):
            serializer.save()
        else:
            raise permissions.PermissionDenied()

    def perform_update(self, serializer):
        if self.request.user.has_perm('productapp.change_product'):
            serializer.save()
        else:
            raise permissions.PermissionDenied()

    def perform_destroy(self, instance):
        if self.request.user.has_perm('productapp.delete_product'):
            instance.delete()
        else:
            raise permissions.PermissionDenied()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.user.has_perm('productapp.add_product'):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def synchronize_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST' and request.user.has_perm('productapp.change_product'):
        product.synchronization = not product.synchronization
        product.save()
        return Response({'synchronization': product.synchronization}, status=status.HTTP_200_OK)
    return Response({'status': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

# Podobnie dla innych widoków, jak `edit_product` oraz `DeleteProductView`

@permission_classes([IsAuthenticated])
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not request.user.has_perm('productapp.change_product'):
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('productapp:list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})





class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id, *args, **kwargs):
        if not request.user.has_perm('productapp.delete_product'):
            return Response({'status': 'error', 'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

