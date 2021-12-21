# Devcamper Django y React

Devcamper es una aplicación web donde puedes encontrar bootcamps cerca de tu área. También puedes registrar tu propio bootcamp con todos sus cursos, o escribir reseñas para los bootcamps existentes. Esta aplicación se basa en el curso de desarrollo de APIs con Node de Brad Traversy, pero le di un giro y la implementé en Django y React.

## Backend
El backend de esta aplicación está hecha en Django y la API se creo usando el Django Rest Framework. Para toda la parte de autenticación de usuarios se usaron las librerías de Simple JWT y Djoser, y para la geolocalización se utilizó Geopy.

## Frontend
El frontend de esta aplicación está hecho en React. Se utilizó axios para manejar todas las requests y responses, todo el estado es manejado por medio de hooks. El código del frontend se encuentra en el siguiente repositorio.
https://github.com/Diegoav87/react-devcamper-api
