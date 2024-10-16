FROM python:3.12.6

COPY . ./app
WORKDIR /app

RUN python -m pip install pdm
RUN pdm install --prod

EXPOSE 8000

CMD ["pdm", "run", "start"]