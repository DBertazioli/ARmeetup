#!/usr/bin/env python
# coding: utf-8

# In[1]:


#from __future__ import print_function

import os 
try:    
    import folium
except ImportError:
    get_ipython().system('pip install --user folium')
    import folium
    
from folium import plugins
import pandas as pd
import numpy as np


# ## Data Prep

# In[10]:


ddrop=pd.read_csv("/root/NeoMeetup/Visualizations/map/ddrop_all.csv")

# ## Let's build a map

# In[16]:


#legend template
import branca
from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: fixed; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend (draggable!)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Bacino d'utenza</li>
    <!-- questo è un commento <li><span style='background:orange;opacity:0.7;'></span>Medium</li>
    <li><span style='background:green;opacity:0.7;'></span>Small</li> -->

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""



#macro = MacroElement()
#macro._template = Template(template)

html = """
    <h3> Event ID  : </h3><p>{}</p>
    <h3> Event Name: </h3><p></p>
    <h3> Location: </h3><p>{}</p>
    """

legend_html = """
     <div style=”position: fixed; 
     bottom: 50px; left: 50px; width: 100px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     “>&nbsp; Cool Legend <br>
     &nbsp; East &nbsp; <i class=”fa fa-map-marker fa-2x”
                  style=”color:green”></i><br>
     &nbsp; West &nbsp; <i class=”fa fa-map-marker fa-2x”
                  style=”color:red”></i>
      </div>
     """
#m.get_root().add_child(macro)

#m


# In[17]:


import branca #brrr
#m1 = folium.Map(location=[20,0], tiles="Mapbox Bright", zoom_start=2)
from folium.plugins import MarkerCluster
from folium.features import DivIcon

m = folium.Map(location=[ddrop['v_lat'].mean(),ddrop['v_lon'].mean()], zoom_start=12)
mc=MarkerCluster()

for line in ddrop.itertuples():
    #try:
        if str(line.v_lat) != "nan" : #where exists use venue lat/lon
            lat=line.v_lat
        else: #elsewhere use group lat
            lat=line.g_lat
            #print("g_lat: ",lat)
        if str(line.v_lon) != "nan": #where exists use venue lat/lon
            lon=line.v_lon
        else: #elsewhere use group lat
            lon=line.g_lon

        f = branca.element.Figure()
        m1=folium.Map([float(lat), float(lon)], zoom_start=10) #eventualmente aggiungere il livello di zoom in base al raggio può essere fyco

        iframe = branca.element.IFrame(
            html=html.format(ddrop['ID_event'].at[line.Index], ddrop['venue_name'].at[line.Index]), 
            width=400, height=240)
        popup1 = folium.Popup(iframe, show=True)


        m1.add_child(folium.Circle(
          location=[float(lat), float(lon)],
          popup=popup1,
          radius=int(ddrop.iloc[line.Index]['maxdist'])*1000,
          #radius=1,
          color='crimson',
          fill=False,
          #fill_color='crimson',

        ))
        #print (lat,"   ", lon)
        #trying to add some text
        #m1.add_child(folium.Marker(
            #location=[45.5,8.5],#[lat, lon],
            #icon=DivIcon(icon_size=(150,36), icon_anchor=(0,0),html='<div style="font-size: 24pt">Bacino d\'utenza</div>')
            #))

        #macro1 = MacroElement()
        #macro1._template = Template(template)
        #m1.get_root().add_child(macro1)

        f.html.add_child(branca.element.Element("<h1>Bacino d'utenza</h1>"))
        #f.html.add_child(branca.element.Element(legend_html))

        #fig = folium.element.Figure()
        #fig.html.add_child(folium.element.Element("<h1>This is a title</h1>"))

        #m1.title = 'My fancy title here'
        #f.add_child(m1)
        m1.add_to(f)

        #iframe = branca.element.IFrame(html=html.format(ddrop['event_id'].at[line.Index], ddrop['city'].at[line.Index]), width=500, height=300)
        #popup = folium.Popup(iframe)
        iframe = branca.element.IFrame(width=1000, height=600)
        f.add_to(iframe)

        # Let's put the IFrame in a Popup
        popup = folium.Popup(iframe, max_width=2650)
        mc.add_child(
            folium.Marker(
            location = [float(lat), float(lon)], 
            popup=popup,
            ))
        #if line.Index is 10:
        #    break
    #except Exception as e:
    #    print(e)
m.add_child(mc)
plugins.Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    force_separate_button=True
).add_to(m)


#macro = MacroElement()

#macro._template = Template(template)

#m.get_root().add_child(macro)
#map.get_root().add_child(macro1)

folium.LayerControl().add_to(m)

#display(m)
    
#Save it as html
m.save('/home/dario/NeoMeetup/Visualizations/map/MEETTHEWORLD.html')


# In[ ]:


print "map saved with success"


# In[ ]:
