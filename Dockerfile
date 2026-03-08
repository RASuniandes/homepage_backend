FROM python:3.11-slim

WORKDIR /app

# =====================================================
# SYSTEM DEPENDENCIES
# =====================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 \
  libffi-dev \
  shared-mime-info \
  fonts-dejavu \
  fonts-liberation \
  fonts-freefont-ttf \
  libglib2.0-0 \
  curl \
  gcc \
  default-libmysqlclient-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# =====================================================
# PYTHON DEPENDENCIES
# =====================================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =====================================================
# APP CODE
# =====================================================
COPY . .

# =====================================================
# ENVIRONMENT
# =====================================================
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Change 5001 to 80
EXPOSE 5001

# =====================================================
# HEALTHCHECK
# =====================================================
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# =====================================================
# START
# =====================================================
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5001"]
