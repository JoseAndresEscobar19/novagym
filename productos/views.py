import json
from django.db import DatabaseError
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from productos.filters import CategoriaFilter, ProductoFilter
from productos.forms import *
from .serializers import *
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
# Create your views here.
#Send email
def enviarCorreo(request):
    if request.method=="POST":
        titulo=request.POST["titulo"]
        receptor=request.POST["receptor"]
        mensaje=request.POST["mensaje"]
        send_mail(titulo,mensaje,receptor,["admin@novagym.com"])
        return render(request,"template.html",{})

#PRODUCTO

@api_view(["GET"])
def productoList(request):
    producto= Producto.objects.all()
    serializer=ProductoSerializer(producto,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def productoDetail(request,id):
    producto= Producto.objects.get(id=id)
    serializer=ProductoSerializer(producto,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def productoCreate(request):
    serializer=ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def productoUpdate(request,id):
    producto= Producto.objects.get(id=id)
    serializer=ProductoSerializer(instance=producto,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def productoDelete(request,id):
    producto= Producto.objects.get(id=id)
    try:
        producto.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Categoria

@api_view(["GET"])
def categoriaList(request):
    categoria= Categoria.objects.all()
    serializer=CategoriaSerializer(categoria,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def categoriaDetail(request,id):
    categoria= Categoria.objects.get(id=id)
    serializer=CategoriaSerializer(categoria,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def categoriaCreate(request):
    serializer=CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def categoriaUpdate(request,id):
    categoria= Categoria.objects.get(id=id)
    serializer=CategoriaSerializer(instance=categoria,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def categoriaDelete(request,id):
    categoria= Categoria.objects.get(id=id)
    try:
        categoria.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Inventario

@api_view(["GET"])
def inventarioList(request):
    inventario= Inventario.objects.all()
    serializer=InventarioSerializer(inventario,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def inventarioDetail(request,id):
    inventario= Inventario.objects.get(id=id)
    serializer=InventarioSerializer(inventario,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def inventarioCreate(request):
    serializer=InventarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def inventarioUpdate(request,id):
    inventario= Inventario.objects.get(id=id)
    serializer=InventarioSerializer(instance=inventario,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def inventarioDelete(request,id):
    inventario= Inventario.objects.get(id=id)
    try:
        inventario.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#ProductoDescuento

@api_view(["GET"])
def descuentoList(request):
    descuento= ProductoDescuento.objects.all()
    serializer=ProductoDescuentoSerializer(descuento,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def descuentoDetail(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    serializer=ProductoDescuentoSerializer(descuento,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def descuentoCreate(request):
    serializer=ProductoDescuentoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def descuentoUpdate(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    serializer=ProductoDescuentoSerializer(instance=descuento,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def descuentoDelete(request,id):
    descuento= ProductoDescuento.objects.get(id=id)
    try:
        descuento.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def createCategoria(request):
    if request.method=='POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createCategoria")
    else:
        form=CategoriaForm()
    return render(request,'createCategoria.html',{'form':form})

def createProducto(request):
    if request.method=='POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createProducto")
    else:
        form=ProductoForm()
    return render(request,'createProducto.html',{'form':form})

def createInventario(request):
    if request.method=='POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createInventario")
    else:
        form=InventarioForm()
    return render(request,'createInventario.html',{'form':form})


def createDescuento(request):
    if request.method=='POST':
        form = DescuentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos:createDescuento")
    else:
        form=DescuentoForm()
    return render(request,'createDescuento.html',{'form':form})


class crearCategoria(CreateView):
    form_class =CategoriaForm
    model=Categoria
    template_name = 'categoria_nueva.html'
    title = "CREAR CATEGORIA"
    success_url = reverse_lazy('productos:listarCategoria')

class ListarCategoria(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Categoria
    context_object_name = 'categoria'
    template_name = "lista_categoria.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=CategoriaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Categorias"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarProductos(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Producto
    context_object_name = 'producto'
    template_name = "lista_productos.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=ProductoFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Productos"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        #inventario = Inventario.objects.all()
        #producto = Producto.objects.all()
        #combo= zip(inventario,producto)
        #context['combo'] = combo
        inventario = Inventario.objects.filter(usaNovacoins=0)
        context['combo'] = inventario
        return context
        
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarProductosNC(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Producto
    context_object_name = 'producto'
    template_name = "lista_productos.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=ProductoFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Productos"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        #inventario = Inventario.objects.all()
        #producto = Producto.objects.all()
        #combo= zip(inventario,producto)
        #context['combo'] = combo
        inventario = Inventario.objects.filter(usaNovacoins=1)
        context['combo'] = inventario
        context['nc'] = 1
        return context
        
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

def deleteCategoria(request,id):
    query = Categoria.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Categoria eliminada con éxito.")
        return redirect('productos:listarCategoria')
    return render(request, "ajax/categoria_confirmar_elminar.html", {"categoria": query})

class CrearProducto(CreateView):
    form_class =ProductoForm
    template_name = 'producto_nuevo.html'
    title = "CREAR PRODUCTO"

    def get_context_data(self, **kwargs):
        context = super(CrearProducto, self).get_context_data(**kwargs)
        context['product_meta_formset'] = ProductoMeta()
        context['descuento_meta_formset'] = DescuentoMeta()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_meta_formset = ProductoMeta(self.request.POST)
        descuento_meta_formset = DescuentoMeta(self.request.POST)
        if form.is_valid() and product_meta_formset.is_valid() and descuento_meta_formset.is_valid():
            return self.form_valid(form, product_meta_formset,descuento_meta_formset)
        else:
            return self.form_invalid(form, product_meta_formset)
        
    def form_valid(self, form, product_meta_formset,descuento_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_metas = product_meta_formset.save(commit=False)
        for meta in product_metas:
            meta.producto = self.object
            meta.save()
        descuento_metas = descuento_meta_formset.save(commit=False)
        for meta in descuento_metas:
            meta.producto = self.object
            meta.save()
        return redirect(reverse("productos:listarProductos"))
    def form_invalid(self, form, product_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                product_meta_formset=product_meta_formset
                                )
        )
class UpdateProducto(UpdateView):
    template_name = "producto_nuevo.html"
    model = Producto
    form_class = ProductoForm
    context_object_name = "first_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['product_meta_formset'] = ProductoMetaU(self.request.POST,instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(self.request.POST,instance=self.object)
        else:
            context['product_meta_formset'] = ProductoMetaU(instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(instance=self.object)
        return context

    def forms_valid(self, first, seconds,third):
        try:      
            seconds.save()
            third.save()
            first.save()
            messages.success(self.request, "Actualización exitosa!")

        except DatabaseError as err:
            print(err)
            messages.error(self.request, "Ooops!  Algo salio mal...")
        return redirect(reverse("productos:listarProductos"))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        first_form = self.get_form(form_class)
        second_forms = ProductoMetaU(self.request.POST,instance=self.object)
        third_forms = DescuentoMetaU(self.request.POST,instance=self.object)
        if first_form.is_valid() and second_forms.is_valid() and third_forms.is_valid():
                    return self.forms_valid(first_form , second_forms,third_forms)
        else:
            messages.error(self.request, "Ooops! Algo salio mal...")
            return redirect(reverse("productos:listarProductos"))

class CrearProductoNC(CreateView):
    form_class =ProductoForm
    template_name = 'producto_nuevo.html'
    title = "CREAR PRODUCTO"

    def get_context_data(self, **kwargs):
        context = super(CrearProductoNC, self).get_context_data(**kwargs)
        context['product_meta_formset'] = ProductoMetaNC()
        context['descuento_meta_formset'] = DescuentoMeta()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        product_meta_formset = ProductoMetaNC(self.request.POST)
        descuento_meta_formset = DescuentoMeta(self.request.POST)
        if form.is_valid() and product_meta_formset.is_valid() and descuento_meta_formset.is_valid():
            return self.form_valid(form, product_meta_formset,descuento_meta_formset)
        else:
            return self.form_invalid(form, product_meta_formset)
        
    def form_valid(self, form, product_meta_formset,descuento_meta_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving ProductMeta Instances
        product_metas = product_meta_formset.save(commit=False)
        for meta in product_metas:
            meta.producto = self.object
            meta.save()
        descuento_metas = descuento_meta_formset.save(commit=False)
        for meta in descuento_metas:
            meta.producto = self.object
            meta.save()
        return redirect(reverse("productos:listarProductosNC"))
    def form_invalid(self, form, product_meta_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                product_meta_formset=product_meta_formset
                                )
        )

class UpdateProductoNC(UpdateView):
    template_name = "producto_nuevo.html"
    model = Producto
    form_class = ProductoForm
    context_object_name = "first_obj"
    def get_success_url(self):
        return redirect(reverse("productos:listarProductosNC"))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['product_meta_formset'] = ProductoMetaNCU(self.request.POST,instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(self.request.POST,instance=self.object)
        else:
            context['product_meta_formset'] = ProductoMetaNCU(instance=self.object)
            context['descuento_meta_formset'] = DescuentoMetaU(instance=self.object)
        return context

    def forms_valid(self, first, seconds,third):
        try:      
            seconds.save()
            third.save()
            first.save()
            messages.success(self.request, "Actualización exitosa!")

        except DatabaseError as err:
            print(err)
            messages.error(self.request, "Ooops!  Algo salio mal...")
        return redirect(reverse("productos:listarProductosNC"))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        first_form = self.get_form(form_class)
        second_forms = ProductoMetaNCU(self.request.POST,instance=self.object)
        third_forms = DescuentoMetaU(self.request.POST,instance=self.object)
        if first_form.is_valid() and second_forms.is_valid() and third_forms.is_valid():
                    return self.forms_valid(first_form , second_forms,third_forms)
        else:
            messages.error(self.request, "Ooops! Algo salio mal...")
            return redirect(reverse("productos:listarProductos"))
    
def deleteProducto(request,id):
    producto = Producto.objects.get(id=id)
    inventario = Inventario.objects.get(id=id)
    descuento = ProductoDescuento.objects.get(id=id)
    if request.POST:
        nc=inventario.usaNovacoins
        descuento.delete()
        inventario.delete()
        producto.delete()
        if nc==0:
            messages.success(request, "Producto eliminado con éxito.")
            return redirect('productos:listarProductos')
        else:
            messages.success(request, "Producto eliminado con éxito.")
            return redirect('productos:listarProductosNC')
    return render(request, "ajax/producto_confirmar_elminar.html", {"producto": producto})


def getAllProducts(request):
    urls={}
    productos=Inventario.objects.all()
    for producto in productos:
        id=producto.id
        descuento=ProductoDescuento.objects.get(id=id)
        urls[producto.producto.nombre]={
                            "codigo":producto.producto.codigo,
                            "descripcion":producto.producto.descripcion,
                            "imagen":request.build_absolute_uri('/media/')+str(producto.producto.imagen),
                            "categoria":str(producto.producto.categoria),
                            "talla":str(producto.producto.talla),
                            "precio":float(producto.precio),
                            "stock":producto.stock,
                            "novacoins":producto.novacoins,
                            "usaNovacoins":producto.usaNovacoins,
                            "porcentajeDescuento":str(descuento.porcentaje_descuento)+"%",
                            "fechaHoraDesde":str(descuento.fecha_hora_desde),
                            "fechaHoraHasta":str(descuento.fecha_hora_hasta),
                            "descuentoActivo":descuento.estado
                            }
    return HttpResponse(json.dumps(urls))