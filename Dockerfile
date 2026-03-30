FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
# Only copy the specific application files needed.
# This ensures the final image is small and secure.
COPY main.py .

# Create a non-root user and group
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser \
	&& chown -R appuser:appuser $APP_HOME

# Switch to non-root user
USER appuser

# Run the web service on container startup.
# Use gunicorn for production. Cloud Run sets the PORT environment variable.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 120 main:app
