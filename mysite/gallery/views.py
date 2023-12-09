from django.shortcuts import render,redirect
from gallery.models import Post
from django.contrib.auth.models import User
from gallery.forms import UploadForm

def display_images(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'gallery/index.html', {'posts' : posts})

    
from django.contrib.auth.decorators import login_required


def image_upload(request):
    if request.method == 'POST':
        # Create a mutable copy of Post
        mutable_post = request.POST.copy()

        
        current_user_id = request.user.id

        
        mutable_post["user"] = str(current_user_id)

        form = UploadForm(mutable_post, request.FILES)
        if form.is_valid():
            # Create a form instance without saving it to the database
            post_instance = form.save(commit=False)

            # Set the user_id field before saving
            post_instance.user_id = current_user_id
            post_instance.save()

            return redirect('gallery:success')
    else:
        form = UploadForm()

    return render(request, 'gallery/upload.html', {'form': form})


def image_detail(request,pk):
    if request.method == "GET":
        post = Post.objects.get(pk=pk)
        
        return render(request,"gallery/detail.html",{"post":post})
    
    if request.method == "POST":
        post_to_delete = Post.objects.get(pk=pk)
        post_to_delete.delete()
        return redirect("gallery:display_images")




def success(request):
    return render(request, 'gallery/success.html', {})
