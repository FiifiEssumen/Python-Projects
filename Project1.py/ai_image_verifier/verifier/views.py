from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .utils import predict_image
import os

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        file_name = default_storage.save('temp_images/' + image_file.name, ContentFile(image_file.read()))
        file_path = default_storage.path(file_name)

        # Predict if the image is AI-generated
        prediction = predict_image(file_path)

        # Clean up the temporary file
        os.remove(file_path)

        # Return the result
        if prediction > 0.5:  # Assuming 0.5 is the threshold
            result = "AI-generated"
        else:
            result = "Real"

        return JsonResponse({'result': result})

    return render(request, 'verifier/upload.html')
# Create your views here.
