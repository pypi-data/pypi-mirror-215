import io
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re

mass2element = {
    16: 'O',
    12: "C",
    1: "H",
    14: 'N', 
    -999: 'X',
}
element2color = {
    "O": 'rgba(255, 0, 0, 1.0)',
    "C": 'rgba(105, 105, 105, 1.0)',
    "H": 'rgba(255, 255, 255, 1.0)',
    'N': 'rgba(255, 0, 255, 1.0)',
    "X": 'rgba(138, 43, 226, 1.0)',
}
element2size = {
    "O": 74.,
    'N': 74.,
    "C": 77.,
    "H": 46.,
    "X": 90.,
}

def read_lmp_data(fname):
    lmp_str = ""
    with open(fname, 'r') as lmp_data:
        lmp_str = lmp_data.read()
    
    sec_names = []
    for sec_name in re.finditer('\n+[A-Z][a-z]*.*\n+', lmp_str):
        sec_names.append(sec_name.group(0))
    
    sec_strs = []
    next_str = lmp_str
    mass_sec_id = -1
    atom_sec_id = -1
    bond_sec_id = -1
    angle_sec_id = -1
    dihedral_sec_id = -1
    improper_sec_id = -1
    
    lj_coeff_sec_id = -1
    bond_coeff_sec_id = -1
    angle_coeff_sec_id = -1
    dihedral_coeff_sec_id = -1
    improper_coeff_sec_id = -1
    for sec_name in sec_names:
        _str_list = next_str.split(sec_name)
        sec_strs.append(_str_list[0])
        next_str = _str_list[1]
        if "Masses" in sec_name:
            mass_sec_id = sec_names.index(sec_name) + 1
        if "Atoms" in sec_name:
            atom_sec_id = sec_names.index(sec_name) + 1
        if "Bonds" in sec_name:
            bond_sec_id = sec_names.index(sec_name) + 1
        if "Angles" in sec_name:
            angle_sec_id = sec_names.index(sec_name) + 1
        if "Dihedrals" in sec_name:
            dihedral_sec_id = sec_names.index(sec_name) + 1
        if "Impropers" in sec_name:
            improper_sec_id = sec_names.index(sec_name) + 1
        if 'Pair Coeffs' in sec_name:
            lj_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Bond Coeffs' in sec_name:
            bond_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Angle Coeffs' in sec_name:
            angle_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Dihedral Coeffs' in sec_name:
            dihedral_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Improper Coeffs' in sec_name:
            improper_coeff_sec_id = sec_names.index(sec_name) + 1

    sec_names = ['head',] + sec_names
    sec_strs.append(next_str)
    
    return sec_names, sec_strs, mass_sec_id, atom_sec_id, bond_sec_id, angle_sec_id, dihedral_sec_id, improper_sec_id, lj_coeff_sec_id, bond_coeff_sec_id, angle_coeff_sec_id, dihedral_coeff_sec_id, improper_coeff_sec_id

def viz_mol(_df, _bond_df, annotation=False, box=None, writeHTML=False):
    
    df = _df.copy(deep=True)
    bond_df = _bond_df.copy(deep=True)
    
    df.loc[:, 'text'] = ['atom-'] * len(df)
    df.loc[:, 'text'] = df.loc[:, 'text'] + df.loc[:, 'id'].astype('str')

    df['tip'] = 'id: ' + df['id'].astype('str') + '<br>type: ' + df['type'].astype('str')
    if "element" in df.columns:
        df['tip'] = df['tip'] + '<br>element: ' + df['element'].astype('str')
    if "q" in df.columns:
        df['tip'] = df['tip'] + '<br>charge: ' + df['q'].astype('str')
    if "comment" in df.columns:
        df['tip'] = df['tip'] + '<br>comment: ' + df['comment'].astype('str')
    bond_df.loc[:, 'text'] = ['bond-'] * len(bond_df)
    bond_df.loc[:, 'text'] = bond_df.loc[:, 'text'] + bond_df.loc[:, 'id'].astype('str')
    
    bond_dict_x = df.set_index('id').to_dict()['x']
    bond_dict_y = df.set_index('id').to_dict()['y']
    bond_dict_z = df.set_index('id').to_dict()['z']
    bond_df.loc[:, 'x1'] = bond_df['at1'].map(bond_dict_x)
    bond_df.loc[:, 'y1'] = bond_df['at1'].map(bond_dict_y)
    bond_df.loc[:, 'z1'] = bond_df['at1'].map(bond_dict_z)

    bond_df.loc[:, 'x2'] = bond_df['at2'].map(bond_dict_x)
    bond_df.loc[:, 'y2'] = bond_df['at2'].map(bond_dict_y)
    bond_df.loc[:, 'z2'] = bond_df['at2'].map(bond_dict_z)
    
    df.loc[:, 'showarrow'] = False
    df.loc[:, 'opacity'] = 0.8
    df.loc[:, 'font']=[{'color':'rgba(0,0,255,1)',}] * len(df)
    bond_df.loc[:, 'showarrow'] = False
    bond_df.loc[:, 'opacity'] = 0.8
    bond_df.loc[:, 'font']=[{'color':'rgba(0,0,255,1)',}] * len(bond_df)
    bond_df.loc[:, 'x'] = (bond_df.loc[:, 'x1'] + bond_df.loc[:, 'x2']) * 0.5
    bond_df.loc[:, 'y'] = (bond_df.loc[:, 'y1'] + bond_df.loc[:, 'y2']) * 0.5
    bond_df.loc[:, 'z'] = (bond_df.loc[:, 'z1'] + bond_df.loc[:, 'z2']) * 0.5

    
    if annotation:
        annotation_list = df[['x', 'y', 'z', 'showarrow', 'opacity', 'text', 'font']].to_dict('records') + \
            bond_df[['x', 'y', 'z', 'showarrow', 'opacity', 'text', 'font']].to_dict('records')
    else:
        annotation_list = []
    data=[go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], 
                                       text=df['tip'],
                                       mode='markers',
                                       marker=dict(
                                           color=df['color'],
                                           size=df['size'] * 3.4 / (len(df)**(1./3.)),
                                           opacity=1.0,
                                       ))]
    
    for index, row in bond_df.iterrows():
        data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                 y=[row['y1'], row['y2']], 
                                 z=[row['z1'], row['z2']], 
                                 mode='lines',
                                 line=dict(
                                     color='rgba(220, 200, 200, 0.5)',
                                     width=5,
                                 )))
        if row['bond_order'] == 2:
            
            
            data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                     y=[row['y1'], row['y2']], 
                                     z=[row['z1'], row['z2']],
                                     mode='lines',
                                     line=dict(
                                         color='rgba(150, 150, 150, 0.35)',
                                         width=30,
                                     )))
            
            if row['bond_order'] == 3:            
                data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                         y=[row['y1'], row['y2']], 
                                         z=[row['z1'], row['z2']],
                                         mode='lines',
                                         line=dict(
                                             color='rgba(100, 100, 100, 0.25)',
                                             width=50,
                                         )))
                
    xyzmin = min([df['x'].min(), df['y'].min(), df['z'].min()])
    xyzmax = max([df['x'].max(), df['y'].max(), df['z'].max()])
    if box != None:
        xlo = box[0][0]
        xhi = box[0][1]
        ylo = box[1][0]
        yhi = box[1][1]
        zlo = box[2][0]
        zhi = box[2][1]
        
        xyzmin = min([df['x'].min(), df['y'].min(), df['z'].min(), xlo, ylo, zlo])
        xyzmax = max([df['x'].max(), df['y'].max(), df['z'].max(), xhi, yhi, zhi])
        annotation_list.append({'x': xhi, 
                                'y': ylo, 
                                'z': zlo, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "X",  
                                'font': {'size': 30, 'color':'rgba(255,0,0,1)',}})
        annotation_list.append({'x': xlo, 
                                'y': yhi, 
                                'z': zlo, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "Y",  
                                'font': {'size': 30, 'color':'rgba(0,255,0,1)',}})
        annotation_list.append({'x': xlo, 
                                'y': ylo, 
                                'z': zhi, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "Z",  
                                'font': {'size': 30, 'color':'rgba(0,0,255,1)',}})
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(225, 0, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(0, 225, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(0, 0, 225, 1.0)',
                                     width=3,
                                 )))
        
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 )))
        
    
    fig = go.Figure(data=data)
    
    
    DeltaX = xyzmax - xyzmin
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )

    if writeHTML:
        fig.write_html("vizmol.html")
    fig.show()
    
    
    
def open_lmp_data(lammps_data_file, viz=True, annotation=False, double_bonds=[], triple_bonds=[], box=False, unwrap=False, resize=False):
    
    sec_names, sec_strs, mass_sec_id, atom_sec_id, bond_sec_id, angle_sec_id, dihedral_sec_id, improper_sec_id, lj_coeff_sec_id, bond_coeff_sec_id, angle_coeff_sec_id, dihedral_coeff_sec_id, improper_coeff_sec_id = read_lmp_data(lammps_data_file)
    
    L_df = pd.read_csv(io.StringIO('\n'.join(sec_strs[0].split('\n')[-3:])), 
                sep=r'\s+', 
                names=['_min', '_max'], 
                usecols=[0, 1]).reset_index(drop=True)

    xhi = L_df.loc[0, '_max']
    xlo = L_df.loc[0, '_min']
    yhi = L_df.loc[1, '_max']
    ylo = L_df.loc[1, '_min']
    zhi = L_df.loc[2, '_max']
    zlo = L_df.loc[2, '_min']

    Lx = xhi - xlo
    Ly = yhi - ylo
    Lz = zhi - zlo

    mass_df = pd.read_csv(io.StringIO(sec_strs[mass_sec_id]), sep=r'\s+', names=['type', 'mass'], usecols=[0, 1]).reset_index(drop=True)
    mass_df['element'] = mass_df['mass'].round().map(mass2element)
    type_element_map = mass_df.set_index('type').to_dict()['element']
    
    
    if unwrap:
        df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', 
                         names=['id', 'mol', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'], 
                         usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reset_index(drop=True)
        df.index = df.index + 1
        
        df['_x'] = df['x']        
        df['x'] = df['x'] + (Lx * df['ix'])
        df['_y'] = df['y']        
        df['y'] = df['y'] + (Ly * df['iy'])
        df['_z'] = df['z']        
        df['z'] = df['z'] + (Lx * df['iz'])
    else:
        df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', names=['id', 'mol', 'type', 'q', 'x', 'y', 'z'], usecols=[0, 1, 2, 3, 4, 5, 6]).reset_index(drop=True)
        df.index = df.index + 1
        if resize:
            xhi = df["x"].max() + 1.
            xlo = df["x"].min() - 1.
            yhi = df["y"].max() + 1.
            ylo = df["y"].min() - 1.
            zhi = df["z"].max() + 1.
            zlo = df["z"].min() - 1.
            Lx = xhi - xlo
            Ly = yhi - ylo
            Lz = zhi - zlo

    df['element'] = df['type'].map(type_element_map)
    df['color'] = df['element'].map(element2color)
    df['size'] = df['element'].map(element2size)
    
    bond_df = pd.read_csv(io.StringIO(sec_strs[bond_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2'], usecols=[0, 1, 2, 3]).reset_index(drop=True)
    bond_df.index = bond_df.index + 1
    bond_df['bond_order'] = 1
    bond_df.loc[double_bonds, 'bond_order'] = 2
    bond_df.loc[triple_bonds, 'bond_order'] = 3
    angle_df = pd.read_csv(io.StringIO(sec_strs[angle_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3'], usecols=[0, 1, 2, 3, 4]).reset_index(drop=True)
    angle_df.index = angle_df.index + 1
    
    dihedral_df = pd.read_csv(io.StringIO(sec_strs[dihedral_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
    dihedral_df.index = dihedral_df.index + 1
    
    improper_df = pd.read_csv(io.StringIO(sec_strs[improper_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
    improper_df.index = improper_df.index + 1
    
    lj_coeff = None
    if lj_coeff_sec_id != -1:
        lj_coeff = pd.read_csv(io.StringIO(sec_strs[lj_coeff_sec_id]), names=['type', 'epsilon', 'sigma'], sep=r'\s+')
    bond_coeff = None
    if bond_coeff_sec_id != -1:
        bond_coeff = pd.read_csv(io.StringIO(sec_strs[bond_coeff_sec_id]), names=['type', 'kr', 'r0'], sep=r'\s+')
    angle_coeff = None
    if angle_coeff_sec_id != -1:
        angle_coeff = pd.read_csv(io.StringIO(sec_strs[angle_coeff_sec_id]), names=['type', 'ktheta', 'theta0'], sep=r'\s+')
    dihedral_coeff = None
    if dihedral_coeff_sec_id != -1:
        dihedral_coeff = pd.read_csv(io.StringIO(sec_strs[dihedral_coeff_sec_id]), names=['type', 'k1', 'k2', 'k3', 'k4'], sep=r'\s+')
    improper_coeff = None
    if improper_coeff_sec_id != -1:
        improper_coeff = pd.read_csv(io.StringIO(sec_strs[improper_coeff_sec_id]), names=['type', 'k', 'd', 'n'], sep=r'\s+')
    if viz==True: 
        if box==True:
            viz_mol(df, bond_df, annotation=annotation, box=[[xlo, xhi], [ylo, yhi], [zlo, zhi]])
        else:
            viz_mol(df, bond_df, annotation=annotation, box=None)
    
    return mass_df, df, bond_df, angle_df, dihedral_df, improper_df, [[xlo, xhi], [ylo, yhi], [zlo, zhi]], lj_coeff, bond_coeff, angle_coeff, dihedral_coeff, improper_coeff



def read_xyz_traj(filename='traj.xyz'):
    colnames = ["at", "x", "y", "z"]
    with open(filename, 'r') as myfile:
        xyz = myfile.read()
    frame_natoms = []
    frame_nsteps = []
    frame_xyzs = []
    line_list = xyz.split('\n')
    i = 0
    while i < len(line_list):
        if line_list[i].isdigit():
            frame_natoms.append(int(line_list[i]))
            frame_nsteps.append(int(re.sub("[^0-9]", "", line_list[i+1])))
            frame_xyzs.append(pd.read_csv(io.StringIO("\n".join(line_list[i+2:i+2+frame_natoms[-1]])), sep=r"\s+", names=colnames))
            i = i + 2 + frame_natoms[-1]
        else:
            i = i + 1
    print("Read xyz file with: " + str(frame_natoms[-1]) + " atoms, " + str(len(frame_nsteps)) + " frames. ")
    return frame_natoms, frame_nsteps, frame_xyzs


def viz_xyz_traj(_natoms, _nsteps, _xyzs, mass_df, writeHTML=False):
    _xyz_lims = pd.DataFrame([[_xyzs[i]["x"].min(), _xyzs[i]["x"].max(), 
                               _xyzs[i]["y"].min(), _xyzs[i]["y"].max(), 
                               _xyzs[i]["z"].min(), _xyzs[i]["z"].max()] for i in range(0, len(_xyzs))], 
                             columns=["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"])
    xyzmin = min(_xyz_lims["xmin"].min(), _xyz_lims["ymin"].min(), _xyz_lims["zmin"].min())
    xyzmax = max(_xyz_lims["xmax"].max(), _xyz_lims["ymax"].max(), _xyz_lims["zmax"].max())
    duration = 150

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": duration, 
                                              "redraw": True},
                                    "fromcurrent": True, 
                                    "mode": "immediate",
                                    "transition": {"duration": duration,
                                                   "easing": "quadratic-in-out"}
                                   }],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": duration, 
                                                "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": duration}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Step:",
            "visible": True,
            "xanchor": "left"
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }


    # make frames
    for k in range(0, len(_xyzs)):
        _xyzs[k]["element"] = _xyzs[k]["at"].map(dict(zip(mass_df["type"], mass_df["element"])))
        _xyzs[k]["mass"] = _xyzs[k]["at"].map(dict(zip(mass_df["type"], mass_df["mass"])))
        _xyzs[k]["color"] = _xyzs[k]["element"].map(element2color)
        _xyzs[k]["size"] = _xyzs[k]["element"].map(element2size)
        _xyzs[k]['id'] = _xyzs[k].index + 1
        _xyzs[k]['tip'] = "id: " + _xyzs[k]['id'].astype('str') + '<br>' + 'type: ' + _xyzs[k]['at'].astype('str') + '<br>'
        curr_frame = go.Frame(
            data=[
                go.Scatter3d(
                #dict(
                    mode="markers",
                    x=_xyzs[k]["x"],
                    y=_xyzs[k]["y"],
                    z=_xyzs[k]["z"],
                    text=_xyzs[k]['tip'],
                    marker=dict(
                        color=_xyzs[k]["color"],
                        size=_xyzs[k]["size"] * 3.4 / (len(_xyzs[k])**(1./3.)),
                        opacity=1.0,
                    ),
                )
            ],
            name=str(_nsteps[k]),
        )


        fig_dict["frames"].append(curr_frame)

        slider_step = {
            "args": [
                [str(_nsteps[k])],
                {
                    "frame": {
                        "duration": duration,
                        "redraw": True,
                    },
                    "mode": "immediate",
                    "transition": {
                        "duration": duration,
                    }
                }
            ],
            "label": str(_nsteps[k]),
            "method": "animate",
            "name": str(_nsteps[k]),
        }
        sliders_dict["steps"].append(slider_step)


    fig_dict['data'] = fig_dict["frames"][0]['data']
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig = go.Figure(fig_dict)

    DeltaX = xyzmax - xyzmin
    annotation_list = []
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )

    if writeHTML:
        fig.write_html("xyztraj.html")
    fig.show()
    
    

def viz_lmp_traj(type2cgenff, fname="traj.lammpstrj", writeHTML=False):
    traj = None
    with open(fname, 'r') as myfile:
        traj = myfile.read()

    _nsteps = []
    _natoms = []
    _xyzs = []
    traj_list = traj.split("\n")


    xlo = []
    xhi = []
    ylo = []
    yhi = []
    zlo = []
    zhi = []
    i = 0
    while i < len(traj_list):
        if traj_list[i].startswith("ITEM:"):
            if "TIMESTEP" in traj_list[i]:
                _nsteps.append(int(traj_list[i+1]))
                _natoms.append(int(traj_list[i+3]))
                _x, _y, _z = traj_list[i+5:i+8]
                _xlo, _xhi = _x.split(" ")
                _ylo, _yhi = _y.split(" ")
                _zlo, _zhi = _z.split(" ")
                xlo.append(float(_xlo))
                xhi.append(float(_xhi))
                ylo.append(float(_ylo))
                yhi.append(float(_yhi))
                zlo.append(float(_zlo))
                zhi.append(float(_zhi))
                _xyz = pd.read_csv(io.StringIO(traj_list[i+8].replace("ITEM: ATOMS ", "") + "\n" + "\n".join(traj_list[i+9:i+9+_natoms[-1]])), header=0, sep=r"\s+")
                _xyz["element"] = _xyz["mass"].round(0).map(mass2element)
                _xyz["cgenff"] = _xyz["type"].map(type2cgenff)
                _xyz["color"] = _xyz["element"].map(element2color)
                _xyz["size"] = _xyz["element"].map(element2size)
                _xyz['tip'] = "id: " + _xyz['id'].astype('str') + '<br>' + \
                              'type: ' + _xyz['type'].astype('str') + '<br>' + \
                              'cgenff: ' + _xyz['cgenff'].astype('str') + '<br>' + \
                              'charge: ' + _xyz["q"].apply(lambda i: ("+" if i > 0 else "") + str(i)).astype('str')
                _xyzs.append(_xyz)
                i = i+9+_natoms[-1]
        else:
            i = i + 1


    xyzmin = min(min(xlo), min(ylo), min(zlo))
    xyzmax = max(max(xhi), max(yhi), max(zhi))

    duration = 100

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": duration, 
                                              "redraw": True},
                                    "fromcurrent": True, 
                                    "mode": "immediate",
                                    "transition": {"duration": duration,
                                                   "easing": "quadratic-in-out"}
                                   }],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": duration, 
                                                "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": duration}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Step:",
            "visible": True,
            "xanchor": "left"
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    annotation_list = []
    annotation_list.append({'x': xhi[0]+1, 
                            'y': ylo[0], 
                            'z': zlo[0], 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "X",  
                            'font': {'size': 30, 'color':'rgba(255,0,0,1)',}})
    annotation_list.append({'x': xlo[0], 
                            'y': yhi[0]+1, 
                            'z': zlo[0], 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "Y",  
                            'font': {'size': 30, 'color':'rgba(0,255,0,1)',}})
    annotation_list.append({'x': xlo[0], 
                            'y': ylo[0], 
                            'z': zhi[0]+1, 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "Z",  
                            'font': {'size': 30, 'color':'rgba(0,0,255,1)',}})
    # make frames
    for k in range(0, len(_xyzs)):

        _xyzs[k]["color"] = _xyzs[k]["element"].map(element2color)
        _xyzs[k]["size"] = _xyzs[k]["element"].map(element2size)
        curr_frame = go.Frame(
            data=[
                go.Scatter3d(
                    mode="markers",
                    x=_xyzs[k]["x"],
                    y=_xyzs[k]["y"],
                    z=_xyzs[k]["z"],
                    text=_xyzs[k]['tip'],
                    marker=dict(
                        color=_xyzs[k]["color"],
                        size=_xyzs[k]["size"] * 3.4 / (len(_xyzs[k])**(1./3.)),
                        opacity=1.0,
                    ),
                ),

                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(225, 0, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(0, 225, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(0, 0, 225, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                ))
            ],
            name=str(_nsteps[k]),
        )






        fig_dict["frames"].append(curr_frame)

        slider_step = {
            "args": [
                [str(_nsteps[k])],
                {
                    "frame": {
                        "duration": duration,
                        "redraw": True,
                    },
                    "mode": "immediate",
                    "transition": {
                        "duration": duration,
                    }
                }
            ],
            "label": str(_nsteps[k]),
            "method": "animate",
            "name": str(_nsteps[k]),
        }
        sliders_dict["steps"].append(slider_step)


    fig_dict['data'] = fig_dict["frames"][0]['data']
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig = go.Figure(fig_dict)

    DeltaX = xyzmax - xyzmin
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )
    if writeHTML:
        fig.write_html(fname+".html")
    fig.show()
