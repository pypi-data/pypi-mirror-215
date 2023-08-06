import panel as pn
from panel.template import FastListTemplate
from nabla_home import NablaHome
from widgets import bcreate
from readtoml import readconfig
import json
pn.extension()


#--------------------------- Homepage ------------------------------

# Custom CSS styles
fileinput_style = """
:host(.custom_button) {
    background-color:#2f2f2f ;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;

}
"""
btn_style= """
:host(.cbtn){
border: 3px solid black;
}
"""


# Logo pulsar
png = pn.pane.PNG('assets/pulsars-logo.png', sizing_mode='fixed', width=450)
bh1 = pn.widgets.Button(name='New Project',button_type="primary",height =80,width=150)
file_type = ".toml"
bh2 = pn.widgets.FileInput(name="Load Project",height=80,width=150,stylesheets=[fileinput_style],
                            css_classes= ["custom_button"])
#config_file
conf={}
if bh2.value is not None:
    config_file= bh2.value.decode()
    conf = readconfig(config_file) # input configuration dictionary

bh3 = pn.widgets.Button(name="🤖 Pulsars-ML",height=80,width=150,stylesheets=[btn_style],
                            css_classes= ["cbtn"])


bh4 = pn.widgets.Button(name="▼ Pulsars-SIM",height=80 ,width=150,stylesheets=[btn_style],
                            css_classes= ["cbtn"])
bh4.on_click(lambda event: show_page(pages["Nabla_homepage"]))
#horizontal spacer
sph = pn.Spacer(width=400)  
bbox = pn.GridBox(bh1, bh2, bh3, bh4, ncols=2, sizing_mode='stretch_both', spacing=10,
                        align='center', align_items='center', justify_content='center')
text = """
## ☕️ About
**Pulsars** (pronounced "Pulsar") is a **high-level** python API and a GUI platform, 
built upon **State Of The Art (SOTA)** python libraries, to help researchers, engineers and curious minds 
to **practically** use [Machine Learning (ML)](https://en.wikipedia.org/wiki/Machine_learning), 
[Deep Learning](https://en.wikipedia.org/wiki/Deep_learning) algorithms and/or 
solve [Partial Differential Equations](https://en.wikipedia.org/wiki/Partial_differential_equation) 
using the [Finite Element Method (FEM)](https://en.wikipedia.org/wiki/Finite_element_method).
You can see **Pulsars** as a **unified toolbox** to **manage** the **cumberstone stuff** 
which is generally involved for solving **real world problems** using ML/DL and/or FEM numerical simulations.

## 🧩 Pulsars components

The Pulsars library is composed of two main components which could be used together or independently:

### 🤖Pulsars-ML: The Machine Learning Side
- 🔁 Machine Learning Lifecycle ([mlflow](https://mlflow.org/))
- 🧮 Machine Learning Algorithms ([scikit-learn](https://scikit-learn.org/stable/index.html), 
[XGBoost](https://xgboost.readthedocs.io/en/stable/)...)
- 🕸️ Deep Learning Algorithms ([Keras](https://keras.io/), [Tensorflow](https://www.tensorflow.org/))
- 🛠️ Hyperparameters Tuning ([Ray Tune](https://docs.ray.io/en/latest/tune/index.html))
- 👓 Experiments Tracking ([MLflow tracking](https://mlflow.org/docs/latest/tracking.html))
- 📈 Results visualization ([Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/index.html))

### ▼ Pulsars-SIM: The Numerical Simulation Side
- 🕸️ Mesh generation ([Gmsh](https://gmsh.info/), [Meshio](https://github.com/nschloe/meshio))
- ⚙️ Efficient FEM solver ([FEniCSx](https://fenicsproject.org/))
- 📈 Results visualization ([PyVista](https://docs.pyvista.org/), [Matplotlib](https://matplotlib.org/), 
[Bokeh](https://bokeh.org/)...)
"""

#------------------------------------------------------------------
# HomePage
class HomePage:
    def __init__(self,):
        self.content = pn.Column(
            pn.Row(
                pn.Column(png, align='center', sizing_mode='fixed', width=400),
                sph,
                bbox,
                sizing_mode='stretch_width',
                align='center',
                align_items='center',
                justify_content='center'
            ),
            pn.pane.Markdown(text)
        )

    def view(self):
        return self.content



# Instantiate pages and add them to the pages dictionary

pages = {
    "Home_page": HomePage(),
    "Nabla_homepage": NablaHome(conf),
}

# Create the main area and display the first page
main_area = pn.Column(pages["Home_page"].view())

# Function to show the selected page
def show_page(page_instance):
    main_area.clear()
    main_area.append(page_instance.view())

# Define buttons to navigate between pages
page1_button = pn.widgets.Button(name="Home_page", button_type="primary") # return to homepage 
page1_button.on_click(lambda event: show_page(pages["Home_page"]))


# Create the Template
template = FastListTemplate(
    title="Pulsars App",
    main=[main_area],
)

# Serve the Panel app
template.servable()