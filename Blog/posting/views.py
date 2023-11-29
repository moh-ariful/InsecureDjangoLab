from audioop import reverse
from django.shortcuts import render, reverse, redirect
from posting.models import Posting
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from .forms import PostingForm
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection  # Import tambahan utk sqli
from django.utils.safestring import mark_safe  # Import tambahan utk sqli
from django.http import Http404
import logging
# Create your views here.


# Home
""" def index(request):
    postings = Posting.objects.all().order_by('-id')
    paginator = Paginator(postings, 2)
    page = request.GET.get('page')
    postings = paginator.get_page(page)
    context = {
        'postings': postings
    }

    return render(request, 'posting/index.html', context) """

# Home - rentan sqli
def index(request):
    page = request.GET.get('page')
    if page is not None:
        query = "SELECT * FROM blog_posting WHERE page = %s"  # Ini sesuaikan ya dgn struktur tabel yg ada
        postings = Posting.objects.raw(query, [page])
    else:
        postings = Posting.objects.all()
    context = {'postings': postings}
    return render(request, 'posting/index.html', context)


""" class SearchPosting(View):
    def get(self, request):
        query = self.request.GET.get('q')

        query_list = Posting.objects.filter(
            Q(judul__icontains=query) |
            Q(konten__icontains=query)
        )

        context = {
            'query_list': query_list,
        }

        return render(request, 'posting/search.html', context ) """


logger = logging.getLogger(__name__)
class SearchPosting(View):
    def get(self, request):
        query = self.request.GET.get('q')

        # Raw SQL query dgn input langsung dari user
        raw_query = f"SELECT * FROM posting_posting WHERE judul LIKE '%%{query}%%' OR konten LIKE '%%{query}%%'"

        logger.debug("Executing SQL query: %s", raw_query)

        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_query)
                result_list = cursor.fetchall()

            # Membuat objek Posting dari hasil query
            query_list = [Posting(id=row[0], judul=row[1], konten=row[2], image=row[3], date=row[4], penulis_id=row[5]) for row in result_list]

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            query_list = []

        context = {
            'query_list': query_list,
        }

        return render(request, 'posting/search.html', context)


""" class DetailPosting(generic.DetailView):
    model = Posting
    template_name = 'posting/detail.html' """


""" class DetailPosting(generic.DetailView):
    model = Posting
    template_name = 'posting/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posting = self.get_object()
        posting.konten = mark_safe(posting.konten)  # Menggunakan mark_safe untuk mencegah escaping
        context['posting'] = posting
        return context """

# Rentan SQLI
class DetailPosting(generic.DetailView):
    model = Posting
    template_name = 'posting/detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        # Langsung memasukkan 'pk' ke dlm query
        # PERHATIAN: Ini amat rentan thd SQL Injection
        query = f"SELECT * FROM posting_posting WHERE id = '{pk}'"

        logger.debug("Executing SQL query: %s", query)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()

            if not result:
                raise Http404('Posting tidak ditemukan')

            # Mengisi objek Posting dgn hasil query
            posting = self.model(judul=result[1], konten=result[2], image=result[3], date=result[4], penulis_id=result[5])
            return posting

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise Http404('Error dalam memproses permintaan')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posting = self.get_object()
        posting.konten = mark_safe(posting.konten)
        context['posting'] = posting
        return context


# Mmebuat posting
""" class AddPost(LoginRequiredMixin,generic.CreateView):
    model = Posting
    fields = ['judul', 'penulis', 'date', 'image', 'konten']
    template_name = 'posting/addpost.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk}) """

# Rentan sqli
class AddPost(LoginRequiredMixin, generic.CreateView):
    model = Posting
    fields = ['judul', 'penulis', 'date', 'image', 'konten']
    template_name = 'posting/addpost.html'

    def form_valid(self, form):
        judul = form.cleaned_data['judul']
        # Raw SQL query dengan input langsung dari form
        query = "INSERT INTO posting (judul) VALUES ('%s')" % judul
        # Eksekusi query (ini hanya contoh, tidak disarankan)
        with connection.cursor() as cursor:
            cursor.execute(query)
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Posting
    form_class = PostingForm
    template_name = 'posting/addpost.html'

    def form_valid(self, form):
        post = self.get_object()

        if self.request.user != post.penulis:
            messages.error(self.request, 'Anda tidak berhak melakukan update!')
            return redirect('/')

        messages.success(self.request, "Post berhasil diupdate!")
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Posting
    template_name = 'posting/deletepost.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        if self.request.user != post.penulis:
            messages.error(self.request, 'Anda tidak berhak menghapus posting ini!')
            return redirect('/')

        messages.success(self.request, "Posting berhasil dihapus!")
        return super().delete(request, *args, **kwargs)
