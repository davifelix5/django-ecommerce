from PIL import Image
from django.conf import settings
import os


def resize_img(img, new_width=800):
    original_img_path = os.path.join(settings.MEDIA_ROOT, img.name)
    original_img = Image.open(original_img_path)
    old_width, old_heigth = original_img.size

    if not old_width > new_width:
        return

    new_heigth = (800 * old_heigth) / old_width
    new_heigth = round(new_heigth)

    new_img = original_img.resize((new_width, new_heigth), Image.LANCZOS)
    new_img.save(
        original_img_path,  # Sobrescrevendo a original
        optimize=True,
        quality=50
    )
    original_img.close()
