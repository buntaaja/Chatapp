from flask import Flask, render_template
from wtform_fields import *
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure app
@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit(): # It will return True if the forms is submited through POST method
        return "Great success!"
    return render_template("index.html", form=reg_form)
#'postgres://fboecypywtrptr:0748b3a20a2fa3f0ef77dbbcb5c6d0a64022b55af2e6bc3bc52e912f5fa0383c@ec2-34-242-199-141.eu-west-1.compute.amazonaws.com:5432/d9vgh90ob3qi9f'

if __name__ == "__main__":
    app.run(debug=True)