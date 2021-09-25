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
