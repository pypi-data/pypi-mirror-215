import panel as pn
from widgets import bcreate
import panel as pn

from nabla_materials import nablaMaterials
from nabla_solver import nablaSolver
from readtoml import readconfig

pn.extension('floatpanel')


#nabla page
class NablaHome:
    def __init__(self,conf):
        self.conf=conf
    
        #-------------- style -----
        cs1 = {'border': '1px solid black'}
        cs2 = {'border': '3px solid black',
               "weight": 'bolder',
               "font-size": "20px"} 
        
        # #config parameters
        # keys={}
        # values={}
        # if conf is not None:
        #     keys = list(conf['geopars'].keys())
        #     values = list(conf['geopars'].values())



        # #geo plan
        # names = ["Hst1","Hst2","Hst3","Hp1"]
        # # Home buttons
        # geobuttons = bcreate(nb=14,names=conf["geometry_parameters"],
        #                 bwidgets="FloatInput", btype="primary", h=80, w=150)
       
        # geo parameters
        f1 = pn.widgets.FloatInput(name ='Hst1', value=5., step=1e-1, start=0, end=1000,width=120)
        f2 = pn.widgets.FloatInput(name ='Hst2', value=5., step=1e-1, start=0, end=1000,width=120)
        f3 = pn.widgets.FloatInput(name ='Hst3', value=5., step=1e-1, start=0, end=1000,width=120)
        f4 = pn.widgets.FloatInput(name ='Hp1', value=5., step=1e-1, start=0, end=1000,width=120)
        f5 = pn.widgets.FloatInput(name ='Hpo', value=5., step=1e-1, start=0, end=1000,width=120)
        f6 = pn.widgets.FloatInput(name ='rst1', value=5., step=1e-1, start=0, end=1000,width=120)
        f7 = pn.widgets.FloatInput(name ='rst2', value=5., step=1e-1, start=0, end=1000,width=120)
        f8 = pn.widgets.FloatInput(name ='r1', value=5., step=1e-1, start=0, end=1000,width=120) 
        f9 = pn.widgets.FloatInput(name ='rm', value=5., step=1e-1, start=0, end=1000,width=120)
        f10 = pn.widgets.FloatInput(name='Hm', value=5., step=1e-1, start=0, end=100,width=120)
        f11 = pn.widgets.FloatInput(name ='Hsb3', value=5., step=1e-1, start=0, end=1000,width=120)
        f12 = pn.widgets.FloatInput(name='Hsb2', value=5., step=1e-1, start=0, end=1000,width=120)
        f13 = pn.widgets.FloatInput(name='Hsb1', value=5., step=1e-1, start=0, end=1000,width=120)
        f14 = pn.widgets.FloatInput(name='Delta', value=5., step=1e-1, start=0, end=1000,width=120) 

        geoinputs1   = pn.GridBox(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14
                                  ,ncols=3,sizing_mode='stretch_both')
    

        #mesh parameters
        select_mesh = pn.widgets.Select(name='Default mesh size', options=['Coarse', 'Normal', 'Thin'],sizing_mode='stretch_width')
        spv1 = pn.Spacer(height=40)
        #advanced mesh setting
        # Define the content widgets
        w1 = pn.widgets.TextInput(name='Text:')
        w2 = pn.widgets.FloatSlider(name='Slider')
        mesh_adv = pn.Card(w1, w2, title='⚙️ Mesh setting', styles={'background': 'WhiteSmoke'},collapsed=True,
                           header_background='#2f2f2f',header_color='white',sizing_mode='stretch_width')
        
        #control buttons
        mesh_gene =pn.widgets.Button(name="🔍 Mesh viz",height=80,width=120,
                                     sizing_mode='stretch_width')
        mesh_val =pn.widgets.Button(name="✔️ Mesh validation",height=80,width=150,
                                    button_type="success",sizing_mode='stretch_width')
        spv2 = pn.Spacer(height=100)
        ctrl_row = pn.Row(mesh_gene,mesh_val,)


        #box
        geobox= pn.WidgetBox("## Geometry plan",pn.pane.PNG('assets/sps-geo.png', sizing_mode='fixed', width=500),
                             name="geobox",styles=cs1)
        geoinputbox  = pn.WidgetBox("## Geometry parameters",geoinputs1,styles=cs1)
        meshinputbox = pn.WidgetBox("## Mesh parameters",select_mesh,spv1,mesh_adv,styles=cs1)
        meshparabox = pn.WidgetBox(meshinputbox,spv2,ctrl_row)


        #geotab
        geohome = pn.Row(geobox,geoinputbox,meshparabox,name="Geometry & Mesh")
        materialhome = nablaMaterials()
        solverhome = nablaSolver() 

        geohometabs=pn.Tabs(geohome,materialhome,solverhome,
                            sizing_mode='stretch_both',styles=cs2)
        self.content = geohometabs



    def view(self):
        return self.content