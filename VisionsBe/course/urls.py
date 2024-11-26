from django.urls import path
from . import views
from VisionsBe import settings
from django.conf.urls.static import static 

urlpatterns=[
    path('', views.CourseList.as_view(), name='home'),
    path('signup/', views.UserCreateView.as_view(), name = 'signup' ),
    path('profile/<int:pk>', views.UserUpdateView.as_view(), name='profile'),
    path('detail/<slug:slug>/', views.CourseDetail.as_view(), name='coursedetail'),
    path('sections/<slug:slug>', views.SectionList.as_view(), name='sectionlist'),
    path('sections/<slug:slug>/<int:pk>', views.SectionDetail.as_view(), name='sectiondetail'),
    path('assessment/<slug:slug>/<int:sectionid>/<int:pk>/', views.AssessmentDetail.as_view(), name='assessment'),
    path('assessment/<slug:slug>/<int:sectionid>/<int:aid>/<int:pk>', views.question_detail, name='question'),
    path('result/<int:pk>', views.UserAssessmentDetail.as_view(), name='result'),
    path('review/<slug:slug>', views.CreateReview.as_view(), name='review'),
    path('wishlist/<slug:slug>', views.CreateWishlist.as_view(), name='create_wishlist'),
    path('wishlist', views.WishlistList.as_view(), name='show_wishlist'),
    path('deletewishlist/<int:pk>', views.DeleteWishlist.as_view(), name='remove_wishlist'),
    path('cart/add/<slug:slug>', views.CreateCart.as_view(), name='create_cart'),
    path('cart/', views.CartList.as_view(), name='cart_list'),
    path('cart/delete/<int:pk>', views.DeleteCart.as_view(), name='delete_cart'),
    path('review/update/<int:pk>', views.UpdateReview.as_view(), name='update_review'),
    path('review/delete/<int:pk>', views.DeleteReview.as_view(), name='delete_review'),
    path('payments/success', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('mycourse', views.MyCourseList.as_view(), name='mycourse'),
    path('mycourse/<slug:slug>', views.CreateMyCourse.as_view(), name='create_mycourse'),
    path('certificate/<slug:slug>', views.certificate, name='certificate'),
    path('search', views.search, name='search'),
    path('favourite/add/<slug:slug>', views.CreateFavourite.as_view(), name='create_favourite'),
    path('favourites', views.FavouriteList.as_view(), name='favourite'),
    path('favourite/remove/<int:pk>', views.DeleteFavourite.as_view(), name='removefavourite')
]   


urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)