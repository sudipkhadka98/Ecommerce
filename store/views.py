from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category,AddToCart,APIKey
from django.contrib import messages
from django.views.generic import CreateView, UpdateView ,DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import NewUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

#this is an template view:
class MyTemplateView(TemplateView):
    template_name = 'index.html'


#List view(Show category list):
class CategoryListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    
#this is for search category:
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = queryset = Category.objects.all()
        if query is not None and query != '':
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)

    )
        return queryset
    

#List view (show product list):
class ProductListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['category_id'])
    
    


#Detail view (show detail of an product):
class ProductDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Product
    template_name = 'product/product_detail.html'
    fields  = ["image", "product_name", "description", "price","pub_date"]
    context_object_name = 'detail'
    pk_url_kwarg = 'product_id'


#this create signup:
class CustomSignupView(CreateView):
    form_class = NewUserForm
    template_name = 'user/signup.html'
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Sign-up successful. You can now log in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid sign-up information.")
        return super().form_invalid(form)

#this create login:
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    next_page = '/' # success_url doesn't work to redirect; we need to use next_page

#this create logout
class CustomLogoutView(LogoutView):
    next_page = '/login/' # success_url doesn't work to redirect; we need to use next_page


#this is a creatview (add an product):
class CreateIndividualProduct(LoginRequiredMixin, CreateView):  
    login_url = '/login/'
    model = Product  
    fields = ["category","image", "product_name", "description", "price","pub_date"]
    template_name  = 'product/create_product.html'
    # context variable passed to the template is 'form'
    def get_success_url(self):
        category_id = self.object.category.id  # Assuming the Product model has a ForeignKey to Category
        return reverse('product_list', args=[category_id])


    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


#this is a updateview(update individual item)
class UpdateIndividualProduct(LoginRequiredMixin, UpdateView):  
    login_url = '/login/'
    model = Product
    template_name = 'product/update_product.html'
    fields = ["category","image", "product_name", "description", "price","pub_date"]
    pk_url_kwarg = 'product_id'
    
    def get_success_url(self):
        product = self.get_object()
        return reverse_lazy('product_list', kwargs={'category_id': product.category.id})


#this is deleteview (delete individual item)
class DeleteIndividualProduct(LoginRequiredMixin, DeleteView):  
    login_url = '/login/'
    model = Product 
    template_name = 'product/delete_product.html' # DeleteView Requires confirmation template with a POST method form
    pk_url_kwarg = 'product_id'
    
    def get_success_url(self):
        product = self.get_object()
        return reverse_lazy('product_list', kwargs={'category_id': product.category.id})

#categories
class CreateIndividualCategory(LoginRequiredMixin, CreateView):  
    login_url = '/login/'
    model = Category 
    fields = ["name", "description"]
    template_name  = 'category/create_category.html'
    success_url = reverse_lazy('category_list') 

class UpdateIndividualCategory(LoginRequiredMixin, UpdateView):  
    login_url = '/login/'
    model = Category
    fields = ["name", "description"]
    template_name = 'category/update_category.html'
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('category_list') 

class DeleteIndividualCategory(LoginRequiredMixin, DeleteView):  
    login_url = '/login/'
    model = Category
    template_name = 'category/delete_category.html' # DeleteView Requires confirmation template with a POST method form
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('category_list') 



#cart item
class CartItemListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = AddToCart
    template_name = 'cart/cartitem_list.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return AddToCart.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()  # Fetch cart items
        for item in cart_items:
            item.total_price = item.quantity * item.product.price
        context['cart'] = cart_items  # Add to context
        return context
    
class AddToCartView(LoginRequiredMixin, CreateView):
    model = AddToCart
    fields = ['quantity']  # Ensure 'added_at' is in your model fields
    template_name = 'add_to_cart_form.html'
    success_url = reverse_lazy('cartitem_list')

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, pk=product_id)
        form.instance.user = self.request.user
        form.instance.product = product
        return super().form_valid(form)
    
class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = AddToCart
    fields = ['quantity']
    template_name = 'cart/cart_item_form.html'
    success_url = reverse_lazy('cartitem_list')

class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = AddToCart
    template_name = 'cart/cart_item_confirm_delete.html'
    success_url = reverse_lazy('cartitem_list')

#rest api
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer, AddToCartSerializer
from rest_framework import permissions


class IsAuthenticatedOrValidAPIKey(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        
        api_key = request.META.get('HTTP_AUTHORIZATION')
        if api_key:
            try:
                key_obj = APIKey.objects.get(key=api_key)
                if key_obj:
                    return True
            except APIKey.DoesNotExist:
                return False
        return False


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrValidAPIKey]
    model=Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        
        api_key = self.request.META.get('HTTP_AUTHORIZATION')
        if api_key is not None:
            print(f"Received API key: {api_key}")
            try:
                key_obj = APIKey.objects.get(key=api_key)
                user = key_obj.user
                return self.model.objects.filter(user=user)
            except:
                # Handle the case where the key is invalid
                return None  # Or return an empty queryset

    #     user = self.request.user
    #     return self.model.objects.filter(user=user) # Return a queryset of Todos that belong to the current user

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        
        api_key = self.request.META.get('HTTP_AUTHORIZATION')
        if api_key is not None:
            print(f"Received API key: {api_key}")
            try:
                key_obj = APIKey.objects.get(key=api_key)
                user = key_obj.user
                return self.model.objects.filter(user=user)
            except:
                # Handle the case where the key is invalid
                return None  # Or return an empty queryset

        user = self.request.user
        return self.model.objects.filter(user=user) # Return a queryset of Todos that belong to the current user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddToCartViewSet(viewsets.ModelViewSet):
    queryset = AddToCart.objects.all()
    serializer_class = AddToCartSerializer

    def get_queryset(self):
        
        api_key = self.request.META.get('HTTP_AUTHORIZATION')
        if api_key is not None:
            print(f"Received API key: {api_key}")
            try:
                key_obj = APIKey.objects.get(key=api_key)
                user = key_obj.user
                return self.model.objects.filter(user=user)
            except:
                # Handle the case where the key is invalid
                return None  # Or return an empty queryset

        user = self.request.user
        return self.model.objects.filter(user=user) # Return a queryset of Todos that belong to the current user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)