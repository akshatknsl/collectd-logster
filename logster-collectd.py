import collectd
import subprocess

LOGFILE = []
PARSER = []
VERBOSE = False

def fetch_info():
  data = {}
  for i in range(len(LOGFILE)):
    cmd = subprocess.Popen("logster -o stdout %s %s" % (PARSER[i],LOGFILE[i]), shell=True, stdout=subprocess.PIPE)
    data[LOGFILE[i]] = []
    for line in cmd.stdout:
      data[LOGFILE[i]].append(line.split())
      
  return data

def configure_callback(conf):
  global LOGFILE, PARSER, VERBOSE
  for child in conf.children:
    if child.key == 'Verbose':
      VERBOSE = child.values[0]
    else:
      LOGFILE.append(child.values[0])
      PARSER.append(child.values[1])

def dispatch_value(info, type, type_instance=None):
  
  #log_verbose('Sending value: %s=%s' % (type_instance, value))
  
  for k in info.keys():
    for i in info[k]:
      val = collectd.Values(plugin='logster-collectd')
      val.type = type
      val.values = [i[2]]
      val.plugin_instance = k
      val.type_instance = i[1]
      val.time = float(i[0])
      val.dispatch()

def read_callback():
  log_verbose('Read callback called')
  for i in LOGFILE:
    log_verbose('log %s' % i)
  info = fetch_info()
  
  if not info:
    collectd.error('logster did not return')
  
  # send high-level values
  dispatch_value(info,'gauge')

def log_verbose(msg):
    if not VERBOSE:
        return
    collectd.error('logster [verbose]: %s' % msg)

collectd.register_config(configure_callback)
collectd.register_read(read_callback)