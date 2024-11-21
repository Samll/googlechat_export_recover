import os
import json
from datetime import datetime
from jinja2 import Template
import itertools

# Load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Convert date string to desired timestamp format
def format_timestamp(date_str):
    dt = datetime.strptime(date_str, "%A, %B %d, %Y at %I:%M:%S %p %Z")
    return dt.strftime("%d/%B/%Y %H:%M:%S")

# Generate a dictionary of unique colors for users
def assign_colors(users):
    pastel_colors = [
        "rgba(173, 216, 230, 0.8)",  # Light Blue
        "rgba(240, 128, 128, 0.8)",  # Light Coral
        "rgba(144, 238, 144, 0.8)",  # Light Green
        "rgba(255, 182, 193, 0.8)",  # Light Pink
        "rgba(255, 255, 224, 0.8)",  # Light Yellow
        "rgba(221, 160, 221, 0.8)",  # Plum
        "rgba(255, 222, 173, 0.8)",  # Navajo White
    ]
    color_cycle = itertools.cycle(pastel_colors)
    return {user: next(color_cycle) for user in users}

# Extract member names and handle groups
def extract_member_names(members):
    extracted_names = []
    for member in members:
        if member["user_type"] == "Group":
            # Use the email field before the @ symbol as the name
            group_name = member["email"].split("@")[0]
            extracted_names.append(group_name)
        else:
            extracted_names.append(member["name"])
    return extracted_names

# Generate a unique folder name
def generate_unique_folder_name(base_path, folder_name):
    counter = 1
    new_folder_name = folder_name
    while os.path.exists(os.path.join(base_path, new_folder_name)):
        new_folder_name = f"{folder_name}_{counter}"
        counter += 1
    return new_folder_name

# Generate HTML with modal and user-specific colors
def generate_html(messages, user_colors, output_path):
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Export</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 20px; }
            .message { margin-bottom: 20px; padding: 10px; border-radius: 10px; max-width: 60%; }
            .sender { font-weight: bold; margin-bottom: 5px; }
            .timestamp { font-size: 0.8em; color: gray; margin-bottom: 5px; }
            .image { height: 100px; cursor: pointer; border-radius: 5px; }
            .modal { 
                display: none; 
                position: fixed; 
                z-index: 1000; 
                left: 0; 
                top: 0; 
                width: 100%; 
                height: 100%; 
                overflow: auto; 
                background-color: rgba(0, 0, 0, 0.8); 
            }
            .modal-content {
                display: block;
                margin: 5% auto;
                max-width: 90%;
                height: auto;
            }
            .close {
                position: absolute;
                top: 20px;
                right: 35px;
                color: white;
                font-size: 30px;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div style="display: flex; flex-direction: column;">
            {% for msg in messages %}
            <div class="message" style="background-color: {{ user_colors[msg['sender']] }};">
                <div class="sender">{{ msg['sender'] }}</div>
                <div class="timestamp">{{ msg['timestamp'] }}</div>
                {% if msg['type'] == 'text' %}
                    <div>{{ msg['content'] }}</div>
                {% elif msg['type'] == 'image' %}
                    <div>
                        {% for image in msg['content'] %}
                        <img src="{{ image }}" class="image" alt="Image" onclick="openModal('{{ image }}')">
                        {% endfor %}
                    </div>
                {% elif msg['type'] == 'file' %}
                    <div>
                        {% for file in msg['content'] %}
                        <a href="{{ file }}" download>{{ file }}</a><br>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <!-- Modal -->
        <div id="imageModal" class="modal">
            <span class="close" onclick="closeModal()">&times;</span>
            <img class="modal-content" id="modalImage">
        </div>
        
        <script>
            function openModal(imageSrc) {
                var modal = document.getElementById('imageModal');
                var modalImg = document.getElementById('modalImage');
                modal.style.display = "block";
                modalImg.src = imageSrc;
            }
            
            function closeModal() {
                var modal = document.getElementById('imageModal');
                modal.style.display = "none";
            }
        </script>
    </body>
    </html>
    """
    jinja_template = Template(template)
    rendered_html = jinja_template.render(messages=messages, user_colors=user_colors)

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(rendered_html)

# Process a single folder
def process_chat_folder(folder_path):
    chat_file = os.path.join(folder_path, "messages.json")
    group_file = os.path.join(folder_path, "group_info.json")
    
    if not os.path.isfile(chat_file) or not os.path.isfile(group_file):
        return  # Skip folders without required files

    # Load chat and group data
    chat_data = load_json(chat_file)
    group_data = load_json(group_file)
    
    # Extract member names
    current_members = extract_member_names(group_data.get("members", []))
    
    # Check for a "name" field in group_info
    group_name = group_data.get("name")
    
    # Add "DeletedUser" if only one member is found
    if len(current_members) == 1:
        current_members.append("DeletedUser")
    
    # Initialize messages
    messages = []
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

    # Collect unique users
    unique_users = set()
    for msg in chat_data.get("messages", []):
        if msg.get("message_state") == "DELETED":
            continue  # Skip deleted messages
        unique_users.add(msg["creator"]["name"])
    
    user_colors = assign_colors(unique_users)

    for msg in chat_data.get("messages", []):
        if msg.get("message_state") == "DELETED":
            continue  # Skip deleted messages
        timestamp = format_timestamp(msg["created_date"])
        sender = msg["creator"]["name"]

        if "text" in msg:  # Text messages
            messages.append({
                "timestamp": timestamp,
                "sender": sender,
                "content": msg["text"],
                "type": "text"
            })
        elif "attached_files" in msg:  # Attachments
            images = []
            files = []
            for file in msg["attached_files"]:
                extension = os.path.splitext(file["export_name"])[1].lower()
                if extension in image_extensions:
                    images.append(file["export_name"])
                else:
                    files.append(file["export_name"])
            if images:
                messages.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "content": images,
                    "type": "image"
                })
            if files:
                messages.append({
                    "timestamp": timestamp,
                    "sender": sender,
                    "content": files,
                    "type": "file"
                })

    # Determine output file name
    if group_name:
        output_name = group_name.replace(" ", "_").replace("/","_")
    else:
        valid_names = [name.replace(" ", "_") for name in current_members]
        output_name = "_".join(valid_names)

    output_file = os.path.join(folder_path, f"{output_name}_Chat.html")

    # Generate HTML
    generate_html(messages, user_colors, output_file)

    # Rename the folder, ensuring unique name
    parent_path = os.path.dirname(folder_path)
    unique_folder_name = generate_unique_folder_name(parent_path, output_name)
    new_folder_path = os.path.join(parent_path, unique_folder_name)
    os.rename(folder_path, new_folder_path)

    print(f"Processed: {new_folder_path}")

# Traverse all folders recursively
def process_all_folders(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if "messages.json" in filenames and "group_info.json" in filenames:
            process_chat_folder(dirpath)

# Root directory to process
root_directory = "."  # Replace with the actual root directory

# Execute the script
process_all_folders(root_directory)
