from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
db = SQLAlchemy(app)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)

@app.route('/', methods=['GET'])
def quiz():
    best_score = Grade.query.order_by(Grade.score.desc()).first()
    best_score_value = best_score.score if best_score else 0
    return render_template('quiz.html', best_score=best_score_value)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('username')
    question1 = request.form.get('question1')
    question2 = request.form.get('question2')
    question3 = request.form.get('question3')
    question4 = request.form.get('question4')

    score = 0
    if question1 == 'convolutional neural network': score += 25
    if question2 == 'object detection': score += 25
    if question3 == 'feature extraction': score += 25
    if question4 == 'image segmentation': score += 25

    new_grade = Grade(name=name, score=score)
    db.session.add(new_grade)
    db.session.commit()

    best_score = Grade.query.order_by(Grade.score.desc()).first()
    best_score_value = best_score.score if best_score else 0
    
    return jsonify({'name': name, 'score': score, 'best_score': best_score_value})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
