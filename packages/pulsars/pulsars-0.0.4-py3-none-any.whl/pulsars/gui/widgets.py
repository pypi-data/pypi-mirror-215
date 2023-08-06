import panel as pn


#buttons creation
def bcreate(nb,names,bwidgets,btype,h,w):
    blist=[] 
    for i in range(0,nb):
        if bwidgets=="Button":
            b = pn.widgets.Button(name=names[i],
                                    button_type=btype,
                                    height=h,
                                    width=w)
        elif bwidgets=="FloatInput":
            b = pn.widgets.FloatInput(name=names[i],
                                    width=120)

        blist.append(b)
    return blist