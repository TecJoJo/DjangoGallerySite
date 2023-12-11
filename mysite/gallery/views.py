from django.shortcuts import render,redirect
from gallery.models import Post
from django.contrib.auth.models import User
from gallery.forms import UploadForm
from PIL import Image
import os



def display_images(request):
    if request.method == 'GET':
        posts_of_user = Post.objects.filter(user__id = request.user.id)
        posts_of_rest_users = Post.objects.exclude(user__id = request.user.id)
        return render(request, 'gallery/index.html', {'user_posts' : posts_of_user,"rest_posts":posts_of_rest_users})

    





def image_upload(request):
    
    size = (300, 300)

    if request.method == 'POST':
        # Get the uploaded image file
        img_file = request.FILES["image"]

       
        mutable_post = request.POST.copy()
        current_user_id = request.user.id
        form = UploadForm(mutable_post, request.FILES)

        if form.is_valid():
            
            post_instance = form.save(commit=False)

            
            post_instance.user_id = current_user_id
            post_instance.save()

            
            img_id = post_instance.id

            # Open the uploaded image using PIL
            with Image.open(img_file) as im:
                # Convert the image to RGB mode
                im = im.convert("RGB")

                # Resize the image to exactly 300x300
                im = im.resize(size)

                # Specify the directory to save the thumbnail
                thumbnail_dir = os.path.join("media", "thumbnails")

                # Create the directory if it doesn't exist
                os.makedirs(thumbnail_dir, exist_ok=True)

                # Specify the name for the thumbnail using the image ID
                thumbnail_name = f"{img_id}_thumbnail.jpg"

                # Specify the full path to save the thumbnail
                thumbnail_path = os.path.join(thumbnail_dir, thumbnail_name)

                
                im.save(thumbnail_path, "JPEG")
                

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
