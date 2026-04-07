from PIL import Image, ImageFilter
import os

# Increase pixel limit for massive images
Image.MAX_IMAGE_PIXELS = None 

def create_responsive_versions(filename, sizes, sharpen_factor=1.0):
    """Generates multiple resized versions of an image for srcset with customizable sharpening."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    img = Image.open(filename)
    original_size = img.size
    print(f"Processing {filename}: {original_size} (Sharpen Factor: {sharpen_factor})")

    base_name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    for size in sizes:
        # We always want at least one version, and others only if large enough
        ratio = size / original_size[0]
        new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
        
        # Don't upscale smaller sources unless necessary for high-DPI
        if original_size[0] < size and size > 1500:
            continue
            
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Apply sharpening for web-sized images to maintain crispness
        if size <= 1500:
            # We apply it twice if a higher sharpen factor is requested for fine-detailed logos
            resized_img = resized_img.filter(ImageFilter.SHARPEN)
            if sharpen_factor > 1.0:
                resized_img = resized_img.filter(ImageFilter.SHARPEN)
            
        output_name = f"{base_name}_{size}{ext}"
        resized_img.save(output_name, optimize=True)
        print(f"  Saved: {output_name} ({new_size})")

if __name__ == "__main__":
    # Standard targets
    standard_targets = [
        'USEMAFirstpage.png',
        'USVlogo.png',
        'Usema Circle.png'
    ]
    
    # Process standard targets with default sharpening
    for target in standard_targets:
        create_responsive_versions(target, [600, 1200, 2500])
        
    # Process Circle of Care with specialized sizes and extra sharpening
    # This logo has fine icons/text that need to 'pop' on mobile
    create_responsive_versions('Circle of Care.png', [600, 1200, 1500, 2500], sharpen_factor=1.5)
