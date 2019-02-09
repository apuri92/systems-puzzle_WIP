# Solution

## Connectivity 
In docker-compose.yml:
nginx has ports mapped the wrong way. Should be 8080:80 rather than 80:8080. Need to map 8080 on local machine to 80 on nginx to make localhost:8080 work. format is hostserver:dockercontainer
    
    nginx:
        image: "nginx:1.13.5"
        ports:
            - "8080:80"


Then, running container gives a bad gateway error. Getting error

    connect() failed (111: Connection refused) while connecting to upstream, client: 192.168.48.1, server: localhost, request: "GET / HTTP/1.1", upstream: "http://192.168.48.2:5001/", host: "localhost:8080"

Checking dockerfile, app.py, and flaskapp.conf. container is exposed on 5001, and flaskapp on 5001. but app.run(host='0.0.0.0') by default looks at port 5000 . Specify either port in app.run(host ='0.0.0.0',port=5001), or change the port container should expose to 5000, and flaskpp to 5000 

        app.run(host='0.0.0.0',port=5001)


Setup similar to 

	https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example


## Confirming writes to database
Access database:

    docker exec -tiu postgres systems-puzzle_wip_db_1 psql

within psql, connect to database, list relations, and print table contents:

    \c flaskapp_db
    \dt
    select * from items;

## Confirming reads from database
somthing wrong here. Command below is returning empty list. 
	
	db_session.query(Items).all()
	
Checking what is in list: 

	[<models.Items object at 0x7fd7e2d24208>, <models.Items object at 0x7fd7e2d24278>,....

can get properties of object added, so use length of list to get the current item added, and return that as success message. Other info can be printed out as well.


## Data validation
forms.py: Set quantity to integer field, and add a NumberRange validator with min=1
	
	quantity = IntegerField('quantity', validators=[NumberRange(min=1,message="Enter integer"),DataRequired()])

added else condition for form validation failing, and print out errors.

	def flash_errors(form):
		"""Flashes form errors"""
		print(form.errors)

Need to implement error message on same page...

--------------------------------------------------------------------------------------------------------



# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Introduction](README.md#introduction)
3. [Puzzle details](README.md#puzzle-details)
4. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
5. [FAQ](README.md#faq)

# Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

# Introduction

Imagine you're on an engineering team that is building an eCommerce site where users can buy and sell items (similar to Etsy or eBay). One of the developers on your team has put together a very simple prototype for a system that writes and reads to a database. The developer is using Postgres for the backend database, the Python Flask framework as an application server, and nginx as a web server. All of this is developed with the Docker Engine, and put together with Docker Compose.

Unfortunately, the developer is new to many of these tools, and is having a number of issues. The developer needs your help debugging the system and getting it to work properly.

# Puzzle details

The codebase included in this repo is nearly functional, but has a few bugs that are preventing it from working properly. The goal of this puzzle is to find these bugs and fix them. To do this, you'll have to familiarize yourself with the various technologies (Docker, nginx, Flask, and Postgres). You definitely don't have to be an expert on these, but you should know them well enough to understand what the problem is.

Assuming you have the Docker Engine and Docker Compose already installed, the developer said that the steps for running the system is to open a terminal, `cd` into this repo, and then enter these two commands:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:

    docker-compose up -d

At that point, the web application should be visible by going to `localhost:8080` in a web browser. 

Once you've corrected the bugs and have the basic features working, commit the functional codebase to a new repo following the instructions below. As you debug the system, you should keep track of your thought process and what steps you took to solve the puzzle.

## Instructions to submit your solution
* Don't schedule your interview until you've worked on the puzzle 
* To submit your entry please use the link you received in your systems puzzle invitation
* You will only be able to submit through the link one time
* For security, we will not open solutions submitted via files
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo

# FAQ

Here are some common questions we've received. If you have additional questions, please email us at `devops@insightdata.com` and we'll answer your questions as quickly as we can (during PST business hours), and update this FAQ. Again, only contact us after you have read through the Readme and FAQ one more time and cannot find the answer to your question.

### Which Github link should I submit?
You should submit the URL for the top-level root of your repository. For example, this repo would be submitted by copying the URL `https://github.com/InsightDataScience/systems-puzzle` into the appropriate field on the application. **Do NOT try to submit your coding puzzle using a pull request**, which would make your source code publicly available.

### Do I need a private Github repo?
No, you may use a public repo, there is no need to purchase a private repo. You may also submit a link to a Bitbucket repo if you prefer.

### What sort of system should I use to run my program (Windows, Linux, Mac)?
You should use Docker to run and test your solution, which should work on any operating system. If you're unfamiliar with Docker, we recommend attending one of our Online Tech Talks on Docker, which you should've received information about in your invitation. Alternatively, there are ample free resources available on docker.com.

### How will my solution be evaluated?
While we will review your submission briefly before your interview, the main point of this puzzle is to serve as content for discussion during the interview. In the interview, we'll evaluate your problem solving and debugging skills based off how you solved this puzzle, so be sure to document your thought process.

### This eCommerce site is ugly...should I improve the design?  
No, you should focus on the functionality. Your engineering team will bring on a designer and front-end developer later in the process, so don't worry about that aspect in this puzzle. If you have extra time, it would be far better to focus on aspects that make the code cleaner and easier to use, like tests and refactoring.

### Should I use orchestration tools like Kubernetes?
While technologies like Kubernetes are quite powerful, they're likely overkill for the simple application in this puzzle. We recommend that you stick to Docker Compose for this puzzle.

