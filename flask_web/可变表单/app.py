from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField


@app.route('/')
def test():
    class DynamicForm(FlaskForm):
        pass

    for i in range(0, 5):
        setattr(DynamicForm, 'form-' + str(i), StringField(i))

    form = DynamicForm()
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()
