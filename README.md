collectd-logster
================

A [Logster](https://github.com/etsy/logster/) plugin for [collectd](http://collectd.org) using collectd's [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml). 

Install
-------
 1. Place logster-collectd.py in /opt/collectd/lib/collectd/plugins/python (assuming you have collectd installed to /opt/collectd).
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
Add the following to your collectd config **or** use the included redis.conf.

    <LoadPlugin python>
      Globals true
    </LoadPlugin>

    <Plugin python>
      ModulePath "/usr/lib64/collectd"
      Import "logster-collectd"

      <Module "logster-collectd">
        request "/log/file/name.log" "Parser"
        Verbose "false"
      </Module>
    </Plugin>

