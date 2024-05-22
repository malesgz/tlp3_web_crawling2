import os
import requests
from bs4 import BeautifulSoup

# Validación y creación de una carpeta si no existe.
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Descarga la imagen por la url.
def download_image(img_url, folder):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        # Nombre del archivo en base a la URL.
        filename = os.path.join(folder, img_url.split("/")[-1])

        # Guardar la imagen en el directorio.
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Se descargo la imagen: {filename}")
    except requests.RequestException as e:
        print(f"Error al descargar {img_url}: {e}")

# URLs relativas a absolutas
def make_absolute_url(base_url, relative_url):
    if relative_url.startswith(('http://', 'https://')):
        return relative_url
    else:
        return requests.compat.urljoin(base_url, relative_url)

# Extrae y descarga imágenes de la página web.
def scrape_images(url, folder='imagenes'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ensure_directory(folder)
        
        img_tags = soup.find_all('img')
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                img_url = make_absolute_url(url, img_url)
                if img_url.lower().endswith(valid_extensions):
                    download_image(img_url, folder)
    
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")

# URL inicial para hacer scraping
start_url = 'https://www.coca-cola.com/ar/es'
scrape_images(start_url)
