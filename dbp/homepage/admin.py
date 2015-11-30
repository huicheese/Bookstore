from django.contrib import admin

# Register your models here.
from .models import Books, Customers, OrderItems, Orders, Ratings, Feedbacks

#admin.ModelAdmin enable us to change what is shown on the admin page
class BooksAdmin(admin.ModelAdmin):
	#What to display when you enter the Book database in admin
	list_display = ('title', 'stock','price')
	#Enable filtering by stock or price (just testing)
	list_filter = ('stock', 'price')

class CustomersAdmin (admin.ModelAdmin):
	list_display = ('fullname','loginid')

class FeedbacksAdmin (admin.ModelAdmin):
	list_display = ('loginid','isbn')

class FeedbacksAdmin2 (admin.ModelAdmin):
	list_display = ('loginid','isbn')

class RatingsAdmin (admin.ModelAdmin):
	list_display = ('isbn','feedbackid','ratingid')

#to register the models with the admin site
admin.site.register(Books, BooksAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(OrderItems)
admin.site.register(Orders)
admin.site.register(Ratings, RatingsAdmin)
#admin.site.register(Feedbacks2, FeedbacksAdmin2)
