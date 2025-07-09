import os
import re

def analyze_spring_boot_project(project_path):
    """
    Analyzes a Spring Boot project to identify REST API endpoints and Java DTOs.

    Args:
        project_path (str): The root path of your Spring Boot project.
                            Example: 'D:/Learning Projects/TicketMgmtApplication'
    """
    print(f"Starting analysis of project: {project_path}\n")

    if not os.path.isdir(project_path):
        print(f"Error: Project path '{project_path}' does not exist or is not a directory.")
        return

    java_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))

    if not java_files:
        print("No Java files found in the specified project path.")
        return

    rest_controllers = {}
    java_objects = {}

    # Regex patterns
    # Matches class declarations and their annotations
    class_pattern = re.compile(r"(?:@(?:RestController|Controller|Service|Component|Repository|Entity|Data|Getter|Setter|NoArgsConstructor|AllArgsConstructor)\s*)*\s*(?:public|private|protected)?\s*(?:abstract)?\s*(?:final)?\s*class\s+([A-Za-z0-9_]+)(?:\s+implements\s+[^{]+)?(?:\s+extends\s+[^{]+)?\s*{")
    
    # Matches method declarations and their annotations within a class
    method_pattern = re.compile(r"(?:@(?:GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*(?:\(\s*value\s*=\s*\"([^\"]*)\"|\(\s*\"([^\"]*)\")?\s*\)|\s*@RequestMapping\s*(?:\(\s*value\s*=\s*\"([^\"]*)\"|\(\s*\"([^\"]*)\")?,\s*method\s*=\s*RequestMethod\.([A-Z]+)\s*\))?\s*(?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*([A-Za-z0-9_<>,\s]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)\s*(?:throws\s+[^{]+)?\s*{")
    
    # Matches @RequestBody annotation and its type
    request_body_pattern = re.compile(r"@RequestBody\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)")
    
    # Matches @RequestParam, @PathVariable and their types
    request_param_path_var_pattern = re.compile(r"@(?:RequestParam|PathVariable)(?:\([^)]*\))?\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)")
    
    # Matches package declaration
    package_pattern = re.compile(r"package\s+([a-zA-Z0-9_\.]+);")


    for file_path in java_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            # Extract package name
            package_match = package_pattern.search(content)
            package_name = package_match.group(1) if package_match else "default.package"

            # Find all classes
            for class_match in class_pattern.finditer(content):
                class_name = class_match.group(1)
                full_class_name = f"{package_name}.{class_name}"

                # Check if it's a RestController
                if "@RestController" in content[class_match.start():class_match.end() + 200]: # Look a bit ahead for annotation
                    controller_base_path = ""
                    class_request_mapping_match = re.search(r"@RequestMapping\s*(?:\(\s*value\s*=\s*\"([^\"]*)\"|\(\s*\"([^\"]*)\")?\)", content[class_match.start():])
                    if class_request_mapping_match:
                        controller_base_path = class_request_mapping_match.group(1) or class_request_mapping_match.group(2) or ""
                    
                    rest_controllers[full_class_name] = {
                        "base_path": controller_base_path,
                        "endpoints": []
                    }

                    # Find methods within this controller
                    class_content = content[class_match.start():] # Search from the class start
                    for method_match in method_pattern.finditer(class_content):
                        method_return_type = method_match.group(5)
                        method_name = method_match.group(6)
                        method_params_str = method_match.group(7)

                        endpoint_path = method_match.group(1) or method_match.group(2) or method_match.group(3) or method_match.group(4) or ""
                        http_method = method_match.group(5) if method_match.group(5) in ["GET", "POST", "PUT", "DELETE"] else None

                        # Infer HTTP method from annotation if not explicitly in RequestMapping
                        if not http_method:
                            if "@GetMapping" in class_content[method_match.start():method_match.end() + 50]:
                                http_method = "GET"
                            elif "@PostMapping" in class_content[method_match.start():method_match.end() + 50]:
                                http_method = "POST"
                            elif "@PutMapping" in class_content[method_match.start():method_match.end() + 50]:
                                http_method = "PUT"
                            elif "@DeleteMapping" in class_content[method_match.start():method_match.end() + 50]:
                                http_method = "DELETE"
                        
                        full_endpoint_path = os.path.join(controller_base_path, endpoint_path).replace("\\", "/")
                        
                        request_body_type = None
                        request_params = []

                        # Parse method parameters for @RequestBody and other params
                        if method_params_str:
                            req_body_match = request_body_pattern.search(method_params_str)
                            if req_body_match:
                                request_body_type = req_body_match.group(1)
                            
                            for param_match in request_param_path_var_pattern.finditer(method_params_str):
                                param_type = param_match.group(1)
                                param_name = param_match.group(2)
                                request_params.append(f"{param_type} {param_name}")

                        rest_controllers[full_class_name]["endpoints"].append({
                            "method_name": method_name,
                            "http_method": http_method,
                            "path": full_endpoint_path,
                            "request_body_type": request_body_type,
                            "request_params": request_params,
                            "response_type": method_return_type
                        })
                
                # Check if it's a potential Java object/DTO/Entity
                # Simple heuristic: if it's not a controller/service/repository and has fields
                # This is a very basic check. More robust would involve looking for getters/setters or Lombok annotations.
                if "@RestController" not in content[class_match.start():class_match.end() + 200] and \
                   "@Service" not in content[class_match.start():class_match.end() + 200] and \
                   "@Repository" not in content[class_match.start():class_match.end() + 200] and \
                   "@Entity" in content[class_match.start():class_match.end() + 200] or \
                   "@Data" in content[class_match.start():class_match.end() + 200] or \
                   re.search(r"(?:private|protected|public)\s+[A-Za-z0-9_<>,\s]+\s+[A-Za-z0-9_]+\s*;", content[class_match.start():class_match.end() + 500]): # Look for field declarations
                    
                    java_objects[full_class_name] = {
                        "fields": []
                    }
                    # Attempt to extract fields (very basic)
                    field_pattern = re.compile(r"(?:private|protected|public)\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)\s*;")
                    for field_match in field_pattern.finditer(content[class_match.start():]):
                        field_type = field_match.group(1)
                        field_name = field_match.group(2)
                        java_objects[full_class_name]["fields"].append(f"{field_type} {field_name}")


    print("\n--- Identified REST API Endpoints ---")
    if rest_controllers:
        for controller_name, data in rest_controllers.items():
            print(f"\nController: {controller_name}")
            print(f"  Base Path: {data['base_path']}")
            for endpoint in data['endpoints']:
                print(f"    Method: {endpoint['http_method']} {endpoint['path']}")
                print(f"      Java Method: {endpoint['method_name']}")
                if endpoint['request_body_type']:
                    print(f"      Request Body: {endpoint['request_body_type']}")
                if endpoint['request_params']:
                    print(f"      Request Params: {', '.join(endpoint['request_params'])}")
                print(f"      Response Type: {endpoint['response_type']}")
    else:
        print("No @RestController classes found.")

    print("\n--- Identified Java Objects (DTOs/Entities) ---")
    if java_objects:
        for obj_name, data in java_objects.items():
            print(f"\nObject: {obj_name}")
            if data['fields']:
                print("  Fields:")
                for field in data['fields']:
                    print(f"    - {field}")
            else:
                print("  No fields identified (or complex structure).")
    else:
        print("No potential Java objects/DTOs/Entities found.")

    print("\nAnalysis complete. Remember to manually verify the extracted information.")

# --- How to use the script ---
# 1. Save this code as a Python file (e.g., `analyze_backend.py`).
# 2. Open your terminal or command prompt.
# 3. Navigate to the directory where you saved the script.
# 4. Run the script, replacing the placeholder path with your actual project path:
#    python analyze_backend.py
#
#    Example for your path:
#    project_root = r"D:\Learning Projects\TicketMgmtApplication"
#    analyze_spring_boot_project(project_root)
#
#    Note: Use raw string (r"...") for Windows paths to avoid issues with backslashes.
#    The path you provided `D:\Learning Projects\TicketMgmtApplication\src\main\java\ticketmgmt\controller`
#    is a sub-directory. You should provide the *root* of your Spring Boot project,
#    which would likely be `D:\Learning Projects\TicketMgmtApplication`.

# Example usage (uncomment and modify with your actual project path):
# project_root = r"D:\Learning Projects\TicketMgmtApplication"
# analyze_spring_boot_project(project_root)

# To run it, you'll need to uncomment the last two lines and provide your path.
# For example:
project_root = r"D:\Learning Projects\TicketMgmtApplication"
analyze_spring_boot_project(project_root)
