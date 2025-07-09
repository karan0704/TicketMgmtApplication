import os

# Define folder structure and files with sample content
project_structure = {
    "frontend": {
        "index.html": "<!-- index.html entry point -->",
        "assets": {
            "styles.css": "/* styles.css */"
        },
        "dashboard": {
            "dashboard.js": "// dashboard.js",
            "dashboard.html": "<!-- dashboard.html -->"
        },
        "customers": {
            "customers.js": "// customers.js",
            "customers.html": "<!-- customers.html -->"
        },
        "engineers": {
            "engineers.js": "// engineers.js",
            "engineers.html": "<!-- engineers.html -->"
        },
        "tickets": {
            "tickets.js": "// tickets.js",
            "tickets.html": "<!-- tickets.html -->"
        },
        "files": {
            "files.js": "// files.js",
            "files.html": "<!-- files.html -->"
        },
        "shared": {
            "api.js": "// shared/api.js\nconst API_BASE_URL = 'http://localhost:8080/api';",
            "modal.js": "// shared/modal.js\nfunction closeModal() { document.getElementById('ticketModal').style.display = 'none'; }",
            "alert.js": "// shared/alert.js\nfunction showAlert(msg) { alert(msg); }",
            "utils.js": "// shared/utils.js\nfunction isValidEmail(email) { return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email); }"
        }
    }
}

base_path = "/mnt/data"


def create_structure(base, structure):
    for name, content in structure.items():
        path = os.path.join(base, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)


create_structure(base_path, project_structure)
"/mnt/data/frontend structure with all files created."
