from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from demo.models import Server, MongoHealthHack, db
from flask.ext.mongoengine.wtf import model_form
import datetime
import platform

health = Blueprint('health', __name__, template_folder='templates')

class HealthView(MethodView):
    def get(self):
        try:
            MongoHealthHack.objects.all().delete()
        except:
            return render_template('maintenance.html')

        # Update that we've seen this host
        try:
            server = Server.objects.get(servername=platform.node())
        except db.DoesNotExist:
            server = Server(servername=platform.node())
        except db.MultipleObjectsReturned:
            Server.objects.filter(servername=platform.node()).delete()
            server = Server(servername=platform.node())

        server.last_checkin = datetime.datetime.now()
        server.save()


        web_servers = Server.objects.all()

        servers = []
        for web_server in web_servers:
            server = {}
            server['server_name'] = web_server.servername
            server['last_checkin'] = web_server.last_checkin

            current_time = datetime.datetime.now()
            warning_time = datetime.timedelta(0,20)
            critical_time = datetime.timedelta(0,40)

            time_delta = current_time - server['last_checkin']

            if time_delta > critical_time:
                server['alert_level'] = 'danger'
            elif time_delta > warning_time:
                server['alert_level'] = 'warning'
            else:
                server['alert_level'] = 'info'

            servers.append(server)

        return render_template('servers.html', servers=servers)

class LbHealthCheckView(MethodView):
    def get(self):
        try:
            MongoHealthHack.objects.all().delete()
            return 'OK'
        except:
            return 'Failure'

# Register the urls
health.add_url_rule('/', view_func=HealthView.as_view('health'))
health.add_url_rule('/healthcheck', view_func=LBHealthCheckView.as_view('health'))
