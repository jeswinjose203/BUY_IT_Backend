# #for local
# # Base image
# FROM python:3.11-slim

# # Environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy project
# COPY . /app/

# # Expose port
# EXPOSE 8000

# # Run server using Gunicorn
# CMD ["gunicorn", "delivery_app_backend.wsgi:application", "--bind", "0.0.0.0:8000"]








# Base image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Start the app
CMD ["/app/entrypoint.sh"]
