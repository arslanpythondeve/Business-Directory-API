# Use the official lightweight Python 3.11 image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install all Python dependencies
# --no-cache-dir reduces the image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . .

# Expose port 8000 so the application can be accessed from outside the container
EXPOSE 8000

# Start the FastAPI application using Uvicorn
# app.main:app means:
# - app   -> project folder name
# - main  -> main.py file
# - app   -> FastAPI instance inside main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]