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


@main.route("/startup_info", methods=['GET', 'POST'])
@login_required
def business_plan():
    if request.method == "POST":
        data = request.form
        # new_plan = Bplan(
        #                 title = data['title'],
        #                 industry = data['industry'],
        #                 funds_needed = data['funds_needed'],
        #                 content = data['content'],
        #                 user_id = current_user.id,
        #             )
        # new_plan.save()
        return redirect('/home')
    else:
        return render_template('startup_info.html')


