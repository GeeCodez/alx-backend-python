# Step 1- user python 3.10 as base container
FROM python:3.10

# Step 2- set working directory
WORKDIR /app

# Step 3- copy requirements.txt to the contaner
COPY requirements.txt .

# Step 4- install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5- copy the rest of the application code to the container
COPY . .

# Step 6- Expose the django port
EXPOSE 8000

# Step 7- run the django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]