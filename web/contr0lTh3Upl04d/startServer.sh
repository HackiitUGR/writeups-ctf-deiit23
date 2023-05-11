#!/bin/bash

docker build -t etsiit_file_upload:1.0 .

docker run --name FileUploadServer -d -p 80:80 etsiit_file_upload:1.0
