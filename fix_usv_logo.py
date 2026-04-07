from PIL import Image, ImageFilter
import os

# Increase pixel limit for massive images
Image.MAX_IMAGE_PIXELS = None 

def find_logo_bounds(img, threshold=245):
    """Deep scan for anything darker than the threshold to find the 'real' logo."""
    w, h = img.size
    # Convert to grayscale for easy comparison
    gray = img.convert('L')
    pixels = gray.load()
    
    left, top, right, bottom = w, h, 0, 0
    found_any = False
    
    # We step every 10 pixels first for speed, then refine if needed
    # But for a 2k image, 2M pixels is fast enough
    for y in range(h):
        for x in range(w):
            if pixels[x, y] < threshold:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
                found_any = True
    
    if found_any and left < right:
        # Pad by 50px for safety
        pad = 50
        return (max(0, left-pad), max(0, top-pad), min(w, right+pad), min(h, bottom+pad))
    return None

def crop_and_optimize(filename, sizes):
    """Crops via deep scan and generates responsive versions."""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    img = Image.open(filename)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Detect the 'real' bounds
    bbox = find_logo_bounds(img, threshold=250) # Very high threshold to catch everything but absolute white

    if bbox:
        print(f"Cropping {filename} from {img.size} to {bbox[2]-bbox[0]}x{bbox[3]-bbox[1]} (Deep Scan Cache)")
        img = img.crop(bbox)
    else:
        print(f"No content found in {filename} to crop via Deep Scan.")

    original_size = img.size
    base_name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    for size in sizes:
        ratio = size / original_size[0]
        new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
        
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Subtle sharpening for smaller versions to maintain crispness
        if size <= 1200:
            resized_img = resized_img.filter(ImageFilter.SHARPEN)
            
        output_name = f"{base_name}_{size}{ext}"
        resized_img.save(output_name, optimize=True)
        print(f"  Saved: {output_name} ({new_size})")

if __name__ == "__main__":
    crop_and_optimize('USVlogo.png', [600, 1200, 2500])
