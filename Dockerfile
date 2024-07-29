# Use the official Python image from the Docker Hub
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /myapp

# Install dependencies
COPY requirements.txt /myapp/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /myapp/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]
