import json

from flask import Flask, request
import src.apis as apis
import src.controllers as controllers



"""
DEFINE APP
"""
app = Flask(__name__)

app.config["CACHE_TYPE"] = "null"

app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
)


"""
WITH CONTROLLERS
"""
@app.route('/')
def index():
	return controllers.index()

@app.route('/login')
def login():
	return controllers.login()

@app.route('/logout')
def logout():
	return controllers.logout()

@app.route('/login-post', methods=['POST'])
def login_post():
	username = request.args['username']
	password = request.args['password']
	return controllers.login_post(username, password)

@app.route('/attractions/')
def home():
	return controllers.home()

@app.route('/search', methods=['GET'])
def search():
	query = request.args['query']

	return controllers.home(query)

@app.route('/attractions/<int:id>')
def attracts(id):
	return controllers.attracts()



"""
API COLLECTIONS
"""
@app.route('/apis/attracts')
def get_attracts():
	return apis.get_attracts()

@app.route('/apis/attracts_index')
def get_attracts_index():
	return apis.get_attracts_index()
    
@app.route('/apis/attract/')
def get_attract():
	index_name = request.args.get('index_name')
	return apis.get_attract(index_name)

@app.route('/apis/images/')
def get_all_images_url():
	query = request.args.get('q')
	filenames = apis.get_all_images_url(query)

	return filenames

@app.route('/apis/images_index')
def get_index_images_url():
	data = apis.get_index_images_url()

	return data

@app.route('/apis/image/<int:index>')
def get_image(index):
	image = apis.get_image(index)

	return image

@app.route('/apis/attractions/<int:attract>')
def get_data_criteria(attract):
	data = apis.get_data_criteria(attract)

	return data

@app.route('/apis/attractions/<int:attract>/suggestions')
def get_suggestions(attract):
	data = apis.get_suggestions(attract)

	return data

@app.route('/apis/attractions/<int:attract>/sentiment')
def get_sentiment(attract):
	data = apis.get_sentiment(attract)

	return data



"""
MAIN EXCECUTION
"""
if __name__ == '__main__':
	app.run(debug=True)