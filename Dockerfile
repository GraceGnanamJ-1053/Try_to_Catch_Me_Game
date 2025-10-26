# --- Build Stage ---
# 1. Use an official Python image
FROM python:3.11-slim as builder

# 2. Set the working directory
WORKDIR /app

# 3. Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
# 4. Use a smaller, more secure base image for the final app
FROM python:3.11-slim

WORKDIR /app

# 5. Copy the installed dependencies from the "builder" stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 6. Copy your game code
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app.py .

# 7. Expose the port your Flask app runs on
EXPOSE 5000

# 8. Command to run your app
# We use Gunicorn (a production server) instead of Flask's debug server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]