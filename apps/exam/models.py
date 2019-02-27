from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):

    def reg_validator(self, postData):
        errors={}
        #name errors
        if len(postData["first_name"]) < 1:
            errors["first_name_error"] = "Please enter first name!"
        elif len(postData["first_name"]) < 2:
            errors["first_name_error"] ="please enter valid first name!"
        elif not re.compile(r'^[a-zA-Z]{2,}$').match(postData["first_name"]):
            errors["first_name_error"] = "First Name should have letters only (not numbers or special characters)!"

        #last name errors
        if len(postData["last_name"]) < 1:
            errors["last_name_error"] = "Please enter last name!"
        elif len(postData["last_name"]) < 2:
            errors["last_name_error"] = "please enter a valid Last Name!"
        elif not re.compile(r'^[a-zA-Z]{2,}$').match(postData["last_name"]):
            errors["last_name_error"] = "Last Name should have letters only (not numbers or special characters)!"
        
        #email errors
        if len(postData["email"]) < 1:
            errors["email_error"] = "Email cannot be blank!"
        elif not re.compile(r'^[a-zA-Z0-9+-_]+@[a-zA-Z0-9+-_]+.[a-zA-Z0-9+-_]$').match(postData["email"]):
            errors["email_error"] = "Please enter vaild email form (eg. abc123@gmail.com)!"
        #email already exits errors
        elif len(User.objects.filter(email=postData["email"])) > 0:
            errors["dublicate_email"] = "Email already exits. Please use new email!"

        #password errors
        if len(postData["password"]) < 3:
            errors["password_error"] ="password needs to be more than 3 characters!"
        elif postData["password"] != postData["confirm_password"]:
            errors["password_error"] = "password did not match!"

        return errors

    def login_validator(self, postDATA):
        existing = User.objects.filter(email=postDATA["login_email"])
        errors={}
        #check if the email already exists
        if len(existing)==0:
            errors["one"]="Email is not register. Please register ar first!"
        #check if the password is correct
        elif not bcrypt.checkpw(postDATA["login_password"].encode(), existing[0].password.encode()):
            errors["two"] = "password is not correct!"
        
        return errors

class JobManager (models.Manager):
    def job_validator(self, postDATA):
        errors={}
        #title errors
        if len(postDATA["title_post"]) < 1:
            errors["title_error"] = "please enter Job Title!"
        elif len(postDATA["title_post"]) < 3:
            errors["title_error"] = "Job Tile must be more than 3 characters!"
        #description errors
        if len(postDATA["description_post"]) < 1:
            errors["description_error"] = "please enter description!"
        elif len(postDATA["description_post"]) < 10:
            errors["description_error"] = "Descption must be more than 10 characters!"

        #location error
        if len(postDATA["location_post"]) < 1:
            errors["location_error"] = "please enter a location!"
        
        return errors

    def edit_validator(self, postDATA):
        errors={}
        #title errors
        if len(postDATA["edit_one"]) < 1:
            errors["edit_title_error"] = "please enter Job Title!"
        elif len(postDATA["edit_one"]) < 3:
            errors["edit_title_error"] = "Job Tile must be more than 3 characters!"
        #description errors
        if len(postDATA["edit_two"]) < 1:
            errors["edit_description_error"] = "please enter description!"
        elif len(postDATA["edit_two"]) < 10:
            errors["edit_description_error"] = "Descption must be more than 10 characters!"

        #location error
        if len(postDATA["edit_three"]) < 1:
            errors["edit_location_error"] = "please enter a location!"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now =True)
    #jobs
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length =255)
    created_by=models.ForeignKey(User, related_name='created_jobs')
    claimed_by=models.ForeignKey(User, related_name='claimed_jobs', null=True)
    # user = models.ForeignKey(User, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManager()

