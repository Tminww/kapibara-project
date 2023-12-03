# base image
FROM node:latest

# set working directory
WORKDIR /code

# add `/app/node_modules/.bin` to $PATH
ENV PATH /code/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /code/package.json
COPY package-lock.json /code/package-lock.json
RUN npm install
RUN npm install @vue/cli@3.7.0 -g

# start app
CMD ["npm", "run", "dev", "--host"]