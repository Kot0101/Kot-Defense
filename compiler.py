import os

# Файлы или папки, которые нужно игнорировать (чтобы не собирать мусор)
IGNORE_LIST = {
    'venv', '.venv', 'env', '__pycache__', '.git', '.idea', '.vscode',
    'pack_project.py', 'output_project.md'  # игнорируем сам скрипт и результат
}

def pack_project_to_markdown(output_file="output_project.md"):
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# СТРУКТУРА ПРОЕКТА\n\n")
        
        # 1. Сначала пишем красивое дерево файлов для нейронки
        out.write("```text\n")
        for root, dirs, files in os.walk(project_root):
            # Фильтруем игнорируемые папки на лету
            dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
            
            level = root.replace(project_root, '').count(os.sep)
            indent = ' ' * 4 * level
            sub_folder = os.path.basename(root)
            if sub_folder and sub_folder not in IGNORE_LIST:
                out.write(f"{indent}{sub_folder}/\n")
            
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if f.endswith('.py') and f not in IGNORE_LIST:
                    out.write(f"{sub_indent}{f}\n")
        out.write("```\n\n---\n\n")
        
        # 2. Собираем содержимое всех .py файлов
        out.write("# ИСХОДНЫЙ КОД\n\n")
        
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
            
            for file in files:
                if file.endswith('.py') and file not in IGNORE_LIST:
                    full_path = os.path.join(root, file)
                    # Получаем относительный путь (например: source/utils/math.py)
                    rel_path = os.path.relpath(full_path, project_root)
                    
                    out.write(f"## Файл: `{rel_path}`\n")
                    out.write("```python\n")
                    
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"# Не удалось прочитать файл: {e}\n")
                        
                    out.write("\n```\n\n---\n\n")
                    
    print(f" Готово! Весь проект собран в файл: {output_file}")

if __name__ == "__main__":
    pack_project_to_markdown()