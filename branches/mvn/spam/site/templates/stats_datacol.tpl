<ul>
{% for item, stat in data.bytime %}
    {% if stat %}
    <li>In the last {{ item }}: <em>{{ stat }}</em></li>
    {% endif %}
{% endfor %}
</ul>
Total: <em>{{ data.total }}</em>

