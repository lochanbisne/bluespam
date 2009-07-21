<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
	<meta http-equiv="Content-Language" content="en-us" />
	
	<title>{% block title %}Bluetooth Guerilla System - MobileVideoNet{% endblock %}</title>
	
	<meta name="ROBOTS" content="ALL" />
	
	<link href="/media/css/base.css" rel="stylesheet" type="text/css" media="screen" />
	<link href="/media/css/print.css" rel="stylesheet" type="text/css" media="print" />
	<link href="/static/base.css" rel="stylesheet" type="text/css" media="screen" />

{% block extrahead %}
{% endblock %}
    </head>
    
    <body>
	<div id="heading">

		<h1>{% block pagetitle %}Bluetooth Guerilla System{% endblock %}</h1>
		{% include "nav.tpl" %}
	    </div>

	</div>


	<hr />
	
	{% block content %}
	{% endblock %}

	<hr />
	<p class="sub">Created by <a href="http://www.scherpenisse.net/">Arjan Scherpenisse</a> and <a href="http://www.mobilevideonet.com/">MobileVideoNet</a>. Software &copy;2008, 2009 Arjan Scherpenisse.<br />
	This software is open source and released under the MIT license. <a href="http://code.google.com/p/bluespam/">Visit site for more info</a>.</p>

    </body>
</html>

