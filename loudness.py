#/usr/bin/python
# -*- coding: utf-8 -*-

from string import Template
import os
import subprocess
import glob
import sys

__version__     ='0.2.1'
__author__      ='seb a.k.a. mikrolax'
__author_email__='seb@mikrolax.me'
__url__='http://mikrolax.github.com/loudnessPlotter/'
__download_url__='https://github.com/mikrolax/loudnessPlotter/zipball/master'


tpl_CDN='''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>loudnessPlotter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="plot loudness mesurement">
    <meta name="author" content="seb 'mikrolax'">
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">

    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="excanvas.min.js"></script><![endif]-->
    <link rel="shortcut icon" href="favicon.ico">
  </head>
  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="#">loudnessPlotter</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <!-- <li class="active"><a href="https://github.com/mikrolax/loudnessPlotter/issues">Bugs</a></li> -->
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
    
  <div class="container">
    <h3> $filename </h3><hr>
      $htmlstats
      <div id="placeholder" style="width:900px;height:450px"></div>
      
            
    <footer>
      <hr>
      <p class="pull-right"> <a href="http://mikrolax.github.com/loudnessPlotter">loudnessPlotter</a> - 2012 </p>
    </footer>
  </div>
  
  <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>  
  <script language="javascript" type="text/javascript">
  $(document).ready(function() {
  $.plot($("#placeholder"), $datas,$options);
  });
  </script>

  </body></html>
'''


tpl_multi_fromCDN='''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <title>loudnessPlotter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="plot loudness mesurement">
    <meta name="author" content="seb 'mikrolax'">
    <!-- Le styles -->
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="excanvas.min.js"></script><![endif]-->
    <link rel="shortcut icon" href="favicon.ico">
    
  </head>
  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="#">loudnessPlotter</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <!-- <li class="active"><a href="#">Home</a></li> -->
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
    
  <div class="container">
  $tabbedplaceholder
  <footer>
  <hr>
  <p class="pull-right"> <a href="http://mikrolax.github.com/loudnessPlotter">loudnessPlotter</a> - 2012 </p>
  </footer>
  </div>
  
  <script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  <script src="http://cdnjs.cloudflare.com/ajax/libs/flot/0.7/jquery.flot.min.js"></script>
<script language="javascript" type="text/javascript">
$(document).ready(function() {
$plots
});
</script>
</body></html>
'''
    

#for py2exe freezing support 
def we_are_frozen():
  """Returns whether we are frozen via py2exe.
  This will affect how we find out where we are located."""
  return hasattr(sys, "frozen")
def module_path():
  """ This will get us the program's directory,
  even if we are frozen using py2exe"""
  if we_are_frozen():
    return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
  else:
    return os.path.dirname(os.path.abspath(__file__))

#TODO: rewrite only 2 main module function : analyse() and write(). run() could do both.

def writeHTML(loudnessdata,htmlout): 
  """    Write a single self-contained HTML page with graph. """
  fout=open(htmlout+'.html','w')
  htmlstats=HTMLstats(stats(loudnessdata))
  datas=[] 
  M=[]
  S=[]
  I=[]
  idx_m=0
  idx_s=0
  idx_i=0  
  for val in loudnessdata['M']:
    M.append([idx_m*2*0.1,loudnessdata['M'][idx_m]])
    idx_m+=1
  for val in loudnessdata['S']:
    S.append([idx_s*0.1,loudnessdata['S'][idx_s]])
    idx_s+=1
  for val in loudnessdata['M']:
    I.append([idx_i*2*0.1,loudnessdata['I'][0]]) 
    idx_i+=1  
  Mdict={}
  Mdict['label']='Momentary'
  Mdict['data']=M
  Sdict={}
  Sdict['label']='Short-Term'
  Sdict['data']=S  
  Idict={}
  Idict['label']='Integrated'
  Idict['data']=I  
  datas.append(Mdict)
  datas.append(Sdict)
  datas.append(Idict)
  options='''{  series: {lines: {show: true, steps: true },points: { show: false },bars: { show: false }},
  yaxis: { tickFormatter: function (v) { return v + " LUFS"; } },
  xaxis: { tickFormatter: function (v) { return v + " s"; } },
  legend: { position: 'se' }  }'''
  #if snippet ==True:
  #  s = Template(snippet)
  #  page=s.safe_substitute(filename=os.path.basename(htmlout),htmlstats=htmlstats,datas=datas,options=options) #,options=options  
  #else:
  s = Template(tpl_CDN)
  page=s.safe_substitute(filename=os.path.basename(htmlout),htmlstats=htmlstats,datas=datas,options=options) #,options=options
  print 'write %s' %htmlout+'.html'
  fout.write(str(page))
  return page#not really needed...



def stats(loudnessdata):
  """ get min/max/average value of M,S,(I) value. Return a dictionnary  """
  stats={}
  stats['M']={}
  stats['S']={}
  idx=0
  maxVal=-100
  minVal=0
  avgVal=0
  for item in loudnessdata['M']:
    try:
      data=float(loudnessdata['M'][idx])
    except:
      #print loudnessdata['M'][idx] #weird => : 1.#F
      data=-100.0
      pass
    if data > maxVal:
      maxVal=data
    elif data < minVal:
      minVal=data
    avgVal+=data/len(loudnessdata['M'])     
    idx+=1  
  stats['M']['min']=minVal
  stats['M']['max']=maxVal
  stats['M']['avg']='{0:.2f}'.format(avgVal)    
  idx=0
  maxVal=-100
  minVal=0
  avgVal=0
  for item in loudnessdata['S']:
    try:
      data=float(loudnessdata['S'][idx])
    except:
      #print loudnessdata['S'][idx]
      data=-100
      pass    
    if data > maxVal:
      maxVal=data
    elif data < minVal:
      minVal=data
    avgVal+=data/len(loudnessdata['S'])     
    idx+=1  
  stats['S']['min']=minVal
  stats['S']['max']=maxVal
  stats['S']['avg']='{0:.2f}'.format(avgVal)   
  try:
    data=float(loudnessdata['I'][0])
  except:
    data=-100.0
  stats['I']=data
  #stats['LRA']=LRA(loudnessdata)
  stats['LRA']=loudnessdata['LRA']
  return stats

def parseLoudnessLog(filepath):
  """ return dict : { 'M' : [val,val2],
                      'S' : [value,value],
                      'I' : [integratedvalue]}
      value are string reprensenting LUFS value                
  """
  loudnessdata={}
  loudnessdata['M']=[]
  loudnessdata['S']=[]
  loudnessdata['I']=[]
  key=''
  lines = open(filepath,'r').readlines()
  for line in lines:
    if 'ebu_mode=s' in line:  
      key='S'
    if 'ebu_mode=m' in line:  
      key='M'
    if 'ebu_mode=i' in line:  
      key='I'      
    if 'Lk=' in line:
      data=line.rsplit()[1]
      loudnessdata[key].append(data.rsplit('Lk=')[1])  
  return loudnessdata   
  
def HTMLstats(stats):
  """ return html from M,S,I stats dictionnary (returned by stats())  """
  html='''<dl class="dl-horizontal">'''
  s=m=i=''   
  for key in stats.keys():
    if key=='M':
      m='''<dt>Momentary max</dt> <dd>'''+str(stats['M']['max'])+''' LUFS</dd>'''
      m+='''<dt>Momentary min</dt> <dd>'''+str(stats['M']['min'])+''' LUFS</dd>'''
      m+='''<dt>Momentary average</dt> <dd>'''+str(stats['M']['avg'])+''' LUFS</dd>'''
    elif key=='S':
      s='''<dt>Short-term max</dt> <dd>'''+str(stats['S']['max'])+''' LUFS</dd>'''
      s+='''<dt>Short-term min</dt> <dd>'''+str(stats['S']['min'])+''' LUFS</dd>'''
      s+='''<dt>Short-term average</dt> <dd>'''+str(stats['S']['avg'])+''' LUFS</dd>'''
    elif key=='I':
      i='''<dt>Integrated</dt> <dd>'''+str(stats['I'])+''' LUFS</dd>'''
    elif key=='LRA':
      lra='''<dt>Loudness Range</dt> <dd>'''+str(stats['LRA'])+''' LU</dd>'''    
    else:
      pass
  html+=m+s+i+lra    
  html+='''</dl>'''
  return html  

def LRA(loudnessdata):
  import math
  absThreshold=-70.0
  relThreshold=-20.0  
  absGated=[]
  idx=0
  for item in loudnessdata['S']:
    try:
      data=float(loudnessdata['S'][idx])
    except:
      data=-100.0           #will not be taken into account or exit? 
    if data > absThreshold:
      absGated.append(data)  
    idx+=1    
  n=len(absGated)
  if n==0:
    return 'nan'    
  power=0
  for item in absGated:
    power+=pow(10,item/10)
  power=power/n
  integrated=10*math.log10(power)  
  relGated=[]
  for data in absGated:
    if data > integrated+ relThreshold:
      relGated.append(data)  
  n=len(relGated)    
  relGated.sort()
  idx=(n-1)*0.1+1  
  perclow=relGated[int(idx)]
  idx=(n-1)*0.95+1
  perchigh=relGated[int(idx)]
  lra=perchigh-perclow
  return lra
  
  
class LoudnessPlotter(object):
  """ base class for launching executable, parse log and write output HTML file """
  def __init__(self,filelist,outpath):
    """ init some self used value """
    self.filelist=filelist
    self.outpath=outpath
    self.loudnessdata={}
    self.toolspath=module_path()
    if sys.platform == 'win32':
      self.wavtoolpath=os.path.join(self.toolspath,'wave_analyze.exe')
    else:
      self.wavtoolpath=os.path.join(self.toolspath,'wave_analyze')
    self.processed=[]
    self.failed=[]
    # options
    self.snippet=False
    self.autoscale=True
    self.outfilename=None
    self.template=None
    
  def analyse(self):
    """ launch wave_analyze executable on each file of self.filelist putting stdout in a file 
     fills self.processsed file path list
    """
    done=0
    for item in self.filelist:
      logfile=item+'_loudness.txt'
      if len(self.filelist) > 1:
        print 'loudness analyse :: %s :: %s' %(str(done*100/len(self.filelist)),os.path.basename(item))
      #else:
      #  print 'loudness analyse :: %s' %os.path.basename(item)
      if os.path.isfile(logfile):
        #print 'remove %s' %logfile
        os.remove(logfile)
      error_mode=0  
      for ebu_mode in ['m','s','i']:
        #print 'ebu mode %s' %ebu_mode
        log=open(logfile,'a')
        log.write('ebu_mode=%s\n' %ebu_mode)
        log.flush()
        cmd=self.wavtoolpath+' "'+item+'" '+ebu_mode   
        #print cmd
        res=subprocess.call(cmd,stdout=log,shell=True) 
        if res!=0: 
          #print 'error analysing %s' %item
          error_mode+=1 
        log.close()
      if error_mode>0:  
        self.failed.append(item)     
        #print 'error analysing %s' %item
      else:       
        self.processed.append(item)  
      done+=1
    for f in self.processed:
      self.loudnessdata[os.path.basename(f)]=parseLoudnessLog(f+'_loudness.txt')
      self.loudnessdata[os.path.basename(f)]['LRA']=LRA(self.loudnessdata[os.path.basename(f)])
    return self.loudnessdata
        
  def process(self):
    """ base function to parse and write HTML based on internal config """
    if len(self.filelist)==0:
      print 'No file to process. Abort'
      return 1
    self.analyse() #fills self.processed else flot bugs (no data on one placeholder for width/height seems to affect them all)
    if len(self.processed)==1:
      self.writeIndividual()
    else :  
      return self.write() 
        
  def writeIndividual(self):
    """ write single HTML file for an individual file"""
    for key in self.loudnessdata.keys():
      writeHTML(self.loudnessdata[key],os.path.join(self.outpath,key))


  def getHtmlContent(self):
    """ get content for multi-files, return tabed content and the plots (to put in js)"""
    tabbedplaceholder=''
    if len(self.failed)>0:    #if some test failed display notif    
      tabbedplaceholder+='''<div class="alert">
      <button type="button" class="close" data-dismiss="alert">×</button>
      <strong>Warning! </strong>''' 
      for item in self.failed:
        tabbedplaceholder+='''<br>error while processing :'''+os.path.basename(item)
      tabbedplaceholder+='''</div>'''    
    tabbedplaceholder+='''<div class="tabbable"> 
                        <!-- <ul class="nav nav-tabs"> -->
                        <ul class="nav nav-pills">
                        '''    
    i=0                    
    for f in self.loudnessdata.keys(): 
      name=os.path.splitext(os.path.basename(f))[0]
      if i==0:
        tabbedplaceholder+='''<li class="active"><a href="#'''+name.replace(' ','')+'''" data-toggle="tab">'''+name+'''</a></li>
        '''      
      else:
        tabbedplaceholder+='''<li><a href="#'''+name.replace(' ','')+'''" data-toggle="tab">'''+name+'''</a></li>
        '''
      i+=1      
    tabbedplaceholder+='''</ul><hr>
    '''
    tabbedplaceholder+='''<div class="tab-content">
    '''  
    j=0
    for tab in self.loudnessdata.keys():
      name=os.path.splitext(os.path.basename(tab))[0]   
      if j==0:
        tabbedplaceholder+='''<div class="tab-pane active" id="'''+name.replace(' ','')+'''"> 
        ''' 
      else:
        tabbedplaceholder+='''<div class="tab-pane" id="'''+name.replace(' ','')+'''">
        ''' 
      #print tab
      #only for min/max/average, do not compute LRA again        
      tabbedplaceholder+=HTMLstats(stats(self.loudnessdata[tab]))+''' 
      <div id="'''+'placeholder'+name.replace(' ','')+'''" style="width:1000px;height:450px"></div></div>'''  
      j+=1
    tabbedplaceholder+='''</div>
    
    </div> 
    '''    
    
    plots=''
    for item in self.loudnessdata.keys():
      datas=[] #getData(self.loudnessdata[item])
      M=[]
      S=[]
      I=[]
      idx_m=0
      idx_s=0
      idx_i=0
      for val in self.loudnessdata[item]['M']:
        M.append([idx_m*2*0.1,self.loudnessdata[item]['M'][idx_m]])
        idx_m+=1
      for val in self.loudnessdata[item]['S']:
        S.append([idx_s*0.1,self.loudnessdata[item]['S'][idx_s]])
        idx_s+=1  
      for val in self.loudnessdata[item]['M']:
        I.append([idx_i*2*0.1,self.loudnessdata[item]['I'][0]],) 
        idx_i+=1
      Mdict={}
      Mdict['label']='Momentary'
      Mdict['data']=M
      Sdict={}
      Sdict['label']='Short-Term'
      Sdict['data']=S  
      Idict={}
      Idict['label']='Integrated'
      Idict['data']=I  
      
      #Idict['points']={'show':'false'} 
      #Idict['lines']={'show':'true'} 
      #Idict['bars']={'show':'false','horizontal':'false'}
      
      datas.append(Mdict)
      datas.append(Sdict)
      datas.append(Idict)
      if self.autoscale==True:
        options='''{
              series: {lines: {show: true, steps: true },points: { show: false },bars: { show: false }},
              yaxis: { tickFormatter: function (v) { return v + " LUFS"; } },
              xaxis: { tickFormatter: function (v) { return v + " s"; } },
              legend: { position: 'se' }}'''
      else:
        options='''{
              series: {lines: {show: true, steps: true },points: { show: false },bars: { show: false }},
              yaxis: { min:-70, max: 0, tickFormatter: function (v) { return v + " LUFS"; } },
              xaxis: { tickFormatter: function (v) { return v + " s"; } },
              legend: { position: 'se' }}'''

      name=os.path.splitext(os.path.basename(item))[0]
      plots+='''$.plot($("#placeholder'''+name.replace(' ','')+'''"), '''+str(datas)+''','''+options+''');             
             '''    
    return (tabbedplaceholder,plots)
  
  def write(self):
    """ write single HTML file for a list of file"""  
    tabbedplaceholder,plots =self.getHtmlContent()
    
    if self.template != None and os.path.exists(self.template):
      print 'using template file :  %s' %self.template
      s = Template( open(self.template,'r').read() ) 
    else:  
      s = Template(tpl_multi_fromCDN)
    #options=  
    page=s.safe_substitute(tabbedplaceholder=tabbedplaceholder,plots=plots)
    
    if self.outfilename != None:
      print 'write %s' %os.path.join(self.outpath,self.outfilename)            
      fout=os.path.join(self.outpath,self.outfilename) 
    else:
      print 'write %s' %os.path.join(self.outpath,'loudness.html')            
      fout=os.path.join(self.outpath,'loudness.html')
    open(fout,'w').write(page)
    return page     #not needed but usefull...


def cli():
  """ Simple command line interface. Process file or path, based on input args """
  if we_are_frozen():
    msg=''' loudnessPlotter : analyse and plot loudness in HTML\n usage: loudnessPlotter.py [inpath] [outpath]'''
  else:
    msg=''' loudnessPlotter : analyse and plot loudness in HTML\n usage: python loudness.py [inpath] [outpath]'''

  if len(sys.argv) > 1:
    pass
  else:
    print msg
    return 1      

  inpath=os.path.abspath(sys.argv[1])
  outpath=os.path.abspath(sys.argv[2])  
  wavfilelist=[]
  if os.path.isdir(inpath):
    wavfilelist=glob.glob(os.path.join(inpath,'*.wav'))
    print 'nb file to process: %s' %len(wavfilelist)     
  elif os.path.isfile(inpath) and os.path.splitext(inpath)[1]=='.wav' :
    wavfilelist.append(inpath)
  else:
    print msg
    return 1
    
  loud=LoudnessPlotter(wavfilelist,outpath)
  loud.process()  
  
if __name__ == "__main__":
  cli()
