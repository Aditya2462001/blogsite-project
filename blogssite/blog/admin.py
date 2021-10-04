from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Author)
admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(ContactMe)




admin.site.site_header  =  "WebDev Administration"  
admin.site.site_title  =  "Webdev admin site"
admin.site.index_title  =  "Webdev Admin"
