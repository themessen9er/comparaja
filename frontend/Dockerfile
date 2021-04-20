FROM node:alpine

WORKDIR /project

ENV PATH /project/node_modules/.bin:$PATH

COPY ./app/ /project/
RUN npm install
RUN npm install @vue/cli -g
RUN npm run build

# start app
CMD ["npm", "run", "serve"]