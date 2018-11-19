# def chart1(request):
#     """
#     lineChart page
#     """
#     start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
#     nb_element = 150
#     xdata = range(nb_element)
#     xdata = map(lambda x: start_time + x * 1000000000, xdata)
#     ydata = [i + random.randint(1, 10) for i in range(nb_element)]
#     ydata2 = map(lambda x: x * 2, ydata)

#     tooltip_date = "%d %b %Y %H:%M:%S %p"
#     extra_serie1 = {
#         "tooltip": {"y_start": "", "y_end": " cal"},
#         "date_format": tooltip_date,
#         'color': '#a4c639'
#     }
#     extra_serie2 = {
#         "tooltip": {"y_start": "", "y_end": " cal"},
#         "date_format": tooltip_date,
#         'color': '#FF8aF8'
#     }
#     chartdata = {'x': xdata,
#                  'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1,
#                  'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2}

#     charttype = "lineChart"
#     chartcontainer = 'linechart_container'  # container name
#     data = {
#         'charttype': charttype,
#         'chartdata': chartdata,
#         'chartcontainer': chartcontainer,
#         'extra': {
#             'x_is_date': True,
#             'x_axis_format': '%d %b %Y %H',
#             'tag_script_js': True,
#             'jquery_on_ready': False,
#         }
#     }
#     return render_to_response('govisewana/chart.html', data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
        """
        View to list all users in the system.

        * Requires token authentication.
        * Only admin users are able to access this view.
        """
        authentication_classes = (authentication.TokenAuthentication,)
        permission_classes = (permissions.IsAdminUser,)
        def get(self, request, format=None):
            """
            Return a list of all users.
            """
            user={"name":"sac", "age":12}
            usernames = [user.username for user in User.objects.all()]
            return Response(usernames)        
