{% extends "base_twocolumn.tpl" %}

{% block column1 %}
<h2>Active devices</h2>
{% if active_devices %}
<ul>
    {% for device in active_devices %}
    <li>
	<strong> {{ device.name }} </strong>
	{% if device.locked %}[busy...]{% endif %}
	<br />
	Last seen @ {{ device.lastseen }}
    </li>
    {% endfor %}
</ul>
{% else %}
No active devices found... is the scanner running?
{% endif %}
<hr />


<h2>Active files</h2>
{% if active_schedules %}
<ul>
    {% for schedule in active_schedules %}
    <li>
	<strong> {{ schedule.datafile }} </strong>
    </li>
    {% endfor %}
</ul>
{% else %}
No schedules...
{% endif %}
<hr />


<h2>Recent devices</h2>
{% if latest_devices %}
<ul>
    {% for device in latest_devices %}
    <li>
	<strong> {{ device.name }} </strong> <br />
	Last seen @ {{ device.lastseen }}
    </li>
    {% endfor %}
</ul>
{% else %}
No devices...
{% endif %}
<hr />


{% endblock %}



{% block column2 %}

<h2>Last succesful transfers</h2>

{% if last_sent_ok %}
<ul>
    {% for l in last_sent_ok %}
    <li>
	<strong> {{ l.device.name }} </strong> --&gt; {{ l.schedule }} <br />:
	{{ l.send_time }} - 

	<strong>SUCCESS</strong>
    </li>
    {% endfor %}
</ul>
{% endif %}

<hr />

<h2>Log</h2>

{% if last_sent %}
<div class="controls">
    <a onclick="return confirm('Are you sure?');" href="/clear_sent/">clear sent</a>
</div>
<ul>
    {% for l in last_sent %}
    <li>
	<strong> {{ l.device.name }} </strong> --&gt; {{ l.schedule }} <br />:
	{{ l.send_time }} - 
	{% ifequal l.exitcode  0 %}
	<strong>SUCCESS</strong>
	{% endifequal %}
	{% ifequal l.exitcode 256 %}
	Timeout, trying again soon
	{% endifequal %}
	{% ifequal l.exitcode 512 %}
	Client rejected; blacklisting
	{% endifequal %}
	{% ifequal l.exitcode 768 %}
	Aggressive mode, trying again soon
	{% endifequal %}
    </li>
    {% endfor %}
</ul>
{% else %}
No devices...
{% endif %}
<hr />


<h2>Blacklisted</h2>
{% if blacklist %}
<div class="controls">
    <a onclick="return confirm('Are you sure?');" href="/clear_blacklist/">clear blacklist</a>
</div>
<ul>
    {% for b in blacklist %}
    <li><strong>{{ b.device }}</strong> <br />
	From {{ b.ban_from }} to {{ b.ban_until }}
    </li>
    {% endfor %}
</ul>
{% else %}
Nobody's blacklisted
{% endif %}

<hr />


{% endblock %}
