<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
	<meta http-equiv="Content-Language" content="en-us" />
	
	<title>{% block title %}BlueSpam{% endblock %}</title>
	
	<meta name="ROBOTS" content="ALL" />
	
	<link href="/media/css/base.css" rel="stylesheet" type="text/css" media="screen" />
	<link href="/media/css/print.css" rel="stylesheet" type="text/css" media="print" />
	<link href="/static/base.css" rel="stylesheet" type="text/css" media="screen" />

	<script type="text/javascript">
	    setTimeout(function() { window.location.reload(); }, 5000);
	</script>
    </head>
    
    <body>
	<div id="heading">

	    <img src="/static/logo.gif" />

	    <div class="top">
		<h1>{% block pagetitle %}BlueSpam - bluetooth file distribution{% endblock %}</h1>
		{% include "nav.tpl" %}
	    </div>

	</div>


	<hr />
	
	{% block content %}
	{% endblock %}

	<hr />
	<p class="sub">&copy;2008, 2009 <a href="http://www.scherpenisse.net/">Arjan Scherpenisse</a>; this software is open source and released under the MIT license.</p>

    </body>
</html>

