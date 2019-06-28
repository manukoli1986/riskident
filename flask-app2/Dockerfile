#FROM python:3
FROM frolvlad/alpine-python3

#Created By
MAINTAINER "Mayank Koli"

#Expose port 
EXPOSE 80

#Using default directory
WORKDIR /usr/src/app

#COPY code from localhost into docker container
COPY . ./

#Installing modules using requirement file
RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

#Setting up default running mode 
CMD [ "python3", "app.py" ]
#CMD [ "flask", "run", "--host=0.0.0.0", "--port=80" ]
