from django.shortcuts import render

from rest_framework.response import Response
#from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_csv.renderers import StaticHTMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer

# Pagination
from django.core.paginator import Paginator,EmptyPage

# Class-based views w filtering classes
from rest_framework import viewsets

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
# Ordering class-based    
    ordering_fields = ['price', 'inventory']
# Search class-based (default lookup_field is icontains) 
    search_fields=['title', 'category__title']

# Create your views here.



@api_view(['GET', 'POST'])
#@renderer_classes([YAMLRenderer])
#@renderer_classes([CSVRenderer])
def menu_items(request,):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
# Filtering ?category=Desserts&to_price=3
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
# Searching ?search=Chocolate
        search = request.query_params.get('search')
# Ordering ?ordering=inventory,-price
        ordering = request.query_params.get('ordering')
# Pagination        
        perpage = request.query_params.get('perpage', default=2)
        if int(perpage) > 4:
            return Response({'error': 'you asked for too many items per page'},status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            items = items.filter(price__lte = to_price)
# i to be case insensitive
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
# added for ordering by multiple fields, comma separated             
            ordering_fields = ordering.split(",")
#            items = items.order_by(ordering)
            items = items.order_by(*ordering_fields)

# Pagination
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items=[]

        serialized_item = MenuItemSerializer(items, many = True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
#        serialized_item.validated_data
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
#        return Response(serialized_item.data)
#    return Response(items.values())

@api_view()
def single_item(request, id):
#    item = MenuItem.objects.get(pk=id)
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

#from rest_framework import generics
#from .models import MenuItem
#from .serializers import MenuItemSerializer

# Create your views here.

#class MenuItemsView(generics.ListCreateAPIView):
#    queryset = MenuItem.objects.all()
#    serializer_class = MenuItemSerializer

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# Hiperlinks: Option HyperLinkRelatedField 

from .models import Category 
from .serializers import CategorySerializer

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 


#Renderers
@api_view() 
@renderer_classes ([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
#    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data':serialized_item.data}, template_name='menu-item.html')


@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)