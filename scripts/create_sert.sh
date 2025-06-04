#!/bin/bash

SSL_PATH=$(pwd)/../apache/ssl
openssl req -x509 -newkey rsa:2048 -keyout $SSL_PATH/server.key -out $SSL_PATH/server.crt -days 365 -nodes -config $SSL_PATH/server.conf -extensions v3_req