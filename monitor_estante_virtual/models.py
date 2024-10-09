from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import hashlib
from django.contrib.auth.models import User

    
class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    titulo_ou_autor = models.CharField(max_length=100, blank=True, default='')
    titulo = models.CharField(max_length=100, blank=True, default='')
    autor = models.CharField(max_length=100, blank=True, default='')
    editora = models.CharField(max_length=100, blank=True, default='')
    cidade = models.CharField(max_length=100, blank=True, default='')
    vendedor = models.CharField(max_length=100, blank=True, default='')
    idioma = models.CharField(max_length=100, blank=True, default='')
    preco_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0), MaxValueValidator(999_999)], blank=True, null=True)
    preco_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0), MaxValueValidator(999_999)], blank=True, null=True)
    ano_de_publicacao = models.CharField(max_length=4, blank=True, default='')
    tipo_de_livro = models.CharField(max_length=100, choices=[
        ('',''),('novo','novo'),('usado','usado'),('ambos','ambos')], blank=True, default='')
    isbn = models.CharField(max_length=20, blank=True, default='')
    
    def __str__(self):
        return f"({', '.join(k + ': ' + v for k,v in self.__dict__.items() if v and isinstance(v,str))})"


class Collection(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, 
        choices=[('success', 'Success'), ('failed', 'Failed'), ('in_progress', 'In Progress')])
    total_books_found = models.IntegerField(default=0)


class Book(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    publisher = models.CharField(max_length=100, blank=True, default='')
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book_type = models.CharField(max_length=100, choices=[
        ('',''),('novo','novo'),('usado','usado'),('ambos','ambos')], default='')
    # image = models.ImageField(upload_to = 'monitor_estante_virtual/')
    url = models.CharField(max_length=1_000, blank=True, default='', unique=True)
    
    constraints = [
        models.UniqueConstraint(fields=['title', 'author', 'price', 'book_type'], name='unique_book')
    ]

    def generate_hash(self):
        return hashlib.sha256(self.__repr__().encode()).hexdigest()
    
    def __str__(self):
        return f'Book: {self.title} ---- {self.author} -- {self.price}'
    
def upload_to_collection_folder(instance, filename):
    # Get the collection id from the related collection
    import os
    collection_id = instance.collection.id
    # Construct the upload path using the collection id
    return os.path.join(f'/monitor_collections/{collection_id}', filename)