from datetime import datetime, timedelta


def get_metrics(metrics, context):
    end = datetime.utcnow()
    start = end - timedelta(minutes=5)
    resource_id = "2d16ab4e-68c5-449b-9608-7c67c570dac1"
    metric = "cpu-usage"
    params = {
        "start": fmt_date(start),
        "end": fmt_date(end),
        "downsampling": "max",
    }
    url = '/metrics/%s/resources/%s/points' % (metric, resource_id)
    resp = context.api.get(url, params=params)
    return resp.json()


def fmt_date(date):
    return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
