from flask import Flask, render_template, request, redirect, url_for, flash, session
from student_management.models import *
from student_management import app


@app.route('/admin_subject_management')
def admin_subject_management():
    if 'user' in session:
        subjects = Subject.query.all()
        return render_template('pages/admin/admin_subject_management.html', subjects=subjects)
    else:
        return redirect(url_for('login'))


@app.route('/admin_subject_add')
def admin_subject_add():
    if 'user' in session:
        return redirect(url_for('admin_subject_management'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_subject_add_csv')
def admin_subject_add_csv():
    if 'user' in session:
        if session['grant_permission'] == True:
            return render_template('admin_subject_add_csv.html')
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_subject_search')
def admin_subject_search():
    if 'user' in session:
        return redirect(url_for('admin_subject_management'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_subject_edit')
def admin_subject_edit():
    if 'user' in session:
        return redirect(url_for('admin_subject_management'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_subject_delete')
def admin_subject_delete():
    if 'user' in session:
        return redirect(url_for('admin_subject_management'))
    else:
        return redirect(url_for('admin_login'))
