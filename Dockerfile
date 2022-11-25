FROM python:3.8.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt time_series/requirements.txt

WORKDIR /time_series

RUN pip install -r requirements.txt

COPY . /time_series

EXPOSE 8501

# CMD ["streamlit", "run", "About.py"]