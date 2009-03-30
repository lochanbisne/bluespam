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
	<style>
	    body { width: 960px; margin: auto; margin-top: 40px; }
	    .column { float: left; width: 480px; }
	    hr { margin-top: 20px; }
	    div.controls { float: right; }
	</style>

	<script type="text/javascript">
	    setTimeout(function() { window.location.reload(); }, 5000);
	</script>
    </head>
    
    <body>
	<h1>{% block pagetitle %}BlueSpam{% endblock %}</h1>

	<div class="controls">
	    &copy;2008 <a href="http://www.on-signal.org/">on-signal</a>
	</div>


	<hr />
	
	{% block content %}
	{% endblock %}
    </body>
</html>

