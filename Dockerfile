FROM numenta/nupic:latest
COPY ai_module/inference  /app
WORKDIR /app
EXPOSE 80 443
RUN apt-get clean \
    && apt-get -y update

# Install requirements.txt
RUN pip install flask --src /usr/local/src
RUN pip install waitress --src /usr/local/src

CMD waitress-serve --call 'run:create_app'

