import os
from flask import Flask, \
    render_template, request, send_file, redirect



def index():
    return render_template('dashboard.html')

def login():
    return render_template('login.html')

def logout():
    return redirect('/login')

def login_post(username, password):
    if username is not None and password is not None:
        return redirect('/')
    
    return render_template('login.html')

def home(query=None):
    if query is not None:
        return redirect(
            '/attractions/?q=' + query, code=302)

    return render_template('attractions.html')

def search():
    return render_template('index.html')

def attracts():
    return render_template('criteria.html')
