from django.db import models

# Create your models here.

class ProductModel(models.Model):
    class Meta:
        db_table = "product"

    product_url = models.CharField(max_length=256, default='')
    product_name = models.CharField(max_length=256, default='')
    product_num = models.IntegerField(primary_key= True)
    img_src = models.CharField(max_length=256, default='')
    product_score = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductKeyword(models.Model):
    class Meta:
        db_table = "PDkeyword"
        ordering = ["-keyword_frequency"]
    product_reference = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, default='')
    review = models.CharField(max_length=256, default='') #해당 키워드의 대표 리뷰
    keyword_score = models.FloatField(default=0) #키워드의 점수 (긍정이면 + 부정이면 -)
    keyword_frequency = models.IntegerField(null=True)