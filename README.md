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

```json
{"categories":[{"name":"Breads"},{"name":"Cakes"}],"success":true}
```

### GET '/recipes'

- Returns a list of recipe object.
- The result of this endpoint is paginated in groups of 3. A request argument may be entered to specify a specific page.

```bash
curl https://le-mitron.herokuapp.com/recipes
```

```json
{"recipe":[{"category":1,
            "description":"Symmetrical butter receptacle",
            "id":1,
            "instructions":"many",
            "name":"Sandwich bread",
            "time":"3h"
            },
            {"category":2,
            "description":"Unworthy fruits second chance",
            "id...
```

### GET 'categories/<category_id>/recipes'

- Return a list of all recipe in that category

```bash
curl https://le-mitron.herokuapp.com/categories/1/recipes
```

```json
{"category":"Breads","recipes":[{"category":1,"description":"Symmetrical butter
                    receptacle","id":1,"instructions":"many","name":"Sandwich bread","time":"3h"}],"success":true}
```

### GET '/recipes/<recipe_id>/ingredients'

- Return a list of ingredients with quantity and measurement for given recipe.

```bash
curl https://le-mitron.herokuapp.com/recipes/1/ingredients
```

```json
{"ingredients":[{"measurement":"tbs","name":"Salt","quantity":"1/2"},{"measurement":"g","name":"Wat
                    er","quantity":"300"}],"success":true}
```

### POST '/recipes'

- Search for recipes containing the specified query in their name.
- Takes a json object containing the string to match.
- Return a list of recipes matching the search term.

```bash
curl -d "{\"searchTerm\":\"bread\"}" -H "Content-Type: application/json" -X POST https://le-mitron.herokuapp.com/recipes
```

### POST '/recipes/create'

- Create a new recipe with the data provided.
- Takes a json object as argument containing the name, time, category, description and instructions of the recipe.
- Return the success value.

```bash
curl -d -H "Content-Type: application/json" -X POST https://le-mitron.herokuapp.com/recipes/create
```

### POST '/category/create'

- Create a new category with the data provided.
- Takes a json object as argument containing the nam of the category.

```bash
curl -d "{\"name\": \"Pies\"}" -H "Content-Type: application/json" -X POST https://le-mitron.herokuapp.com/category/create
```

### PATCH 'recipes/<recipe_id>/modify'

- Modify an existing recipe with provided information.
- Takes one or many section of the recipe i.e name, time, description.

```bash

```

### DELETE '/recipes'

- Delete a recipe.

```bash
curl -X DELETE https://le-mitron.herokuapp.com/recipes/3
```
