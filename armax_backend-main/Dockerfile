FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev python3-dev \
    postgresql postgresql-client libffi-dev libc-dev libpq5 tree

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.11-slim
WORKDIR /app

# RUN addgroup appuser && adduser appuser -G appuser

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY entrypoint.sh .
# RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN ["chmod", "+x", "/app/entrypoint.sh"]

COPY . .

ENTRYPOINT ["bash", "-c", "./entrypoint.sh"]
