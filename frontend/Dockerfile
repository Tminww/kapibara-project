# base image
FROM node:latest

# set working directory
WORKDIR /code

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /code/node_modules/.bin:$PATH

RUN curl -fsSL https://bun.sh/install | bash

RUN source /root/.bashrc
# install and cache app dependencies
COPY package.json /code/package.json
COPY bun.lock /code/bun.lock

COPY . .


RUN bun install
# RUN npm install @vue/cli@3.7.0 -g

# start app
# CMD ["npm", "run", "dev", "--", "--host"]
EXPOSE 5173
CMD ["bun", "run", "dev"]