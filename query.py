from datetime import datetime


def get_metrics(context,
                resource_id,
                metric,
                start,
                end,
                downsampling="mean"):
    params = {
        "start": fmt_date(start),
        "end": fmt_date(end),
        "downsampling": downsampling,
    }
    url = '/metrics/%s/resources/%s/points' % (metric, resource_id)
    resp = context.api.get(url, params=params)
    return resp.json()


def fmt_date(date):
    return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S.%fZ")


def get_resources_for_application(context, name):
    """
        Pass in an id for an application to get the list of
        resources that are part of this application
    """
    url = '/query'
    json = {
        "queries": [{
                "key": "connections.applications.name",
                "values": [name],
            }
        ],
        "metadata_queries": [],
        "attributes": [
            "id",
            "base.name"
        ],
        "group_by_attributes": [],
        "aggregations": []
    }

    response = context.api.post(url, json)
    return response.json()["items"]


def get_metrics_for_application(context, name, metric, start, end):
    resources = get_resources_for_application(context, name)
    resource_metrics = []
    for resource in resources:
        resource_metric = get_metrics(context,
                                      resource['id'],
                                      metric,
                                      start,
                                      end)
        resource_metrics.append(resource_metric)

    return resource_metrics
