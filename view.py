import jinja2
from jinja2 import Template

def get_color(value, max=100):
    return "hsl({},50%,50%)".format((1 - value/max) * 120)

"""Render stuff"""
def render_block(data):
    template_str = """
    <div class="application clearfix">
        <div class="application__header">
          <span class="title">{{data.application_name}}</span>
        </div>
        <div class="application__body">
            <div class="treemap">
                {% for item in data['children'] %}
                <div class="application__item" style="background-color: {{get_color(item.value)}}">
                  <span class="name">{{item.name}}</span>
                  <span class="stats">{{item.label}}: {{item.value}}%</span>
                  <div class="application__children">
                        {% for child in item['children'] %}
                            <div class="application__item-child"  style="background-color: {{get_color(child.value)}}">
                                <div class="application__item-child-name">{{child.label}}</div>
                                <span class="stats">{{child.value}}%</span>
                            </div>
                        {% endfor%}
                  </div>

                </div>
                {% endfor%}
            </div>
        </div>
    </div>
    """

    template = e.from_string(template_str);
    return template.render(data=data);

e = jinja2.Environment()
e.globals['get_color'] = get_color
e.globals['render_block'] = render_block

def render_style():
    template_str = """
    <!-- Table of the 10 servers with most CPU -->
    <style>
        .metric_block {
            margin: 5px;
            float: left;
            width: 48%;
        }

        .clearfix:after {
          content: "";
          display: table;
          clear: both;
        }

        .application {
          padding: 5px;
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
          padding: 8px;
        }

        .application__item-child {
            border: 1px solid #000;
            width: 33%;
            float: left;
            padding: 4px;
        }

        .application__item-child-name {
            min-width: 96%;
            max-width: 96%;
            white-space: nowrap;
            text-overflow: ellipsis;
            overflow: hidden;
        }
    </style>
    """
    template = e.from_string(template_str);
    return template.render();


def render(datasets):
    template_str = """
    {% for data in datasets %}
    <div class="metric_block">
        {{ render_block(data) }}
    </div>
    {% endfor %}
    """
    template = e.from_string(template_str);
    return render_style() + template.render(datasets=datasets);


def test_render():
    data = { 'application_name': 'Glen'}
    items = [
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "b5fccd6e-60d4-4301-b98f-9d55e6bcd6da",
            "value": 2,
            "name": "cmp-ct-master"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "edd55db3-fe2b-4726-a919-2b5aa18d6d3d",
            "value": 0.7,
            "name": "cmp-ct-flex3"
        },
        {
            "name": "cmp-ct-services2",
            "value": 10.68,
            "label": "cpu-usage",
            "id": "4ba0941f-df88-427b-ac59-6e509154f8b8",
            "children": [],
            "unit": "percent"
        },
        {
            "name": "cmp-ct-backup",
            "value": 10.2,
            "label": "cpu-usage",
            "id": "e9f9e8eb-48d7-4451-a563-e04a44d1c5b9",
            "children": [],
            "unit": "percent"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "024d3b4e-1338-4b45-bf7f-3ddaf667e51c",
            "value": 1.1,
            "name": "cmp-ct-flex1"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "5e563725-2069-43ba-92c8-68d4f8bad246",
            "value": 0.4,
            "name": "cmp-ct-wp"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "b9c849c4-5413-4727-9861-46a06d6944cd",
            "value": 0.4,
            "name": "cmp-ct-flex4"
        },
        {
            "name": "cmp-ct-containers2",
            "value": 20.36,
            "label": "cpu-usage",
            "id": "21bd79e3-cbbf-41f2-94ee-e278da3078b4",
            "children": [
                {
                    "value": 72.26,
                    "name": "cmp-ct-containers2",
                    "unit": "percent",
                    "label": "Docker CPU usage [Trident]"
                },
                {
                    "value": 68.9,
                    "name": "cmp-ct-containers2",
                    "unit": "percent",
                    "label": "Docker CPU usage [Glass]"
                },
                {
                    "value": 38.2,
                    "name": "cmp-ct-containers2",
                    "unit": "percent",
                    "label": "Docker CPU usage [Babel]"
                },
                {
                    "value": 34.05,
                    "name": "cmp-ct-containers2",
                    "unit": "percent",
                    "label": "Docker CPU usage [SparkCustomerApi]"
                },
                {
                    "value": 30.58,
                    "name": "cmp-ct-containers2",
                    "unit": "percent",
                    "label": "Docker CPU usage [InfluxdbAdapter2]"
                }
            ],
            "unit": "percent"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "1a6144fe-4860-4c0b-9679-dc5d1d901db1",
            "value": 6.35,
            "name": "cmp-ct-services3"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "7e938cef-5bdf-49df-b36b-9aecfa99c1ac",
            "value": 7.61,
            "name": "cmp-ct-services1"
        },
        {
            "unit": "percent",
            "label": "cpu-usage",
            "id": "063511d7-6ae6-4949-bfdf-4c96ae951381",
            "value": 0.4,
            "name": "cmp-ct-flex2"
        },
        {
            "name": "cmp-ct-containers1",
            "value": 14.86,
            "label": "cpu-usage",
            "id": "4c012732-cd1f-421f-95b5-6a873953a873",
            "children": [],
            "unit": "percent"
        }
    ]

    data['children'] = items;
    print(data)
    return render([data, data])



def get(event, context):

    table = test_render()
    return {
        "html": table
    }
    pass
