from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import PageForm
from .models import Page


class StaffRequiredMixin(object):
    """
    Este mixin requerirá que el usuario sea miembro de staff
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse_lazy('admin:login'))

        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.
class PageListView(ListView):
    model = Page


class PageDetailView(DetailView):
    model = Page


class PageCreate(StaffRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    # fields = ['title', 'content', 'order'] # lo quito pq ya tenemos en forms.py
    success_url = reverse_lazy('pages:pages')

    # def dispatch(self, request, *args, **kwargs):
    #     # print(request.user)
    #
    #     # para evitar que escriba en la ruta /create si no es admin entra a login.
    #     if not request.user.is_staff:
    #         return redirect(reverse_lazy('admin:login'))
    #
    #     return super(PageCreate, self).dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse('pages:pages')


class PageUpdate(StaffRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    # fields = ['title', 'content', 'order'] # lo quito pq ya tenemos en forms.py
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + "?ok"


class PageDelete(StaffRequiredMixin, DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')

# def page(request, page_id, page_slug):
#     page = get_object_or_404(Page, id=page_id)
#     return render(request, 'pages/page.html', {'page':page})


# def pages(request):
#     pages = get_list_or_404(Page)
#     return render(request, 'pages/pages.html', {'pages':pages})
