import os
import subprocess
import gc
import torch

# Rutas del proyecto y del nuevo proyecto migrado a Java 8
project_path = "C:/Users/josue/Desktop/tu_archivo"
new_project_path = "C:/Users/josue/Desktop/EcommerceApp_java8"
os.makedirs(new_project_path, exist_ok=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Usando dispositivo: {device}")

def generate_response_with_ollama(prompt, max_new_tokens=700):
    """Ejecuta Ollama y devuelve la respuesta generada."""
    try:
        result = subprocess.run(
            # SE PUEDE CAMBIAR EL MODELO SEGUN LOS QUE TENGAS INSTALADOS CON OLLAMA O QUE PUEDAS UTILIZAR
            ["ollama", "run", "granite-code:8b-instruct", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error al ejecutar Ollama: {e}")
        return "Error en la generación del análisis."

def migrate_file(file_path, new_file_path):
    """Migra un archivo a Java 8 y guarda la versión actualizada."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
        return

    # Prompt para migrar el código a Java 8
    migration_prompt = (
        f"Realiza la migración del siguiente código de Java 6 a Java 8, asegurando compatibilidad total con Java 8. \n"
        f"- No agregues comentarios explicativos, notas o símbolos innecesarios. \n"
        f"- Aplica expresiones lambda y la API de Streams cuando sea posible y adecuado, manteniendo la lógica intacta. \n"
        f"- Simplifica bucles y estructuras redundantes si puedes transformarlos en lambdas o métodos de colección de Java 8. \n"
        f"- Mantén la estructura y la lógica sin alterar el comportamiento original del código. \n"
        f"- Conserva las convenciones de estilo y asegúrate de que el código esté ordenado y fácil de leer.\n\n"
        f"Código a migrar:\n\n{content}\n"
    )

    # Obtener la versión migrada del código
    migrated_code = generate_response_with_ollama(migration_prompt)

    # Guardar el archivo migrado en la nueva ruta
    try:
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(migrated_code)
        print(f"{file_path} migrado y guardado en {new_file_path}.")
    except Exception as e:
        print(f"Error al guardar {new_file_path}: {e}")

def process_migration():
    """Procesa y migra cada archivo en el proyecto a Java 8."""
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith((".java", ".jsp")):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                new_file_path = os.path.join(new_project_path, relative_path)

                # Crear el directorio si no existe
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

                print(f"Migrando {file_path}...")
                migrate_file(file_path, new_file_path)

                # Liberar memoria entre archivos
                torch.cuda.empty_cache()
                gc.collect()

    print("Migración completa. Revisa el proyecto migrado en la carpeta correspondiente.")

if __name__ == "__main__":
    print("Iniciando migración del proyecto a Java 8...")
    process_migration()
    print(f"Migración completa. Revisa el nuevo proyecto en: {new_project_path}")
