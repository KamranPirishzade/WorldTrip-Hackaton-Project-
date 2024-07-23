from flask import Flask, render_template, request, redirect, url_for,session,jsonify
import openai

app = Flask(__name__)
app.secret_key='chatgpt'

openai.api_key = 'YOUR-API-KEY'

users = {
    "john.doe@example.com": {
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    },
    "jane.smith@example.com": {
        "first_name": "Jane",
        "last_name": "Smith",
        "password": "password456"
    },
    "alice.jones@example.com": {
        "first_name": "Alice",
        "last_name": "Jones",
        "password": "password789"
    }
}

@app.route('/')
def home():
    if session.get('username'):
        return render_template('index.html',username=session.get('username'))
    else:
        return render_template('index.html',username=None)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        username = f"{first_name} {last_name}"
        session["username"]=username

        # Save user to the dictionary (in a real application, save to the database)
        users[email] = {'first_name': first_name, 'last_name': last_name, 'password': password}


        return redirect(url_for('user_home', username=username))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            username = f"{users[email]['first_name']} {users[email]['last_name']}"
            session["username"] = username
            return redirect(url_for('user_home', username=username))
        else:
            error="Wrong email or password!"
            return render_template('login.html',error=error)

    return render_template('login.html')

@app.route('/user_home/<username>')
def user_home(username):
    return render_template('user_home.html', username=username)

@app.route('/about')
def about():
    return render_template('about.html',username=session.get('username'))

@app.route('/help_center')
def help_center():
    return render_template('help-center.html',username=session.get('username'))


@app.route('/ai_planner')
def ai_planner():
    return render_template('ai.html', username=session.get('username'))

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    
        generated_text = response['choices'][0]['message']['content'].strip()
        return jsonify({'text': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


