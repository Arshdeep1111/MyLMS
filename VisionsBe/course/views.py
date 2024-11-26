from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import request
from django.contrib.auth import login
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import VisionsBe.settings
import os


# Create your views here.

class CourseList(ListView):
    model = Course
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['mycourse'] = []
            for i in My_course.objects.filter(user=self.request.user):
                context['mycourse'].append(i.course)
            context['ratinglist'] = [20,40,60,80,100]
        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'course/signup.html'
    def get_success_url(self):
        return '/'
    
    def form_valid(self, form):
        user = User.objects.create_user(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], email = form.cleaned_data['email'], username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        userprofile = UserProfile.objects.create(user=user, phone=form.cleaned_data['phone'])
        userprofile.save()
        login(self.request,user)
        for c in Course.objects.all():
            if c.isfree:
                myc = My_course.objects.create(user=user, course=c)
                myc.save()
        messages.success(self.request, 'Logged In Successfully!')
        return HttpResponseRedirect(self.get_success_url())



class UserUpdateView(UpdateView):
    model = User
    form_class=UserUpdateForm
    template_name = 'course/profile.html'


    def get_initial(self):
        initial = super().get_initial()
        initial['phone'] = UserProfile.objects.get(user=User.objects.get(email=self.request.user.email)).phone
        return initial
    
    def get_success_url(self):
        return '/'


class CourseDetail(LoginRequiredMixin, DetailView):
    login_url='/registration/login'
    model = Course
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teachers"] = Teacher.objects.filter(course=self.object)
        context["tag"] = Tag.objects.filter(course=self.object)
        context["learning"] = Learning.objects.filter(course=self.object)
        context["prerequisite"] = Prerequisite.objects.filter(course=self.object)
        context["review"] = Review.objects.filter(course=self.object)
        try:
            context['myreview']=Review.objects.filter(user=self.request.user, course=self.object)
        except Review.DoesNotExist:
            context['accept_review']=True
        else:
            context['accept_review']=False
        context['user'] = self.request.user
        try:
            context['wishlist'] = Wishlist.objects.get(user=self.request.user, course=self.object) 
        except Wishlist.DoesNotExist: 
            context['isinwishlist'] = False
        else: 
            context['isinwishlist'] = True
        try:
            context['cart']=Cart.objects.get(user=self.request.user, course=self.object)
        except Cart.DoesNotExist:
            context['isincart'] = False
        else:
            context['isincart'] = True
        context['mycourse'] = []
        for i in My_course.objects.filter(user=self.request.user):
                context['mycourse'].append(i.course)
        context['favcourse'] = []
        for i in Favourite.objects.filter(user=self.request.user):
                context['favcourse'].append(i.course)
                if i.course==self.object:
                    context['fav'] = i
        context['showcertificate'] = False
        if self.object in context['mycourse']:
            totalassessment = len(list(Section.objects.filter(course=self.object)))
            passedin = 0
            for ua in UserAssessment.objects.all():
                if ua.user == self.request.user and ua.assessment.section.course == self.object:
                    if ua.has_passed:
                        passedin +=1
            if totalassessment == passedin:
                context['showcertificate'] = True
        context['ratinglist'] = [20,40,60,80,100]
        return context

class SectionList(ListView):
    model = Section
    def get_queryset(self):
        return Section.objects.filter(course=Course.objects.get(slug=self.kwargs['slug']))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            myc = My_course.objects.get(user=self.request.user, course=self.object_list[0].course)
        except:
            context['ismycourse'] = False
        else:
            context['ismycourse'] = True
        return context

class SectionDetail(DetailView):
    model = Section
    fields = ['topic', 'description', 'is_preview']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(section=self.object)
        context['notes'] = Note.objects.filter(section=self.object)
        context['assessment'] = Assessment.objects.get(section=self.object)
        return context

class AssessmentDetail(LoginRequiredMixin,
DetailView):
    model = Assessment
    fields = ['name', 'total_marks', 'passing_marks']
    login_url = '/registration/login/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.filter(assessment=self.object)[0]
        try:
            context['ua']=UserAssessment.objects.get(assessment=self.object, user=self.request.user) 
        except:
            pass
        return context


@login_required(login_url='/registration/login/')
def question_detail(request, slug, sectionid, aid, pk):
    question = Question.objects.get(pk=pk)
    choices = Choice.objects.filter(question=question)
    context = {'question': question, 'choices': choices}
    context['now']=list(Question.objects.filter(assessment = question.assessment)).index(question)
    context['prev'] = list(Question.objects.filter(assessment = question.assessment))[context['now']-1].id
    context['has_prev'] = context['now']-1!=-1
    n=len(list(Question.objects.filter(assessment = question.assessment)))
    context['has_next'] = context['now']+1!=n
    if context['has_next']:
        context['next'] = list(Question.objects.filter(assessment = question.assessment))[context['now']+1].id
    if request.method=='POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except:
            context['error_message'] = 'You did not select a choice'
        else:
            context['selected_choice']=selected_choice
            ua = UserAssessment.objects.get_or_create(user=request.user, assessment=question.assessment)
            ua[0].attempted = True
            if selected_choice.is_correct:
                ua[0].marks+=question.positive_marks
            else:
                ua[0].marks-=question.negative_marks
            ua[0].save()
            context['ua']=ua[0]
    return render(request, 'course/question_detail.html', context)

class UserAssessmentDetail(LoginRequiredMixin, DetailView):
    login_url='/registration/login/'
    model = UserAssessment
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.marks>=self.object.passing_marks:
            context[self.object.has_passed] = True
        try:
            context['nextsection']=list(Section.objects.filter(course=self.object.assessment.section.course))[list(Section.objects.filter(course=self.object.assessment.section.course)).index(self.object.assessment.section)+1]
        except:
            context['hasnextsection']=False
        else:
            if context['nextsection'].is_preview or context['nextsection'].course.isfree:
                context['hasnextsection']=True
            else:
                try:
                    mycourse = My_course.objects.get(user=self.request.user, course=context['nextsection'].course)
                except:
                    context['hasnextsection'] = False
                else:
                    context['hasnextsection']=True
        return context
    
class CreateReview(LoginRequiredMixin, CreateView):
    login_url = '/registration/login/'
    model = Review
    form_class = ReviewForm
    
    def get_success_url(self):
        return '/detail/'+self.kwargs['slug']+'/'

    def form_valid(self, form):
        form.instance.user=self.request.user 
        course=get_object_or_404(Course, slug=self.kwargs['slug'])
        form.instance.course=course
        reviews=Review.objects.filter(course=course)
        course.rating = (int(course.rating)*len(reviews)+int(form.cleaned_data['rating']))/(len(reviews)+1)
        course.save()
        return super().form_valid(form)


class CreateWishlist(LoginRequiredMixin, CreateView):
    login_url = '/registration/login'
    model = Wishlist
    form_class = WishlistForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course=get_object_or_404(Course, slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        return '/wishlist'

class WishlistList(ListView):
    paginate_by = 9
    def get_queryset(self):
        return Wishlist.objects.filter(user = self.request.user)

class DeleteWishlist(DeleteView):
    model = Wishlist
    success_url = '/wishlist'

class CreateCart(LoginRequiredMixin, CreateView):
    login_url='/registration/login/'
    model=Cart
    form_class = CartForm

    def form_valid(self, form):
        form.instance.user=self.request.user
        c=Course.objects.get(slug=self.kwargs['slug'])
        form.instance.course=c
        form.instance.amount=c.price
        try:
            w=Wishlist.objects.get(course=c, user=self.request.user)
        except:
            pass
        else:
            w.delete()
        if form.cleaned_data['coupon']:
            coupon = Coupon.objects.get(code = form.cleaned_data['coupon'])
            if coupon.course == c:
                
                form.instance.amount=c.price*(1-(coupon.discount/100))
                coupon.limit -=1
                coupon.save()
            else:
                messages.error(self.request, 'This coupon code is not valid for this course.')
                return HttpResponseRedirect('/cart/add/'+self.kwargs['slug'])
        return super().form_valid(form)
        

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return context
    
    def get_success_url(self):
        return '/cart/'

class CartList(LoginRequiredMixin, ListView):
    login_url = '/registration/login/'
    model = Cart
    def get_queryset(self):
        try:
            queryset= Cart.objects.filter(user=self.request.user)
        except: 
            return super().get_queryset()
        else:
            return queryset
            
        
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['total'] = 0
        for i in self.object_list:
            context['total']+=i.amount
        return context


class DeleteCart(LoginRequiredMixin, DeleteView):
    login_url='/registration/login/'
    model=Cart
    success_url = '/cart/'

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(pk=self.kwargs['pk'])
        if cart.coupon:
            cart.coupon.limit+=1
            cart.coupon.save()
        return super().post(request, *args, **kwargs)

class UpdateReview(LoginRequiredMixin, UpdateView):
    login_url = '/registration/login/'
    model=Review
    form_class = ReviewForm
    
    def get_success_url(self):
        return '/detail/'+self.object.course.slug
    
    def form_valid(self, form):
        course=self.object.course
        rev=Review.objects.filter(course=course)
        course.rating=0
        for i in rev:
            if i == self.object:
                print("True")
                course.rating=course.rating+self.object.rating
            else:
                course.rating=course.rating+i.rating
        course.rating=course.rating/len(rev)
        course.save()
        return super().form_valid(form)


class DeleteReview(LoginRequiredMixin, DeleteView):
    login_url = '/registration/login/'
    model = Review

    def get_success_url(self):
        return '/detail/'+Review.objects.get(pk=self.kwargs['pk']).course.slug

    def post(self, request, *args, **kwargs):
        review = Review.objects.get(pk=self.kwargs['pk'])
        course = review.course
        rev = Review.objects.filter(course=course)
        course.rating=0
        for i in rev:
            if i!=review:
                course.rating=course.rating+i.rating
        course.rating=course.rating/(len(rev)-1)
        course.save()
        return super().post(request, *args, **kwargs)

def payment_success(request):
    pass

def payment_failure(request):
    pass

class MyCourseList(LoginRequiredMixin, ListView):
    login_url = '/registration/login'
    model=My_course
    paginate_by = 9
    def get_queryset(self):
        try:
            q = My_course.objects.filter(user=self.request.user)
        except:
            return super().get_queryset()
        else:
            return q

def certificate(request, slug):
    course = My_course.objects.get(course=Course.objects.get(slug=slug), user=request.user)
    if course.certificate:
        certurl = 'course/static/course/images/Certificate'+str(course.id)+request.user.first_name+'.png'
    else:
        image = Image.open('course/static/course/images/Certificate.png')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('course/static/course/fonts/Oswald-Medium.ttf', size=100)
        (x, y) = (500, 570)
        name = request.user.first_name + ' ' + request.user.last_name
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), name, fill=color, font=font)
        (x, y) = (500, 840)
        coursename = course.course.name
        draw.text((x,y), coursename, fill=color, font=font)
        certurl = 'course/static/course/images/Certificate'+str(course.id)+request.user.first_name+'.png'
        image.save(certurl)
        course.certificate = True
        course.save()
    render(request, 'course/certificate.html')
    wrapper = FileWrapper(open(certurl, 'rb'))
    content_type = mimetypes.guess_type(certurl)[0]
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename=Certificate.png'
    return response

def search(request):
    keyword = request.GET.get('search', '')
    tags = list(Tag.objects.filter(tag=keyword))
    return render(request, 'course/search.html', {'tags': tags})

class CreateFavourite(CreateView):
    model = Favourite
    form_class = FavouriteForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course=get_object_or_404(Course, slug=self.kwargs['slug'])
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return context
    def get_success_url(self):
        return '/favourites'

class FavouriteList(ListView):
    model = Favourite
    paginate_by = 9
    def get_queryset(self):
        q = Favourite.objects.filter(user=self.request.user)
        return q

class DeleteFavourite(DeleteView):
    model = Favourite
    success_url = '/'

class CreateMyCourse(LoginRequiredMixin, CreateView):
    login_url = '/registration/login'
    model = My_course
    form_class = MyCourseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course=get_object_or_404(Course, slug=self.kwargs['slug'])
        c=Course.objects.get(slug=self.kwargs['slug'])
        try:
            c=Cart.objects.get(course=c, user=self.request.user)
        except:
            pass
        else:
            c.delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        return '/mycourse'