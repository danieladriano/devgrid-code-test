FROM python:3.8.12-buster
LABEL maintaner="Daniel Domingos Adriano"

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/.
RUN pip3 install -r requirements.txt

COPY app.py /app/.
COPY process_weather.py /app/.
COPY cities.csv /app/.
COPY init.sh /app/.

ENV PORT=8888
ENV WORKERS=1
ENV API_KEY=""
ENV API_UNIT="metric"

RUN chmod u+x /app/init.sh
EXPOSE $PORT
CMD ["/bin/bash"]
ENTRYPOINT ["sh", "/app/init.sh"]