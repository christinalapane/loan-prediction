from flask import Flask, render_template, request
import loan as l
import pandas as pd
import names

app = Flask(__name__)

# code for dashboard

df = pd.read_csv('train.csv')


# client information
df_banking = pd.DataFrame().assign(Loan_ID=df['Loan_ID'], Income=df['ApplicantIncome'],
                                   Co_Income=df['CoapplicantIncome'], Loan_Amount=df['LoanAmount'],
                                   Term_Length=df['Loan_Amount_Term'], Property=df['Property_Area'],
                                   Loan_Status=df['Loan_Status'])

# adding names to clients for the dashboard
loan_id_list = list(df_banking.Loan_ID.unique())
names_list = []
for i in range(614):
    names_list.append(names.get_full_name())

df_banking.insert(1, 'Clients', names_list)
loan_missing = df_banking['Loan_Amount'].isnull()
term_missing = df_banking['Term_Length'].isnull()

df_banking.loc[loan_missing, 'Loan_Amount'] = 146.0
df_banking.loc[term_missing, 'Term_Length'] = 360


@app.route('/', )
def hello():
    return render_template('index.html')


@app.route('/statistics')
def stats():
    return render_template('statistics.html')


@app.route('/application')
def application():
    return render_template('application.html')


@app.route('/capstone')
def capstone():
    return render_template('Capstone.html')


@app.route('/status', methods=['POST', 'GET'])
def status():
    if request.method == 'POST' or request.method == 'GET':
        user = request.form['user']
        password = request.form['pass']
        data = df_banking
        if user == 'admin' and password == 'password':
            return render_template('status.html', user=user, tables=[data.to_html()], titles=[''])
        else:
            wrong = 'You do not have access to this page.'
            return render_template('login.html', wrong=wrong)


@app.route('/dashboard')
def dash():
    return render_template('status.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sub', methods=['POST'])
def submit():
    if request.method == 'POST':

        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        income = int(request.form['income']) / 10
        co = int(request.form['co'])
        loan = int(request.form['loan']) / 10
        term = request.form['term']
        credit = request.form['credit']
        property_type = request.form['property_type']

        # male = 1, female = 2
        # yes = 1 no = 2
        # grad = 1 no = 2
        # self employed = 1, not = 2
        # credit no =2, yes=1
        # dependents, 3 or more = 3
        # urban = 3, semi=2, rural =1

        if gender == 'm':
            g_count = 1
        else:
            g_count = 2

        if married == 'single':
            m_count = 2
        else:
            m_count = 1

        if dependents == "0":
            d_count = 0
        elif dependents == '1':
            d_count = 1
        elif dependents == '2':
            d_count = 2
        elif dependents == '3':
            d_count = 3

        if education == 'not':
            e_count = 2
        else:
            e_count = 1

        if employed == 'self':
            emp_count = 1
        else:
            emp_count = 2

        if term == '300':
            t_count = 300
        elif term == '360':
            t_count = 360
        elif term == '380':
            t_count = 380
        else:
            t_count = 480

        if credit == 'no':
            c_count = 2
        else:
            c_count = 1

        if property_type == 'rural':
            p_count = 1
        elif property_type == 'semi':
            p_count = 2
        else:
            p_count = 3

        to_predict_list = [g_count, m_count, e_count, emp_count, income, co, loan, t_count, p_count, d_count, c_count]
        result = l.loan_prediction(to_predict_list)

        if int(result) == 0:
            number = result
            prediction = 'You have been approved! '
        else:
            number = result
            prediction = ' You have unfortunately been denied'

        return render_template('sub.html', result=result, prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
