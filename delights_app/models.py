from django.db import models

class Catigory(models.Model):
    type= models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Delight(models.Model):
    name= models.CharField(max_length=50)
    des= models.TextField()
    image= models.CharField(max_length=255)
    price= models.DecimalField(decimal_places=2, max_digits=6)
    catigory= models.ForeignKey(Catigory, related_name="delights", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Rating(models.Model):
    rating= models.IntegerField(default=0)
    rated_by= models.ForeignKey('login_app.User', related_name="user_ratings", on_delete=models.CASCADE)
    rate_for= models.ForeignKey(Delight, related_name="delight_ratings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Review(models.Model):
    review= models.TextField()
    uploaded_by= models.ForeignKey('login_app.User', related_name="reviews", on_delete=models.CASCADE)
    review_for= models.ForeignKey(Delight, related_name="delight_reviews", on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class TempDelight(models.Model):
    temp_delight= models.ForeignKey(Delight, related_name="temp_delight_orders", on_delete=models.CASCADE)
    qty= models.IntegerField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Order(models.Model):
    paid_amount= models.DecimalField(decimal_places=2, max_digits=6)
    ordered_by= models.ForeignKey('login_app.User', related_name="orders", on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class DelightOrder(models.Model):
    delight= models.ForeignKey(Delight, related_name="delight_orders", on_delete=models.CASCADE)
    quantity= models.IntegerField()
    order= models.ForeignKey(Order, related_name="order_delight_orders", on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


