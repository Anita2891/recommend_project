# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
#ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies, then install Python packages
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Collect static files after copying the application
RUN python manage.py collectstatic --noinput

# Expose port 8000 to allow external access to the app
EXPOSE 8000

# Run the container using gunicorn (or Django's development server)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "recommend_project.wsgi:application"]
