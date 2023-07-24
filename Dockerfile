FROM python:3.11-slim-bookworm as dev

WORKDIR /work

RUN apt-get update

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pytest mypy pyyaml

COPY pyparepackage.py /work/pyparepackage.py

CMD ["python", "pyparepackage.py"]
