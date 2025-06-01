from django.db import models
import hashlib






class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    image=models.ImageField(upload_to="img/product/img-upload")

    def __str__(self):
        return self.name

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  
    email = models.EmailField()

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)

    def check_password(self, raw_password):
        return self.password == hash_password(raw_password)

    def __str__(self):
        return self.username



    
class Sanpham(models.Model):
    name = models.CharField("Tên sản phẩm", max_length=200)
    description = models.TextField("Mô tả", blank=True)
    price = models.DecimalField("Giá bán", max_digits=10, decimal_places=0)

    def __str__(self):
        return self.name
