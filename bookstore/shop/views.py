import csv
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.apps import apps
from urllib.parse import urlencode
from datetime import date, datetime
from decimal import Decimal
from .models import User, Book, Genre, BooksGenre, Publisher, Order
from .forms import CustomUserCreationForm


def home(request):
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()
    return render(request, 'home.html', {'genres': genres, 'publishers': publishers})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def genre_books(request, id):
    genre = get_object_or_404(Genre, id=id)
    book_ids = BooksGenre.objects.filter(genre_id=genre.id).values_list('book_id', flat=True)
    books = Book.objects.filter(id__in=book_ids)
    return render(request, 'genre_books.html', {'genre': genre, 'books': books})


def publisher_books(request, id):
    publisher = get_object_or_404(Publisher, id=id)
    books = Book.objects.filter(publisher=publisher)

    books_with_genres = []
    for book in books:
        genres = Genre.objects.filter(id__in=BooksGenre.objects.filter(book_id=book.id).values_list('genre_id', flat=True))
        books_with_genres.append({'book': book, 'genres': genres})

    return render(request, 'publisher_books.html', {'publisher': publisher, 'books_with_genres': books_with_genres})


@login_required
def user_orders(request):
    orders = Order.objects.filter(client=request.user)
    return render(request, 'orders.html', {'orders': orders})

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)
    if not order.is_paid:
        order.is_paid = True
        order.save()
    return redirect('purchased_books')


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    order = Order.objects.filter(client=request.user, book=book).first()
    is_ordered = order is not None
    is_paid = order.is_paid if order else False
    has_unpaid_order = is_ordered and not is_paid
    
    return render(request, 'book_detail.html', {
        'book': book,
        'is_ordered': is_ordered,
        'is_paid': is_paid,
        'has_unpaid_order': has_unpaid_order
    })

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    order, created = Order.objects.get_or_create(
        client=request.user, 
        book=book,
        defaults={'total_sum': book.cost}
    )
    
    if created:
        return redirect('user_orders')
    else:
        return redirect('book_detail', book_id=book.id)
    

@login_required
def purchased_books(request):
    orders = Order.objects.filter(client=request.user, is_paid=True)
    books = [order.book for order in orders]
    return render(request, 'purchased_books.html', {'books': books})

@login_required
def read_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'read_book.html', {'book': book})
    
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)

    if order.is_paid:
        return HttpResponseForbidden("Этот заказ уже оплачен и не может быть отменен.")
    
    order.delete()
    return redirect('user_orders')


@login_required
def export_data(request, model_name, format, **filters):
    model = apps.get_model('shop', model_name)
    
    queryset = model.objects.filter(**filters).values()
    
    if format == 'json':
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{model_name}.json"'

        def date_converter(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()

            raise TypeError(f"Type {type(obj)} not serializable")
        
        
        def date_converter(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            elif isinstance(obj, Decimal):
                return float(obj)
            raise TypeError(f"Type {type(obj)} not serializable")


        json_data = list(queryset)
        response.write(json.dumps(json_data, ensure_ascii=False, indent=4, default=date_converter))
        
        return response
    
    elif format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
        
        response.write('\ufeff')
        writer = csv.writer(response)
        
        if queryset:
            headers = list(queryset[0].keys())
            writer.writerow(headers)

            for row in queryset:
                writer.writerow(list(row.values()))
                
        return response
    else:
        return HttpResponse("Unsupported format", status=400)
    

@login_required
def export_page(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("Только для сотрудников и суперпользователей")

    return render(request, 'export_page.html')