from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
# from classify.models import 

main = Blueprint('main', __name__)


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
@login_required
def startup_info():
	# this function renders the information page
    
    values = {} #create an empty dictionary to store cookies
    for feature in features:
        values[feature] = request.cookies.get(feature)

    print("Session data: %s" % session.get('Year'))#work on sessions look at helper functions
    
    return render_template('startup_info.html', features=features, values=values)