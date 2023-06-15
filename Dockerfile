# Fetch the official Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code
COPY . .

# Expose the port Streamlit will use
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "ui.py"]