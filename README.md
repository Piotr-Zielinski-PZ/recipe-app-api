# recipe-app-api
Recipe app api source code.

## Adding a new SSH key to your GitHub account
>*Here's a [website](https://docs.github.com/en/enterprise-server@3.0/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to a simple guide*

#### Using GitHub.com
1. Copy the SSH public key to your clipboard.


>Note: *If your SSH public key file has a different name than the example code, modify the filename to match your current setup. When copying your key, don't add any newlines or whitespace.*


```bash
$ cat ~/.ssh/id_ed25519.pub
# Then select and copy the contents of the id_ed25519.pub file
# displayed in the terminal to your clipboard
```
2. In the upper-right corner of any page, click your profile photo, then click Settings.

3. In the user settings sidebar, click SSH and GPG keys.

4. Click New SSH key or Add SSH key.

5. In the "Title" field, add a descriptive label for the new key. For example, if you're using a personal Mac, you might call this key "Personal MacBook Air".

6. Paste your key into the "Key" field.

7. Click Add SSH key.

8. If prompted, confirm your GitHub Enterprise Server password.

#### Using GitHub CLI
1. To add an SSH key to your GitHub account, use the ssh-key add subcommand, specifying your public key.

``` bash
gh ssh-key add key-file
```

2. To include a title for the new key, use the -t or --title flag.

``` bash
gh ssh-key add key-file --title "personal laptop"
```

## Starting GitHub project

>Note: *Note that before starting a new project the SSH connection between GitHub and your computer have to be set*

1. Start by heading over to [GitHub](github.com) and just click on **new** button which takes you to the page that allows you to create a new repository.

2. Customize your repository:
- Give your repository the name.
- Give it the description.
- You can choose to initialize your project with **README** file.
- Check the *gitignore* file and choose **Python**.
- For the license you can choose a *MIT license*.

3. When you're done click *create repository* and what this will do is create a repository and take you to the repository page.

4. Once you're on the repository page click on *code* and then click a copy icon to copy the SSH link of the repository URL to your clipboard.

5. Launch terminal, move to your project's folder and type

``` bash
git clone <YOUR REPOSITORY SSH URL>
```

## Adding Dockerfile
>Note: *A docker file is simply a file that contains a list of instructions for Docker to build a Docker image. So you basically we describe here all the dependencies that we need for our project in our Docker file.*

1. Create a new file in our project's root directory called *Dockerfile*.

- *FROM python:3.7-alpine* - the image that we're going to inherit our Docker file from. In this case we're going to create our Docker file from the python 3.7 image. The one we're going to use is the 3.7 Alpine image and it's basically a lightweight version of Docker. So pretty much Alpine runs Python 3.7.

>Note: *So with Docker we can basically build images on top of other images. The benefit of this is that we can find an image that has pretty much everything that we need for our project and then we can just add the customized bits that we need just for our specific product.*

- *MAINTAINER Piotr Zielinski* - this is optional but it's useful just to know who's maintaining this Docker image.

- *ENV PYTHONUNBUFFERED 1* - it tells Python to run in unbuffered mode which is recommended when running Python within Docker containers.

>Note: *The reason for this is that it doesn't allow Python to buffer the outputs. It just prints them directly. And this avoids some complications with the Docker image when we're running our python application.*

- Next we're going to install our dependencies:

>Note: *We're going to store our dependencies in a requirements.txt list which we're going to create later. We need to copy our requirements.txt file to requirements.txt. on the Docker image.*

  - *COPY ./requirements.txt /requirements.txt* - it copies from the neighboring directory to the Docker file - copies the requirements file that we're going to create here and copies it on the Docker image to /requirements.txt.
  - *RUN pip install -r /requirements.txt* - it takes the requirements file that we've just copied and it installs it using pip into the Docker image.

- Now we create a directory within our Docker image that we can use to store our application source code:
  - *RUN mkdir /app* - it creates a empty folder on our Docker image called **/app**.
  - *WORKDIR /app* - it switches to **/app** as the default directory. So any application we run using our Docker container will run starting from this location unless we specify otherwise.
  - *COPY ./app /app* - it copies from our local machine the **/app** folder to the **/app** followed that we've created on an image.

- Next we're going to create a user that is going to run our application using Docker:
  - *RUN adduser -D user* - it creates *user* with *-D* whitch means that the user will be only able to run applications.
  - *USER user* - it switches Docker to the *user* that we've just created.

>Note: *The reason why we do this is for security purposes. If we don't do this then the image will run our application using the root account which is not recommended because that means if somebody compromises our application they then have root access to the whole image. Whereas if we create a separate user just for our application then this limits the scope that an attacker would have in our documentation.*

2. Create a new file in our project's root directory called *requirements.txt*:

- *Django>=2.1.3,<2.2.0* - it installs Django's version equal to or higher than 2.1.3 but less than 2.2.0.
- *djangorestframework>=3.9.0<3.10.0* - it installs Django REST framework's version equal to or higher than 3.9.0 but less than 3.10.0.

3. Create a new folder in our project's root directory called *app*.

4. Open terminal and navigate to the project's directory, then type:

``` bash
docker build .
```
or, if it doesn't work:
``` bash
sudo docker build .
```

>Note: *It builds which ever **Dockerfile** is in the root of our project that we're currently in.*

## docker-compose configuration

>Note: *Docker compose is a tool that allows us to run our Docker image easily from our project location. So it allows us to easily manage the different services that make up our project. So for example one service might be the python application that we run. Another service might be the database.*

1. Create a new file in our project's root directory called *docker-compose.yml*:

>Note: *This is a yaml file that contains the configuration for all of the services that make up our project.*

- *version: "3"* -  version of Docker compose that we're going to be writing our file for.

- Next we define the services that make up our application. Right now we only need one service for our Python Django application:

``` yml
services:
  app:
    build:
      context: .
```
What this says is we're going to have a service called *app* and the build section of the configuration we're going to set the context to is *"."* which is our current directory that we're running docker-compose from.

``` yml
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
```
#### ports
In this part we're going to map our project from port 8000 on our host to port 8000 on our image.

#### volumes
Volume allows us to get the updates that we make to our project into our Docker image in real time. So it maps of volume from our local machine here into our Docker container that will be running our application. It maps the *app* directory which we have in our project to the *app* directory in our Docker image. This means that whenever we change a file or we change something in the project it'll be automatically updated in the container and we don't need to restart Docker to get the changes into effect.

#### command
This is the command that is used to run our application in our Docker container. It says "shell, run command, which is python manage.py runserver 0.0.0.0:8000". So this will run the Django development server available on all the IP addresses that run on the Docker container. It's going to run on port 8000 which is going to be mapped through the ports configuration to our local machine. So we can run our application and we can connect to it on port 8000 on our local machine.

2. Open terminal and navigate to the project's directory, then type:

``` bash
docker-compose build
```

What this does is it builds our image using the Dock compose configuration.
