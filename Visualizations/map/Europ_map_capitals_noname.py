#!/usr/bin/env python3.6
# coding: utf-8

# In[1]:


import os 
import folium   
from folium import plugins
import pandas as pd
import numpy as np


# In[2]:


# ## Data Prep


# In[4]:


process=False

if process:    
    data=pd.read_csv("/home/dario/NeoMeetup/Visualizations/map/export_european_capitals.csv")
    data.head()
    data.sort_values("ID_event").head()

    print(len(data))

    for line in data.itertuples():
        if data.iloc[line.Index]['dist']==0:
            data['dist'].at[line.Index]=7 #arbitrary for milan
    data.head()   

    data.sort_values(["ID_event","dist"], inplace=True)
    data

    ddrop=data.drop_duplicates(subset="ID_event" , keep="last")
    ddrop=ddrop.drop("ID_member", axis=1)
    #ddrop.sort_values("ID_event")
    ddrop=ddrop.reset_index()
    ddrop.head()

    d=data.groupby("ID_event")['dist'].quantile(0.75).reset_index()
    print(d.head())
    d.rename(columns={'dist':'maxdist'}, inplace=True)
    ddrop=ddrop.merge(d, on="ID_event")
    ddrop.head()

    d1=data.groupby("ID_event")['ID_member'].count().reset_index()
    print(d1.head())

    d1.rename(columns={'ID_member':'count_part'}, inplace=True)
    ddrop=ddrop.merge(d1, on="ID_event")
    ddrop.head()
    ddrop.to_csv("post_proc.csv")

else:
    ddrop=pd.read_csv("post_proc.csv")
    

#ddrop1=pd.read_csv("post_proc.csv")
ddrop.head()


# In[15]:


ddrop[ddrop.g_city=="Stockholm"].reset_index()
print(len(ddrop))
ddrop=ddrop[ddrop.count_part>1].reset_index()
len(ddrop)


# In[16]:


# ## Let's build a map


# In[17]:


#legend template
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


html = """
    <h3> Event ID  : </h3><p>{}</p>
    <h3> Event Name: </h3><p></p>
    <h3> Location: </h3><p>{}</p>
    """
html1 = """
    <h2> Welcome to the meetup event map!  </h2>
    <h3> Some tips: </h3><p>{}</p>
    <h3> Some other tips: </h3><p>{}</p>
    """
html2 = """
<div style="
    position: fixed; 
    top: 110px;
    left: 90px;
    width: 270px;
    height: 340px;
    z-index:9999;
    font-size:14px;
    ">
    <h3> Event ID: <a style="color:#e6194b;font-size:70%;">{}</a></h3>
    <h3> Location: </h3><p><a style="color:#e6194b;font-size:85%;">{}</a></p>
    <h3> Raggio del bacino d'utenza: <a style="color:#e6194b;font-size:70%;">{} Km</a> </h3>
    <h3> Partecipants: <a style="color:#e6194b;font-size:70%;">{}</a></h3>

</div>
<div style="
    position: fixed; 
    top: 100px;
    left: 75px;
    width: 270px;
    height: 350px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    filter: blur(8px);
    -webkit-filter: blur(8px);
    opacity: 0.7;
    ">
</div>
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
legend_html2 = '''
<div style="
    position: fixed; 
    bottom: 50px;
    left: 50px;
    width: 250px;
    height: 40px;
    z-index:9999;
    font-size:14px;
    ">
    <p><a style="color:#e6194b;font-size:150%;margin-left:20px;">⭕</a>&emsp;Bacino d'utenza </p>
</div>
<div style="
    position: fixed; 
    bottom: 50px;
    left: 50px;
    width: 150px;
    height: 40px; 
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    filter: blur(8px);
    -webkit-filter: blur(8px);
    opacity: 0.9;
    ">
</div>
'''


# In[18]:


#ddrop=ddrop.sort_values('maxdist', ascending=False).reset_index()
#ddrop.head()


# In[19]:


n=5000
ddrop.maxdist=ddrop.maxdist.mask(ddrop.maxdist>n,n)
ddrop.head()


# In[20]:


def zoom_on_radius(radius):
    if radius >=10000:
        return 2
    if (radius >=1000 and radius <10000):
        return 3
    if (radius >= 500 and radius<1000):
        return 5
    if (radius >= 100 and radius<5000):
        return 6
    if (radius >= 50 and radius<100):
        return 8
    else:
        return 10


# In[21]:


import branca #brrr
from folium.plugins import MarkerCluster
from folium.features import DivIcon, FeatureGroup
from folium import IFrame

import base64 #jpeg encoding

stop=False
n_stop=300

capital_list=["Roma", "Stockholm"]
coord_list=[]
#for capital in capital_list:
#    coord=ddrop1[ddrop1.g_city==capital].reset_index()

coord_list.append([41.9, 12.48])#Roma
coord_list.append([59.33, 18.07])#stockholm
coord_list.append([51.50, -0.12])#Londra
print(coord_list)


m = folium.Map(location=[ddrop['v_lat'].mean(),ddrop['v_lon'].mean()], zoom_start=5, min_zoom=2)
mc=MarkerCluster()

radius_events = FeatureGroup(name='Events')
heat_events= FeatureGroup(name='Country')

country_list=["italy","sweden", "gb"]

images_list=["../heatmap_italy.jpg","../heatmap_spain.jpg","../heatmap_france.jpg"]
#coord_list=
for i  in range(len(country_list)):
    
    encoded = base64.b64encode(open("../heatmap_"+country_list[i]+".jpg", 'rb').read())#.decode()                           
    html4 = '<img src="data:image/jpg;base64,{}">'.format
    #print(20*'-',encoded.decode('UTF-8'))
    f = branca.element.Figure()
    iframe = IFrame(html4(encoded.decode('UTF-8')), width=1200, height=600)
    h_popup = folium.Popup(iframe, max_width=2650)
    heat_events.add_child(
            folium.Marker(
            location = coord_list[i], 
            popup=h_popup,
            )
        ).add_to(m)
    f.html.add_child(branca.element.Element('<h1><a style="color:#e6194b;font-size:100%;margin-left:330px;">{}</a></h1>'.format("Country: "+country_list[i])))
    f.add_to(iframe)
    #f.add_to_(m)
    #m.add_to(f)

for line in ddrop.itertuples():
    
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
        m1=folium.Map([float(lat), float(lon)], zoom_start=zoom_on_radius(line.maxdist), min_zoom=2) #eventualmente aggiungere il livello di zoom in base al raggio può essere fyco

        iframe = branca.element.IFrame(
            html=html.format(ddrop['ID_event'].at[line.Index], ddrop['venue_name'].at[line.Index]), 
            width=400, height=240)
        popup1 = folium.Popup(iframe, show=True)
        f.html.add_child(branca.element.Element('<h1><a style="color:#e6194b;font-size:100%;margin-left:330px; margin-top:10px;">{}</a></h1>'.format("Event Name Here")))

        
        m1.add_child(folium.Circle(
          location=[float(lat), float(lon)],
          #popup=popup1,
          #radius=int(ddrop.iloc[line.Index]['maxdist'])*1000,
          radius=int(line.maxdist)*1000, #km->m
          color='crimson',
          fill=False,
          #fill_color='crimson',
        ))
        '''
        plugins.Fullscreen(
            position='topright',
            title='Expand me',
            title_cancel='Exit me',
            force_separate_button=True
        ).add_to(m1)
        '''
        f.html.add_child(branca.element.Element(legend_html2))
        
        #html_now=html2.format(ddrop['ID_event'].at[line.Index], ddrop['venue_name'].at[line.Index], line.count_part)
        html_now=html2.format(line.ID_event, line.venue_name,int(line.maxdist), line.count_part)
        
        f.html.add_child(branca.element.Element(html_now))
        
        #f.add_child(legend)
        
        #f.html.add_child(branca.element.Element("<h1>Bacino d'utenza</h1>"))
        
        m1.add_to(f)

        iframe = branca.element.IFrame(width=1000, height=600)
        f.add_to(iframe)

        # Let's put the IFrame in a Popup
        popup = folium.Popup(iframe, max_width=2650)
        
        mc.add_child(
            folium.Marker(
            location = [float(lat), float(lon)], 
            popup=popup,
            ))
        '''
        mc.add_child(radius_events.add_child(
            folium.Marker(
            location = [float(lat), float(lon)], 
            popup=popup,
            )
        ))'''
              
        
        if stop:           
            if line.Index is n_stop:
                break
radius_events.add_child(mc)        
m.add_child(radius_events)
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
    
#Save it as html
m.save('export_europe_capitals.html')
print("finished")


# In[7]:


#Heatmap


# In[4]:


lat_df=ddrop[['v_lat', 'v_lon']]
print(len(ddrop))
str(lat_df.v_lat[0]) == "nan"

for line in lat_df.itertuples():
    if str(line.v_lat) == "nan":
        lat_df['v_lat'].at[line.Index]= ddrop['g_lat'].at[line.Index]
    if str(line.v_lon) == "nan":
        lat_df['v_lon'].at[line.Index]= ddrop['g_lon'].at[line.Index]
len(lat_df)

lat_df.isna().any()

lat_df=lat_df.astype(float)

from folium.plugins import HeatMap


map_hooray = folium.Map(location=[ddrop['v_lat'].mean(),ddrop['v_lon'].mean()], zoom_start=5)


# List comprehension to make out list of lists
heat_data = [[row['v_lat'],row['v_lon']] for index, row in lat_df.iterrows()]

# Plot it on the map
HeatMap(heat_data).add_to(map_hooray)

# Display the map
map_hooray.save("heat_europe.html")

