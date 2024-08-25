# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the current directory contents into the container at /app
COPY . /app/

# Step 6: Ensure the Python path is set correctly (optional but recommended)
ENV PYTHONPATH=/app

# Step 7: Collect static files
RUN python manage.py collectstatic --noinput

# Step 8: Expose the port the app runs on
EXPOSE 8000

# Step 9: Define environment variables
# ENV DJANGO_SETTINGS_MODULE=myproject.settings.production  # Adjust as needed
# ENV DJANGO_SETTINGS_MODULE=.settings
ENV PYTHONUNBUFFERED=1

# Step 10: Run the Django development server or your WSGI server
# CMD ["gunicorn", "--bind", "localhost:8000","syntaq_backend.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]