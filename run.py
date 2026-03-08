from app.main import create_app
from app.config import get_settings
app = create_app()
print("✅ Application created successfully")
settings = get_settings()
print("App is running on PORT:", settings.PORT, "http://localhost:" + str(settings.PORT))
print("Current settings:")
for key, value in settings.model_dump().items():
  print(f"{key}: {value}")