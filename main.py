from datetime import datetime, timedelta
from query import get_resources_for_application, get_metrics
import operator
import re


RULE = {
    "application": "CMP (Core)",
    "rule": {
        "type": "spike",
        "metric": "cpu-usage",
        "value": 10,
        "child_metric": "docker-cpu-usage.*",
    }
}


def get(event, context):
    end = datetime.utcnow()
    start = end - timedelta(minutes=20)

    name = RULE.get("application")
    name = re.sub(r'([()])', r'\\\1', name)
    resources = get_resources_for_application(context, name)
    rule = RULE["rule"]
    data = {}
    for resource in resources:
        data[resource['id']] = r = {}
        r['name'] = resource['base']['name']
        if rule["type"] == "spike":
            metric = rule['metric']
            metrics = get_metrics(context,
                                  resource['id'],
                                  metric,
                                  start,
                                  end)
            r['metrics'] = metrics
            points = metrics[0]['values'][-2:]
            values = map(operator.itemgetter('value'),
                         points)
            if (values[1] - values[0]) > rule['value']:
                child_metrics = get_metrics(context,
                                            resource['id'],
                                            rule['child_metric'],
                                            start,
                                            end)
                r['child_metrics'] = child_metrics

    return data
