from django.http.response import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from .models import *
from django.template.loader import render_to_string


from django.urls import reverse

from django.utils.encoding import force_bytes, force_text , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator




# Create your views here.
def index(request):
    categories = Categories.objects.all()
    posts = Post.objects.all()
    feedbacks = Feedback.objects.all()
    context = {
        'categories':categories,
        'posts' : posts ,
        'feedbacks' : feedbacks ,
        'count':len(posts) - 2,
    }
    return render(request,'base.html',context)


def search(request):
    input = request.GET.get('search')
    if len(input) == 0:
        posts = Post.objects.filter(Q(title__icontains = input), Q(author__fname__icontains = input))[:5]
        categories = Categories.objects.filter(Q(title__icontains = input))[:5]
    else:
        posts = Post.objects.filter(Q(title__icontains = input), Q(author__fname__icontains = input))
        categories = Categories.objects.filter(Q(title__icontains = input))
    data = render_to_string('search-box.html',{'posts':posts,'categories':categories})

    return JsonResponse({'data':data})

def contactMe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message')

        contact = ContactMe(name = name , email = email , number = number , message = message)
        contact.save()

        mail = EmailMessage(
        subject=f'Contact By - {name} - {number}',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER,]
        )
        mail.send()

        messages.success(request,'Your Response is recoreded !')

    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password = password)
        if user is not None : 
            if user.is_active :
                login(request,user)
                return redirect('/user_panal')
        else:
            messages.info(request,'Cradential are wrong or Account Not activate at please try again !')
            return redirect('/login')
    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        city = request.POST.get('city')
        number = request.POST.get('number')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('vpassword')
        if password1 != password2 :
            messages.info(request, "both password not match please try again !")
            return render(request,'register.html',
                    {'fname':fname,'lname':lname ,'email':email,'username':username,'city':city,'number':number})
        if User.objects.filter(username = username).exists():
            messages.info(request, "Username already exit create another username !")
            return render(request, 'register.html', {'fname': fname, 'lname': lname, 'email': email, 'city': city, 'number': number})
        user = User.objects.create_user(first_name = fname ,
         last_name = lname , email = email , 
         username = username , password = password1)
        user.is_active = False
        user.save()

        author = Author(author = user , email = email ,city = city , fname = fname , lname = lname , number = number)
        author.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        domain = get_current_site(request).domain

        link = reverse('activate',kwargs = {'uidb64':uidb64,'token':token})
        
        activate_url = 'http://'+domain+link

        email_body = f'hiii {username},\n Please you this link to verify your account \n {activate_url}'
        email_subject = 'Activate Your account'

        
        mail = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[email,]
        )
        mail.send()
        messages.info(request,'Your Account is created but you have to activate your account with the link send in the mail.')
        return redirect('/login')
    return render(request,'register.html')

def verificationEmail(request,uidb64,token):
    try:
        id = urlsafe_base64_decode(force_text(uidb64))
        user = User.objects.get(pk = id)

        if not token_generator.check_token(user,token):
            messages.info(request,'your account is activated please login and enjoy the experience of natura gallary ')
            return redirect('/login')

        if user.is_active:
            messages.info(request,'your account is activated please login and enjoy the experience of natura gallary ')
            return redirect('/login')
            
        user.is_active = True
        user.save()
        messages.success(request,'account activate successfully')
        return redirect('/login')

    except Exception as e:
        pass
    
    return redirect('/login')


def view_post(request,slug):
    author = request.user
    post = Post.objects.get(slug = slug)
    categories = Categories.objects.all()
    comment = Comment.objects.all()
    comments = comment.filter(post = post)
    replys = Reply.objects.all()
    replys = replys.filter(author = post.author)
    like = Like.objects.get(post =post)
    context = {
        'author':str(author),
        'post':post,
        'post_author':str(post.author),
        'categories': categories,
        'comments':comments,
        'replys' : replys,
        'like':like,
    }
    return render(request,'view_post.html',context)

def all_posts(request):
    posts = Post.objects.all()
    categories = Categories.objects.all()
    context = {
        'posts':posts,
        'categories': categories,
    }
    return render(request,'all_posts.html',context)

def all_categorise(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories,
    }
    return render(request,'all_category.html',context)

def categoryPost(request,slug):
    category = Categories.objects.get(title = slug)
    posts = Post.objects.all()
    posts = posts.filter(category = category)
    print(posts)
    return render(request,"category_post.html",{"posts":posts,"category":category})


def user_panal(request):
    if request.user.is_active :
        author = Author.objects.get(author = request.user)
        post = Post.objects.all()
        posts = post.filter(author = author)
        context = {
            'author':author ,
           'posts':len(posts),
        }
        return render(request,'user_panal.html',context)
    else:
        return redirect('/login')



def logout_view(request):
    logout(request,)
    return redirect('/login')


def posts(request):
    if request.user.is_active:
        author = Author.objects.get(author=request.user)
        post = Post.objects.all()
        posts = post.filter(author=author)
        category = Categories.objects.all()
        context = {
            'posts': posts,
             "author":author,
             'categories':category,
        }
        return render(request,'user-panal/post.html',context)
    else:
        return redirect('/login') 

def create_posts(request):
    if request.user.is_active :
        pk = 0
        author = Author.objects.get(author = request.user)
        category = Categories.objects.all()
        if request.method == 'POST':
            image = request.FILES.get('image')
            title = request.POST.get('title')
            subtitle = request.POST.get('subtitle')
            post = request.POST.get('post')
            categorie = request.POST.get('categories')
            for i in category:
                if i.title == categorie:
                    pk = i.id 
            if pk != 0:
                category = Categories.objects.get(id = pk)
            elif pk == 0:
                category = Categories(title = categorie)
                category.save()
            save_post = Post(title=title, subtitle=subtitle, author=author,post=post,image = image)
            save_post.save()
            like = Like(post = save_post, like = 0)
            like.save()
            save_post.category.add(category)
            messages.info(request,"Post created!!!")
        context = {
            'author' : author ,
        }
        return render(request,'user-panal/create-post.html',context)
    else:
        return redirect('/login')
    
def edit_post(request,pk):
    if request.user.is_active :
        author = Author.objects.get(author=request.user)
        post = Post.objects.get(id = pk)
        category = Categories.objects.all()
        if request.method == 'POST':
            image = request.FILES.get('image')
            title = request.POST.get('title')
            subtitle = request.POST.get('subtitle')
            post_get = request.POST.get('post')
            categorie = request.POST.get('categories')
            pk = 0
            for i in category:
                if i.title == categorie:
                    pk = i.id 
            if pk != 0:
                category = Categories.objects.get(id = pk)
            elif pk == 0:
                category = Categories(title = categorie)
                category.save()
            post.title = title 
            post.subtitle = subtitle 
            post.post = post_get
            post.image = image 
            post.save()
            return redirect('/posts/')
        context ={
            'author':author,
            'post':post,
        }
        return render(request, 'user-panal/edit_post.html',context)
    else:
        return redirect('/')


def delete_post(request,pk):
    if request.user.is_active :
        author = Author.objects.get(author=request.user)
        post = Post.objects.get(id = pk)
        post.delete()
        print('successful')
        return redirect('/posts/')
    else:
        return redirect('/')
    
    


def comments(request):
    if request.user.is_active :
        author = Author.objects.get(author=request.user)
        post = Post.objects.all()
        posts = post.filter(author=author)
        context = {
            'posts': posts,
            'author':author,
        }
        return render(request,'user-panal/comments.html',context)
    else:
        return redirect('/login')
    
def get_comments(request,pk):
    if request.user.is_active:
        author = Author.objects.get(author=request.user)
        post = Post.objects.all()
        posts = post.filter(author=author)
        get_post = Post.objects.get(id = pk)
        comments = Comment.objects.all()
        comments = comments.filter(post = get_post)
        get_reply = Reply.objects.all()
        context = {
            'posts': posts,
            'comments' : comments,
            'author':author,
            'replay':get_reply,
        }
        return render(request, 'user-panal/comments.html',context)


def replay(request):
    if request.method == 'POST':
        author_name = request.POST.get('author')
        post_id = request.POST.get('post_id')
        comment_id = request.POST.get('comment_id')
        replay = request.POST.get('reply')
        comment = Comment.objects.get(id=comment_id)
        if str(request.user) == author_name:
            author = Author.objects.get(author = request.user)
            replay = Reply(comment=comment,author=author,replay=replay )
            replay.save()
    return redirect('/get_comments/'+ post_id)


def commentOnPost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        client_name = request.POST.get('client_name')
        comment_inp = request.POST.get('comment')
        print(post_id,client_name,comment_inp)
        post = Post.objects.get(slug = post_id)
        get_comment = Comment(post = post,name = client_name , comment = comment_inp)
        get_comment.save()
    print("Comment successful add comment")
    return redirect('/post/'+post_id)

def like(request,slug):
    post = Post.objects.get(slug = slug)
    like = Like.objects.get(post = post)
    like.like = int(like.like)+ 1
    like.save()
    print(like.like)
    return redirect('/post/'+slug)



def edit_profile(request):
    if request.user.is_active :
        author = Author.objects.get(author = request.user)
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            city = request.POST.get('city')
            number = request.POST.get('number')
            username = request.POST.get('username')
            print(fname,lname,email,city,number,username)
            user = User.objects.get(username = author)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.username = username
            user.save()
            author.fname = fname 
            author.lname = lname
            author.email = email
            author.city = city
            author.number = number 
            author.author = user 
            author.save()
            return redirect('/user_panal')
        context = {
            'author':author ,
        }
        return render(request,'user-panal/edit-profile.html',context)
    else:
        return redirect('/login')

def image_update(request):
    if request.user.is_active:
        author = Author.objects.get(author = request.user)
        if request.method == 'POST':
            image = request.FILES.get('image')
            author.image = image
            author.save()
            print("File Successfully Uploaded!!")
            return redirect('/user_panal')
        return render(request, 'user-panal/edit-profile.html',{"form":form})
    return redirect('/login')




def feedback(request):
    if request.user.is_active :
        author = Author.objects.get(author = request.user)
        if request.method == 'POST':
            feedback = request.POST.get('feedback')
            rate = request.POST.get('rate')
            save_feedback = Feedback(author = author,feedback = feedback,rate = rate)
            save_feedback.save()
            messages.info(request,'Feedback successfully send!!!')
            return redirect('/user_panal')
        return render(request, 'user-panal/feedback.html',{'author':author})
    else:
        return redirect('/login')



    





