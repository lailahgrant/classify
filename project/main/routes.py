from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from utils import features
# from classify.models import 

main = Blueprint('main', __name__)

features = features()


@main.route("/")
@main.route("/home")
def home():
    # if current_user.is_authenticated:
    #     return render_template('home.html')
    # return render_template('login.html')
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


# @main.route("/startup_info", methods=['GET', 'POST'])
# @login_required
# def startup_info():
#     if request.method == "POST":
#         data = request.form
#         new = Company(
#                         title = data['title'],
#                         industry = data['industry'],
#                         funds_needed = data['funds_needed'],
#                         content = data['content'],
#                         user_id = current_user.id,
#                     )
#         new.save()
#         return redirect('/home')
#     else:
#         return render_template('startup_info.html')
@main.route("/startup_info", methods=['GET'])
# @login_required
def startup_info():
	# this function renders the information page
    # features = features()
    values = {} #create an empty dictionary to store cookies
    for feature in features:
        values[feature] = request.cookies.get(feature)

    # print("Session data: %s" % session.get('Year'))#work on sessions look at helper functions
    
    return render_template('startup_info.html', features=features, values=values)

@main.route('/classify')
@login_required
def get_value():
	
    print("\n:::FORM DATA:::")
    for f in features:
        if f in request.args:
            print(f, ":", request.args.get(f))
        else:
            print(f, ":", "(not submitted)")
    print(":::END FORM DATA:::")

    home_features = [request.args.get(i) or 0.0 for i in features]
    print(home_features)
    city =''
    for feature in features[15:]:
        print(request.args.get(feature))
        if request.args.get(feature)== "None":
            print(feature)
            city = feature

    chosen_city = city
    graph_city = 'city'+chosen_city.replace(' ',"_")
    session['city'] = graph_city
    print(graph_city)

    # change the strings recieved back to number
    home_features = [1 if feature == 'on' else feature for feature in home_features]
    home_features = [1 if feature == 'None' else feature for feature in home_features]

    # use the trained data to estimate the value 
    model = joblib.load('trained_model.pkl')
    # model = joblib.load('reg_model.pkl')#data type error
    # model = joblib.load('knn_model.pkl')
    predicted = model.predict([home_features])


    # format the results of the prediction
    predicted = round(predicted[0],2)
    predicted = "{:,}".format(predicted)

    resp = make_response(render_template('home_value.html', predicted=predicted, chosen_city=chosen_city))

    # set cookies (giving the user previous info entered)
    for feature in features:
    	feature_value = request.args.get(feature) #get value given by user
    	if feature_value:
    		resp.set_cookie(feature, feature_value) #set the cookie to feature value

    session['Year'] = request.args.get('year_built')
    

    return resp
