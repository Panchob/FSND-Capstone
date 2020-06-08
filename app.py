import os
from flask import Flask, request, abort, jsonify
from models import *
from flask_cors import CORS
from auth.auth import requires_auth, AuthError

RECIPE_PER_PAGE = 3


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        return response

    @app.route('/')
    def hello():
        return "This is the landing page of Le Mitron.\
        Front End is comming soon!"

    @app.route('/recipes')
    def retrieve_recipe():
        page = request.args.get('page', 1, type=int)

        try:
            selection = Recipe.query.order_by(Recipe.id).\
                        paginate(page, RECIPE_PER_PAGE).items
        except:
            abort(404)

        if len(selection) == 0:
            abort(404)

        recipes = [recipe.format() for recipe in selection]
        return jsonify({
            'success': True,
            'recipe': recipes,
        })

    @app.route('/recipes', methods=['POST'])
    def search_recipes():
        body = request.get_json()

        searchTerm = body.get("searchTerm", None)
        search_results = Recipe.query.\
            filter(Recipe.name.ilike("%{}%".format(searchTerm))).all()

        recipes = [recipe.format() for recipe in search_results]

        return jsonify({
            'success': True,
            'recipes': recipes,
        })

    @app.route('/recipes/create', methods=['POST'])
    @requires_auth('post:recipes')
    def create_new_recipe(payload):
        body = request.get_json()

        name = body.get('name', None)
        category = body.get('category', None)
        time = body.get('time', None)
        description = body.get('description', None)
        instructions = body.get('instructions', None)

        try:
            new_recipe = Recipe(name, time, description,
                                instructions, category)
            db.session.add(new_recipe)
            db.session.commit()

            return jsonify({
                'success': True,
                'created': new_recipe.id
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
    @requires_auth('delete:recipes')
    def delete_recipe(payload, recipe_id):
        try:
            recipe = Recipe.query.\
                     filter(Recipe.id == recipe_id).one_or_none()

            if recipe is None:
                abort(404)

            db.session.delete(recipe)
            db.session.commit()

            return jsonify({
                'success': True,
                'deleted': recipe_id
            })

        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    @app.route('/categories/create', methods=['POST'])
    @requires_auth('post:categories')
    def create_new_category(payload):
        body = request.get_json()

        name = body.get('name', None)

        try:
            new_category = Category(name)
            db.session.add(new_category)
            db.session.commit()
            return jsonify({
                'success': True,
                'created': new_category.id
            }), 200
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/categories')
    def retrieve_categories():
        selection = Category.query.all()
        categories = [category.format() for category in selection]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/categories/<category_id>/recipes')
    def list_recipe_from_category(category_id):

        selection = Recipe.query.\
            filter(Recipe.category == category_id).all()
        recipes = [recipe.format() for recipe in selection]
        category = Category.query.get(category_id)

        if category is None:
            abort(404)

        return jsonify({
            'success': True,
            'recipes': recipes,
            'category': category.name
        })

    @app.route('/recipes/<recipe_id>/ingredients')
    def list_ingredients_from_recipe(recipe_id):

        selection = Quantity.query.\
            filter(Quantity.recipe_id == recipe_id).all()

        if selection is None:
            abort(404)

        ingredients = []
        for s in selection:
            ingredient = {
                'name': Ingredient.query.get(s.ingredient_id).name,
                'quantity': s.quantity,
                'measurement': Measurement.query.get(s.measurement_id).name
            }
            ingredients.append(ingredient)

        return jsonify({
            'success': True,
            'ingredients': ingredients
        })

    @app.route('/recipes/<int:recipe_id>/modify', methods=['PATCH'])
    @requires_auth('patch:recipes')
    def modify_recipe(payload, recipe_id):
        body = request.get_json()

        try:
            recipe = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()
            if not recipe:
                abort(404)

            if 'name' in body:
                recipe.name = body.get('title')

            if 'time' in body:
                recipe.time = body.get('time')

            if 'description' in body:
                recipe.description = body.get('description')

            if 'instructions' in body:
                recipe.instructions = body.get('instructions')

            if 'category' in body:
                recipe.category = body.get('category')

            db.session.commit()

            return jsonify({
                'success': True,
                'recipe': recipe.format()
            })

        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "ressource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
