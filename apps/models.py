from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    image = models.ImageField(upload_to='static/images', null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.id} - {self.name}'


class Status(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f'{self.id} - {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='static/images', verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.CharField(max_length=300, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Cart(models.Model):
    guest_session_id = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.guest_session_id} - {self.date_create}'


class CartDetails(models.Model):
    cart_id = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    count = models.IntegerField()

    class Meta:
        verbose_name = 'Элемент деталей корзины'
        verbose_name_plural = 'Детали корзины'
    def __str__(self):
        return f'{self.cart_id} - {self.product.name}'


class Pay(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id} - {self.name}'

class Delivery(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.id} - {self.name}'


class Orders(models.Model):
    guest_session_id = models.CharField(max_length=200, verbose_name='ИД сессии гостя')
    date_create = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE, null=True, verbose_name='Способ оплаты')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True, verbose_name='Способ доставки')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')
    number = models.CharField(max_length=11, null=True, verbose_name='Номер телефона')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, verbose_name='Статус')
    total_sum = models.DecimalField(null=True, max_digits=20, decimal_places=2, verbose_name='Итоговая сумма')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.guest_session_id} - {self.date_create} - {self.status}'

class OrderDetails(models.Model):
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, verbose_name='ИД заказа')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент деталей заказа'
        verbose_name_plural = 'Детали заказов'
    def __str__(self):
        return f'{self.product.name} - {self.product.price}р'