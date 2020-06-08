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

To run tests on a local machine, a database must be created and the path adapted in test_app.py.

## Endpoints

Here are examples of endpoint that does not require authorization.

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
{"category":"Breads",
 "recipes":[{"category":1,
             "description":"Symmetrical butter receptacle",
             "id":1,
             "instructions":"many",
             "name":"Sandwich bread",
             "time":"3h"}],
 "success":true}
```

### GET '/recipes/<recipe_id>/ingredients'

- Return a list of ingredients with quantity and measurement for given recipe.

```bash
curl https://le-mitron.herokuapp.com/recipes/1/ingredients
```

```json
{"ingredients":[{"measurement":"tbs",
                 "name":"Salt",
                 "quantity":"1/2"},
                {"measurement":"g",
                  "name":"Water",
                  "quantity":"300"}],
"success":true}
```

### POST '/recipes'

- Search for recipes containing the specified query in their name.
- Takes a json object containing the string to match.
- Return a list of recipes matching the search term.

```bash
curl -d "{\"searchTerm\":\"bread\"}" -H "Content-Type: application/json" -X POST https://le-mitron.herokuapp.com/recipes
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

## Endpoints with RBAC

Bellow are all the endpoints that only work provided the correct token.

Two roles have been created in this application:

- Admin: Have all the access.
- Editor: Can create and modify a recipe.

Here are Tokens for both of these:

ADMIN_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE2MjYwOTAsImV4cCI6MTU5MTcxMjQ5MCwiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIHBvc3Q6Y2F0ZWdvcmllcyBkZWxldGU6cmVjaXBlcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInBvc3Q6cmVjaXBlcyIsInBhdGNoOnJlY2lwZXMiLCJwb3N0OmNhdGVnb3JpZXMiLCJkZWxldGU6cmVjaXBlcyJdfQ.EgioqpPWxO9nUk2sxFGeJbFPNOauWT77K5mAoGxCrsJpIRRgTyIvbn65O6mh9Cd1IssBH4c9nnBBdRETieCY_aIMbexDU5vD6EmA3YRacH2A4SOoaiz19IEJJEvcalTKs_pYllN1X7DstB0ggNcFGydAhIrR2YgiFVWdDjHGjfvuqUbleFjDrJF6IxLqnp1cIUXHayIXMRwlScsQwQDXfJPS2DxDxTWFcpNXrQtrlotFyY2XTeX6nW3rgDX_t7BLKo4OHtA3nxzv4wfHU3yEX9JHPHoDPSJvsg519MBVqhhC8yrLsxuigRNnGamn_gvOnXY9xzltrSm1S20NtrQ4UA'

EDITOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE2MjYyMTMsImV4cCI6MTU5MTcxMjYxMywiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicG9zdDpyZWNpcGVzIiwicGF0Y2g6cmVjaXBlcyJdfQ.Dw7frMHaGpQLw5bZhp829xz1OOQ0tgXz7J8049Gx7yfNlcwanMlR6471lG01iF8auv3BxYkMHh6nyzSEjoHbzcXOc-Y207VxLe7QelceLIz8bgbVklDMeLWPSIfa6oBinLZp2oVYwVj2j5S2BwbRy2nQ10xqXzkBmAXWCn5DF4NPC2HzUs-DYjr744Mgs1MgIvQUo4YPA1-jQqbe8VEHZmTqkc_nWyGqJ2cIhlCnB8s3J_zMb_HJ5yiIir8EHpJk8smjmvqENSWYRFtHS5noE20o2Sl_ESlqxHGZeD0pOarS_kDcZTCLrAUiTisMoSaeyP-E4KjsUsXDsrKKVAgL7w'

### POST '/recipes/create'

- Create a new recipe with the data provided.
- Takes a json object as argument containing the name, time, category, description and instructions of the recipe.
- Return the success value.

### POST '/categories/create'

- Create a new category with the data provided.
- Takes a json object as argument containing the nam of the category.

### PATCH 'recipes/<recipe_id>/modify'

- Modify an existing recipe with provided information.
- Takes one or many section of the recipe i.e name, time, description.

### DELETE '/recipes'

- Delete a recipe.
