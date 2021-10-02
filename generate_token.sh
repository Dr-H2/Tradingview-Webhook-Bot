#!/bin/bash

token=`openssl rand -base64 12`
rm token
echo $token > token
echo Your token is the following:
echo $token
echo Please put it in your webhook accordingly \(\{..., 'token':...\}.\)
