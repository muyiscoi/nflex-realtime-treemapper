from datetime import datetime, timedelta
from query import (
    get_resources_for_application,
    get_metrics,
    get_current_metrics
)
import operator
import re


RULE = {
    "application": "CMP (Core)",
    "rule": {
        "type": "threshold",
        "metric": "cpu-usage",
        "value": 10,
        "child_metric": "docker-cpu-usage.*",
    }
}


def get(event, context):
    end = datetime.utcnow()
    start = end - timedelta(minutes=5)

    name = RULE.get("application")
    name = re.sub(r'([()])', r'\\\1', name)
    resources = get_resources_for_application(context, name)
    rule = RULE["rule"]
    data = {}
    resource_ids = [r['id'] for r in resources]
    resource_names = {
        r['id']: r['base']['name']
        for r in resources
    }

    current = get_current_metrics(context,
                                  resource_ids,
                                  rule['metric'])
    data = []
    """
    r = {'name':'', 'label':'', 'value': '', 'unit':'',
        children: list(m)}
    """
    for resource_id, point in current.items():
        r = {}
        r['id'] = resource_id
        r['name'] = resource_names[resource_id]
        r['label'] = rule['metric']
        r['value']  = point['value']
        r['unit']  = point['unit']
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
                    'value': m['values'][-1]['value']
                })

            r['children'] = sorted(r['children'],
                                    key=operator.itemgetter('value'),
                                    reverse=True)
        data.append(r)

    return data
