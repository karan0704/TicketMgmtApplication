import os

# 🔧 Change this to your actual project root directory
project_root = r"D:\Learning Projects\TicketMgmtApplication"

# 📄 Output file
output_file = "spring_project_dump.txt"

# 🎯 File extensions to include
allowed_extensions = {".java", ".xml", ".properties", ".yml", ".yaml", ".gradle", ".txt"}

with open(output_file, "w", encoding="utf-8") as out_file:
    for root, _, files in os.walk(project_root):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in allowed_extensions):
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, project_root)
                out_file.write(f"\n\n--- File: {relative_path} ---\n")
                try:
                    with open(full_path, "r", encoding="utf-8") as code_file:
                        out_file.write(code_file.read())
                except Exception as e:
                    out_file.write(f"[Could not read file: {e}]\n")

print(f"✅ Spring Boot project exported to: {output_file}")
