# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 21:07:43 2022

@author: hbora

@Title : SI507 Final Project - User input

@Description: This file calls the main function which returns to it the final 
list of restaurants. The list is displayed as a table in a flask using html
framework.
"""

from flask import Flask, render_template_string
from main import get_res

app = Flask(__name__)

@app.route('/')
def index():
    return 'Please to /results'

@app.route('/results')
def display():
    global res
    return render_template_string('''

    {% for record in labels  %}
        <table border=1>
            <tbody>
                {% for key, value in record.items() %}
                    <tr>
                        <td><b>{{key}}</b></td>
                        <td>&nbsp;&nbsp;{{value }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endfor %}

    ''', labels=res)

if __name__ == '__main__':
    global res
    res = get_res() #get final listings from main file
    app.run(debug=False) #display on flask app
