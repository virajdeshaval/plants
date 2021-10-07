from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        if request.method == 'POST':
            abort(405)

        # get the page argument off of a request
        page = request.args.get('page', 1, type=int)

        # As we defaulted to page 1, we will start with index 0
        # this is an index of the plant field from which index to start showing the page result
        # example, to show 10 things to show in a page
        # start with plant[0] and end at index plant[9].
        # for page = 2, start at index plant[10] and end at index plant[19]
        start = (page - 1) * 2
        end = start + 2
        # get all the plants information
        plants = Plant.query.all()

        # format the information that we got using the format method
        formatted_plants = [plant.format() for plant in plants]

        return jsonify({
            'success': True,
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants) 
        })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        # get specific plants
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:
            return jsonify({
            'success': True,
            'plant': plant.format()
        })

    return app

















    # @app.route('/plants', methods=['GET','POST'])
    # #@cross_origin
    # def get_plants():
    #     # Implement pagniation
    #     page = request.args.get('page', 1, type=int)
    #     start = (page - 1) * 10
    #     end = start + 10

    #     plants = Plant.query.all()
    #     formatted_plants = [plant.format() for plant in plants]
    #     return jsonify({
    #         'success': True,
    #         'plants':formatted_plants[start:end],
    #         'total_plants':len(formatted_plants)
    #         })

    # @app.route('/plants/<int:plant_id>')
    # def get_specific_plant(plant_id):
    #     plant = Plant.query.filter(Plant.id==plant_id).one_or_none()
    #     if plant is None:
    #         abort(404)
    #     else:   
    #         return jsonify({
    #             'success': True,
    #             'plant': plant.format()
    #         })