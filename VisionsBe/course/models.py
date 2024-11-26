from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import *

# Create your models here.
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('password').blank = False
User._meta.get_field('password').null = False

class UserProfile(models.Model):
    phoneNumberRegex = RegexValidator(regex = r"^\d{10}$")
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 10, unique = True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(blank=True, null=True)
    sub_heading = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_on = models.DateField()
    last_updated = models.DateField()
    language = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    marked_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    price = models.FloatField()
    length = models.DurationField(default=0)
    rating = models.IntegerField(default=100)
    slug = models.SlugField(unique=True)
    students = models.IntegerField(default=0)
    favourite_by = models.IntegerField(default=0)
    isfree = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def save(self):
        if not self.price:
            self.price=self.marked_price(1-self.discount)
        return super().save()


class Learning(models.Model):
    learning = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Prerequisite(models.Model):
    prerequisite = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    achievement = models.TextField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    topic = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    is_preview = models.BooleanField(default = False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.topic


class Video(models.Model):
    link = models.URLField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Note(models.Model):
    link = models.URLField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    total_marks = models.IntegerField(default=0)
    passing_marks = models.IntegerField(default=0)
    section = models.OneToOneField(Section, on_delete=models.CASCADE, null=True)
    def __str__(self) :
        return self.name

class Question(models.Model):
    question = models.CharField(max_length=100)
    positive_marks = models.IntegerField(default=0)
    negative_marks = models.IntegerField(default=0)
    explanation = models.TextField(max_length=500)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question

class Choice(models.Model):
    name = models.CharField(max_length=50)
    is_correct=models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    review = models.TextField(max_length=200)
    rating = models.IntegerField(default=100)

    
class UserAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    passing_marks = models.IntegerField(default=0)
    attempted = models.BooleanField(default=False)
    marks = models.IntegerField(default=0)
    has_passed = models.BooleanField(default=False)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Coupon(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    code = models.CharField(max_length=25)
    limit = models.IntegerField(default=50)
    discount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.code

class Payment(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    txnamount = models.CharField(max_length=10)
    txnid = models.CharField(max_length=70, null=True, blank=True)
    banktxnid = models.CharField(max_length=100, null=True, blank=True)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, null=True, blank=True)
    respcode = models.CharField(max_length=10, null=True, blank=True)
    respmsg = models.CharField(max_length=500, null=True, blank=True)
    txndate = models.DateTimeField(default=datetime.now)
    gatewayname = models.CharField(max_length=15, null=True, blank=True)
    bankname = models.CharField(max_length=500, null=True, blank=True)
    paymentmode = models.CharField(max_length=15, null=True, blank=True)
    checksumhash = models.CharField(max_length=110, null=True, blank=True)
    
    
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)


class My_course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    certificate = models.BooleanField(default = False)
