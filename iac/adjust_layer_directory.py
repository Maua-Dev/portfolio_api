import os
import shutil
import subprocess
from pathlib import Path 

BUILD_DIRECTORY = "build"
PYTHON_TOP_LEVEL_DIR = os.path.join(BUILD_DIRECTORY, "python")
REQUIREMENTS_FILE = "requirements-app.txt"

PROJECT_ROOT = Path(__file__).parent.parent 
SHARED_CODE_SOURCE = os.path.join(PROJECT_ROOT, "src", "shared")


def adjust_layer_directory():
    """
    Prepara um diretório 'build' para uma Lambda Layer do AWS CDK.
    
    A função junta o código local compartilhado e as dependências externas (pip)
    na estrutura de pastas que a Lambda espera (/python).
    """

    # Garante que o build seja sempre limpo, removendo qualquer artefato antigo.
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    
    # Cria a estrutura de pastas 'build/python/src/'.
    # Isso é necessário para que os imports 'from src.shared...' funcionem na Lambda.
    shared_code_intermediate_dir = os.path.join(PYTHON_TOP_LEVEL_DIR, "src")
    os.makedirs(shared_code_intermediate_dir)

    # Copia o código compartilhado (de 'src/shared') para dentro da estrutura da Layer.
    # O resultado final será 'build/python/src/shared'.
    print(f"Copiando código de: {SHARED_CODE_SOURCE}") # Adicionado para debug
    shared_code_dest = os.path.join(shared_code_intermediate_dir, os.path.basename(SHARED_CODE_SOURCE))
    shutil.copytree(SHARED_CODE_SOURCE, shared_code_dest)

    # Se o arquivo de dependências existir, instala todas as bibliotecas.
    # O arquivo de requirements também precisa ser lido a partir da raiz.
    requirements_path = os.path.join(PROJECT_ROOT, REQUIREMENTS_FILE)
    if os.path.exists(requirements_path):
        # Instala os pacotes diretamente na pasta 'build/python'.
        # Isso permite que a Lambda importe as bibliotecas de forma padrão (ex: import requests).
        subprocess.check_call(
            ["pip", "install", "-r", requirements_path, "-t", PYTHON_TOP_LEVEL_DIR, "--no-cache-dir"]
        )
    else:
        # Apenas um aviso caso o arquivo não seja encontrado.
        print(f"Aviso: Arquivo '{requirements_path}' não encontrado. Nenhuma dependência externa será instalada.")


# Ponto de entrada do script.
if __name__ == '__main__':
    adjust_layer_directory()