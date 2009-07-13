{% extends "base.tpl" %}

{% block content %}
<h2>Statistics</h2>

<dl>
    <dt>Number of found phones</dt>
    <dd>{% with latest_devices as data %}{% include "stats_datacol.tpl" %}{% endwith %}</dd>

    <dt>Total sent: all files</dt>
    <dd>{% with sent_files as data %}{% include "stats_datacol.tpl" %}{% endwith %}</dd>

    {% for stat in file_stats %}
    <dt>Total sent:  {{ stat.file }}</dt>
    <dd>{% with stat.sent as data %}{% include "stats_datacol.tpl" %}{% endwith %}</dd>
    {% endfor %}

</dl>

<p>
    <h3>Actions</h3>
    <li><a onclick="return confirm('Are you sure? This action cannot be undone.');" href="/clear_sent/">clear all "sent file" statistics</a></li>
</p>

{% endblock %}
