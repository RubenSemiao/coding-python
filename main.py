import requests
from bs4 import BeautifulSoup
import subprocess
import zipfile
import os

def download_subtitles(movie_name):
    search_url = f"https://www.opensubtitles.org/pt/search/sublanguageid-por/moviename-{movie_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar o primeiro link de legenda usando a tag 'a' com href que contém 'subtitles/'
        subtitle_link = soup.find('a', href=lambda href: href and '/subtitles/' in href)
        
        if subtitle_link:
            href = subtitle_link.get('href')
            subtitle_id = href.split('/')
            subtitle_url = f"https://www.opensubtitles.org/pt/subtitleserve/sub/{subtitle_id}"
            print(f"URL de download da legenda: {subtitle_url}... Fazendo download...")
            try:
                output_file = f"{movie_name}.zip"  # Nome do arquivo de saída
                subprocess.run(["wget", subtitle_url, "-O", output_file], check=True)
                print(f"Download completo: {output_file}")
                return output_file
            except subprocess.CalledProcessError as e:
                print(f"Erro ao fazer download: {e}")
        else:
            print("Nenhuma legenda encontrada.")
    else:
        print(f"Erro ao buscar resultados: {response.status_code}")
    return None

def unzip_file(zip_file, extract_to='.'):
    """
    Descompacta o arquivo zip especificado para o diretório de destino.
    
    :param zip_file: Caminho para o arquivo zip
    :param extract_to: Diretório onde os arquivos serão extraídos (padrão é o diretório atual)
    """
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Arquivos extraídos para {os.path.abspath(extract_to)}")
    except zipfile.BadZipFile:
        print("Erro: arquivo zip inválido.")

def process_folder(folder_path):
    """
    Processa todos os arquivos de vídeo na pasta e tenta fazer o download das legendas para cada um.
    
    :param folder_path: Caminho da pasta onde os arquivos de vídeo estão armazenados
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.mp4', '.avi', '.mkv')):  # Verifica se o arquivo é um vídeo
            movie_name = os.path.splitext(file_name)[0]
            print(f"Procurando legendas para: {movie_name}")
            zip_file = download_subtitles(movie_name)
            if zip_file:
                unzip_file(zip_file, folder_path)  # Extrai na mesma pasta do filme

# Exemplo de uso
#folder_path = "/mnt/c/Users/Rúben/Downloads/PopcornTime"
#process_folder(folder_path)

download_subtitles("Blink.Twice.2024.720p.WEBRip.800MB.x264-GalaxyRG.mkv")