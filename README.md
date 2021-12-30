# Devcamper Django y React
Devcamper is a web application where you can find bootcamps near your area. You can also register your own bootcamp with all its courses, or write reviews for existing bootcamps. This app is based on Brad Traversy's API development course with Node, but I gave it a twist and implemented it in Django and React.

## Features
- Authentication
  - Login
  - Registration
  - Password Reset
  - User profile
  - Change password
  - Logout
- Bootcamps
  - CRUD for bootcamps
  - Search bootcamps within radius
  - Search filters
  - Pagination
  - Upload bootcamp image
- Courses
  - CRUD for courses
  - Average course cost for bootcamp
- Reviews
  - CRUD for reviews
  - Calculate average rating for bootcamp

## Backend
The backend of this application is made in Django and the API was created using the Django Rest Framework. The Simple JWT and Djoser libraries were used for the entire user authentication part, and Geopy was used for geolocation.

## Frontend
The frontend of this application is made in React. Axios was used to handle all the requests and responses, the entire state is handled through hooks. The frontend code is in the following repository.
[See the frontend repo](https://github.com/Diegoav87/react-devcamper-api)

[Live website](https://devcamper-django.netlify.app/)
