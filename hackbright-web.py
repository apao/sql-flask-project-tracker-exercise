from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_grade_list = hackbright.get_student_projects_and_grades_by_github(github)
    project_title_url_list = []

    for project, grade in project_grade_list:
        url_for_project = "/project?title=%s" % (project)
        temp_tuple = (project, grade, url_for_project)
        project_title_url_list.append(temp_tuple)

    html = render_template("student_info.html", 
                           first=first, last=last, github=github, studentprojects=project_title_url_list)

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


@app.route("/project")
def get_project_info_from_db():
    """Show information about student's project."""

    title = request.args.get('title')
    project_title = hackbright.get_project_by_title(title)
    all_students_grades_by_project = hackbright.get_students_grades_by_project(title)

    html = render_template("project-info.html",
                            project_title=project_title,
                            all_students_grades_by_project=all_students_grades_by_project)

    return html




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
