# 토이 프로젝트 카페(쇼핑몰) 프로젝트

**개발인원 : 개인** <br/>
**개발기간 : 2024/06.01~2024/06.31**
## 프로젝트 소개 
이 Django 프로젝트는 사용자 인증(allauth), 상품 관리, 장바구니 기능, 주문 처리, 포함한 전자 상거래 플랫폼입니다. 주요 기능으로는 다음과 같습니다:

- 사용자는 카테고리별로 상품을 조회할 수 있습니다.
- 장바구니에 상품을 추가하거나 바로 주문할 수 있습니다.
- 관리자는 상품을 등록하고 관리할 수 있습니다.
- 이 프로젝트는 Django의 ORM을 사용하여 데이터베이스와 상호작용하며, 페이지네이션을 통해 대용량 데이터를 효과적으로 처리합니다. 코드는 가독성을 고려하여 작성되었으며, 사용 
 자 경험을 중시하는 디자인을 채택하고 있습니다.
- Docker 활용하여 배포

## Stack
**Enviroment**  


<img src="https://img.shields.io/badge/Pycharm-E34F26?style=for-the-badge&logo=Pycharm&logoColor=white">  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">



**Development** 


<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=Bootstrap&logoColor=white"> 



## 화면 구성 📺

| 마이 페이지 | 쇼핑 카트 |
| --- | --- |
| ![My Page](https://github.com/Choi9912/Django_CafeShop/assets/76863081/dfe24d3b-b161-415d-bd6e-2e0aa4e71202) |  ![ShoppingCart](https://github.com/Choi9912/Django_CafeShop/assets/76863081/8e4a009b-d98d-452d-9f57-3fccc581d4b2) |


| 카테고리 | 디테일 |
| --- | --- |
| ![category](https://github.com/Choi9912/Django_CafeShop/assets/76863081/1adae9f3-d834-4f1e-9f37-41638b8a6d5e) | ![detail_coffee](https://github.com/Choi9912/Django_CafeShop/assets/76863081/f2b91f12-d896-4c4f-b654-8bd31a101d91) |


 
- Category
```python
class Category(models.Model):
    sort = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.sort)
```

- Product
```python
  class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = ImageField(upload_to='photos/', blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    hit = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.name, self.pub_date)
```

- Point
```python
  class Point(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    all_point = models.IntegerField()
    able_point = models.IntegerField()
  
```

- Cart
```python
  class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_product', blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '{} // {}'.format(self.user, self.products.name)
```

- Post
```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)
```

- Order
```python
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    name = models.CharField(max_length=100, verbose_name='상품명')
    amount = models.PositiveIntegerField(verbose_name='결제금액')
    quantity = models.IntegerField(default=1)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return '{} by {}'.format(self.products.name, self.user)
```

