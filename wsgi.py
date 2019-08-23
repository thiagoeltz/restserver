from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from elasticapm.contrib.flask import ElasticAPM
from flask_oauthlib.client import OAuth
import endpoint.register
import endpoint.next_integer
import endpoint.current_integer
import endpoint.retrieve_token
import endpoint.refresh

application = Flask(__name__)
application.config['ELASTIC_APM'] = {
'APP_NAME': 'thinkific',
'SERVICE_NAME': 'thinkific-apm',
'SECRET_TOKEN': 'vV7Mf1mvHaDwqjVqdc',
'SERVER_URL': 'https://2101c127879b4876897d931e5e37bfb3.apm.us-east-1.aws.cloud.es.io:443'
}
application.config['JWT_SECRET_KEY'] = '844-m64qc871jwt-secret-stringd931e5e37b'
application.config['PROPAGATE_EXCEPTIONS'] = True
application.config['GOOGLE_ID'] = "505980036844-m64qc87154ftahi26o8qibgv3ehjfs60.apps.googleusercontent.com"
application.config['GOOGLE_SECRET'] = "0Su4AWCDsfkThAKmv9Xer0pC"
application.debug = True
application.secret_key = 'development'
oauth = OAuth(application)
google = oauth.remote_app(
    'google',
    consumer_key=application.config.get('GOOGLE_ID'),
    consumer_secret=application.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
api = Api(application)
apm = ElasticAPM(application)
jwt = JWTManager(application)

api.add_resource(endpoint.register.UserRegistration, '/registration')
api.add_resource(endpoint.refresh.TokenRefresh, '/refresh')
api.add_resource(endpoint.retrieve_token.UserRetrieveToken, '/retrieve')
api.add_resource(endpoint.next_integer.IntegerVerifyNext, '/next')
api.add_resource(endpoint.current_integer.IntegerVerifyCurrent, '/current')


@application.route('/')
def index():
    if 'google_token' in session:
        return redirect(url_for('readme'))
    return redirect(url_for('login'))


@application.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@application.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@application.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    jsonify({"data": user_info.data})
    return redirect(url_for('index'))


@application.route('/read')
def readme():
    if 'google_token' in session:
        return render_template('readme.html')
    return redirect(url_for('login'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


if __name__ == '__main__':
    application.run()


