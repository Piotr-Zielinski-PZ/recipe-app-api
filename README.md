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
This is the command that is used to run our application in our Docker container. It says "shell, run command, which is `python manage.py runserver 0.0.0.0:8000`". So this will run the Django development server available on all the IP addresses that run on the Docker container. It's going to run on port 8000 which is going to be mapped through the ports configuration to our local machine. So we can run our application and we can connect to it on port 8000 on our local machine.

2. Open terminal and navigate to the project's directory, then type:

``` bash
docker-compose build
```
or, if it doesn't work:
``` bash
sudo docker-compose build
```

What this does is it builds our image using the Dock compose configuration.

## Creating Django project using the Docker configuration

>Note: *We used Docker compose to run a command on our image that contains the Django dependency and that will create the project files that we need for our app.*

1. Open terminal and navigate to the project's directory, then type:

``` bash
docker-compose run app sh -c "django-admin.py startproject app ."
```
or, if it doesn't work:
``` bash
sudo docker-compose run app sh -c "django-admin.py startproject app ."
```

We run commands using docker-compose by typing `docker-compose run` and then the name of the service that we want to run the command on. This is if you have multiple services. Here we only have one service so we're just going to use our service called *app*.
We're going to run the command on *app* and then anything we pass in after is going to be the command that gets run on the Linux container that we've created using our Docker file.
We type `run sh -c` so it runs a shell script. We pass in a command in speech marks.

>Note: *The reason we use `sh -c` is because it makes it very clear to see the command that we're running versus all the Docker compose command.*

Finally the command `django-admin.py startproject app .` just runs the Django admin management command that comes when we install Django which we do via our **requirements.txt**. It runs the `startproject` command which starts a new project called *app* and using *"."* we say to start the project in our current location because this process is going to run on our Docker container. It's going to base it from the last **WORKDIR** that we set in our Dockerfile.

## Travis-CI

*Travis is a really useful continuous integration tool that lets us automate some of the tests and checks on our project every time we push it to Github. For example every time we push a change to GithHub we can make it run our Python unit tests and our Python linting so if there is any issues with our code we can see straight away via an email notification that the build is broken*

1. Firstly, enable Travis-CI for project:

- head over to [Travis-CI website](travis-ci.com),

- sign up or sign in with your GitHub account.

>Note: *if GitHub projects weren't automatically pulled over to Travis-CI use a guide shown on Travis-CI dashboard.*

2. Secondly, create Travis-CI configuration file:

*Configuration file is the file that tells Travis what to do every time we push a change to our project.*

- create a new file in our project's root directory called *.travis.yml*,

- the first line of our Travis file is what *language* Travis should expect our project to be in. Next we  specify the *version* of the language:

``` yml
language: python
python:
  - "3.6"
```

- next we're going to tell Travis what *services* we need to use. We're just need the Docker service and all of the subservices are going to be contained within our *docker-compose.yml* file and our *Dockerfile* configuration:

``` yml
services:
  - docker
```

- next we specify a *before_script* which is a script that Travis will run before it executes any of the automation commands that we're going to input next. So before it runs anything we need to install docker compose by typing:

``` yml
before_script: pip install docker-compose
```

- next we specify the script in which we're going to run our *docker-compose* command for running our tests:

``` yml
script:
  - docker-compose run app sh -c "python manage.py test && flake8"
```

We run our linting tool which we're going to install in our project. Linting tool is going to be called *flake8* so we're gonna run it every time we push a change to GitHub. Travis is going to spin up a Python server running Python 3.6 so it's going to make the docker service available. It's going to use pip to install docker-compose and then finally it's going to run our script and if this exits with a failure then it will fail the build and it will send us a notification.

3. Next, add *flake8* linting tool to **requirements.txt**:

>Note: *you can look up the latest version of *flake8* on pypi*.

- type *flake8>=3.6.0.<3.7.0* - it installs flake8's version equal to or higher than 3.6.0 but less than 3.7.0.

- next we add a *flake8* config and we do that in our Python project, which is *app* where we create new file called *.flake8*:
  - add *[flake8]* at the beginning of the file,
  - in next line we add some *exclusions* because we're going to exclude some of the automated scripts and tools that are created by Django (Django work to a 100 character limit whereas we will work with 79 character limit). We exclude all the Django stuff so it doesn't fail on the linting when we run our project.

  ``` flake8
  exclude =
    migrations,
    __pycache__,
    manage.py,
    settings.py
  ```

## Creating a simple unit test

1. First, create a file in *app* directory called *count.py* in which put a simple function, like so:

``` Python
def add(x, y):
    """Add two numbers together."""
    return x + y
```

2. Now create in the same folder a *tests.py* file in which we will be putting all our tests:

>Note: *The Django unit test framework looks for any files that begin with tests and it basically uses them as the tests when we run the Django run unit tests command. So we want to make sure that any tests are in a folder or a file name that begins with tests*.

- first thing we're gonna do in our *tests.py* is we're gonna import the Django **TestCase**,

>Note: *The TestCase is a class that comes with Django that basically has a bunch of helper functions that help us test our Django code*.

- next we're going to import the function that we're going to test,

- create a class called after the class that we want to test which will inherit from the TestCase,

- inside this class create a testing function which starts with *"test"*,

- inside our function we're going to use an assertion.

*So a test is setup of two components: the setup stage where we setup our function for tests and assertion stage where we actually test the output - we confirm that the output equals what we expected it to equal.*

Here's how *test.py* should looks like:
``` Python
from django.test import TestCase
from app.count import add


class CountTests(TestCase):
    """Testing calculation."""

    def test_add_numbers(self):
        """Test that two numbers are added together."""
        self.assertEqual(add(3, 8), 11)
```

- launch up terminal, go to *app* directory and type `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"`.

## Creating a core app and setting up models.py

#### Preparing the environment

The first thing we're going to do is we're going to create a **core** app which will hold all of the central code that is important to the rest of the sub apps. It's going to create anything that is shared between one or more apps like migrations, database. We will put this all in the **core** module just so it's all in one place and it's very clear where the kind of central point of all these things is.

1. Delete *count.py* and *tests.py*.

2. Launch up a terminal and type `docker-compose run app sh -c "python manage.py startapp core"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py startapp core"`.

3. Inside *core* app folder delete *views.py* and *tests.py*.

4. Create a *tests* folder inside *core* app folder and create there *__init\__.py* file.

5. Go to the *settings.py* and add *core* to the **INSTALLED_APPS** list.

Now that we have our *core app* we'll create our custom user model. Since we're working with test-driven development we're going to write our test first and then we're going to implement our model afterwards.

#### Creating model tests

##### Testing creating new user when the email is successful

1. First, go into our *tests* folder and create a new file called *test_models.py*.

We'll be testing if our helper function for our model is able to create a new user. So we're going to use the *create_user_function* to create a user and then we're going to verify that the user has been created as expected.

2. Inside, import *TestCase* class and *get_user_model*:

``` Python
from django.test import TestCase
from django.contrib.auth import get_user_model
```

3. Create test class called *ModelTests*. Next, inside this test class we're going to create our test case which is function called *test_create_user_with_email_successful*.

4. Now let's set up our test so what we're gonna do is we're simply going to pass in a email address and a password and then we're going to verify that that user has been created and that the email address is correct and the password is correct.

``` Python
def test_create_user_with_email_successful(self):
    """Test creating new user when the email is successful."""
    email = 'test00@outlook.com'
    password = '12345678'
    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
```

We're calling the *create_user* function on the *UserManager* for our user model that we're going to create in a next step.

We also want to make sure that the email address in our created user equals the email address we passed in. We can't check the password the same way like we did checking an email. This is because the password is encrypted so we can only check it using the *check_password* function on our user model.

5. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command. We expect this test to fail because we haven't created the feature yet.

###### Next proceed creating **create_user** method in **UserManager** class.

##### Testing if the email for new user is normalized

Now that we have our *create_user* function we can add a new feature to the function to normalize the email address that the users sign up with. It's not a required step but it is recommended because the second part of the user domain name for email addresses should be case-insensitive. We're going to make that part all lowercase every time a new user registers.

1. Inside *ModelTests* class in *test_models.py* add new function called *test_new_user_email_normalized*.

2. Inside this function create an email variable all uppercase for the domain part.

3. Below, let's create our user and for the password we're just gonna add a random string.

4. Next let's use an assertion:

``` Python
self.assertEqual(user.email, email.lower())
```

so whole test function should looks like this:

``` Python
def test_new_user_email_normalized(self):
      """Test the email for new user is normalized."""
      email = 'test@OUTLOOK.COM'
      user = get_user_model().objects.create_user(email, 'test123')

      self.assertEqual(user.email, email.lower())
```

5. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed updating **create_user** method in **UserManager** class.

##### Testing creating user with no email raises error

Next we're going to add validation to ensure that an *email* field has actually been provided when the *create_user* function is called. We want to make sure that if we call the create_user function and we don't pass an email address (so if we just pass a blank string or we just pass a non value) we want to make sure we raise a *ValueError* that says the email address was not provided.

1. Inside *ModelTests* class in *test_models.py* add new function called *test_new_user_invalid_email*.

2. Type:

``` Python
with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'test123')
```

Anything that we run in here should raise the value error. And if it doesn't raise a *ValueError* then this test will fail.

3. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed updating **create_user** method in **UserManager** class.

##### Testing creating new superuser

Now that we have our *create_user* function finished there's just one more function that we need to add to our user model manager and that is the *create_superuser* function. *create_superuser* is a function used by the Django CLI when we're creating new users using the command line. So we want to make sure it's included in our custom *User* model so that we can take advantage of the Django management command for creating a superuser.
We are going to test test that a superuser is created when we call *create_superuser* and that it is assigned the **is_staff** and the **is_superuser** settings.

1. Inside *ModelTests* class in *test_models.py* add new function called *test_create_new_superuser*.

2. Below this let's create our user with `user = get_user_model().objects.create_superuser()` and inside *create_superuser* pass an email address and password.

3. Next let's take care of assertion, so let's type:

``` Python
self.assertTrue(user.is_superuser)
self.assertTrue(user.is_staff)
```

The reason why we didn't add *is_superuser* field in our *User* model but we add it here is *is_superuser* is included as part of the *PermissionsMixin*.

Final code should looks like this:

``` Python
def test_create_new_superuser(self):
      """Test creating new superuser."""
      user = get_user_model().objects.create_superuser(
          'test@outlook.com',
          'test123'
      )

      self.assertTrue(user.is_superuser)
      self.assertTrue(user.is_staff)
```

3. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed creating **create_superuser** method in **UserManager** class.

#### Creating models

##### Creating **create_user** method in **UserManager** class

When we call *create_user* it'll create a new user model, it'll set the password and it'll save the model and then it'll return the user model that it has just created.


1. Alright so load up the models.py and import the *AbstractBaseUser* the *BaseUserManager* and the *PermissionsMixin*.

``` Python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
```

2. Next we create our *UserManager* class. The manager class is a class that provides the helper functions for creating a **user** or creating a **superuser**.

So let's type class *UserManager* and let's extend the *BaseUserManager* - we're going to pull in all of the features that come with the *BaseUserManager* but we're going to override a couple of the functions to handle our email address instead of the username that this class expects:

``` Python
class UserManager(BaseUserManager):
    """Manage creating new users."""
```

3. Now lets create function *create_user* and the first argument is *self*, the second - *email*, third - *password=None* in case you want to create a user that is not active that doesn't have a password and the last argument will be _**extra_fields_.

>Note: *any of the extra functions that are passed in when we call the create_user will be passed into extra fields so that we can then just add any additional fields that we create without user model*.

4. Now, below our *create_user* definition let's create our user so let's type

``` Python
user = self.model(email = email, **extra_fields)
```

It's going to pass the email first and then it's going to pass anything extra that we add.

>Note: *The way the management commands work is we can access the model that the manager is for by typing "self.model". This is effectively the same as creating a new user model and assigning it to the user variable*.

5. Below this we are going to set the password. We can't set the password in this call because the password has to be encrypted. It's very important that the password is not stored in clear text. We do that by using the *set_password* helper function that comes with the Django *BaseUserManager* or the *AbstractBaseUser*.

6. Next we're going to save the user so we're going to type *user.save()* and we're also use *using=self.db*. It's required to support multiple databases. Then finally we're going to return the user.

Finally, our code should looks like:

``` Python
class UserManager(BaseUserManager):
    """Manage creating new users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save new user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
```

So now we have the manager class let's go ahead and create our *User* model.

##### Creating *User* model.

1. Create *User* class and extend it by the *AbstractBaseUser* and the *PermissionsMixin*.

It basically gives us all the features that come out of the box with the Django *User model* but we can then build on top of them and customize it to support our email address.

2. Now we define the fields of our database model:

``` Python
email = models.EmailField(max_length=255, unique=True)
name = models.CharField(max_length=255)
is_active = models.BooleanField(default=True)
is_staff = models.BooleanField(default=False)
```

3. Next we're going to assign the user manager to the objects attribute:

``` Python
objects = UserManager()
```

4. And then finally we're going to add the `USERNAME_FIELD = email` so by default the *username* field is *"username"* and we're customizing that to *"email"*.

5. Next we will move on to our *settings.py* and we will customize our user model in here. Scroll down and type:

``` Python
AUTH_USER_MODEL = 'core.User'
```

So *core* is the name of our app and *User* is the name of the model in our app that we want to assign as the custom user model.

6. Head back to the terminal and make migrations using `docker-compose run app sh -c "python manage.py makemigrations"` and then `docker-compose run app sh -c "python manage.py migrate"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py makemigrations"` and then `sudo docker-compose run app sh -c "python manage.py migrate"`.

7. So now we have our migrations we can run our tests again using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

##### Updating **create_user** method in **UserManager** class (normalizing error)

All we need to do for this is wrap our email with the normalized email function.

1. We simply replace this line:

``` Python
user = self.model(email=email, **extra_fields)
```

with this line:

``` Python
user = self.model(email=self.normalize_email(email), **extra_fields)
```

*normalize_email* is a helper function that comes with the *BaseUserManager*.

2. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

##### Updating **create_user** method in **UserManager** class (rising ValueError)

1. To implement this feature in our models go to the *create_user* method and between creating user object and the doc-string type:

``` Python
if not email:
      raise ValueError('Users must have an email address!')
```

We raise a *ValueError* and pass there a message.

2. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

##### Creating **create_superuser** method in **UserManager** class

1. Inside *UserManager* class create *create_superuser* method.

2. Defining this method let's pass in *self*, *email* and *password*. Because we're only really going to be using the *create_superuser* with the command-line we don't need to worry about the extra fields.

3. Below this let's create our user using our create_user function so we type:

``` Python
user = self.create_user(email, password)
```

4. At this point we have a user the same as the user that is created using *create_user* method so next we need to give him extra privileges:

``` Python
user.is_staff = True
user.is_superuser = True
```

5. Then because we modified the user we need to save it and then finally we return the user so the final code should looks like:

``` Python
def create_superuser(self, email, password):
      """Create and save new superuser."""
      user = self.create_user(email, password)
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)

      return user
```

6. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

## Setting up admin.py

#### Creating admin tests

We're going to update our Django admin so that we can manage our custom user model. This will give us a nice easy interface that we can use to log in and see which users have been created, create users ourselves or make changes to existing users. So as with anything with test-driven development we're going to start by adding the tests.

##### Testing admin

1. Let's go to our project and in the *tests* folder let's add a new file called *test_admin.py* - this is where we're going to store all of our admin page unit tests.

2. Start by adding a few imports inside *test_admin.py* file:

``` Python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
```

**reverse** is a helper function which allows us to generate URLs for our Django admin page.
**Client** allows us to make test requests to our application in our unit tests.

3. Create a test class called *AdminSiteTests* and we're going to inherit from *TestCase*.

4. Then, the first thing we're going to do is we're going to create a *setUp* function. *setUp* function is ran before every test that we run. Sometimes there are setup tasks that have to be done before every test in our *TestCase* class. Our setup is going to consist of creating our test client. We're going to add a new user that we can use in tests. We're going to make sure the user is logged in and finally we're going to create a regular user that is not authenticated so we can use him to list him in our admin page.

- `self.client = Client()` - makes a *client* variable accessible for other tests,

- `self.admin_user = get_user_model().objects.create_superuser()` - creates *admin_user* object,

- `self.client.force_login(self.admin_user)` - uses the *client* helper function that allows us to log a user in with the Django authentication,

>Note: *This really helps make our tests a lot easier to write because it means we don't have to manually log the user in we can just use this helper function*.

- `self.user = get_user_model().objects.create_user()` - creates *user* object.

Okay so now we have a *client* and *admin*, the *admin* is logged into the *client* and we have a spare *user* that we can use for testing listing and things like that.
Now let's create our first test - test that the users are listed in our Django admin. The reason we need to add a test for this is because we need to slightly customize the Django admin to work with our custom user model. As explained previously the default *User* model expects a *username* and as such the default Django *admin* for the *User* model also expects a *username* which we don't have. We just have the email address so we need to make a few small changes to our *admin.py* file just to make sure it supports our *custom user* model.

1. Define new function inside *AdminSiteTests* class called *test_users_listed*.

2. Create the URL using the *reverse* helper function so it will generate the URL for our list user page. The reason we use reverse function instead of just typing the URL manually is because if we ever want to change the URL in a future it means we don't have to go through and change it everywhere in our test because it should update automatically based on reverse.

>Note: *to use reverse function we simply type the app that we're going for, ":" and the URL that we want*.

3. `res = self.client.get(url)` - this will use our test *client* to perform a **HTTP GET** on the URL that we put inside the brackets.

4. Finally, let's run some assertions:

``` Python
self.assertContains(res, self.user.name)
self.assertContains(res, self.user.email)
```

The *AssertContains* assertion is a Django custom assertion that will check that our response (*res*) contains a certain item (*self.user.name*).
*AssertContains* also has some additional checks that it does that are not quite clear from just these lines. It checks that the **HTTP response** was *HTTP 200*. It looks into the actual content of this response (*res*) and that's because if we manually output this response (*res*) it's just an object. *AssertContains* is intelligent enough to look into the actual output that is rendered and checks for the contents there.

Finally, the *test_admin.py* should looks like:

``` Python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Test admin site."""

    def setUp(self):
        """Set up test environment."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@outlook.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@outlook.com',
            password='test1234',
            name='test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
```

5. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed modifying admin.

We're going to update our Django admin to support changing our *user* model because there's still a few changes that we need to make to our Django admin class to support our custom user model. The *Edit* Page won't work in its current state. We're going to make some changes to make sure that it does work.

1. Let's start by adding a test to *test_admin.py*; we're going to test that the *change page* renders correctly.

>Note: *We don't actually need to test making posts and things like that to the change page because this is all part of the Django admin module and it's not recommended to test the dependencies of your project*.

2. Create a new test called *test_user_change_page*.

3. Generate a **URL** so `url = reverse('admin:core_user_change')` and this time we need to give it an argument - *self.user.id*. The reverse function will create a URL like this: *admin/core/user/7*.

>Note: *Basically anything we pass as the second argument of reverse function will get assigned to the arguments of the URL at the end so that's how we customize the ID*.

4. Type *res = self.client.get(url)* - so we're going to do an **HTTP GET** on the URL.

5. Now, let's do some assertions:

``` Python
self.assertEqual(res.status_code, 200)
```

We test here if a *status code* for the **response** that our client gives is *HTTP 200* which is the status code for *"okay"* so that means the page worked.

6. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed modifying admin (change site).

There's one last thing we need to change in our Django admin before it will work with our custom user model and that is the **ADD page**. This is the page for adding new users in the Django admin.

1. Head over to *test_admin.py* and let's add a new test called *test_create_user_page* with self parameter.

2. Create the URLs - `url = reverse('admin:core_user_add')`.

3. Below type `res = self.client.get(url)` so our test client is going to make a *HTTP GET* to this URL.

4. Then just assert that the *status code* is 200, so type `self.assertEqual(res.status_code, 200)`.

5. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

###### Next proceed modifying admin (add site).

#### Modifying admin

1. Let's go over to our *admin.py* file.

2. Let's make some imports:

``` Python
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
```

3. Create class called *UserAdmin* and we're going to inherit from *BaseUserAdmin*.

4. We need to change the *ordering* so we will set it to the *ID* of the object.

5. The *list_display* we will set to the *email* and the *name* so we're going to list them by email and name.

6. Now all we need to do is register our models.

Finally, *admin.py* should looks like:

``` Python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """Modifies user admin site."""

    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
```

7. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

>Note: *we can't test the Django admin just yet because we still have to set up our database*.

##### Modifying admin (change site)

To implement changing our user model via admin site, therefore to access the *Edit* page we're going to add a *fieldsets* class variable.

First we need to import the *gettext* function. This is the recommended convention for converting strings in our Python to human readable text and the reason we do this is just so it gets passed through the translation engine.

To import **gettext** function type:

``` Python
from django.utils.translation import gettext as _
```

*fieldsets* variable:

``` Python
fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (_('Personal Info'), {'fields': ('name', )}),
    (
        _('Permissions'),
        {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }
    ),
    (_('Important dates'), {'fields': ('last_login', )})
)
```

Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

##### Modifying admin (add site)

After running tests we can head over to our *admin.py* and we add the *add_fieldsets* class variable. This is from the Django admin documentation - the user admin, by default, takes an *add_fieldsets* which defines the fields that we include on the **add page** which is the same as the **create user page**. We're going to customize this *fieldset* to include our email address, password and password 2. With that we can create a new user in the system with a very minimal data. Then if we want to add extra fields like the name and customize that stuff later we can do that in the **edit Page**.

*add_fieldsets* variable:

``` Python
add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('password1', 'password2')
      }),
  )
```

Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

## Setting up database

We're going to set up our Django project to use *Postgres* instead of the default *sqlite* database.

1. Start by making some changes to our *docker-compose.yml* file. That allows us to create a database service and also pass in some database settings into both our app and the database that we're going to run. Let's start by adding the database service, so in *services* add new service called *db*:

``` yml
db:
  image: postgers:10-alpine
  environment:
    - POSTGRES_DB=app
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=supersecretpassword
```

- `image: postgers:10-alpine` this locates the *Postgres* image on docker hub and it pulls down the version with the tag 10 alpine,

- below, we're going to set *environment* variables. If we look on docker hub at the *Postgres* image  we can see all of the available configuration options which can be passed in as environment variables. We're going to set up environment variables for the database: name, the username and the password that is created when our database service starts.

>Note: *We wouldn't use the same password in POSTGRES_PASSWORD variable that we would use on a production system. What we would do in production is on our build server or whatever is building our application like Jenkins or Travis we would then add an encrypted environment variable that overrides this when we push our application. We're just going to use this "supersecretpassword" password for running the server locally for our development server*.

2. Now that we've created our DB service we will modify our *app* service to set some environment variables and also depend on our *db* service:

- we're going to start by adding some *environment* variables to our app. We're going to add *DB_HOST* which needs to equal the name of the service that runs our database and that's going to be *db*,

- next we're going to type *DB_NAME* and that needs to equal our *Postgres DB* so that's going to be *app*,

- next we type our *DB_USER* and this is our user name here which is *Postgres*,

- finally we do *DB_PASS* which is the password that we create here - *supersecretpassword*,

>Note: When we run *docker-compose.yml* we can set different services to depend on other services. So we want our **app** service to depend on the **db** service that we've just created. It means two things:
- the database service will start before the app service,
- the database service will be available via the network when we use the hostname *db*.
So when we're inside our **app** service we can connect to the hostname *db* and then it will connect to whatever container is running on our *db* service.

- below our *environment* level with the *environment* setting we're going to add a *depends_on* and below that we're going to add *db* (it's just a single list item of db).

So finally we should update our *app* service with that:

``` yml
environment:
  - DB_HOST=db
  - DB_NAME=app
  - DB_USER=postgres
  - DB_PASS=supersecretpassword
depends_on:
  - db
```

and create new *db* service:

``` yml
db:
  image: postgers:10-alpine
  environment:
    - POSTGRES_DB=app
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=supersecretpassword
```

3. Next we're going to add *Postgres* support to our *Dockerfile*. We basically need to install the Python package that is used for Django to communicate with Docker and in order to do this we're going to have to add some dependencies to our *Dockerfile* during the build process. We need to update our *requirements.txt* file to add the necessary package and then we need to make some small changes to our *Dockerfile* to add the dependencies required to install these packages:

- open our *requirements.txt* file,

- the package that Django recommends for communicating between Django and *Postgres* is called **psycopg2** and we will use versions between 2.7.5 and 2.8.0, so type `psycopg2>=2.7.5,<2.8.0`,

>Note: *if we try to build this now it wouldn't work because there's some dependencies that are required in order to install this package on any system*.

- head over to the *Dockerfile* and add a new line in between the *COPY requirements* and the *RUN install requirements* and type `RUN apk add --update --no-cache postgresql-client`. With this we're going to install the PostgreSQL client.

This command uses the package manager that comes with Alpine. It says "**run** the package manager, which is **apk** and **add** a package but before that **update** the registry and don't store the registry index (**no cache**) on our *Dockerfile*". The reason we do this is because we really want to minimize the number of extra files and packages that are included in our Docker container.

- now we will install some temporary packages that need to be installed on the system while we run our requirements and then we can remove them after the requirements has run.

`RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev` -  option called *virtual* sets up an alias for our dependencies that we can use to easily remove all those dependencies later so our alias is going to be called `.tmp-build-deps`, then we list out all of the temporary dependencies that are required for installing our Python dependencies. So one of them is *gcc* another one is *libc-dev* another one is *linux-headers* and finally *postgresql-dev*.

>Note: *we want to minimize the number of extra files and packages that are included in our docker container. This is best practice because it means that our docker container for our application has the smallest footprint possible and it also means that we don't include any extra dependencies or anything on our system which may cause unexpected side effects or it may even create security vulnerabilities in our system*.

- now that the temporary requirements are installed we run `RUN pip install -r /requirements.txt` line  which will install our requirements. And below that we add a line that deletes the temporary requirements which we do by typing `RUN apk del .tmp-build-deps`,

- head over to our terminal and let's type `docker-compose build` or, if it doesn't work `sudo docker-compose build` just to make sure that our image can build successfully.

4. Now we have to configure our Django project to use our *Postgres* database:

- head over to the *settings.py*,

- locate our database configuration,

- delete all default options for *sqlite* database and keep the default part of the dictionary in which type:

``` Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}
```
The first line is the database engine that we're going to use, so the engine is going to be the *postgresql* engine.
Below, we add the host value, the database name, the username and the password and we pull in from environment variables. And the way we pull it in as an environment variable is we type *os.environ.get()* and inside the name of the environment variable from *docker-compose.yml* file.

>Note: *the benefit of this solution is that we can easily change our configuration when we run our app on different servers by simply changing them in the environment variables. We don't have to make any changes to our source code in order to modify the hostname, the name, the username or the password. This makes it really useful when running our application in production because we can simply upload our Dockerfile to a service like Amazon ECS or kubernetes and we can just set the appropriate environment variables and then our application should work*.

## Waiting for Postgres

#### Mocking

**Mocking** is an advanced area of testing. **Mocking** is when we override or change the behavior of the dependencies of the code that we're testing. We use **mocking** to avoid any unintended side effects and also to isolate the specific piece of code that we want to test.

**Example**
Imagine we're testing a function that sends an email.
There are two good reasons that we wouldn't want to actually send an email every time we run our tests:

- we should never write tests that depend on external services. This is because we can't guarantee that these services will be available at the point that we run the test and this would make the test unpredictable and unreliable,

- we don't want to be sending spam emails each time we run our test.

When we write our test we can use **mocking** to avoid sending an actual email. We can override the function in the dependency that sends the email and replace it with a *mock object*. Using this *mock object* we can avoid sending an actual email and instead just check that the function was called with the correct parameters.

#### Test wait_for_db

We're going add a **management command** to the *core* app of our Django project. The **management command** is going to be a helper command that allows us to wait for the database to be available before continuing and running other commands. We're going to use this command in our *docker-compose* file when starting our Django app. The reason that we need this command is because once the *Postgres* service has started there are a few extra setup tasks that need to be done on the *Postgres* before it is ready to accept connections. It means that our Django app will try and connect to our database before the database is ready and therefore it will fail with an exception.

>Note: *To improve the reliability of our project we're going to add this helper command that we can put in front of all of the commands we've run in docker compose and that will ensure that the database is up and ready to accept connections before we try to access the database*.

1. We're going to start by creating the unit test for our **command** which we will create in our *core -> tests* folder. Inside, create a new file called *test_commands.py*.

2. The first thing we're going to *import* is the **patch function** from the *unittests.mock* module.

This is going to allow us to *mock* the behavior of the Django *get_database* function. We can basically simulate the database being available and not being available when we test our command.

3. Below, we're going to add the *call_command* function which would allow us to call the command in our source code.

4. Next we're going to *import* the **OperationalError** that Django throws when the database is unavailable. And we're going to use this error to simulate the database being available or not when we run our command.

5. Finally *import* **TestCase**.

6. The first function we're going to create is simply going to test what happens when we call our command and the database is already available:

- define function called *test_wait_for_db_ready*.

To setup our test here we need to simulate the behavior of Django when the **database** is *available*. Our **management command** is going to *try and retrieve* the database connection from Django and it's going to check if (when we try and retrieve it) it retrieves an *OperationalError* or not. So basically if it retrieves an *OperationalError* then the database is not available. If an *OperationalError* is not thrown, then the database is available and the command will continue.

- to setup our test we're going to override the behavior of the **ConnectionHandler** and we're just going to make it *return True* and not throw any exception. Therefore our *call_command* or our *management commands* should just continue and allow us to continue with the execution flow. Let's use the **patch** to *mock* the **ConnectionHandler** to just *return True* every time it's called,

- `django.db.utils.ConnectionHandler` is the location of the code that is being called and the function that is actually called when we retrieve the database is **\__getitem__**. We're going to *mock* the behavior of **\__getitem__** using the *patch* which is assigned as a variable here *gi*,

- the way we *mock* the behavior of a function is we type `gi.return_value = True`. This means that whenever this is called during our test execution it will override it and just replace it with a *mock object* which does two things:
  - one of them is it will just return this value which is *True*,
  - the second thing is it allows us to monitor how many times it was called.

- type *call_command('wait_for_db')* so the *wait_for_db* is going to be the name of the management command that we create,

- now, we can do the **assertions** of our test. We're going to check if **\__getitem__** was called once. So the way that we check that using our **mock object** is we type `self.assertEqual(gi.call_count, 1)`.

>Note: *__return_value__ in __call_count__ are all options that we can set on a mock object*.

7. The second test checks that the *wait_for_db* command will try the database five times and then on the sixth time it'll be successful and it will continue:

- define function called *test_wait_for_db*.

The way it's going to work is it's going to be a *while loop* that checks if the **ConnectionHandler** raises the *OperationalError* and if it does, it'll raise the *OperationalError* then it's going to wait a second and then try again.

That delay is just to make sure that it doesn't flood the output by trying every microsecond to test for the database - it adds a little delay. We can actually remove that delay in our unit test by using decorators.

- above function definition type `@patch('time.sleep', return_value=True)`. We add a **patch decorator** to our function and we're going to mock the *time.sleep*. When we use *patch* as a *decorator* we can  pass in the *return_value*. What it does is it's pretty much exactly the same thing as we've done in the *test_wait_for_db_ready* function, except we put it above the test that we're running. This decorator passes in what is the equivalent of *gi* from the *test_wait_for_db_ready* function. But for this to work we need to add the extra argument to the *function declaration* which is **ts** even though we're not using it we still need to pass it in because while running the test it will error because it'll have an unexpected argument. What this mock does is it replaces the behavior of *time.sleep* and just replaces it with a **mock function** that *returns True*. So that means during our test it won't actually wait the second. The reason we do this is simply just to speed up the test,

- next type `with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:` to mock the behavior of the *\__getitem__* and inside type:
  - `gi.side_effect = [OperationalError] * 5 + [True]` to add the *side-effect* to the function that we're mocking. This *side-effect* is going to raise the *OperationalError* five times and then on the sixth time it's not going to raise the error and then the call should complete, it will just return.
  - now we call our command `call_command('wait_for_db')`,
  - assert that this function has been called six times using `self.assertEqual(gi.call_count, 6)`.

8. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

#### Add wait_for_db command

1. To create our *wait_for_db* management command we're going to start by creating the directory in our **core** app that we are going to store our management commands. So inside *core* app folder create *management* folder and inside this create *commands* folder and *\__init__.py* file and inside *commands* folder create another *\__init__.py* file and finally *wait_for_db.py*

>Note: *This __init__.py file let's Django know that this folder a Python module*.  

2. Start by importing **time** module so we can use it to make our applications sleep for a few seconds in between each database check. Let's also import the **connections** module which we can use to test if the database connection is available. Next we're going to import the **OperationalError** that Django will throw if the database isn't available. Finally we're going to import **BaseCommand** which is the class that we need to build on in order to create our custom command.

3. Let's create command class and following convention let's name it *Command* and it will inherit from **BaseCommand** class.

4. Create function called *handle*, so the *handle* function is what is ran whenever we run this management command. The arguments for *handle* are **self** and then **\*args** and then **\**options**.

>Note: *args and options allow us passing in custom arguments and options to our management commands so if we wanted to let's say customize the wait time or something we could do that as an option*.

We're going to check if the database's available and then once it's available we're going to cleanly exit so that whichever command we want to run next we can run knowing that the database is ready.

5. Next we can actually print things out to the screen during these management commands using `self.stdout.write` and then in the brackets we can write a message to be shown on the screen, like "Waiting for database...".

6. Next we're going to assign a variable called *db_conn* (which is short for database connection) to *None*.

7. In next step we create while loop:

``` Python
while not db_conn:
        try:
            db_conn = connections['default']
        except OperationalError:
            self.stdout.write('Database unavailable, waiting 1 second')
            time.sleep(1)
```

So what this does is while **database connection** (*db_conn*) equals *False* try to set up the **database connection**. If it tried and it set it to the *connection* and the *connection* is unavailable then Django raises the **OperationalError**. So if Django raises the **OperationalError**  we're going to catch that and we're going to output the message "*Database unavailable, waiting 1 second*". Next we're going to sleep for one second. So it just basically pauses the execution for a second and then it will try again and start from the beginning. It will continue this process until the database is finally available in which case this code won't be called and it will just exit.

8. We're going to add one more thing to our function which is just a final message. Type:

`self.stdout.write(self.style.SUCCESS('Database available!'))`

We can wrap our message it in a *success style* which will output the message in a green color just to indicate that the output was successful.

9. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

#### Make docker-compose wait for database

We can now configure *docker-compose* to use the *wait_for_db* command before it starts our Django app.

1. Heading over to the *docker-compose* file.

2. Go to our **app** service and inside **command** block add the *wait_for_db* command and we call it using the **manage.py**. So let's type:

``` yml
command: >
  sh -c "python manage.py wait_for_db &&
          python manage.py migrate &&
          python manage.py runserver 0.0.0.0:8000"
```

We're adding one more command before the service starts and that is the **migrate** command. This will run our database migrations on our database so it will create any tables that are required for our app.

3. Go to terminal and type `docker-compose up`.

#### Solving problem with Travis CI not waiting for database

###### Error:

```
django.db.utils.OperationalError: could not connect to server: Connection refused
556	Is the server running on host "db" (172.18.0.2) and accepting
557	TCP/IP connections on port 5432?
558
559ERROR: 1
560The command "docker-compose run app sh -c "python manage.py test && flake8"" exited with 1.
```

###### Solution:

To solve the problem, update your *.travis-ci.yml* file so the **script:** command is:
`- docker-compose run app sh -c "python manage.py wait_for_db && python manage.py test && flake8"`

#### Creating admin account

To create admin account simply head over to your terminal and type `docker-compose run app sh -c "python manage.py createsuperuser"` and this should start a new process in Docker. Fill in the required fields and you can now head over to admin panel.

## Create user management endpoints

In this section we're going to create our **manage user endpoints**. These **endpoints** are going to allow us to *create users*, to *update users*, to *change a user's password* and to *create user authentication tokens* which can be used to authenticate requests to the other APIs in our project.

#### Create user app

1. Load up the terminal and navigate to **app** folder. Then type `docker-compose run --rm app sh -c "python manage.py startapp users"` (or if it doesn't work use superuser credentials).

>Note: *__--rm__ removes the container after running the command. We can include this optionally on any commands that we want to run once so the docker container doesn't slow down the system after it's ran. So basically if we add the __--rm__ command it should remove the container and just keep the system a little cleaner so it doesn't fill up*.

2. Once the *users* app is started we're just going to do some cleanup:

- remove *migrations.py* because we're going to keep all of them within the **core** app,

- remove the *admin.py* because we're also going to keep them in the **core** app,

- remove the *models.py* because, again, they're in the **core** app,

- finally remove *tests.py* because we're going to create a new subfolder for tests,

- create a new *\__init__.py* file inside *test* folder like so: *tests/\__init__.py*.

3. Open up our app *settings.py* and inside **INSTALLED_APPS**, above the *core* app add Django *rest_framework*. Below that enable the *authtoken* app as well which we are going to be using to authenticate with Django *rest_framework* later. So below *rest_framework* type *rest_framework.authtoken*. Then, finally, below the *core* app enable our **users** app.

#### Add tests for create user API

The first API that we're going to create in our **users** project is the *create users API* so we're going to start by adding some unit tests to *test creating users* and different scenarios when we give different post requests.

1. Inside our *users* app go to *tests* folder and create *test_user_api.py* test file.

2. Start by importing:

- *TestCase*,

- *get_user_model* because we're going to be needing the user model for out tests,

- *reverse* so we can generate our API URLs,

Then we're going to import some rest framework test helper tools:

- *APIClient* a test client that we can use to make requests to our API and then check what the response is,

- *status* this is a module that contains some status codes that we can see in human readable form so instead of just typing **200** it's **HTTP_200_OK**... it just makes the tests a little bit easier to read and understand.

3. It's good practice at the beginning of any API test to create either a *helper function* or a *constant variable* for our URL that we're going to be testing. We'll be testing the *create user URL* so let's create a variable for that called *CREATE_USER_URL*.

>Note: *we call this variable in all caps, because it's just a naming convention for anything we expect to be a constant. With Python it doesn't matter whether this is uppercase or lowercase we're still going to be able to change the value. This is just to understand that we don't expect this value to change during our tests*.

By typing `CREATE_USER_URL = reverse('user:create')` we're going to use *reverse* to reverse our *user create URL* and this should create the *user create* URL and assign it to **CREATE_USER_URL** variable.

4. Add a helper function that we can use to *create* an *example users* for our tests.

>Note: *We create a helper function for anything that we do multiple times in different tests so instead of creating the user for each test individually we can just call the helper function and it just makes it a little bit easier to create users that we're testing with*.

Our function is going to be called *create_user* so let's type `def create_user` and in the arguments add the __**params__ so this is a dynamic list of arguments. We can basically add as many arguments as we want. Then we can pass them directly into the *create_user* function inside the **UserManager** model so we have a lot of flexibility about the fields that we can assign to the users that we create for our samples.

Next type: `return get_user_model().objects.create_user(**params)`.

**get_user_model()** will *retrieve the user model* so then the *objects.create_user()* with _**params_ passed in is just a function to create a user with these parameters. This solution makes the lines a little bit shorter because we're just creating users and we don't have to type all this out, we can just call create_user().

5. Now we can create our *test class* and the class we're going to create is called **PublicUserApiTests** and it's going to inherit from *TestCase*.

>Note: *the reason we call it __public__ is because we separate our API tests into public and private tests. It's just keeps the tests clean because then in our setup we can have one test that authenticates and one that doesn't authenticate:
 - public API is one that is unauthenticated so anyone from the Internet can make a request, for example "creating a user" because when we create a user on a system usually we're creating a user because you haven't got authentication set up already.
 - private API might be "modifying the user" or "change the password". For those types of requests we would expect to be authenticated*.

6. Inside **PublicUserApiTests** class we're going to add:

- **setUp** function in which we're going to type `self.client = APIClient()` and this is just to call our client in our test so every single test we run we don't need to manually create this API client, we just have one client for our test suite that we can reuse for all of the tests,

- **test_create_valid_user_success** to create a test that validates the user with its payload is created successfully:
  - **payload** is the object that we pass to the API when we make the *request*. We're going to test that if we pass in all the correct fields then the user is created successfully. So what we're going to need to create a user is the email, password and a name, so these are the fields in our *payload*,
  - next thing we're going to do is we're going to make our *request*. So we make our requests by typing `res = self.client.post()` and we pass inside the URL we specified previously so the *CREATE_USER_URL* and payload. This will do a *HTTP POST* request to our client, to our URL, for creating users,
  - to create *assertions* we need to ask ourselves a question "what do we expect from this?". Well the first thing is we expect a *HTTP_201_CREATED* response from the API so we type `self.assertEqual(res.status_code, status.HTTP_201_CREATED)`,
  - next we're going to test that the object is actually created so type `user = get_user_model().objects.get(**res.data)` so when we do a *HTTP POST* and *create a user* we expect to see the created user object that's returned in the API along with *HTTP_201_CREATED* status code. We do _**res.data_ to take the dictionary response (which should have an additional ID field) and we just pass it in as the parameters for the *GET*. Then, if this *GET*s the user successfully then we know that the user is actually being created properly,
  - now we can do `self.assertTrue` to test our password, so type: `self.assertTrue(user.check_password(payload['password']))`,
  - finally we want to check that the password is not returned as part of this object and we do that by doing `self.assertNotIn('password', res.data)` so we simply check if the password is in our request data.

- next we're going to test what happens if we try and create a user but the user already exists so we're trying to create duplicate user. To do that create a test function called *test_user_exists*:
  - **payload** we're going to give is an email and a password,
  - then we create our user using our handy *create_user* function and we pass in "unpacked" payload (using _**payload_). So _**payload_ will pass in email equals the email we specified inside our *payload*, password equals our password also from *payload*. Using __*__ just make our code a little less wordy so there's a few less characters there,
  - now we can make the request so we'll type `res = self.client.post(CREATE_USER_URL, payload)`, we also pass in the payload,
  - using **HTTP POST** in our *request* all we expect is a **HTTP_400_BAD_REQUEST**. This is a *bad request* because the user already exists, so we type `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

- before we implement our API there is one more test left, which is *test if the password is too short*. With this we're going to add a password restriction, because we want passwords to be over a certain limit we don't want them really short. For this we'll create a function to test that the password is more than 5 characters long. So let's create a test called *test_password_too_short*:
  - create a *payload* with an email, name and password but this time we'll give it a really short password, like "pw",
  - create a POST request for our *CREATE_USER_URL*, so let's type `res = self.client.post(CREATE_USER_URL, payload)`,
  - we want to first make sure that it returns a **HTTP_400_BAD_REQUEST**. So type `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`,
  - then let's check that the user was never created. To do that we simply create a user object: `user_exists = get_user_model().objects.filter(email=payload['email']).exists()`. We search for any user with email address from our *payload* using *filter()* and then we'll just do *.exists()*. So if the user exists it will return true otherwise it will return false. Therefore, next we'll use `self.assertFalse(user_exists)` so we expect that **user_exists** would be *False* because we don't want the user to exist.

>Note: *every single test that is run refreshes the database so every user that was created in each test is not going to be accessible in any other test; each test basically starts anew*.

7. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add create user API

Next we're going to implement our *create_user* API to make our tests pass. We're going to create a **serializer** for our *create_user request* and then we're going to create a **view** which will handle the request and then we're going to wire this up to a **URL** which will allow us to access the API and also make our tests pass.

1. Start by creating a *serializers.py* file in the **user** app. This is where we're going to store our *serializers* for our user:

- start by importing:
  - *get_user_model* because we're going to need the **user model** to create our model serializer,
  - *serializers* module from the REST framework.

- create our serializer class called **UserSerializer** and we're going to inherit from the *serializers.ModelSerializer* because we're basing our serializer from a model. Django REST framework has a built-in serializer in which we just need to *specify the fields* that we want from our module and it does the database conversion for us. It also helps with the *creating* and *retrieving* from the database. With a **ModelSerializer** all we need to do is specify the *Meta class* inside the serializer and then:
  - `model = get_user_model()` to specify the model that we want to base our *ModelSerializer* from.  Remember to include the brackets at the end, because we want to call the *get_user_model()* so it actually returns the user model class,
  - `fields = ('email', 'password', 'name')` to specify the *fields* that we want to include in serializer. These fields are going to be *converted* to *JSON* while making our **HTTP POST** and then we will *retrieve* that in our *view* and finally we'll *save* it to a model. So we want these *fields* to be accessible in the API either to *read* or *write*. These are the fields that we're going to accept when we create users,
  - `extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}` it allows us to configure a few extra settings in our model sterilizer and what we're going to use this for is to ensure that the password is write only and that the minimum required length is 5 characters.

- after configuring *Meta* class we need to create a function to create users. The *create* function is the function that's called when we create a new object. So define a function called **create** with *self* and *validated_data* arguments. In this function we're going to override the *create function*:
  - `return get_user_model().objects.create_user(**validated_data)` we're calling the *create_user* function from our *model* because by default it only calls the *create* function and we want to use our *create_user* from model **UserManager** to create the user. We do all this to be sure that the password that it stores will be encrypted. Otherwise, using the default *create* function, the password that it sets will just be the clear-text-password that we pass in and then the authentication won't work because it's expecting an encrypted key. We use _**validated_data_ to unwind this variable into the parameters of the *create_user* function. What Django REST framework does is when we're ready to create the user it will call our *create* function that we just created and it will pass in the *validated_data*. The *validated_data* will contain all of the data that was passed into our **serializer** which would be the *JSON data* that was made in the *HTTP POST* and it passes it as the argument to the *create_user* function and then we can use that to create our user.

2. Next let's update our *views.py*:

- import:
  - *UserSerializer* that we've just created,
  - *generics* module provided by rest_framework,
  - remove *render* module, because we're not going to need that.

- create a new view class called *CreateUserView* which will inherit from **CreateAPIView** that comes with the Django REST framework from *generics* module. This view is pre-made for us and allows us to easily make a API that *creates* an object in a database using the serializer that we're going to provide. All we need to specify in this *view* is a *class variable* that points to the *serializer class* that we want to use to create the object. To do that simply type `serializer_class = UserSerializer`.

3. Before we can actually access our API we need to *add a URL* and *wire the URL up to our view*. So we're going to create a new file in our **user** app called *urls.py* and inside:

- import:
  - the *path* function that comes with Django. This is a helper function that comes with Django that allows us to define different paths in our app,
  - our *views.py*.

- define *app_name* and call it *user*. We set it to help identify which app we're creating the URL from while using **reverse** function,

- create **urlpatterns** and inside, with `path('create/', views.CreateUserView.as_view(), name='create'),` wire up this URL with our *view* and then set the *name* so that we can identify it when using the *reverse* lookup function.

4. Finally, we need to update our main app *urls.py* to pass any user request to our **user**'s *urls.py*:

- import *include* module that comes with *django.urls*,

- add a new *path* below the **admin URL**: `path('api/user/', include('user.urls')),`.

It says that any *request URL* that starts with *api/user* it's going to pass in to the *user.url* via  **include** function. **include** is just another *helper function* that helps to basically *define the URLs as a string*.

It will identify the *user* app and it will get the *urls* module and then it will extend it using **include** function so any request that's passed in that matches *api/user* will then get passed on to our *urls.py* in **user** app and then if it matches *create* it will then get passed to our *views.py* which will then *render our API* so then we'll be able to *handle our API requests*.

5. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for creating a new token

Next thing we're going to add to our **users** API is the *create token endpoint*. This is going to be an endpoint which we can use to make a **HTTP POST request**. We can *generate a temporary* **authtoken** that we can then *use to authenticate future requests* with the API. With our API we're going to be using **token authentication**. The way that we log in is we *use an API to generate* a **token** and then we *provide that token as the authentication header* for future requests which we want to authenticate. The benefit of this is _we don't need to send the user's **username** and **password** with every single request_ that we make. We just need to send it *once to create the token* and then we can *use that token for future requests*. If we ever want to revoke the token you can do that in the database.

We're going to start by creating 4 **unit tests**:
- to test that the *token is created okay*,
- to test what happens if we *provide invalid credentials*,
- to check if we're trying to *authenticate against a non-existent user*,
- to check if we *provide a request that doesn't include a password*.

We're going to add them to the **test_user_api.py** file.

1. First, add URL which is going to be called `TOKEN_URL = reverse('user:token')`. This is going to be the URL that we're going to use to make the **HTTP POST request** *to generate our token*.

2. Because the purpose of this API is *to start the authentication* we can just add it to our **PublicUserApiTests**. It's no need to make a new class so inside this create a new test function called:
- **test_create_token_for_user** to *test that the token is created for the user*:
  - first, create **payload** that we're going to use to test the API and pass in an *email* and *password*,
  - **create a user** that matches this authentication so we can test against that user. We'll use our handy *create_user* helper function and pass in __**payload__: `create_user(**payload)`,
  - **make request** and store it in a variable called *res*: `res = self.client.post(TOKEN_URL, payload)`,
  - because we made a request for a login with the *email* and the *password* specified in **payload** so this exists as it is a part of our test we expect to get a **HTTP_200_OK** response and it should contain a token in the data response. Let's test for that `self.assertIn('token', res.data)` so it checks that there is a key called **token** in the **response's data** that we get back. next we can just assert that the response was a **HTTP_200_OK**, so let's **make an assertion** typing `self.assertEqual(res.status_code, status.HTTP_200_OK)`.

- **test_create_token_invalid_credentials** to *test that token is not created if invalid credentials are given*:
  - this time instead of creating a payload we're going to just **create the user** using *create_user()* function and simply pass in an *email* and *password*,
  - **create payload** with the same *email* we used while creating a user and different *password*,
  - **create request** and store it in a variable called *res* and pass there our **payload**: `res = self.client.post(TOKEN_URL, payload)`,
  - we expect that **token doesn't exist in response's data** and when we make this request we'll expect the response to be **HTTP_400_BAD_REQUEST** because the password is incorrect so let's **make the assertions**: `self.assertNotIn('token', res.data)` and `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

- **test_create_token_no_user** to *test that token is not created if user doesn't exist*:
  - **create payload** with *email* and *password*,
  - then we're going to **make a request without creating the user**, by typing `res = self.client.post(TOKEN_URL, payload)`,
  - we expect there's **no token in response's data** and a **HTTP_400_BAD_REQUEST**, so let's **make the assertions**: `self.assertNotIn('token', res.data)` and `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

- **test_create_token_missing_field** to *test that email and password are required*:
  - **create request with payload defined inside** and store it in a variable called *res*: `res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})`, we also set *password* to blank field,
  - we expect this to fail with **no token in response's data** and a **HTTP_400_BAD_REQUEST**, so let's **make the assertions**: `self.assertNotIn('token', res.data)` and `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

3. Save this file and let's head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add create token API

1. Head over to our **serializers.py** where we're going to create our **AuthTokenSerializer**. So we're going to create a new serializer just based off the Django standard *serializers* module and we're going to use this for *authenticating our requests*:
- add imports:
  - **get_user_model**,
  - **authenticate** function which comes with Django and *it's a Django helper command for working with the Django authentication system*. We simply pass in the *username* and *password* and we can authenticate a request,
  - **ugettext_lazy as _** this is a translation module that comes from *django.utils.translation*.

>Note: *whenever we're outputting any messages in the Python code that are going to be output to the screen it's a good idea to pass them through this translation system just so if we ever add any extra languages to our projects we can easily add the language file and it will automatically convert all of the text to the correct language*.

- **create a new class** called **AuthTokenSerializer** and it will inherit from **serializers.Serializer**:
  - **add an email and password** so for **email** simply type `email = serializers.CharField()` and for password we're going to *add a style* and *trim whitespace* because it's possible to have *whitespace* in our password like an extra space before or after and by default the Django the Django REST framework serializer will trim off this white space so for **password** type `password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)`,
  - **add validate function** with *attrs* passed and which we're going to be validating. This function *is called when we validate our serializer*. This validation is basically checking that the inputs (*email* and *password*) are all correct. We are also going to validate that the *authentication credentials* are correct too. This **validate** function will be *based on the default token serializer* that comes with Django REST framework, we'll *modify it to accept our email address instead of username*.

  ``` Python
  def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
  ```

  First we retrieve an *email* and *password* from **attrs** that we passed into the function.

  >Note: *__attrs__ parameter is basically just every field that makes up our serializer. Any field that makes up a sterilizer will get passed into the __validate__ function as dictionary and then we can retrieve the fields via these attributes. We can then validate whether we want to pass this validation or we want to fail the validation*.

  Then we use **authenticate** function to authenticate our request:
  - **first argument** is the *request* that we want to authenticate,

  >Note: *this is how we basically access the context of the request that was made. We're going to pass this into our ViewSet and what the Django REST framework ViewSet does is when a request is made it passes the __context__ into the serializer in the context class variable and from that we can get ahold of the request that was made*.

  - **second argument** is the *username* and we set it to **email** because the *username* is the name of the parameter required for the authenticate and we're authenticating via the *email address*,

  - **third argument** is the *password* and we set it to **password**.

  Then we __state the *if condition*__ `if not user` so *if authentication didn't work and we didn't return a user*, which is what happens if the authentication fails, we'll create the message that we're going to display to the user when they try and call the API. We also put a "*_*" before message to call translation function.

  Next we **raise the validation error** and then the Django REST framework knows how to handle this error by passing the error as a *400 response* and sending a response to the user which describes message "unable to authenticate with provided credentials".

  Finally, we **set our user in the attributes to the user object** and **return attributes**.

  >Note: *whenever we're overriding the __validate__ function we must return the values at the end once the validation is successful*.

2. Head over to the **views.py** where we'll _create a **create token view**_:

- start by importing:
  - **ObtainAuthToken** view which comes with Django REST framework. If we're authenticated using a *username* and *password* (as standard) it's very easy to just switch this on - we can just pass in the **ObtainAuthToken** view directly into our *urls*. Because we are customizing it slightly we need to just basically import it into our views and then extend it with a class and then make a few modifications to the class variables,
  - **api_settings** which are from the Django REST framework,
  - **AuthTokenSerializer**.

- **create class view** called *CreateTokenView* which will inherit from *ObtainAuthToken*,

- **set serializer class** so type `serializer_class = AuthTokenSerializer`,

- **set a renderer class** which will set the renderer so we'll be able to view this endpoint in the browser with the browsable API. This means that we can basically login using browser and type in the *username* and *password*, click "POST" and then *it will return the token*: `renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES`. We use the default ones because if we ever change the renderer class we can do that in the settings and it will update in our view automatically so we don't have to go through the view and change it.

3. Head over to the **urls.py** inside *user* app and create new path `path('token/', views.CreateTokenView.as_view(), name='token'),`.

4. Save all files and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

5. Go to the browser, go to **127.0.0.1:8000/api/user/create** and test creating new user. Then click **POST** and head over to **127.0.0.1:8000/api/user/token**, log in using created user, click **POST** and the token should be created successfully.

#### Add tests for manage user endpoint

The **manage user endpoint** will *allow the authenticated user to update their own profile* this includes **changing their name**, **changing their password**, and also **viewing their user object** so they can see what the values are currently set to.

We're going to **start by adding tests** in our *test_user_api.py* file. We're going to do this within our **PublicUserApiTests** because we're going to test as if we are an *unauthenticated user*:

1. **Add a URL** to the top of the page and we will call it `ME_URL = reverse('user:me')`.

2. **Test that authentication is required for the endpoint**. It's recommend doing this because authentication required on an endpoint is quite an important part because it affects the security. **We don't want API's being made publicly by accident** and a great way to prevent against that is to **add unit tests to make sure that after any changes that we make those API's will always be private**:

- **create test_retrieve_user_unauthorized** test to *test that authentication is required for users*,

- **create HTTP GET request to ME_URL** so type `res = self.client.get(ME_URL)`,

- we expect the error **HTTP_401_UNAUTHORIZED** to occur so **create an assertion** `self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)`.

3. Next we're going to test that that *retrieving profile is successful* and test that _POST is not allowed on the **/me** endpoint_ we're just going to support PATCH and PUT to update it. Finally we're going to test *updating the user profile for authenticated user* using the API.

>Note: *POST is used for creating objects and PUT and PATCH is usually used for editing objects. So we only want them to allow them to edit the endpoint*.

**Create new test class** called **PrivateUserApiTests** which will inherit from *TestCase*. **Private** means that *authentication is required before we can use these endpoints*:

- **create setUp function** which will *do the authentication for each test that we do*. So we don't need to set the authentication every single test, we're just doing the **setUp** and then that happens automatically before each test:
  - **set up a user** _using `self.user = create_user()` helper function and passing in **password**, **email** and **name**_,
  - **set up a client** *using `self.client = APIClient()`* to create a reusable client,
  - **force authenticate method** to *authenticate any requests that the client makes with our sample user*, to do that type `self.client.force_authenticate(user=self.user)`.

>Note: *__force_authenticate__ is a helper function that basically just makes it really easy to simulate making authenticated requests so whichever request we make with this client now will be authenticated with our sample user*.

- **add test_retrieve_profile_success test** with which we'll be able to *test if we can retrieve the profile of the logged in user*:
  - **make the HTTP GET request to ME_URL**, because we've already authenticated in our setup so we don't need to do that authentication, so type `res = self.client.get(ME_URL)`,
  - **assert that we got a HTTP_200_OK** - `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - **assert that the user object returned is what we expect** - `self.assertEqual(res.data, {'name': self.user.name, 'email': self.user.email})` so test if the user got a **name** and an **email** and we get them from a **user** object. We exclude the password because sending a password even if it's hashed is never recommended.

- **add test_post_me_not_allowed test** to *test that we cannot do a HTTP POST request on the profile for a __/me__ endpoint*:
  - **make the HTTP POST request to ME_URL**, so type `res = self.client.post(ME_URL, {})` and we'll just post the empty object to test it,
  - **assert that we get a HTTP_405_METHOD_NOT_ALLOWED**, so type `self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)`. This is the standard response when we try to do a HTTP method that is not allowed on the API.

- **add test_update_user_profile test** so we're going to update the user via the API and we're going to *test that the updates worked for authenticated user*:
  - **create a payload** with defined *name* and *password* and make sure that they're different from the values that we set in **setUp** for the default user to simply know that the test is working,
  - **make the HTTP PATCH request to ME_URL** and pass in **payload**, so type `res = self.client.patch(ME_URL, payload)`
  - **use the refresh_from_db()** helper function on our user *to update the user with the latest values from the database*,
  - **verify that each of the values we provided was updated** so **assert that the name of the user is equal to name from payload** which is the new name we provided. Then **assert true on the check password methods** *to check the password*. To check **name** type: `self.assertEqual(self.user.name, payload['name'])` and to check **password** type: `self.assertTrue(self.user.check_password(payload['password']))`,
  - we expect it to return **HTTP_200_OK** so **make sure that it returns the HTTP_200_OK** by typing: `self.assertEqual(res.status_code, status.HTTP_200_OK)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add manage user endpoint

Now we can create our **manage user endpoint**. We're going to use our existing **UserSerializer** but we're going to add an additional function to the serializer for *updating our user object*. We're also going to add a custom view using the **RetrieveUpdateAPIView** from the Django REST framework **generic** API view options.

1. **Head over to the views.py** file:

- **import**:
  - **authentication** and **permissions** classes from Django **rest_framework** and we're going to use them for our authentication and permissions of our user endpoint,

- **create manage user views** called **ManageUserView** which inherits from **generics.RetrieveUpdateAPIView**:
  - **create a serializer class attribute**, so type `serializer_class = UserSerializer`,
  - next we'll **add two more class variables for authentication and permission**. **Authentication** *is the mechanism by which the authentication happens* and in our case we're going to use is token authentication. **Permissions** *are the level of access that the user has*, so the only permission we're going to add is that the user must be authenticated to use the API they don't have to have any special permissions they just have to be logged in. **Set these class variables**: `authentication_classes = (authentication.TokenAuthentication, )` for **authentication** and `permission_classes = (permissions.IsAuthenticated, )` for **permissions**,
  - **add a get_object function to our API view**. Typically what would happen with an API view is we would link it to a model and **it could retrieve the item and we would retrieve data based models**. **In this case we're going to just get the model for the logged in user**. So we're going **to override the get_object() and return the user that is authenticated**.

  To override the **get_object()** type:

  ``` Python
  def get_object(self):
        """Retrieve and return authentication user."""
        return self.request.user
  ```

  So when the **get_object()** is called the request will have the user attached to it because of the **authentication_classes**. The authentication class takes care of getting the authenticated user and assigning it to the request.

2. Move on to **serializers.py** file, **locate UserSerializer** and below the **create** function we're going to **add an update** function. And the purpose of this is *we want to make sure the __password__ is set using the __set_password__ function instead of just setting it to whichever value is provided*. **Define update** function with **instance** and **validated_data** parameters:

- **instance** is going to be the *model instance that is linked to our model sterializer* so it's going to be our **user object**,

- **validated_data** is going to be these *fields that have been through the validation and ready to update*.

So below our **update** function definition:

- **remove the password from the validated_data** and we do that using the dictionary **pop** function, like so: `password = validated_data.pop('password', None)`. The reason we provide **None** is because *with the pop function we must provide a default value*. We need to provide a default value if password should not exist within our dictionary and because we're going to be allowing the users to optionally provide a password we'll leave this field as **None**,

- **run the update request on the rest of our validated_data** so everything except the password will be updated for our user that we passed using **instance** argument. To do that type `user = super().update(instance, validated_data)`. With **super()** we're calling the model **serializers update functions**, which are the default one, so we can make use of all the functionality that's included in the default one and extend it slightly to customize it for our needs,

- **set the password** using the *if statement* and **save()** the user object to *database*:

``` Python
if password:
        user.set_password(password)
        user.save()
```

So if the user provided a password then we use **set_password** for the **user** object and pass in the **password that comes from validated_data**. We do all that to simply not pass the plain text but to use specially designed methods for setting passwords,

- finally **return a user**.

3. Head over to **user**'s '**urls.py** and add new path for **/me** endpoint: `path('me/', views.ManageUserView.as_view(), name='me'),`.

4. Save all files and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

5. Go to the browser, go to **127.0.0.1:8000/api/user/token** authenticate the user there. Then click **POST** and open up a **Mod Header** extension. **Copy generated token** and inside **Mode Header** create an **Authorization** header and pass in the `Token <COPIED TOKEN FROM 127.0.0.1:8000/api/user/token>`

>Note: *__Mode Header__ allows us to modify the headers of the requests that we make so it makes it really easy to basically simulate and test authentication with our API*.

Now **visit 127.0.0.1:8000/api/user/me** and we should see the user that we are authenticated with. **Test making changes** to any of our user's fields.

## Create tags endpoint

In this section we're going to add our **tags API**. The tags API is going to **allow us to manage tags which we can assign to recipes** in order to help with sorting and filtering of our recipes in the system. We're going to **create our tags endpoint** in a new app called the recipe app. The recipe app is where we're going to store all the recipe related endpoints such as the ones for **creating and updating recipes** and the ones for **creating and updating tags and ingredients**. We're going to start with taking care of tags.

#### Create recipe API

1. Head over to the terminal and navigate to our *app* folder. Then type `docker-compose run --rm app sh -c "python manage.py createapp recipe"` or, if it doesn't work type: `sudo docker-compose run --rm app sh -c "python manage.py createapp recipe"`.

2. Next we're going to clean up some of files inside *recipe app* folder, that we're not going to need:

- remove **admin.py** file, because we're going to keep all the *admin code* in the *core app*,

- remove **migrations** folder,

- remove **models.py**, because that's also in the *core app*,

- remove the **test.py** file,

- create **tests/\__init__.py** for hosting our tests and the **\__init__.py** file is to make it a Python module.

3. Head over to our **app/settings.py** and add our new app in the **INSTALLED_APPS** option.

#### Add tests for tag model

Next we're going to create a new database **model for handling our tag objects**. Our tag model is going to be very basic - it's just going to accept the **name** of the tag and the **user** who owns the tag.

We're going to **start by adding a unit test** for getting the tag object as a *string* and then we're going to **implement our model** and then we're going to **run our migrations** to create the migration which would create the model in the database.

1. Head over to the **core app** and the tests folder and open up the **test_models.py** file. We're going to add a new helper function at the top of the file, right after our imports, to **create users** that just makes it easy for us to create users in our test.
So define a new function called **sample_user** and as a arguments pass in an **email** and assign it some sample email, and **password**, also assign it a sample value.
After definition let's create and return a basic user using **get_user_model()** model and with **create_user(email, password)** method we pass in an *email* and *password*.

2. **Import models from core app**.

3. Next scroll down and inside **ModelTests** create a new test called **test_tag_str()** to test the tag string representation:

- **create tag** so we'll do `tag = models.Tag.objects.create()` and we pass in a **user=sample_user()** using our *sample_user()* function and a **name='Vegan'** which will be our sample name for this tag,

- we expect that **when we convert tag model to a string it gives us the name**, so `self.assertEqual(str(tag), Tag.name)`.

>Note: *So with Django models we can basically specify what field we want to use when we convert the model to a string representation and we're going to set it to the name. __We're using this test only to verify that we can create a model that is called tag__*.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Create tag model

1. Head over to **models.py** inside **core** app.

2. **Import settings** from *django.conf*.

3. **Create new class** called **Tag**, which will inherit from *models.Model*.

4. Next **set a name**, like so: `name = models.CharField(max_length=255)`.

5. **Assign the user foreign key**, but instead of referencing the **user object** directly, which we could do, we're going to use *the best practice method* of **retrieving the auth user model setting** from our Django settings.

>Note: *this is the recommended way to retrieve different settings from the Django settings file so we can basically use this to retrieve our auth user model*.

``` Python
user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
  )
```

- The first argument is the model that we want to base the foreign key off,

- then we need to specify what happens when we delete this object, so when we delete a user therefore what do we want to happen to the tags.

6. Finally we want to **add our string representation** of the model, so we simply define a new function inside our **Tag** class called **\__str__(self)** and `return self.name`.

7. Next we need to register this model to our admin, so **head over to admin.py** inside our **core** app and type there `admin.site.register(models.Tag)` to register our model.

>Note: *we don't need to specify the admin that we want to register it with, because it will just use the default one for the model. There's nothing special about our tag, it's just a very basic model that supports the basic create, read, update and delete functions in the admin panel*.

8. Save this file and **make migrations** using `docker-compose run --rm app sh -c "python manage.py makemigrations"` or if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py makemigrations"`. Then let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for listing tags

We're going to **test that the API requires authentication to access it**. Then we're going to **test that we can list tags in our API** and finally we're going to **test that the tags that are listed are specifically for the user that is authenticated**.

1. First let's create a new unit test file inside **recipe/tests** folder called **test_tags_api.py**.

2. Start by **importing**:

- **get_user_model** from *django.contrib.auth*,

- **reverse** from *django.urls*, for generating the URL,

- **TestCase** from *django.test*,

- **status** from *rest_framework*,

- **APIClient** from *rest_framework.test*,

- **Tag** from *core.models*,

- **TagSerializer** from *recipe.serializers*, the tag serializer which we're going to create to make the tests pass after we write the unit tests.

3. Now let's **create a tags URL using reverse function**: `TAGS_URL = reverse('recipe:tag-list')`. So the URL is going to be in the **recipe** app and the URL is going to be called **tag**. We're going to be using a view set so that automatically appends the action name to the end of the URL for us using the router. For listing tags the URL is going to be called tag-list.

4. **Create the public API tests class** called **PublicTagsApiTests** which will inherit from *TestCase* in which we are going to test that login is required for the API, that's why it's public:

- next, inside **PublicTagsApiTests** let's **create a set up function** in which we'll **set up the client** using *APIClient*, so type `self.client = APIClient()`,

- with that we can **test that login is required for retrieving tags** by creating function called **test_login_required**:
  - **create GET request to TAGS_URL** by typing `res = self.client.get(TAGS_URL)`. It'll make an unauthenticated request to our TAGS_URL,
  - we expect it to fail and return with HTTP_401_UNAUTHORIZED, so let's **make an assertion**, by typing `self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)`.

5. Next we're going to add tests that require authentication. **Create class called PrivateTagsApiTests**:

- first, **create set up function** and inside:
  - **create new user** with given credentials: `self.user = get_user_model().objects.create_user()` and pass there sample **email** and **password**. This is going to be the user we use for authenticating with,
  - **create new client**, so type: `self.client = APIClient()`,
  - **forcibly authenticate a request** passing in our *user* `self.client.force_authenticate(self.user)`.

- now, let's **test retrieving tags**, so **create function called test_retrieving_tags**. All we're going to do is we'll **create a couple of sample tags** and then we're going to **make the request to the API** and then we're going to **check that the tags returned equal what we expect them to equal**, so inside:
  - **create two sample tags**, e.g.: `Tag.objects.create(user=self.user, name='Vegan')` and `Tag.objects.create(user=self.user, name='Dessert')`,
  - **create GET request to TAGS_URL**, which should return our tags, so type `res = self.client.get(TAGS_URL)`,
  - next, let's **make the query on the model that we expect to get** to compare to the result, so let's type `tags = Tag.objects.all().order_by('-name')`. This just ensures that the tags are returned in alphabetic order, but with that we make sure that we can retrieve objects from our database,
  - **serialize our tags object** by typing `serializer = TagSerializer(tags, many=True)` and we set *many* parameter to **True** because we want to make sure it won't assume we want to serialize only one object, but many,
  - we expect HTTP OK code, so **assert** `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we also expect **res.data** (which is the data that was returned in the response) **to be equal the serializer's data** that we passed in. We also expect them to be listed by name, so **assert** `self.assertEqual(res.data, serializer.data)`.

- next, we'll **test that the tags that are retrieved are limited just to the user that is logged in** so we only want to see tags that are assigned to the authenticated user so let's create a new unit test called **test_tags_limited_to_user**:
  - **create a new user** in addition to the user that is created at the *set up* just so we can assign a tag to that user and then we can compare that that tag was not included in the response because it was not the authenticated user: `self.user = get_user_model().objects.create_user()` and pass in sample **email** and **password**,
  - **create a new tag** for our new user: `Tag.objects.create(user=user2, name="SampleName1")`,
  - **create a new tag that is assigned to the authenticated user**, which will be user from our set up: `tag = Tag.objects.create(user=self.user, name="SampleName2")`,
  - **create GET request to TAGS_URL**, so type `res = self.client.get(TAGS_URL)`,
  - we expect the one tag to be returned in the list because that's the only tag assigned to the authenticated user, so we expect it to return HTTP OK code: `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we created only one tag so we expect the length of the results returned to be exactly one, so **assert** `self.assertEqual(len(res.data), 1)`,
  - we also expect that the name of the returned tag in the first response is the tag's name that we created and assigned to the user, so we type: `self.assertEqual(res.data[0]['name'], tag.name)`.

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add feature for listing tags

1. Next we're going to implement the **feature to list our tags**. Let's **start by creating a new serializers file** within our *recipe app*. We're going to call it **serializers.py** and we're going to begin with:

- **importing**:
  - **serializers** from *rest_framework*,
  - **Tag** from *core.models*.

- **create TagSerializer class**:
  - **define Meta class** and as a *model* assign the **Tag** model to it, as *fields*: **id** and **name**, and as *read_only_fields* the **id**.

2. Now, let's move to **views.py** file within our *recipe API*. The view that we're going to create is simply a **ViewSet** and we're going to base it off the generic viewset and we're specifically going to use the *ListModelMixin*.

>Note: *It's a Django REST framework feature where we can pull in different parts of a viewset that we want to use for our application and because we only want to take the list model function and we don't want to add the create, update, delete function we're just going to add the list model function. We can do that very easily by using a combination of the generic ViewSet and the ListModelMixin*.

- first let's do some **imports**:
  - **viewsets, mixins** from *rest_framework*,
  - for authentication **TokenAuthentication** from *rest_framework.authentication*,
  - for permissions **IsAuthenticated** from *rest_framework.permissions*,
  - **Tag** from *core.models*,
  - **serializers** from *recipe*.

- **create our viewset called TagViewSet** which will inherit from **viewsets.GenericViewSet** and **mixins.ListModelMixin**:
  - **add permission_classes** and assign *IsAuthenticated* to it,
  - **add authentication_classes** and assign *TokenAuthentication* to it,
  - **create queryset** because when we're defining a **ListModelMixin** in the generic viewset we need to provide the **queryset** that we want to return, so let's type: `queryset = Tag.objects.all()`,
  - **add serializer_class** and assign *serializers.TagSerializer* to it.

3. Within *recipe app* **create urls.py**:

- start by **including**:
  - **path, include** from *django.urls*,
  - **DefaultRouter** from *rest_framework.routers*,
  - we'll also import a view which we'll be using to render the ViewSet, so **views** from *recipe*.

- **create default router** - feature of the Django REST framework that will automatically generate the URLs for our ViewSet, e.g. one URL might be the */api/recipe/tags* and another URL might be */api/recipe/tag/* so we might add some custom actions to it. **Default router** automatically registers the appropriate URLs for all of the actions in our ViewSets.

To create default router let's type: `router = DefaultRouter()`

To register ViewSet with our default router, type: `router.register('tags', views.TagViewSet)` and we called it *tags*.

- **define the app name**, so `app_name = 'recipe'`, that when we identify the app the reverse function can look up the correct URLs,

- **define urlpatterns** in which we create path `path('', include(router.urls)),`. This will pass any path that matches our *recipe app* (which we defined above) and will pass in our route URLs. So all of the URLs that are generated by our default router will then be included in the URL patterns and if we add any more ViewSets we can just register them here and then they automatically have all of the URLs generated.

4. Head over to **app/urls.py** and add new path which should map the URLs correctly to our *recipe app*, so inside **urlpatterns** let's type: `path('api/recipe/', include('recipe.urls')),`.

5. If we run tests now we'll get `AssertionError: 2 != 1`, because we have to **add the modification to the ViewSet to filter objects by the authenticated user** so **head over to views.py** and **add a function called get_queryset** which will override the get_queryset default function.

>Note: *when we call the list function (so when our viewset is invoked from a URL) it will call get_queryset to retrieve objects and this is where we can apply any custom filtering like limiting it to the authenticated user so whatever we return there it'll will be displayed in the API*.


>Note: *the request objects should be passed in to the self as a class variable and then the user should be assigned to that because authentication is required so if it manages to get this far in calling the API then it would have already been authenticated and it would already have these authenticated permission prove, otherwise it would have just received an unauthenticated request error*.

`return self.queryset.filter(user=self.request.user).order_by('-name')`

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add create tags feature

Next we're going to **add the create tags feature**. We're going to start by adding some basic tests to **check that we can create tags** and also to **check that when we create tags validation is performed correctly** on the create request.

1. Head over to the recipe *app/test_tags_api* and **create new unit test called test_create_tag_successful** to test that creating tag was successful:

- **create a payload**: `payload = {'name': 'TestTag'}` passing only **name**,

- **create GET request to TAGS_URL and pass in payload**: `self.client.post(TAGS_URL, payload)`,

- **create variable called exists** and with that variable we're going to verify the tag exists and the way we do that is we use the *tag.objects.filter* function and we **filter by the tag** and then we just check that that tag **exists()**.

``` Python
exists = Tag.objects.filter(
        user=self.user,
        name=payload['name']
    ).exists()
```

It will **filter all tags** with the user that is the authenticated user and with the name that we created in our test payload. Then we'll just **.exists()** and this will **return a boolean** true or false depending on whether this exists, so if it exists it will be **true** of it doesn't exist it will be **false**.

- with this we can **make assertion**: `self.assertTrue(exists)`, so test will fail if tag wasn't created successfully.

2. Now let's create new test to **test what happens if we create a tag with an invalid name**, so **define new unit test function called test_create_tag_invalid**:

- **create payload** with blank name, like so: `payload = {'name': ''}`,

- **create POST request to TAGS_URL and pass in payload**: `res = self.client.post(TAGS_URL, payload)`,

- we expect it to return HTTP_400_BAD_REQUEST, so let's **make an assertion**: `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

3. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

4. Now we're going to make a small change to our view to enable these tests to pass by **adding support for creating tags**:

- **head over to views.py** and in the **TagViewSet** we're going to change the inheritance for our class by adding the **mixins.CreateModelMixin**. This will add the create option,

- now, we need to **override the perform_create** so that we can *assign the tag to the correct user*. To do that **create new function within TagViewSet called perform_create** and simply type `serializer.save(user=self.request.user)`.


It's very similar to the **get_queryset**, the **perform_create** function is a function that allows us to **hook into the create process** when creating an object. When we create object in our ViewSet **perform_create** function will be invoked and the **validated sterilizer** will be passed in as a *serializer argument* and then we can perform any modifications inside, that we'd like. All we're going to do is we're just going to do **serializer.save()** and **set the user to the authenticated user**.

5. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

## Create ingredients endpoint

In this section we're going to **create our ingredients endpoint**. The ingredients endpoint is going to be very similar to the *tags endpoint* in that it allows us to **create and list ingredients** which we can later assign to recipes for the purposes of *filtering*.

#### Testing ingredient model

1. Head over to the *core app* and the **test_models.py**.

2. Add a new test to the bottom called **test_ingredient_str** to check that our model is converted correctly to a string representation:

- **create a sample ingredient** by typing `ingredient = models.Ingredients.objects.create()` and to create an ingredient pass in the **user=sample_user()** and **name=<SAMPLE NAME>**,

- to verify that the ingredient model exists that it works and that we can create and retrieve a model we'll **create an assertion**: `self.assertEqual(str(ingredient), ingredient.name)` to check if while converting ingredient to string it returns its name.

3. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Creating ingredient model

1. Head over to **models.py**.

2. **create ingredient model called Ingredient**:

- **create name** as *Charfield*,

- **create user** using *ForeignKey* and pass in `settings.AUTH_USER_MODEL, on_delete=models.CASCADE`,

- next we'll create function to handle string representation for this model's objects:
  - inside **Ingredient** model create **\__str__** function,
  - return `self.name`.

3. Head back to the terminal and make migrations using `docker-compose run app sh -c "python manage.py makemigrations"` and then `docker-compose run app sh -c "python manage.py migrate"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py makemigrations"` and then `sudo docker-compose run app sh -c "python manage.py migrate"`.

4. Head over to **admin.py** and **register our new model** by typing `admin.site.register(models.Ingredient)`.

5. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for listing ingredients

Next we're going to add some tests for listing ingredients. Because we're going to create the same type of API that we created for our tags we're going to start by adding the unit tests.

1. Create new test module in the *recipe app* called **test_ingredients_api.py**.

2. **Import**:
- **get_user_model** from *django.contrib.auth*,
- **reverse** from *django.urls*,
- **TestCase** from *django.test*,
- **status** from *rest_framework*,
- **APIClient** from *rest_framework.test*,
- **Ingredient** from *core.models*,
- **IngredientSerializer** from *recipe.serializers*.

3. Create URL, so type: `INGREDIENTS_URL = reverse('recipe:ingredient-list')`, so we're also going to use a default router for our ingredients API and it's going to have the */list* in the URL name which is going to reference to our listing URL.

4. **Add public class** for the public ingredients API test called **PublicIngredientsApiTests**:

- add **setUp** function and inside define new client for test purposes `self.client = APIClient()`,

- create new test function called **test_login_required** to test that to get the *INGREDIENTS_URL* the authenticated client is required:
  - **create HTTP GET request to INGREDIENTS_URL** by typing `res = self.client.get(INGREDIENTS_URL)`,
  - we expect it to return the *HTTP_401_UNAUTHORIZED* error, so **assert** `self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)`.

5. Now we can then move on to testing listing our ingredients by **creating new private class** called **PrivateIngredientsApiTests**:

- add **setUp**:
  - **set up our client** by typing `self.client = APIClient()`,
  - **create new user** by typing `self.user = get_user_model().objects.create()` and pass in an **email** and the **password**,
  - **force authentication** on our client: `self.client.force_authentication(user=self.user)`.

- **add unit test called test_retrieve_ingredient_list** to test retrieving ingredients:
  - first let's create sample ingredients, so type: `Ingredient.objects.create(user=self.user, name='Kale')` and second ingredient: `Ingredient.objects.create(user=self.user, name='Salt')`,
  - **create HTTP GET request to INGREDIENTS_URL**, so type: `res = self.client.get(INGREDIENTS_URL)`,
  - next, we will verify that the returned result matches what we expect it to match. We'll basically retrieve all the ingredients, serialize them and then compare the result to the serialized ingredients. So type `ingredients = Ingredient.objects.all().order_by('-name')`,
  - serialize retrieved ingredients: `serializer = IngredientSerializer(ingredients, many=True)`,
  - we expect it to return *HTTP_200_OK* code, so we do `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we also expect that the data from our request will match the serialized ingredients, so `self.assertEqual(res.data, serializer.data)`.

- next we will **test that the ingredients are limited to the authenticated user**. For this we'll **create new unit test called test_ingredients_limited_to_user**:
  - **create new user**, so `user2 = get_user_model()objects.create()` and pass in **new email** and **new password**,
  - **create new tag** and assign user2 to it: `Ingredient.objects.create(user=user2, name='Vinegar')` and then **create another tag** and assign our user from *setUp* to it: `ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')`. The reason we're not assigning this to an *ingredient* variable is because we don't actually need to reference it at any point in our test whereas **ingredient** we will reference because we'll check that the name of this ingredient matches the name of the ingredient we've created,
  - **create HTTP GET request to INGREDIENTS_URL**: `res = self.client.get(INGREDIENTS_URL)`,
  - we expect it to return *HTTP_200_OK* code, so we do `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we also want the data of our request to include only one element, because we only assigned one ingredient to the currently authenticated client, so we type `self.assertEqual(len(res.data), 1)`,
  - as we expect our request's data to include one element we also expect this element's name to be exactly the same as the **ingredient**'s name, so `self.assertEqual(res.data[0]['name'], ingredient.name)`.

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implement feature for listing ingredients

Next we're going to add the feature to list ingredients from our ingredients endpoint.

1. Head over to the **serializer.py** file:

- **import Ingredient** model that we created previously,

- **create IngredientSerializer**:

- inside *IngredientSerializer* **create Meta class** and inside:
  - **set model to Ingredient's model**: `model = Ingredient`,
  - **set fields to name and id**: `fields = ('name', 'id')`,
  - **set read-only fields to id**: `read_only_fields = ('id', )`.

2. Head over to the **views.py** file:

- import **Ingredient** from *core.models*,

- **create an ingredient's ViewSet called IngredientViewSet** based on **GenericViewSet**:
  - add `authentication_classes = (TokenAuthentication, )`,
  - add `permission_classes = (IsAuthenticated, )`,
  - add `queryset = Ingredient.objects.all()`,
  - add `serializer_class = serializers.IngredientSerializer`
  - add the **get_queryset** function so that we can filter by the objects assigned to the user that is currently authenticated and also order them by name so inside let's type `return self.queryset.filter(user=self.request.user).order_by('-name')`.

3. Head over to **urls.py** and **register Ingredients endpoint** to our default router by typing: `router.register('ingredients', views.IngredientViewSet)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Test creating ingredients

1. Head over to **test_ingredients_api.py** and to **PrivateIngredientsApiTests**.

2. **Create new unit test called test_create_ingredient_successful** to test test if creation of ingredients was successful:

- **create payload** which includes **name**,

- **create HTTP POST request** to post in the **payload** to the **INGREDIENTS_URL** which will create new ingredient object; we also don't assign it to any variable because we don't really need it in our function,

- now we'll check if the ingredient object exists in our database: `exists = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()`,

- we expect that our **exists** variable returns *True*, so `self.assertTrue(exists)`.

3. **Add the test to check passing in blank payload** so define new unit test called **test_create_ingredient_invalid**:

- **create payload** which includes **name** but as its value we'll leave it blank string,

- **create HTTP POST request to INGREDIENTS_URL** and pass in **payload**,

- we expect it to return an *HTTP_400_BAD_REQUEST* so `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implement feature for creating ingredients

1. Open up **views.py** and we'll do small changes to our **IngredientViewSet**.

2. Firstly, in addition to *GenericViewSet* let's base that ViewSet on **ListModelMixin** and on **CreateModelMixin**,

3. **Add perform_create** function which will overwrite the default create function with our custom user's request data which is passed in to the database using *serializer.save()* method.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command. Then, go to the browser and test our new *create ingredients enpoint*.

#### Re-factor tags and ingredients viewsets

The reason we re-factor our viewsets is we can make **views.py** much shorter and simpler.

What we can notice is that the **TagViewSet** and **IngredientViewSet** are pretty much the same: both have *authentication_classes*, and *permission_classes*, both inherit from *CreateModelMixin* and *ListModelMixin* and also both use *get_queryset* and *perform_create* functions.

1. With all that we can simply create **base class** which we can call **BaseRecipeAttrViewSet** and inside let's put all that things that *TagViewSet* and *IngredientViewSet* have in common. Let's also base that class on classes that *TagViewSet* and *IngredientViewSet* inherit.

The final **BaseRecipeAttrViewSet** class should looks like this:

``` Python
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base ViewSet for user owned recipe attributes."""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Returns objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object."""
        serializer.save(user=self.request.user)

```

2. Next we naturally update *TagViewSet* and *IngredientViewSet*, so:

- base both viewsets on our new **BaseRecipeAttrViewSet**,

- delete all unnecessary code from *TagViewSet* and *IngredientViewSet* as in result **views.py** should contain:

``` Python
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base ViewSet for user owned recipe attributes."""

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Returns objects for the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object."""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in a database."""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
```

## Create recipe endpoint

In this section we're going to be **creating our recipe endpoint**. We're going to start by creating a new model in our database for handling recipe objects. Once we create the model we're then going to run the migrations and create the migration file that will create the recipe table in the database.

#### Add tests for creating recipe model

1. **Create the test** in *core/tests/test_models.py*, and scroll down to the bottom.

2. **Add new test to test retrieving string representation of a created object**. Let's call this unit test **test_recipe_str**.

3. Inside **test_recipe_str** create a **recipe** and pass in *user=sample_user()*, *title* as a sample title, *time_minutes* and set it to integer and *price* and set it to the decimal field.

4. Then let's **make an assertion**, so we expect that while converting recipe to string we'll receive a recipe's title, so let's type `self.assertEqual(str(recipe), recipe.title)`.

>Note: *the __user__, __title__, __time_minutes__ and __price__ are the only required fields for each recipe object*.

5. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add recipe model

1. **Head over to the models.py** and scroll to the bottom of the file.

2. **Create class called Recipe** which will inherit from the *models.Model* and then let's assign the fields that we want to give:

- **user**, so type: `user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)`,

- **title**: `title = models.CharField(max_length=255)`,

- **time in minutes**: `time_minutes = models.IntegerField()`,

- **price in decimals**: `price = models.DecimalField(max_digits=5, decimal_places=2)`,

- **link** in case the user wanted to add a link to the recipe: `link = models.CharField(max_length=255, blank=True)` and we set it to be blank, so this field will be optional.

The next two fields are going to be the **ingredients** and the **tags**. These are going to be **ManyToManyFields**, so there are different types of foreign key that we can have in a database:

- **OneToOne** relationship which means we would have *one recipe to one ingredient*,

- **OneToMany** relationship which means we would have *many ingredients to one recipe*,

- **ManyToMany** field allows *many recipes to be assigned to many different ingredients*.

Knowing that, let's add two more fields, which are:

- **ingredients** : `ingredients = models.ManyToManyField('Ingredient')`,

- **tags**: `tags = models.ManyToManyField('Tag')`.

>Note: *Django has this useful feature where we can just provide the name of the class in a string and then it doesn't matter which order we place  our models in*.

3. After creating fields inside **Recipe** class, let's create a function to make our *string representation*, so let's create a **\__str__** function and inside let's type `return self.title`.

4. Save this file and **make migrations** using `docker-compose run --rm app sh -c "python manage.py makemigrations core"` or if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py makemigrations core"`.

5. Now let's **register Recipe model** by heading over to *admin.py* and below other models' registration, type: `admin.site.register(models.Recipe)`.

6. Then let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for listing recipes

1. Start by creating a new test module underneath *recipe/tests*. Let's call the module **test_recipe_api.py**.

2. Inside **test_recipe_api.py** let's do some imports:

- **get_user_model** from *django.contrib.auth*,

- **TestCase** from *django.test*,

- **reverse** from *django.urls*,

- **status** from *rest_framework*,

- **APIClient** from *rest_framework.test*,

- **Recipe** from *core.models*,

- **RecipeSerializer** from *recipe.serializers*.

3. Create URL for our recipe endpoint: `RECIPES_URL = reverse('recipe:recipes-list')`.

4. Next we're going to create a helper function called **sample_recipe**. This is going to allow us to easily create test sample recipes for us for later tests We create this helper function because we know that we're going to create a lot of sample recipes. To create a sample recipe we only have to pass in a *user* and if we want, some additional *parameters*, because this function will create a default *parameters*:

- as the parameters for this function let's pass **user** and __**params__,

- inside **sample_recipe** create a dictionary called *defaults* and put a sample *title*, *time_minutes* and *price* inside.

- next we want it to accept additional *parameters* and for this we'll use **update** function on our **defaults** dictionary and pass in **params**, like so: `defaults.update(params)`

>Note: *update function accepts a dictionary object and it will take whichever keys are in the dictionary and it will update them or if they don't exist it will create them*.

- finally, let's create our sample recipe by typing `return Recipe.objects.create(user=user, **defaults)`.

5. We're going to create three different tests:

- to test that authentication is required:
  - first, let's create a class called **PublicRecipeApiTests** which will inherit from **TestCase**,
  - inside **PublicRecipeApiTests** create a new **setUp** function which will set up our client to an *APIClient*: `self.client = APIClient()`,
  - then, let's create **test_auth_required**,
  - inside, **create HTTP GET request to RECIPES_URL**,
  - finally, **add assertions**, so as we expect it to return a *HTTP_401_UNAUTHORIZED* let's type `self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)`.

- to test that we can retrieve recipes:
  - create class called **PrivateRecipeApiTests** which will inherit from **TestCase**,
  - inside **PrivateRecipeApiTests** create a **setUp** function which also will assign a *APIClient* to our client. We do that by typing `self.client = APIClient()`, then create a user and give him sample credentials, so let's type `self.user = get_user_model().objects.create_user()` and pass in login credentials. When it's done let's *force_authenticate* on our client with created user: `self.client.force_authenticate(self.client)`,
  - then, let's create **test_retrieve_recipes**,
  - inside **test_retrieve_recipes create two recipes** using our *sample_recipe* function by repeating `sample_recipe(user=self.user)` twice. We don't assign any variable to this because we don't need to access them in our test,
  - **create HTTP GET request to RECIPES_URL**: `res = self.client.get(RECIPES_URL)`,
  - now, let's **retrieve recipes from database** by typing `recipes = Recipe.objects.all().order_by('-id')`,
  - then, let's **put retrieved recipes into our serializer** and make it accept many fields, so type: `serializer = RecipeSerializer(recipes, many=True)`,
  - with all that we can **make assertions** and firstly, we expect it to return *HTTP_200_OK* so type `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - then we expect that the data from our GET request will be the same as the data we passed in to the serializer, so `self.assertEqual(res.data, serializer.data)`.

- to test that the recipes are limited to the authenticated user:
  - inside **PrivateRecipeApiTests** create **test_recipes_limited_to_user**
  - **create a new user called user2** using *get_user_model()* function and pass in sample authentication credentials,
  - next, create two sample recipes - one for **user** and second for **user2**: `sample_recipe(user=self.user)` and `sample_recipe(user=user2)`,
  - **create HTTP GET request to RECIPES_URL**: `res = self.client.get(RECIPES_URL)`,
  - **retrieve all recipe objects from database** and order this by *'-id'*: `recipes = Recipe.objects.all().order_by('-id')`,
  - now let's **serialize retrieved recipe objects** and set it to receive many fields: `serializer = RecipeSerializer(recipes, many=True)`,
  - with all that let's **make an assertions** and first of all we expect it to return *HTTP_200_OK*, so type `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we also expect that our request's data will contain only one element, so let's make `self.assertEqual(len(res.data), 1)`,
  - finally, we we expect that the data from our GET request will be the same as the data we passed in to the serializer, so `self.assertEqual(res.data, serializer.data)`.

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implement feature for listing recipes

1. Head over to **serializer.py**:

- **import _Recipe_ model**,

- **create new class called RecipeSerializer**.

The fields that we're going to add are going to be the **id**, **title**, **ingredients**, **tags**, **time_minutes**, **price** and **link**.

- **Create Meta class** inside **RecipeSerializer**:
  - **point our model serializer to the correct model** so type `model = Recipe`,
  - **specify the fields** that we want to return in our serializer: `fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link')`,
  - **add the read-only fields** so `read_only_fields = ('id', )`.

  >Note: *the reason we do this is just to prevent the user from updating the ID when they may create or edit requests. We prevent updating the ID because it's best practice as we don't want to have the primary key changing unless we have a really good reason to change it*.

- now, because we want to filter our *ingredients* and *tags* only to the authenticated user we have to create **new class before RecipeSerializer called UserFilteredPrimaryKeyRelatedField** so we can use it to get access to the *ingredient* and *tag* querysets:

``` Python
class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """PrimaryKeyRelatedField which filters items by user."""

    def get_queryset(self):
        """Limit queryset to authenticated users items."""
        request = self.context.get('request')
        queryset = super().get_queryset()

        return queryset.filter(user=request.user)
```

- next what we need to do is we need to **define the primary key related fields** within our fields. Now because the **ingredients** and the **tags** are not actually part of the sterializer, because they're references to the *ingredient* and *tag* models we need to define these as special fields. We'll add two class variables to the top of our recipe sterilizer (before *Meta* class):
  - `ingredients = UserFilteredPrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())`,
  - `tags = UserFilteredPrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())`.

These two fields create a **UserFilteredPrimaryKeyRelatedField** and all this does it says *"allow many and list the objects from the given queryset"*, so the object with its *id* and *primary key id*. This is how we want it to appear when we're listing our recipes because we don't want it to include the full list of its content. We just wanted to list the *id*\s and then if we want to retrieve the full name of the ingredients we can use the *detail API*.

2. Head over to **views.py** and inside, let's create **RecipeViewSet** and base it on *viewsets.ModelViewSet*:

- **add serializer_class**: `serializer_class = serializers.RecipeSerializer`,

- **add queryset for Recipe**: `queryset = Recipe.objects.all()`,

- **add authentication_classes**: `authentication_classes = (TokenAuthentication, )`,

- **add permission_classes**: `permission_classes = (IsAuthenticated, )`.

- **add _get_queryset_ function** to limit the objects to the authenticated user: `return self.queryset.filter(user=self.request.user)`.

3. Head over to **urls.py** and **register new route** to our default router: `router.register('recipes', views.RecipeViewSet)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for retrieving recipe details

The recipe detail is going to allow us to retrieve a specific recipe returning more details than what the list recipes endpoint returns. The list recipe endpoint is more like a summary of all the recipes that we have and the detailed recipe endpoint is going to be for a specific recipe. The main difference in our app is that the list recipe endpoint is only going to return the ids of the tags and ingredients that are assigned to that recipe whereas the detail view will return the actual name and the id of each tag and ingredient that is assigned.

1. Head over to **test_recipe_api.py** and import **Ingredient**, **Tag** models and **RecipeDetailSerializer**.

2. Above **sample_recipe** helper function let's add **sample_tag** function and it's going to take a *user* and a *name* which default value let's set to *"Main course"*. This function will only return **created tag object**: `return Tag.objects.create(user=user, name=name)`.

>Note: *The reason we didn't use __**params__ is because there's only two fields required for the sample tag so we're just going to provide those fields and we're going to provide the username anyway and then we'll just provide the name as a default argument. So if we wanted to override the name then we have that option*.

3. Now let's do the same for **ingredients**, so let's create a new helper function called **sample_ingredient**, pass in *user* and *name* as a parameters and set default value for *name* to e.g. *"Cinnamon"*. Then simply **return a sample ingredient object**: `return Ingredient.objects.create(user=user, name=name)`.

4. Next we'll create a new **helper function for creating the URL**. So unlike the *RECIPES_URL* we're going to require an argument in our URL, which is the **ID of the recipe** we want to retrieve the detail for. So the *RECIPES_URL* may look something like */api/recipe/recipes/* to access the *recipe app* and *recipes endpoint* while the **detail** may look something like */api/recipe/recipes/1/* so with **recipe's id**. So we're going to need to pass in this argument whenever we create the **recipe detail URL**. We can't just assign it to a standard variable. What we need to do is create a function called **detail_url** with *recipe_id* parameter. This function will only return a **reverse to recipe-detail page** and as a second parameter we'll pass a *recipe_id* as a **args**:

`return reverse('recipe:recipe-detail', args=[recipe_id])` - the first argument is the name of the endpoint that the default router will create for our ViewSet, because we're going to have a **detail** action. The second argument is how we specify arguments with the *reverse* function, we just pass in **args** and then we pass in a list of the arguments we want to add. The reason it's a list is because we may have multiple arguments for a single URL.

5. Now we can add our tests, so scroll down to the **PrivateRecipeApiTests** and add new unit test called **test_view_recipe_detail**:

- **create a sample recipe** using our *sample_recipe* helper function: `recipe = sample_recipe(user=self.user)`,

- **assign a sample tag to this recipe**: `recipe.tags.add(sample_tag(user=self.user))`,

- **assign a sample ingredient to this recipe**: `recipe.ingredients.add(sample_ingredient(user=self.user))`,

- **create sample url** passing in a *recipe's id*: `url = detail_url(recipe.id)`,

- **create a HTTP GET request to our sample url**: `res = self.client.get(url)`,

- **pass our sample recipe to our serializer**: `serializer = RecipeDetailSerializer(recipe)`,

- finally we expect that the HTTP GET request's data will be the same as the data we pass in to the serializer, so let's **make an assertion**: `self.assertEqual(res.data, serializer.data)`.

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implement feature for retrieving recipe details

Next we're going to implement our **feature for retrieving the recipe detail**. We're going to start by **adding a RecipeDetailSerializer** and then we're going to **modify our ViewSet** to return this serializer when accessing the detail action in the ViewSet.

1. **Open up the serializers.py** file and we're going to make a modification of **RecipeSerializer** and we're going to change some of the fields that it returns.

>Note: *the difference between our __list-__ and our __detail-view__ would be that the __detail__ one would specify the actual __ingredients__ and the __tag__ objects that are assigned to that recipe. Whereas __RecipeSerializer__ is using the PrimaryKey related field so it's only going to return the primary key or the ID of the ingredient and the tags associated to that recipe*.

2. Below **RecipeSerializer** create new class called **RecipeDetailSerializer** and base it on **RecipeSerializer**. With Django REST framework we can **nest serializers** inside each other which means that we can type `ingredients = IngredientSerializer(many=True, read_only=True)` and with this `ingredients` variable we create the *related key object* that renders or returns the ingredients objects which we can then pass into our **IngredientSerializer** and convert it to this type of object. We **override _ingredients_ and _tags_ fields** because we want them to include all its fields, not only IDs.

3. Run tests and there should be only one error left and this is because we're not actually using **RecipeDetailSerializer** yet, we still need to implement this in our *views.py*.

4. **Head over to views.py** and override our **RecipeViewSet**'s *get_serializer_class*. This is a function that's called to retrieve the serializer class for a particular request.

We have a number of actions available by default in the **model ViewSet** e.g.:

- **list** which returns list of objects and in our case we want it to be default,

- **retrieve** in which case we want to return the detail sterilizer so when we call the **retrieve** action it serializes it using specified serializer instead of the default one.

So inside **RecipeViewSet** create new function called **get_serializer_class** and specify on what request's action we want to return our **RecipeDetailSerializer** then return this serializer:

``` Python
def get_serializer_class(self):
      """Return appropriate serializer class."""
      if self.action == 'retrieve':
        return serializers.RecipeDetailSerializer
```

5. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for creating recipes

We're going to create three tests:

- **test creating a basic recipe**,

- **tests creating a recipe with tags assigned**,

- **test creating a recipe with ingredients assigned**.

1. Head over to *test_recipe_api.py* and we're going to add all these tests to **PrivateRecipeApiTests**.

2. **Create test_create_basic_recipe** unit test:

- **create payload for our recipe** with sample *title*, sample *time_minutes* and sample *price* and these are the basic minimum fields required for creating a new recipe,

- **create HTTP POST request** to RECIPES_URL with *payload* passed in,

- now we expect it to return *HTTP_200_OK* code so let's type `self.assertEqual(res.status_code, status.HTTP_200_OK)`,

- now let's **retrieve created recipe** from database: `recipe = Recipe.objects.get(id=res.data['id'])`,

- with retrieved recipe we want to make sure that the data in our recipe is exactly the same as the data we passed in with *payload*, but while creating a *recipe* object the Django REST framework will return a dictionary so therefore to get access to the *recipe* object's values we have to use **dictionary keys** to iterate through both, *payload*'s and *recipe*'s elements and then use **getattr** function to get the *key value from recipe*:

``` Python
for key in payload.keys():
        self.assertEqual(payload[key], getattr(recipe, key))
```

3. **Create test_create_recipe_with_tags** unit test:

- **create two sample tags** assigned to the same *user*, so repeat this line twice: `tag1 = Tag.objects.create(user=self.user, name='<SAMPLE NAME>')`,

- **create payload for our recipe** which will contain sample *title*, our *tags*' IDs (use `tag1.id`), sample *time_minutes* and sample *price*,

- **create HTTP POST request for RECIPES_URL** and pass in payload to create this recipe in database,

- now we expect it to pass with *HTTP_200_OK* so `self.assertEqual(res.status_code, status.HTTP_200_OK)`,

- next, **get recipe object** from database: `recipe = Recipe.objects.get(id=res.data['id'])`,

- now, **get all tags from this recipe**: `tags = recipe.tags.all()`,

- with this **tags** variable we can **make some assertions**:
  - first, let's **check that the number of returned tags is exactly the same as the number of tags that we created**: `self.assertEqual(tags.count(), 2)`,
  - **check if the *tag1* is in the *tags*: `self.assertIn(tag1, tags)`,
  - **check if the *tag2* is in the *tags*: `self.assertIn(tag2, tags)`.

4. **Create test_creating_recipe_with_ingredients** unit test (just like with *tags*):

- **create two sample ingredients** assigned to the same *user*, so repeat this line twice: `ingredient1 = Ingredient.objects.create(user=self.user, name='<SAMPLE NAME>')`,

- **create payload for our ingredient** which will contain sample *title*, our *ingredients*' IDs (use `ingredient1.id`), sample *time_minutes* and sample *price*,

- **create HTTP POST request for RECIPES_URL** and pass in payload to create this recipe in database,

- now we expect it to pass with *HTTP_200_OK* so `self.assertEqual(res.status_code, status.HTTP_200_OK)`,

- next, **get recipe object** from database: `recipe = Recipe.objects.get(id=res.data['id'])`,

- now, **get all tags from this recipe**: `ingredients = recipe.ingredients.all()`,

- with this **ingredients** variable we can **make some assertions**:
  - first, let's **check that the number of returned ingredients is exactly the same as the number of ingredients that we created**: `self.assertEqual(ingredients.count(), 2)`,
  - **check if the *ingredient1* is in the *ingredients*: `self.assertIn(ingredient1, ingredients)`,
  - **check if the *ingredient2* is in the *ingredients*: `self.assertIn(ingredient2, ingredients)`.

5. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implement feature for creating recipes

The only thing that we need to change in our ViewSet to **enable creating recipes** is we need to add a *perform_create* function that assigns the user of the recipe to the current **authenticated user**.

1. **Open up our _views.py_** and locate our **RecipeViewSet**.

2. **Add a new function called perform_create** which is going to accept the *serializer* as argument.

3. Now, in order to create a recipe object for a **authenticated user** we'll use *save()* function for serializer object: `serializer.save(user=self.request.user)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command. Then, go to the browser and test our new *create recipe enpoint*.

#### Add tests for updating recipes

Next we're going to add some tests for updating our recipes. Since the update feature comes with the Django REST framework out the box for the *ModelViewSet* we technically don't need to create these tests because we're testing functionality that is already there.

We're going to add two tests to the bottom of **test_recipe_api.py**:

- **test a partial update** of an object using **HTTP PATCH** method,

- **test a full update** of an object using **HTTP PUT** method.

1. **Create new unit test called test_partial_update_recipe**:

- **create sample recipe using sample_recipe function** and pass in a *user*: `recipe = sample_recipe(user=self.user)`,

- **add sample tag to this _recipe_ object using sample_tag** and pass in a *user*: `recipe.tags.add(sample_tag(user=self.user))`,

- **create new tag** because in order to partly update our *payload* with additional fields we have to replace already assigned tag to the recipe with this new tag: `new_tag = sample_tag(use=self.user, name='<SAMPLE NAME>')` and we type here a *name* to override the *name* which was set by default in **sample_tag** function,

- **create payload** to create recipe with given fields - sample *title* and *new_tag*'s ID: `payload = {'title': '<SAMPLE TITLE>', 'tags': [new_tag.id]}`,

- **create detail_url** and pass in a `recipe.id`,

- **create HTTP PATCH request to this url** but we don't have to assign this request to any variable,

- now, after we did *PATCH* request we partly updated our **sample tag** with **new_tag**, but our recipe still holds this **sample tag** so we have to make get refreshed data from database `recipe.refresh_from_db()`,

- with all that we can **make an assertions**:
  - so we expect the recipe's title to be exactly the same as the title we passed in with the payload, so let's type: `self.assertEqual(recipe.title, payload['title'])`,
  - **get all tags from our recipe**: `tags = recipe.tags.all()` and **check that there is only one tag assigned to the recipe**: `self.assertEqual(len(tags), 1)`,
  - **check that new_tag is in tags**: `self,assertIn(new_tag, tags)`.

2. **Create new unit test called test_full_update_recipe**:

- **create sample recipe** using **sample_recipe** helper function and pass in a *user*: `recipe = sample_recipe(user=self.user)`,

- **add sample tag to this recipe** using **sample_tag** helper function: `recipe.tags.add(sample_tag(user=self.user))`,

- so in order to test full update we'll use *HTTP PUT* request to update **sample tag** with the object created using **HTTP PUT** request to the **detail_url** and with **payload** passed in. So let's first **create a payload** and pass in a sample *title*, sample *time_minutes* and sample *price*: `payload = {'title': 'SAMPLE TITLE', 'time_minutes': SMPL_TIME_int, 'price': SMPL_PRICE_dec}`,

- then, **create detail URL** for our recipe using *detail_url*: `url = detail_url(recipe.id)`,

- **create HTTP PUT request to the detail page** and pass in a payload. We also don't need to assign this request to any variable,

- after updating **sample tag** with our *HTTP PUT* request we have to update the **recipe** variable with new tag object from our database: `recipe.refresh_from_db()`,

- with all this let's **make an assertions**:
  - **check it the recipe's title is exactly the same as the title from the payload**: `self.assertEqual(recipe.title, payload['title'])`,
  - **check if the recipe's time_minutes is exactly the same as the payload's**: `self.assertEqual(recipe.time_minutes, payload['time_minutes'])`,
  - **check if the recipe's price is exactly the same as the payload's**: `self.assertEqual(recipe.price, payload['price'])`,
  - **get all recipe's tags**: `tags = recipe.tags.all()` and **check that there is only one element in it**: `self.assertEqual(len(tags), 1)`.

3. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

## Add upload image endpoint

#### Add Pillow requirement

Before adding a **ImageField** to our **recipe** model we need to install the **pillow** Python package which is used for manipulating images which are uploaded in Python.

1. Start by making some changes to the **requirements.txt** file. Add a new dependency underneath *psycopg2*: `Pillow>=5.3.0<5.4.0`.

2. Next we'll make some modifications to our **Dockerfile**. So **Pillow** requires some Linux packages to be installed before we can successfully compile and install it using the *PIP package manager*:

- first, we'll update this line `RUN apk add --update --no-cache postgresql-client` to this `RUN apk add --update --no-cache postgresql-client jpeg-dev`, so we add the JPEG dev dependency to our permanent dependencies of our *Dockerfile*,

- next, we update this line `RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev` with this `RUN apk add --update --no-cache --virtual .tmp-build-deps \ gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev` so we add some temporary build dependencies that are required for installing the *Pillow* package.

3. Next we're going to make some **changes to the file structure** in our Docker container so we have a place where we can store the **static** and **media** files within our container without getting any permission errors, so inside **Dockerfile**, at the bottom of the file, above *adduser*:

- create two new directories:
  - `RUN mkdir -p /vol/web/media`,
  - `RUN mkdir -p /vol/web/static`.
  >Note: *we use __-p__ to create */vol/web* directories automatically*.

- then we leave line for creating user: `RUN adduser -D user`,

- next, add `RUN chown -R user:user /vol/` and it sets the ownership of all the directories (*-R* - recursively) within the volume directory to our custom user,

- finally add `RUN chmod -R 755 /vol/web` so the user can do everything with the directory and the rest can read and execute from the directory.

4. Save that file and open up *settings.py*, scroll down to the bottom and add:

- `MEDIA_URL = '/media/'`, so when we upload media files we have an accessible URL so that we can access them through our web server,

- `MEDIA_ROOT = '/vol/web/media'` and it simply tells Django where to store all the media files,

- `STATIC_ROOT = 'vol/web/static'` like with *MEDIA_ROOT*.

5. Next, we'll make some changes to the **core's urls.py** file and what we need to do is add a reference or a URL for our media files.

>Note: *by default the Django development server will serve static files for any dependencies in our project however it doesn't serve media files by default we need to manually add this in the URLs*.

- Add two more imports:
  - **settings** from *django.conf*,
  - **static** from *django.conf.urls.static*.

Then, after the *urlpatterns* add `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`. It makes the media URL available in our development server so we can test uploading images for our recipes without having to set up a separate web server for serving these media files.

6. Open up terminal, navigate to the project's folder and type `docker-compose build` of if it doesn't work type `sudo docker-compose build`.

#### Modify recipe model

Next we're going to modify our recipe model to accept an **ImageField**. We're going to start by adding the function that generates the name which we're going to call in the **ImageField** on the system after the image has been uploaded.

>Note: *whenever we upload a file to a Django model we need to make sure we change the name and we don't just use the same name that was uploaded. This is to make sure all the names are consistent and also to make sure that there are no conflicts with the name that we upload*.

We're going to generate a function which will create the path to the image on our system and we're going to use a **uuid** to uniquely identify the image that we assign to the **ImageField**.

1. We're going to start by adding some unit tests, so head over to the **core's test_models.py** file.

2. Import **patch** from *unittest.mock*.

3. Scroll down to the bottom and create new unit test called **test_recipe_file_name_uuid**, pass in **mock_uuid** as parameter and we're going to **mock the uuid function** from the default uuid library that comes with Python. We're going to **change the value that it returns** and then we're going to **call our function** and we're going to make sure that the string that is created for the path matches what we expect it to match with the sample UUID:

- add **patch decorator** before function definition so we type `@patch()` and pass in the path of the function that we're going to mock, which is *uuid.uuid4*,

- add the **mock uuid** to the parameters of our test: `uuid = 'test-uuid'` so with this we change the value of this uuid to pretty much sample text which is *test-uuid*,

- then we're going to mock the return value by doing `mock_uuid.return_value = uuid` which means that anytime we call this **uuid** for function that is triggered from within our test it will change the value override the default behavior and just return this *test-uuid* string that we set earlier,

- next we're going to call the function that we'll create after we've done the test and the function will return a *filepath*: `file_path = models.recipe_image_file_path(None, 'myimage.jpg')` and it accepts two parameters: one is the *instance* and we don't need to provide that here so we set it to *None* and second one is the file name of the original file,

- finally, we have to add what we expect this function to return, so we expect something like *uploads/recipe/<RAND_GEN_TXT>.jpg* and to do that simply type `exp_path = f'uploads/recipe/{uuid}.jpg'`,

- make an assertion to check if the *file_path* (which was created using function that we're going to write later) id exactly the same as our expected result *exp_path*: `self.assertEqual(file_path, exp_path)`.

4. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

5. Head over to **models.py** and import **uuid** and **os**.

6. Add new helper-function called **recipe_image_file_path** which will accept *instance* and *filename*:

- first, we want to get an extension from passed in *filename*: `ext = filename.split('.')[-1]` so we split whole *filename* by *"."* and we know that the last element in this list should be an extension, so we select it by typing *[-1]*,

- then we build our **filename** by typing `filename = f'{uuid.uuid4}.{ext}'`, so the first part is generated randomly by the *uuid4* function and then we simply add in an extension,

- finally, what we have to do is we simply return whole path by using `os.path.join()` function and passing in a **path** *uploads/recipe/* and the **filename**.

7. With **recipe_image_file_path** we can scroll down and add new field in our **Recipe model**: `images = models.ImageField(null=True, upload_to=recipe_image_file_path)` and we pass in the *null=True*, because this field is optional and *upload_to=recipe_image_file_path* and we don't use brackets because we want this to be a reference to our helper-function.

8. Save this file and **make migrations** using `docker-compose run --rm app sh -c "python manage.py makemigrations core"` or if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py makemigrations core"`. Then, let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add tests for uploading images to recipe

Now, that we have our **ImageField** available on our *Recipe* model, we can go ahead and add the API for uploading images. We're going to start by adding a few tests to test uploading images through our API.

1. Head over to **test_recipe_api.py**.

2. Import:

- **tempfile** which functions we will use to create a temporary file which we'll remove after we've used it,

- **os**,

- **Image** from *PIL* which is pretty much *Pillow* module and this will import our image class which will let us then create test images which we can then upload to our API.

3. Now, let's create a helper-function called **image_upload_url** which will accept *recipe_id* which we're going to need in order to upload an image and what this function does is it returns URL for recipe image. So we simply do `return reverse('recipe:recipe-upload-image', args=[recipe_id])` - we create this endpoint and pass in recipe's ID.

4. Scroll down to the bottom and we're going to add new **test class** because there's going to be some common functionality for the image upload test that we're going to want to repeat, so let's create new class called **RecipeImageUploadTests** and pass in an argument *TestCase*.

5. Then let's create a **setUp** function:

- **assign APIClient** to our client `self.client = APIClient()`,

- **create new user**: `self.user = get_user_model().objects.create_user()` and pass in a sample *email* and *password*,

- **authenticate our user**: self.client.force_authenticate(self.user),

- **create sample recipe**: `self.recipe = sample_recipe(user=self.user)` and the reason we do that is we're going to need the recipe already created in all our tests, so we don't have to create it every single time.

6. Create another helper-function called **tearDown** which is pretty much the opposite function to the **setUp** function - after all tests if clears an environment so deletes all test files, so in our case all images that were created for the testing purpose. After definition simply type `self.recipe.images.delete()`.

7. We're going to add two tests:

- **test uploading an image just as we would**:
  - test will be called **test_upload_image_to_recipe**,
  - we create **url** variable and assign a image URL to it using *image_upload_url* function: `url = image_upload_url(self.recipe.id)` which accepts recipe's ID and it uses a **sample recipe** from **setUp**,
  - next, type:
  ``` Python
  with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
          img = Image.new('RGB', (10, 10))
          img.save(ntf, format='JPEG')
          ntf.seek(0)
          res = self.client.post(url, {'images': ntf}, format='multipart')
  ```
  It creates a named temporary file on the system at a random location, then, we give it a suffix (in our case it's just an extension of an image). We use a *with* statement and use this **tempfile** as a *nts* (*Named Temporary File*), because, as it's *TEMPORARY FILE* it'll be gone after exiting the **with** statement. We create an *image* object which is `('RGB', (10, 10))` 10x10 black square. We save it as the *tempfile* we've created and with JPEG format. We use `ntf.seek(0)` to set Python to read it every time from the beginning. Then we simply create a **POST** request to the image's URL, as *payload* we pass in the **images** field from our models set to the **ntf**. We also have to pass in a `format='multipart'`, because we want to make a multi-part form request which means a form that consists of data. By default it would just be a form that consists of a JSON object and we actually want to post data.
  - next, we have to refresh our **recipe**'s data from database: `self.recipe.refresh_from_db()`,
  - then we check that it returns a *HTTP_200_OK*: `self.assertEqual(res.status_code, status.HTTP_200_OK)`,
  - we check if the field *'images'* is in the *res.data*: `self.assertIn('images', res.data)`,
  - finally, we check if the path to the image exists: `self.assertTrue(os.path.exists(self.recipe.images.path))`.

- **test uploading an invalid image** just to make sure that it returns a *HTTP_400_BAD_REQUEST*:
- test will be called **test_upload_image_bad_request**,
- we create **url** variable and assign a image URL to it using *image_upload_url* function: `url = image_upload_url(self.recipe.id)` which accepts recipe's ID and it uses a **sample recipe** from **setUp**,
- **create a POST request** to the created URL and as the *payload* we pass in the *'images'* field set to the sample text, just to see that it's invalid. We also put the *format='multipart'* at the end: `res = self.client.post(url, {'images': 'notimage'}, format='multipart')`,
- finally we check that the response was *HTTP_400_BAD_REQUEST*: `self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)`.

8. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Add feature to upload image

1. Head over to the **serializers.py** and add new serializer class called **RecipeImageSerializer** and base it on *serializers.ModelSerializer*. Inside let's create a **Meta** class and inside:

- specify model: `model = Recipe`,

- specify fields: `fields = ('id', 'images')`,

- specify read only fields: `read_only_fields = ('id', )`

2. Head over to the **views.py** and import:

- **action** from *rest_framework.decorators*,

- **Response** from *rest_framework.response*,

- **status** from *rest_framework*.

3. Scroll down to the **RecipeSerializer** and i.e. *get_queryset*, *get_serializer_class* or *perform_create* are actions that we overrode, these are all default actions, so if we didn't override them then they will just perform the default action. To add custom function we'll use this **action** decorator and we pass in define the methods that our action is going to accept and the method could be **POST**, **PUT**, **PATCH** or **GET**.

`@action(methods=['POST'], detail=True, url_path='upload-image')`

- `methods=['POST']` - we choose to make the action just **POST**. We're going to allow users to post an image to our recipe,

- `detail=True` - it says this action will be for the detail - **a specific recipe** - so we're going to only be able to upload images for recipes that **already exist**. We'll also use the *detail_url* that has the ID of the recipe in the URL so it knows which one to upload the image to,

- `url_path='upload-image'` - the path name for our URL and that will be the path that is visible within the URL.

4. Now, with this decorator let's define our function called **upload_image** and pass in *request* and *pk=None* as its parameters:

- **retrieve the recipe object**: `recipe = self.get_object()` it will get the default or the object that is being accessed based on the ID in the URL,

- **call the serializer**: `serializer = self.get_serializer()` and pass in *recipe* and *data=request.data*,

- **check if the serializer's data is valid** so we type `if serializer.is_valid():` and inside this *if* statement:
  - **save serializer**: `serializer.save()` and what that basically does is performs a save on the recipe model with the updated data,
  - then, let's simply return data from serializer and *HTTP_200_OK* code: `return Response(serializer.data, status=status.HTTP_200_OK)`.

- **if it's not valid** return response `return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)`.

5. Go to **RecipeViewSet** and inside **get_serializer_class** function add another *elif* to the *if* statement:

``` Python
elif self.action == 'upload_image':
        return serializers.RecipeImageSerializer
```

just to handle an action of **uploading an image**. We want the Django REST framework to know which serializer to display in the browsable API.

6. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command. Then, go to the browser and test our new *upload image enpoint*.

## Add filtering

Next we're going to add the ability to **filter recipes by tags or ingredients**. This will make it really easy for users to find recipes if they want to find a recipe that has particular ingredients in it or matches particular tags. We're going to start by **creating unit tests** to test our filtering mechanism and then we're going to go ahead and **implement the filtering feature** to our API.

#### Add tests for filtering recipes

1. Head over to *recipe/tests/test_recipe_api.py* and at the bottom of the test case **add a new test called test_filter_recipes_by_tags** to test returning recipes with specific tags.

2. Start by **creating three recipes** and two of them are going to have tags assigned and one of them is not going to have the tags assigned. Then **make the request** with the filter parameters for the tags and ensure that the results returned match the ones with the tags and exclude the one without the tags:

``` Python
    recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
    recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
    tag1 = sample_tag(user=self.user, name='Vegan')
    tag2 = sample_tag(user=self.user, name='Vegetarian')
    recipe1.tags.add(tag1)
    recipe2.tags.add(tag2)
    recipe3 = sample_recipe(user=self.user, title='Fish and chips')

    res = self.client.get(
        RECIPES_URL,
        {'tags': f'{tag1.id},{tag2.id}'}
    )
```

If we want to filter by tags we simply pass a get parameter with a comma separated list of the tag IDs that we wish to filter by.

3. **Serialize the recipes** and **check if they exist in the returned responses** so we expect the first two recipes to be returned so we'll do *assertNotIn* for the third one:

``` Python
    serializer1 = RecipeSerializer(recipe1)
    serializer2 = RecipeSerializer(recipe2)
    serializer3 = RecipeSerializer(recipe3)

    self.assertIn(serializer1.data, res.data)
    self.assertIn(serializer2.data, res.data)
    self.assertNotIn(serializer3.data, res.data)
```

4. Now we'll do the same for ingredients, so after *test_filter_recipes_by_tags* **create new test called test_filter_recipes_by_ingredients**.

5. Start by **creating three recipes** and two of them are going to have ingredients assigned and one of them is not going to have the ingredients assigned. Then **make the request** with the filter parameters for the ingredients and ensure that the results returned match the ones with the ingredients and exclude the one without the ingredients:

``` Python
    recipe1 = sample_recipe(user=self.user, title='Posh beans on toast')
    recipe2 = sample_recipe(user=self.user, title='Chicken cacciatore')
    ingredient1 = sample_ingredient(user=self.user, name='Feta cheese')
    ingredient2 = sample_ingredient(user=self.user, name='Chicken')
    recipe1.ingredients.add(ingredient1)
    recipe2.ingredients.add(ingredient2)
    recipe3 = sample_recipe(user=self.user, title='Steak and mushrooms')

    res = self.client.get(
        RECIPES_URL,
        {'ingredients': f'{ingredient1.id},{ingredient2.id}'}
    )
```

To filter by ingredients we pass in get parameter with comma separated ingredients' IDs.

6. Next, **serialize the recipes** and **check if they exist in the returned responses** so we expect the first two recipes to be returned so we'll do *assertNotIn* for the third one:

``` Python
    serializer1 = RecipeSerializer(recipe1)
    serializer2 = RecipeSerializer(recipe2)
    serializer3 = RecipeSerializer(recipe3)

    self.assertIn(serializer1.data, res.data)
    self.assertIn(serializer2.data, res.data)
    self.assertNotIn(serializer3.data, res.data)
```

7. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implemented feature for filtering recipes

1. Head over to the *views.py* and add new **import Recipe from core.models**.

2. Now, we'll be modifying the **RecipeViewSet** to apply the filters if they are provided as get parameters. We're going to start by retrieving the comma separated string of ID's for our tags and ingredients and then we're going to convert that comma separated string to a list of actual integers and then we can apply the database query to filter our queryset by these provided tags and ingredients.

3. **Go to the get_queryset** method and start by retrieving the **query_params** for tags and ingredients:

``` Python
    tags = self.request.query_params.get('tags')
    ingredients = self.request.query_params.get('ingredients')
```

The request object has a variable called **query_params** which will be a dictionary containing all of the query parameters that are provided in the request. **query_params** is a dictionary so we can get an object using the **get** function and the item we're going to get is the *tags* and *ingredients*.

>Note: *if we have provided tags as a __query_param__ or a __query_string__ then it will be assigned to tags -  the actual string that we've provided. If not, then by default, the __get__ function returns __None__ so the tag's key doesn't exist in our __query_params__ then this will be set to __None__ so that way we can check if it's been provided or not*.

4. Assign our queryset `queryset = self.queryset`. The reason we do this is because we don't want to be reassigning our queryset with the filtered options. We want to actually reference it by queryset, apply the filters and return that instead of our main queryset.

5. Next, we need to create a function that will convert the IDs to list of integers. Above *get_queryset* method create new "private" function called **_params_to_ints** and pass in the **qs** parameter.

To speed up the whole process of converting list of strings to the list of integers we'll use the *list comprehension* so we simply type `return [int(str_id) for str_id in qs.split(',')]` inside our function.

6. Now, go back to the **get_queryset** method and if the *tags* or *ingredients* variable have any value assigned we'll convert these *tags* and *ingredients* using our **_params_to_ints** function and assign it to new variable, then filter **queryset** with our new variable.

``` Python
    if tags:
        tag_ids = self._params_to_ints(tags)
        queryset = queryset.filter(tags__id__in=tag_ids)

    if ingredients:
        ingredient_ids = self._params_to_ints(ingredients)
        queryset = queryset.filter(ingredients__id__in=ingredient_ids)
```

The **tags__id__in** is the Django syntax for filtering on **foreign key** objects. For example we have a tags field in our queryset in a **Recipe** queryset and that has a **foreign key** to the **tags** table which has an ID. So this basically says *"return all of the tags where the ID is in..."* e.g this converted list that we provided.

7. Final step is to change the return instruction in which we want to pass in filtered queryset, so it should look like this: `return queryset.filter(user=self.request.user)`.

8. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command. Then test new feature in the browser.

#### Add tests for filtering tags and ingredients

Next, we're going to add a feature to our API so we can filter tags and ingredients that are assigned to recipes only. We might want to use this filter if we're creating a front-end application that has a drop-down list that we can use to filter recipes by tags and ingredients. In that drop-down we might only want to see the list of tags and ingredients that are actually assigned to recipes already. We might want to exclude any tags and ingredients that are not assigned to any recipes. We're going to start by adding some unit tests.

1. Open up the *test_tags_api.py* and start by **importing the Recipe model**.

2. Scroll down to the bottom and add new test called **test_retrieve_tags_assigned_to_recipe** to test filtering tags by those assigned to recipes.

3. Now, let's **create two tags and one recipe**, **assign one them to a recipe**, the other tag leave unassigned:

``` Python
    tag1 = Tag.objects.create(user=self.user, name='Breakfast')
    tag2 = Tag.objects.create(user=self.user, name='Lunch')
    recipe = Recipe.objects.create(
        title='Coriander eggs on toast',
        time_minutes=10,
        price=5.00,
        user=self.user
    )
    recipe.tags.add(tag1)
```

4. Next **make HTTP GET request** to our API with the **assigned_only** filter set to 1, because we expect it to return an element. If there would be none therefore it would be set to 0.

``` Python
    res = self.client.get(TAGS_URL, {'assigned_only': 1})
```

We pass in this dictionary with the **get parameters** we want to apply to our **GET request**. We're going to call our filter **assigned_only** and if we pass in a one then this will be evaluated to *True* and it will filter by the tags that are *assigned_only*.

5. Then **serialize our tags** and **check that only the tag that is assigned to a recipe gets returned**:

``` Python
    serializer1 = TagSerializer(tag1)
    serializer2 = TagSerializer(tag2)

    self.assertIn(serializer1.data, res.data)
    self.assertNotIn(serializer2.data, res.data)
```

6. Create new test called **test_retrieve_tags_assigned_unique** which will test that the when we apply our filter returned tags will be unique. We do this because when we filter against a related object it can return one item per item that it is assigned to. If we have **two recipes** and we have **one tag** assigned to both of those recipes then when we filter by *assigned_only* those tags will return twice so it will return one for every item that it's assigned to. We need to make sure we return a distinct set of results.

7. Start by **creating a single tag** assigned to variable: `tag = Tag.objects.create(user=self.user, name='Breakfast')`.

8. **Create a secondary tag** that is not assigned to anything: `Tag.objects.create(user=self.user, name='Lunch')`. We don't assign it to any variable, because we only want to return the first tag.

9. **Create two recipes** and **add our tag** to them:

``` Python
    recipe1 = Recipe.objects.create(
        title='Pancakes',
        time_minutes=5,
        price=3.00,
        user=self.user
    )
    recipe1.tags.add(tag)
    recipe2 = Recipe.objects.create(
        title='Porridge',
        time_minutes=3,
        price=2.00,
        user=self.user
    )
    recipe2.tags.add(tag)
```

10. **Make HTTP GET request to our TAGS_URL** and we pass in the **assigned_only** field set to 1:

``` Python
    res = self.client.get(TAGS_URL, {'assigned_only': 1})
```

11. **Make an assertion** so we expect the data returned form our request will contain only one element:

``` Python
    self.assertEqual(len(res.data), 1)
```

12. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

13. Now head over to the **test_ingredients_api.py** and we'll add similar tests:

- **import Recipe model**,

- **test_retrieve_inredients_assigned_to_recipes**:

``` Python
def test_retrieve_inredients_assigned_to_recipes(self):
    """Test filtering ingredients by those assigned to recipes."""
    ingredient1 = Ingredient.objects.create(user=self.user, name='Apples')
    ingredient2 = Ingredient.objects.create(user=self.user, name='Turkey')
    recipe = Recipe.objects.create(
        title='Apple crumble',
        time_minutes=5,
        price=10.00,
        user=self.user
    )
    recipe.ingredients.add(ingredient1)
    res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
    serializer1 = IngredientSerializer(ingredient1)
    serializer2 = IngredientSerializer(ingredient2)

    self.assertIn(serializer1.data, res.data)
    self.assertNotIn(serializer2.data, res.data)
```

- **test_retieve_ingredient_assigned_unique**:

``` Python
def test_retieve_ingredient_assigned_unique(self):
    """Test filtering ingredients by assigned returns unique items."""
    ingredient = Ingredient.objects.create(user=self.user, name='Eggs')
    Ingredient.objects.create(user=self.user, name='Cheese')
    recipe1 = Recipe.objects.create(
        title='Eggs benedict',
        time_minutes=30,
        price=12.00,
        user=self.user
    )
    recipe1.ingredients.add(ingredient)
    recipe2 = Recipe.objects.create(
        title='Coriander eggs on toast',
        time_minutes=20,
        price=5.00,
        user=self.user
    )
    recipe2.ingredients.add(ingredient)
    res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
    self.assertEqual(len(res.data), 1)
```

14. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command.

#### Implemented feature for filtering tags and ingredients

Next we're going to implement our feature to filter by assigned tags and ingredients.

1. Start by heading over to *views.py*.

2. We've inherited both our **tags** and our **ingredients** ViewsSets from **BaseRecipeAttrViewSet**. Now, all we need to do is modify *BaseRecipeAttrViewSet*'s **get_queryset** to apply the filters **if the assigned_only query parameter has been passed in**.

3. Inside **get_queryset** method create new variable called **assigned_only** and we'll going to convert our query parameter to an **integer** first and then we're going to convert it to a **boolean**.

The reason we pass it in as an **integer** first is because our *assigned_only* value is going to be a **0** or a **1**. They're going to be the supported values for *assigned_only*.

We need to do is first convert that to an **integer** and then convert to a **boolean** otherwise if we do **boolean** of a **string** with **'0'** in it then that will convert to *True* which will mean *assigned_only* will be *True* regardless what we put in our string as far as any value has been passed in.

``` Python
    assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
```

If we run our tests without **assigned_only** set by default to **0** it would return an error `int argument must be a string not a non type`. This is because if *assigned_only* doesn't get a value passed then that will convert that to **None**. So this will return **None** and we can't convert an integer to **None**. That's why we add a comma after *assigned_only* and we're going to set a default value of **0**.

4. Next we want to use our filtered queryset so type: `queryset = self.queryset`.

5. Now we'll have condition **if assigned_only converts to true** then we'll do the filtering logic on our queryset to return these objects which recipe's field is not **Null**:

``` Python
    if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
```

This will return only *tags* or *ingredients* that are assigned to *recipes*.

6. Now we need to update the return to return filtered queryset:

``` Python
    return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
```

Now to make sure that returned objects are unique in the way that the items are not duplicated, so it won't return one item for every related item from queryset we add this **distinct()** at the end so it makes sure that the objects returned from queryset are unique.

7. Save file and head over to our terminal and let's run our unit tests using `docker-compose run --rm app sh -c "python manage.py test && flake8"` or, if it doesn't work `sudo docker-compose run --rm app sh -c "python manage.py test && flake8"` command. Then test new feature in the browser.
