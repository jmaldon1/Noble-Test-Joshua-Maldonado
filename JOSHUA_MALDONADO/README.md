STEPS TO RUN PROJECT ON MAC:
1. Create a project folder

2. Install virtualenv into that folder:

    virtualenv -p python3 envname

3. Install nvm:
```
curl https://raw.githubusercontent.com/creationix/nvm/v0.25.0/install.sh | bash

close terminal and reopen

nvm -v
```

4. Install node 8.4.0 and npm 5.6.0 (havn't tested with other versions, but I assume any version greater than this will work):
```
nvm install 8.4.0

npm -v

node -v
```

5. Install AngularCLI
```
npm install -g @angular/cli
ng -v
```

6. Run VIRTUALENV:
```
virtualenv env
source env/bin/activate
```

7. Place the Flask_Angular4(backend) folder into the project folder

8. Place the static(front end) folder into Flask_Angular4/app
```
File Structure should look like this:

ProjectFolder/
	Flask_Angular4/
		/__pycache__
		/app
			/default
			/models
			/static
			...
		manage.py
		requirements.txt
		...
	env/

```

**MAKE SURE TO RENAME static(front_end) TO static**

9. Cd into:

    cd Flask_Angular4/

10. Install Requirements

    pip install -r requirements.txt

11. Run Server

    python manage.py runserver

12. Navigate to `localhost:5000`
    
    wait for server to say: wsgi starting up on http://127.0.0.1:5000

**not sure if anything below is needed, because server runs fine up to this point on my computer**

13. Cd into:

    cd app/static

14. Get node_modules
    
    npm install

15. In a second terminal window:

    ng build --dev --watch