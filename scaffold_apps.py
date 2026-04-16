import os

BASE_DIR = r"c:\Users\ndong\Desktop\EcoMboa\EcoMboa"
APPS_DIR = os.path.join(BASE_DIR, "apps")

apps = [
    'accounts',
    'collection_points',
    'reports',
    'missions',
    'suppliers',
    'sorting_center',
    'buyers',
    'sales',
    'partners',
    'finances',
    'notifications',
    'dashboard',
    'api'
]

if not os.path.exists(APPS_DIR):
    os.makedirs(APPS_DIR)

with open(os.path.join(APPS_DIR, "__init__.py"), "w") as f:
    pass

for app in apps:
    app_dir = os.path.join(APPS_DIR, app)
    os.makedirs(app_dir, exist_ok=True)
    
    with open(os.path.join(app_dir, "__init__.py"), "w") as f:
        pass
    
    # Camel case the app name for the config class
    app_class_name = "".join([word.capitalize() for word in app.split("_")]) + "Config"
    
    apps_py = f"""from django.apps import AppConfig

class {app_class_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app}'
"""
    with open(os.path.join(app_dir, "apps.py"), "w") as f:
        f.write(apps_py)
    
    # Create migrations empty dir with __init__.py
    migrations_dir = os.path.join(app_dir, "migrations")
    os.makedirs(migrations_dir, exist_ok=True)
    with open(os.path.join(migrations_dir, "__init__.py"), "w") as f:
        pass

print("Apps scaffolded.")
