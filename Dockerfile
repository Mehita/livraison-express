# syntax=docker/dockerfile:1

# --- Étape 1 : construire l'environnement Python (outils de build jetés ensuite) ---
FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt seul d'abord : tant qu'il ne change pas, cette couche reste en cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Allègement : les bibliothèques embarquent leurs tests, inutiles dans une API
RUN find /opt/venv -type d -name tests -prune -exec rm -rf {} +

# Sécurité : plus d'installeur de paquets dans l'image livrée
RUN pip uninstall -y pip


# --- Étape 2 : image finale, minimale et sans privilèges ---
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/src

# Utilisateur dédié, sans shell, avec deux dossiers inscriptibles : le modèle et les données
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --home-dir /app --shell /usr/sbin/nologin app \
 && mkdir -p /app /artifacts /data \
 && chown app:app /app /artifacts /data

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app src ./src

USER app

EXPOSE 8000

# Sonde de vivacité : /health ne dépend d'aucune brique externe (pas de curl dans l'image)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["python", "-m", "livraison_express", "serve", "--host", "0.0.0.0", "--port", "8000"]
