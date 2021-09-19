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

## Creating a core app

#### Preparing the environment

The first thing we're going to do is we're going to create a **core** app which will hold all of the central code that is important to the rest of the sub apps. It's going to create anything that is shared between one or more apps like migrations, database. We will put this all in the **core** module just so it's all in one place and it's very clear where the kind of central point of all these things is.

1. Delete *count.py* and *tests.py*.

2. Launch up a terminal and type `docker-compose run app sh -c "python manage.py startapp core"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py startapp core"`.

3. Inside *core* app folder delete *views.py* and *tests.py*.

4. Create a *tests* folder inside *core* app folder and create there *__init\__.py* file.

5. Go to the *settings.py* and add *core* to the **INSTALLED_APPS** list.

Now that we have our *core app* we'll create our custom user model. Since we're working with test-driven development we're going to write our test first and then we're going to implement our model afterwards.

#### Creating tests

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

2. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

##### Updating **create_user** method in **UserManager** class (rising ValueError)

1. To implement this feature in our models go to the *create_user* method and between creating user object and the doc-string type:

``` Python
if not email:
      raise ValueError('Users must have an email address!')
```

We raise a *ValueError* and pass there a message.

2. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.

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

6. Save this test file and let's head over to our terminal and let's run our unit tests using `docker-compose run app sh -c "python manage.py test"` or, if it doesn't work `sudo docker-compose run app sh -c "python manage.py test"` command.
