from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_grade_list = hackbright.get_student_projects_and_grades_by_github(github)
    html = render_template("student_info.html", 
                           first=first, last=last, github=github, items=project_grade_list)

    return html

    # return "%s is the GitHub account for %s %s" % (github, first, last)

@app.route("/student-search")
def get_student_form():
    """Show form to search for a student"""

    return render_template("student_search.html")


@app.route("/student-add-form")
def show_student_add_form():
    """Show form to add a new student"""

    return render_template("student_add.html")


@app.route("/student-added", methods=['POST'])
def add_student_from_form():
    """Add a student to the hackbright database."""

    first = request.form.get("first")
    last = request.form.get("last")
    github = request.form.get("github")

    hackbright.make_new_student(first, last, github)

    url_for_new_student = "/student?github=%s" % (github)

    html = render_template("student_show.html", first=first, last=last, github=github, url=url_for_new_student)

    return html





if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
