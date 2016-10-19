from datetime import datetime, timedelta
from query import (
    get_resources_for_application,
    get_metrics,
    get_current_metrics
)
import operator
import re
from view import render


RULES = [
    {
        "application": "CMP (Core)",
        "rule": {
            "type": "threshold",
            "metric": "cpu-usage",
            "value": 10,
            "child_metric": "docker-cpu-usage.*",
        }
    },
    {
        "application": "CMP (Core)",
        "rule": {
            "type": "threshold",
            "metric": "memory-usage",
            "value": 10,
            "child_metric": "docker-memory-usage.*",
        }
    },
]


def get_data(context, app_name, rule, start, end):
    name = re.sub(r'([()])', r'\\\1', app_name)
    resources = get_resources_for_application(context, name)
    data = {}
    resource_ids = [r['id'] for r in resources]
    resource_names = {r['id']: r['base']['name'] for r in resources}
    current = get_current_metrics(context,
                                  resource_ids,
                                  rule['metric'])
    data = []
    for resource_id, point in current.items():
        r = {
            'id': resource_id,
            'name': resource_names[resource_id],
            'label': rule['metric'],
            'value': round(point['value'], 2),
            'unit': point['unit'],
        }
        if point['value'] > rule['value']:
            child_metrics = get_metrics(context,
                                        resource_id,
                                        rule['child_metric'],
                                        start,
                                        end)
            r['children'] = []
            for m in child_metrics:
                r['children'].append({
                    'name': r['name'],
                    'label': m['label'],
                    'unit': m['unit'],
                    'value': round(m['values'][-1]['value'], 2)
                })

            r['children'] = sorted(r['children'],
                                   key=operator.itemgetter('value'),
                                   reverse=True)[:5]

            data.append(r)

    return data


def get(event, context):
    end = datetime.utcnow()
    start = end - timedelta(minutes=10)
    datasets = []
    for rule in RULES:
        app_name = rule.get("application")
        data = get_data(context,
                         app_name,
                         rule.get('rule'),
                         start,
                         end)
        datasets.append({
            'application_name': app_name,
            'children': data
        })
    table = render(datasets)
    return {
        "html": table
    }
