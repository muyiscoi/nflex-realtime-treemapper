import jinja2
from jinja2 import Template

def get_color(value, max=100):
    return "hsl({},50%,50%)".format((1 - value/max) * 120)


e = jinja2.Environment()
e.globals['get_color'] = get_color

"""Render stuff"""
def render(data):
    template_str = """<!-- Table of the 10 servers with most CPU -->
    <style>
        .clearfix:after {
          content: "";
          display: table;
          clear: both;
        }

        .application {
          padding: 5px;
          border: 1px solid #fff;
        }

        .application_header {
          width: 100%;
          float: left;
        }

        .application__body {
          width: 100%;
          float: left;
          clear: both;
          padding-top: 10px;
        }

        .application__item {
          float: left;
          clear: both;
          width: 100%;
          padding: 5px;
        }
    </style>
    <div class="application clearfix">
        <div class="application__header">
          <span class="title">{{data.application_name}}</span>
        </div>
        <div class="application__body">
            <div class="treemap">
                {% for item in data['children'] %}
                <div class="application__item" style="background-color: {{get_color(item.value)}}">
                  <span class="name">{{item.name}}</span>
                  <span class="stats">{{item.label}}: {{item.value}} {{item.unit}}</span>
                </div>
                {% endfor%}
            </div>
        </div>
    </div>
    """

    template = e.from_string(template_str);
    return template.render(data=data);

def test_render():
    data = { 'application_name': 'Glen'}
    items = []
    metric = 'CPU'
    for i in range(10):
        item = {
            'name': 'item %d' % i,
            'label': metric,
            'value': (10.0 * i)
        }
        items.append(item)

    data['children'] = items;
    print(data)
    return render(data)
