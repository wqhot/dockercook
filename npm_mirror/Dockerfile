FROM verdaccio/verdaccio:5.30.2

USER root

RUN npm install -g npm-cli-adduser

USER verdaccio

WORKDIR /verdaccio

EXPOSE 4873

CMD ["verdaccio"]
