from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import redirect_to_login
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render

from seguridad.filters import ClienteFilter, UsuarioFilter
from seguridad.forms import (RolUsuarioForm, UsuarioDetallesForm,
                             UsuarioEditarForm, UsuarioForm)

from .models import *

# Admin

APP_PERMISSIONS = {
    'seguridad': {'label': 'Usuarios', 'app': 'seguridad', 'model': 'userdetails'},
    # 'novagym':'',
    # 'gimnasio': {'model': 'gimnasio', 'label': ''},
    'productos': {'label': 'Productos', 'app': 'productos', 'model': 'producto'},
    # 'contactenos':'',
    'sponsor': {'label': 'Negocios Afiliados', 'app': 'sponsor', 'model': 'sponsor'},
    'notificaciones': {'label': 'Notificaciones', 'app': 'notificaciones', 'model': 'notificacion'},
}  # TODO: agregar apps:model


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next', None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser or (user.is_active and user.detalles.tipo == 'E'):
                login(request, user)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('novagym:principal')
            if not user.is_active:
              messages.error(request, 'Esta cuenta ha sido desactivada.')
            if not user.detalles.tipo == 'E':
              messages.error(request, 'Solo admin/empleados pueden ingresar.')
            return redirect('seguridad:login_admin')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrecto.')
            return redirect('seguridad:login_admin')
    else:
        if request.user and request.user.is_authenticated:
            return redirect('novagym:principal')
        else:
            return render(request, 'login.html', {"title": "Iniciar Sesión"})


def logout_user(request):
    if request.GET:
        logout(request)
        return redirect('seguridad:login_admin')


class UsuarioPermissionRequieredMixin(PermissionRequiredMixin, AccessMixin):
    raise_exception = False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class ListarUsuarios(LoginRequiredMixin, UsuarioPermissionRequieredMixin, FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = UserDetails
    context_object_name = 'usuarios'
    template_name = "lista_usuarios.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class_emp = UsuarioFilter
    filterset_class_cli = ClienteFilter

    def get_filterset_class(self):
        return self.filterset_class_emp if self.kwargs['type'] == "E" else self.filterset_class_cli

    def get_queryset(self):
        return self.model.objects.filter(tipo=self.kwargs['type'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Empleados" if self.kwargs['type'] == "E" else "Clientes"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context


class CrearUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = UserDetails
    form_class = UsuarioDetallesForm
    user_form_class = UsuarioForm
    template_name = 'usuario_nuevo.html'
    success_url = 'seguridad:listar'
    permission_required = 'seguridad.add_userdetails'

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={'type': self.request.GET['type']})

    def get_success_message(self):
        return "{} creado con éxito.".format("Empleado" if self.request.GET['type'] == 'E' else "Cliente")

    def get_title(self):
        return "Agregar {}".format("empleado" if self.request.GET['type'] == 'E' else "cliente")

    def get_context_data(self, **kwargs):
        context = super(CrearUsuario, self).get_context_data(**kwargs)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class()
        if "form" not in context:
            context['form'] = self.form_class()
        context['title'] = self.get_title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        usuario_form = self.user_form_class(request.POST)
        usuario_detalles_form = self.form_class(request.POST)
        if usuario_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save(commit=False)
            user.email = user.username
            user.save()
            detalles = usuario_detalles_form.save(commit=False)
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            detalles.codigo = sec
            detalles.usuario = user
            detalles.save()
            messages.success(request, self.get_success_message())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({"form": usuario_detalles_form, "user_form": usuario_form,
                                            "title": self.get_title})


class EditarUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = UserDetails
    form_class = UsuarioDetallesForm
    user_form_class = UsuarioEditarForm
    template_name = 'usuario_nuevo.html'
    success_url = 'seguridad:listar'
    permission_required = 'seguridad.change_userdetails'

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={'type': self.request.GET['type']})

    def get_success_message(self):
        return "{} editado con éxito.".format("Empleado" if self.request.GET['type'] == 'E' else "Cliente")

    def get_title(self):
        return "Editar {}".format("empleado" if self.request.GET['type'] == 'E' else "cliente")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class(
                instance=self.object.usuario)
        if "form" not in context:
            context['form'] = self.form_class(
                instance=self.object.detalles)
        context['title'] = self.get_title()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario_detalles_form = self.form_class(
            request.POST, request.FILES, instance=self.object)
        usuario_form = self.user_form_class(
            request.POST, instance=self.object.usuario)
        if usuario_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save()
            detalles = usuario_detalles_form.save(commit=False)
            detalles.usuario = user
            detalles.save()
            messages.success(request, self.get_success_message())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({"form": usuario_detalles_form, "user_form": usuario_form,
                                            "title": self.get_title()})


@login_required
@permission_required('seguridad.delete_userdetails')
def usuario_confirmar_eliminacion(request, pk):
    detalles = UserDetails.objects.get(id=pk)
    if request.POST:
        success_url = reverse_lazy('seguridad:listar', kwargs={
                                   'type': request.POST['type']})
        usuario = detalles.usuario
        usuario.is_active = False
        usuario.save()
        messages.info(request, "Usuario deshabilitado con éxito.")
        return redirect(success_url)
    return render(request, "ajax/usuario_confirmar_elminar.html", {"usuario": detalles})


@login_required
@permission_required('seguridad.delete_userdetails')
def usuario_confirmar_activar(request, pk):
    detalles = UserDetails.objects.get(id=pk)
    if request.POST:
        success_url = reverse_lazy('seguridad:listar', kwargs={
                                   'type': request.POST['type']})
        usuario = detalles.usuario
        usuario.is_active = True
        usuario.save()
        messages.success(request, "Usuario habilitado con éxito.")
        return redirect(success_url)
    return render(request, "ajax/usuario_confirmar_activar.html", {"usuario": detalles})


class CrearRolUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = Group
    form_class = RolUsuarioForm
    template_name = 'grupo_nuevo.html'
    title = 'Crear Rol'
    success_url = 'seguridad:listar'
    permission_required = 'seguridad.add_userdetails'

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={'type': 'E'})

    def get_permissions_template(self, app_name, model):
        permissions = ['view', 'add', 'change', 'delete']
        app_permissions = []
        if self.request.POST:
            app_permissions = self.request.POST.getlist(
                'apps_permissions', None)
        result = {}
        for perm in permissions:
            full_perm_name = app_name+'.'+perm+'_'+model
            result[full_perm_name] = 1 if full_perm_name in app_permissions else 0
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_apps = {}
        for app, details in APP_PERMISSIONS.items():
            current_apps[app] = {'label': details['label'], 'permissions': self.get_permissions_template(
                details['app'], details['model'])}
        context['apps'] = current_apps
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        rol_form = self.form_class(request.POST)
        apps = request.POST.getlist('apps', None)
        apps_permissions = request.POST.getlist('apps_permissions', None)
        next_page = request.POST.get('next', None)

        list_permissions = []
        if rol_form.is_valid() and apps and apps_permissions:
            rol = rol_form.save(commit=False)
            for permission in apps_permissions:
                app, action_model = permission.split('.')  # get the app
                _, model = permission.split('_')  # get the model
                content_type = ContentType.objects.get(
                    app_label=app, model=model)
                perm = Permission.objects.get(
                    content_type=content_type, codename=action_model)
                list_permissions.append(perm)
            if list_permissions:
                rol.save()
                rol.permissions.set(list_permissions)
                messages.success(request, "Rol creado con éxito.")
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(self.get_success_url())
        messages.error(
            request, "Por favor, verifique los datos del rol ingresado.")
        return self.render_to_response(self.get_context_data(**kwargs))


class EditarRolUsuario(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = Group
    form_class = RolUsuarioForm
    template_name = 'grupo_nuevo.html'
    title = 'Editar Rol'
    success_url = 'seguridad:listar'
    permission_required = 'seguridad.change_userdetails'
    context_object_name = 'rol'

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={'type': 'E'})

    def get_permissions_template(self, app_name, model):
        permissions = ['view', 'add', 'change', 'delete']
        app_permissions = []
        if self.request.POST:
            app_permissions = self.request.POST.getlist(
                'apps_permissions', None)
        else:
            app_permissions = self.object.permissions.order_by('codename').values_list(
                'codename', flat=True).distinct()
            app_permissions = [app_name+'.'+perm for perm in app_permissions]

        result = {}
        for perm in permissions:
            full_perm_name = app_name+'.'+perm+'_'+model
            result[full_perm_name] = 1 if full_perm_name in app_permissions else 0
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_apps = {}
        for app, details in APP_PERMISSIONS.items():
            current_apps[app] = {'label': details['label'], 'permissions': self.get_permissions_template(
                details['app'], details['model'])}
        context['apps'] = current_apps
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rol_form = self.form_class(request.POST, instance=self.object)
        apps_permissions = request.POST.getlist('apps_permissions', None)
        next_page = request.POST.get('next', None)

        list_permissions = []
        if rol_form.is_valid() and apps_permissions:
            rol = rol_form.save(commit=False)
            for permission in apps_permissions:
                app, action_model = permission.split('.')  # get the app
                _, model = permission.split('_')  # get the model
                content_type = ContentType.objects.get(
                    app_label=app, model=model)
                perm = Permission.objects.get(
                    content_type=content_type, codename=action_model)
                list_permissions.append(perm)
            if list_permissions:
                rol.save()
                rol.permissions.set(list_permissions)
                messages.success(request, "Rol editado con éxito.")
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(self.get_success_url())
        messages.error(
            request, "Por favor, seleccione los permisos del rol a crear.")
        return self.render_to_response(self.get_context_data(**kwargs))


@login_required
@permission_required('seguridad.delete_userdetails')
def rol_confirmar_eliminacion(request, pk):
    rol = Group.objects.get(id=pk)
    if request.POST:
        rol.delete()
        next_page = request.POST.get('next')
        messages.info(request, "Rol eliminado con éxito.")
        return redirect(next_page)
    return render(request, "ajax/rol_confirmar_elminar.html", {"rol": rol})


@login_required
@permission_required('seguridad.view_userdetails')
def rol_permisos_template(request, pk):
    rol = Group.objects.get(id=pk)

    def get_permissions_template(app_name, model):
        permissions = ['view', 'add', 'change', 'delete']
        app_permissions = []
        app_permissions = rol.permissions.order_by('codename').values_list(
            'codename', flat=True).distinct()
        app_permissions = [app_name+'.'+perm for perm in app_permissions]
        result = {}
        for perm in permissions:
            full_perm_name = app_name+'.'+perm+'_'+model
            result[full_perm_name] = 1 if full_perm_name in app_permissions else 0
        return result

    def get_context_data():
        context = {}
        current_apps = {}
        for app, details in APP_PERMISSIONS.items():
            current_apps[app] = {'label': details['label'], 'permissions': get_permissions_template(
                details['app'], details['model'])}
        context['apps'] = current_apps
        context['readonly'] = 1
        return context

    return render(request, "permisos.html", get_context_data())
