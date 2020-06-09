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

To run tests on a local machine, a database must be created and the path adapted in setup.sh.

```bash
pip install -r requirements.txt
source setup.sh
```

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

ADMIN_TOKEN ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE3MjA0NTIsImV4cCI6MTU5MTgwNjg1MiwiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIHBvc3Q6Y2F0ZWdvcmllcyBkZWxldGU6cmVjaXBlcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInBvc3Q6cmVjaXBlcyIsInBhdGNoOnJlY2lwZXMiLCJwb3N0OmNhdGVnb3JpZXMiLCJkZWxldGU6cmVjaXBlcyJdfQ.koQSFlpYII8eciSfibXn8Ol0_pv1-QhgnvaL5bWMQYNZck40Ohvr7SOMpJ71EWyuiOmJ1VqgQjF5ekmRtDIUef13FbLAwB32WYyURn04RPitMSAhsBM9ePJolqXPSG7_R80_48_sk9TjukN6Fn0s_CoDY_dDkI0U-7UIM-fZ1Ni8KmRbSYDzM8eF3HouFIDhJOPe2BQtzQi2eDtd1Mbo-D2skYtvzn3-X31_25PROFhADeUuMH_wyqeieuNpSYqCzkn9PeZjwNYKb30EjArqQZPhQsEYAC_Wp_70GbI8apHihD3gSKRpxss2w4OnqUp4tFr4Bve-T9g9b4YGeWmWcQ"

EDITOR_TOKEN ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE3MjAzODMsImV4cCI6MTU5MTgwNjc4MywiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicG9zdDpyZWNpcGVzIiwicGF0Y2g6cmVjaXBlcyJdfQ.dsJYYpQLNW2JbWBwKkEkVYYRYLVWZe8mdDkBeOqk7vfzvIO3buytJHvGV3L8-bhUOqVt7faSQdsBZJJLTBhWSxGgGM7N66vdmkKP6TkqRHfGBE989odJ7RFRmb25CAr9S7BFRS1Bo1lgBKo1aUTc_HgUqIPpILnfr41XD0-UViSHqVKKuX4IX5lUsfZy18DJeBQfyQb2MiYqIodpc91ENNYe6AWKYw5oVZp47vmlabDeoM1ZBHLV18B9s_k_4t8pVsI5tl1ImnZTgirXG-jJRswadsoddnPr6u18dLa3qjEnBn2G79MnZbACdR_X_YaarRCrARonZNqsPN16RxGUug"

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
