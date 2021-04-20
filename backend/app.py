from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer
from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
from sqlalchemy_filters.filters import Operator
from sqlalchemy_filters.sorting import SORT_ASCENDING, SORT_DESCENDING
from database import DATABASE_CONNECTION_STRING
import re


# Setup the application components
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_STRING
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Read read the database meta
Base = automap_base()

# Load the view definition
Table("active_broadband_products", Base.metadata,
    Column("id", Integer, primary_key=True),
    autoload_with=db.engine)

Base.prepare(db.engine, reflect=True)

Product = Base.classes.active_broadband_products


#Setup marshalling of webservice models
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product


# The query param format patterns for search/sorting/pagination
FILTER_PARAM_PATTERN = re.compile("^({}):(.+)$".format('|'.join(Operator.OPERATORS.keys())))
SORT_PARAM_PATTERN = re.compile("^(({}|{}):)?(.+)$".format(SORT_ASCENDING, SORT_DESCENDING))


#Single resource for Product querying
@app.route('/products', methods=['GET'])
@cross_origin()
def products_resource():
    db_query = db.session.query(Product)

    # Default query parameters
    filter_queries = []
    sort_specs = []
    pagination_spec = {
        'page_number': 1,
        'page_size': 10
    }

    handle_search_params(request.args.items(),
                         filters=filter_queries,
                         sorts=sort_specs,
                         pagination=pagination_spec)

    #Apply query
    db_query = apply_filters(db_query, filter_queries)
    db_query = apply_sort(db_query, sort_specs)
    db_query, pagination_details = apply_pagination(db_query,
                                      page_number=pagination_spec['page_number'],
                                      page_size=pagination_spec['page_size'])

    # Respond with marshalled results
    response = make_response(ProductSchema(many=True).dumps(db_query))
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.headers['X-Page-Number'] = pagination_details.page_number
    response.headers['X-Page-Size'] = pagination_details.page_size
    response.headers['X-Num-Pages'] = pagination_details.num_pages
    return response


# Handle the query params included in the request url
def handle_search_params(search_params, filters=[], sorts=[], pagination=None):
    # Inspect each query param
    for q, v in search_params:

        # Handle sorting
        if 'sort' == q.lower():
            match = SORT_PARAM_PATTERN.match(v)
            if match:
                _, dir, field = match.groups()
                sorts.append({
                    'field': field.lower(),
                    'direction': dir.lower()
                })

        # Handle pagination
        elif q.lower() == 'page_size':
            pagination['page_size'] = int(v)

        elif q.lower() == 'page_number':
            pagination['page_number'] = int(v)

        # Handle Filtering
        else:
            match = FILTER_PARAM_PATTERN.match(v)
            if match:
                op, val = match.groups()
                filters.append({
                    'field': q.lower(),
                    'op': op,
                    'value': val
                })
    pass


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
