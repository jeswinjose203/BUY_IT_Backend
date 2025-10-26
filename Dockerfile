#for local

# FROM python:3.11-slim


# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# WORKDIR /app

# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt


# COPY . /app/


# EXPOSE 8000

# CMD ["gunicorn", "delivery_app_backend.wsgi:application", "--bind", "0.0.0.0:8000"]




#for deployement
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

# Start the app using entrypoint
CMD ["/app/entrypoint.sh"]
