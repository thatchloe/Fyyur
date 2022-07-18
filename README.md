Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.




## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv**  
 * **SQLAlchemy ORM** 
 * **PostgreSQL** 
 * **Python3** and **Flask** 
 * **Flask-Migrate** 
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies
**HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/)  
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

## Development Setup:

1. **Install the dependencies:**
```
pip install -r requirements.txt
```

2. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

3. **Verify on the Browser**<br>
[http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

## References : 
Udacity Fullstack Web development Nanodegree
