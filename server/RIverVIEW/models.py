from django.db import models

# Create your models here.

class ProductModel(models.Model):
    class Meta:
        db_table = "product"
    def __str__(self):
        return self.product_name
    product_url = models.CharField(max_length=256, default='')
    product_name = models.CharField(max_length=256, default='')
    product_num = models.IntegerField(null=True)
    categories = models.TextField(null=True)
    img_src = models.CharField(max_length=256, default='')
    price = models.CharField(max_length=32, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewModel(models.Model):
    class Meta:
        db_table = "review"
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE,default='')
    review = models.CharField(max_length=1000)

class ProductKeyword(models.Model):
    class Meta:
        db_table = "PDkeyword"
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE, default='')
    keyword = models.CharField(max_length=20, default='')
    summarization = models.CharField(max_length=256, default='') #해당 키워드의 대표 리뷰
    keyword_score = models.FloatField(default=0) #키워드의 점수 (긍정이면 + 부정이면 -)
    keyword_frequency = models.IntegerField(null=True)