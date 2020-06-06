# Le Mitron

"Mitron" is a french word meaning apprentice baker. Making bread is a hobby that I discovered recently and that I particularly love. I took the opportunity of this last project for the full stack Nanodegree program to create a site where I can store my recipes and my tips on my journey so far.

The Capstone project is a way to demonstrate all that I learned within the Udacity program in a single project. I had to start from scratch to create an application with the following prerequisites:

1. It's a Flask application.
2. The data is stored on a Posgresql database.
3. The database is created using SQLAlchemy and migrations are taken care of with Flask migrations system.
4. Authorizations are dealt with Auth0.
5. Endpoints were coded in TDD.
6. There is no front end (yet).
7. Application is deployed on Heroku.

Dependencies to run locally:

```bash
pip install -r requirements.txt
```

## Endpoints

### GET '/categories'

- Fetches a list of all categories
- Request arguments: None

```bash
curl https://le-mitron.herokuapp.com/categories
```

### GET '/recipes'

- Returns a list of recipe object.
- The result of this endpoint is paginated in groups of 3. A request argument may be entered to specify a specific page.

```bash
curl https://le-mitron.herokuapp.com/recipes
```

### GET 'categories/<category_id>/recipes'

### GET '/recipes/<recipe_id>/ingredients'

### POST '/recipes'

### POST '/recipes/create'

### POST '/category/create'

### PATCH 'recipes/recipe_id/modify'

### DELETE '/recipes'
