#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random
import base64

import plotly.express as px
import plotly.graph_objects as gp   
import dash
from dash.exceptions import PreventUpdate
from dash import Dash, dash_table
from dash import Input, Output, State, html
from dash import Dash, dcc, html, Input, Output
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc


# In[2]:


#!pip install jupyter-dash


# # Karma Wangchuk

# In[3]:


def stdc(std):
    stddf = pd.read_csv('both_batches.csv')
    stddf.drop(['Unnamed: 0'],axis=1,inplace=True)
    stddf. astype(str)
    
    b=stddf[['Batch','Name']]
    x = b[['Batch']].value_counts()
    y = len(x)
    d = b[['Name']].count()
    
    
    return[y,d] 


# In[4]:


stddf = pd.read_csv('both_batches.csv')
stddf.drop(['Unnamed: 0'],axis=1,inplace=True)
stddf. astype(str)

b=stddf[['Batch','Name']]
x = b[['Batch']].value_counts()
y = len(x)
d = b[['Name']].count()


# In[5]:


def details(std):
    stddf = pd.read_csv('both_batches.csv')
    stddf.drop(['Unnamed: 0'],axis=1,inplace=True)
    stddf. astype(str)
    
    df = stddf.groupby(['Dzongkhags','LATITUDE','LONGITUDE','Batch',]).count()[['Name']]
    df = df.reset_index()
    df = df.rename(columns={'Name':'Number of Student'})
    
    df1 = pd.read_csv('batch_reader1.csv').copy()
    
    df2 = stddf[['Batch','Gender','Highest Education','Final Score','Grade']].copy()
    
    
    df3 = stddf.groupby(['Batch','Age']).count()[['Grade']]
    df3.reset_index(inplace=True)
    
    
    
    return[df,df1,df2,stddf]


# In[6]:


def graphics(std):
    [df,df1,df2,stddf]=details(std)
    
    fig3 = px.scatter_mapbox(df, lat = 'LATITUDE', lon = 'LONGITUDE', color = 'Batch', hover_name = "Dzongkhags",
                             size='Number of Student', hover_data= {"Dzongkhags":True, "Batch": True,"LATITUDE": False,
                            "LONGITUDE": False},)
    fig3.update_layout(mapbox_style='open-street-map')
    fig3.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
   
    
    fig4 = px.bar(df1, x="Module", y='Score',color='Batch',barmode = 'group')
    fig4.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
    fig4.update_layout(title={'text' : 'Performance vs. Modules', 'font_size' : 20,'x':0.45,'xanchor': 'center'})
    
    fig5 = px.sunburst(df2, path=['Gender','Batch','Highest Education','Grade'], values='Final Score')
    fig5.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
    fig5.update_layout(title={'text' : 'Performance vs. Gender', 'font_size' : 20,'x':0.45,'xanchor': 'center'})
    
    fig6 = px.box(stddf, x = 'Batch', y = 'Age',color='Grade', title = 'Performance vs. Ages')
    fig6.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
    fig6.update_layout(title={'font_size' : 20,'x':0.45,'xanchor': 'center'})
    return[fig3,fig4,fig5,fig6]


# # Rinchen Jamtsho

# In[7]:


df=pd.read_csv('Grades_Final_score_B1.csv')
df1=pd.read_csv('Grades - Final_score_B2.csv')


# In[8]:


gr=df.groupby(['Grade','Highest Education']).count()[['ID']]
gr.reset_index(inplace=True)


# In[9]:


gr1=df.groupby(['Age','Grade','Gender']).count()[['ID']]
gr1.reset_index(inplace=True)


# In[10]:


gp=df1.groupby(['Education','Overall Grade']).count()[['ID']]
gp.reset_index(inplace=True)


# In[11]:


gp1=df1.groupby(['Age','Overall Grade','Gender']).count()[['ID']]
gp1.reset_index(inplace=True)


# # Kiran Gurung

# In[12]:


df1=pd.read_csv('Grades_Final_score_Batch11.csv')
df2=pd.read_csv('Grades_Final_score_Batch22.csv')
df3 = pd.concat([df1,df2],axis=0)


# In[13]:


def getscore(students):
    name = df3[df3['Name']==students]
    batch = name.iloc[0,6]  
    rank = name.iloc[0,18]
    grade = name.iloc[0,17]
    return [batch,rank,grade]


# In[14]:


def drawfig(students):
    name = df3[df3['Name']==students]
    data = name[['Module 1','Module 2','Module 3','Module 4','Module 5','Module 6','Module 7','Module 8','Module 9']]
    moduledf=data.T
    moduledf.reset_index(inplace=True)
    moduledf.rename(columns={'index':'Module',moduledf.columns.values[1]:'Score'},inplace=True)
    moduledf[['Score']]=moduledf[['Score']].astype(int)
    
    fig7 = px.bar(moduledf, x = 'Module', y = 'Score',color='Module', labels = {'Score' : 'TOTAL SCORE', 'Name' : 'MODULES'})
    fig7.update_layout(title={'text': 'AVERAGE SCORE OBTAINED BY STUDENT IN EACH MODULE', 'font_size':20,
                             'x':0.45,'xanchor': 'center'})
    return fig7


# # Namgay Tshering

# In[15]:


df4=pd.read_csv('both_batches.csv')
df4.drop(['Unnamed: 0'],axis=1,inplace=True)
df4=df4. astype(str)


# # Layout

# In[16]:


app = JupyterDash(external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.FONT_AWESOME])
app.title = "Dashboard for Data Analytics (first batch and second batch) Performance"
server = app.server


# In[17]:


image_filename =  'batch1.jpg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename =  'batch2.jpg'
encoded_image2 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = 'ibm.png'
ibm = base64.b64encode(open(image_filename, 'rb').read())
image_filename = 'drmyo.JPG'
drmyo = base64.b64encode(open(image_filename, 'rb').read())
image_filename = 'desuung.png'
desuung = base64.b64encode(open(image_filename, 'rb').read())


# In[18]:


students=list(df3['Name'])

app.layout= dbc.Container([
    html.Div([

        html.Div([
            html.Img(
                    src = 'data:/image/png;base64,{}'.format(desuung.decode()),
                    height = '90 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '4%',
                    'height' : 'auto'}), 

        html.Div([
            html.H1(children='DSP Data Analytics Students Performance Dashboard',
                    style = {'font-family': 'Comic Sans MS','textAlign':'center','color':'#fcba03','fontsize':60}
            )],
            className='col-8',
            style = {'padding-top' : '4%'}
        ),

        html.Div([
            html.Img(
                    src = 'data:/image/png;base64,{}'.format(ibm.decode()),
                    height = '80 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '4%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%'}
        ),
    
    html.Br(),
    html.Br(),
        
    html.Div([
        dbc.Row([
                dbc.Col(
                    dbc.Card([
                    dbc.CardImg(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), top=True),
                    dbc.CardBody([
                            html.H4("First Batch", className="card-title"),
                            html.P(
                                "There are total 20 students with "
                                "16 Male student and 4 Female student",
                                className="card-text",
                            ),
                        ],style={'font-family': 'Comic Sans MS','fontsize':20}),
                ],
                ),),
                
                dbc.Col(
                    dbc.Card([
                    dbc.CardImg(src='data:image/jpg;base64,{}'.format(drmyo.decode()), top=True),
                    dbc.CardBody([
                            html.H4("Dr. Myo Thida", className="card-title"),
                            html.P(
                                "She is our lecturer who comes from Myanmar and "
                                "she is the person who taught us to move in the right",
                                className="card-text",
                            ),
                        ],style={'font-family': 'Comic Sans MS','fontsize':20}),
                ],
                ),),
            
                dbc.Col(
                    dbc.Card([
                    dbc.CardImg(src='data:image/jpg;base64,{}'.format(encoded_image2.decode()), top=True),
                    dbc.CardBody([
                            html.H4("Second Batch", className="card-title"),
                            html.P(
                                "There are total 20 students with "
                                "9 Male student and 11 Female student",
                                className="card-text",
                            ),
                        ],style={'font-family': 'Comic Sans MS','fontsize':20}),
                ],
                ),),
        ]),
    ],style={'display':'flex'}),
    
    
    html.Br(),
    html.Br(),
    
    html.Div([
        dbc.Button('Overall',id='overall',color='info',className="col-1 mx-auto",size="lg"),
        dbc.Button('By Batch',id='batch',color='info',className="col-2 mx-auto",size="lg"),
        dbc.Button('By individual',id='individual',color='success',className="col-3 mx-auto",size="lg"),
        dbc.Button('Detailed Info',id='project',color='danger',className="col-4 mx-auto",size="lg")  

    ],style={'display':'flex','font-family': 'Comic Sans MS'}),
    
    
    html.Br(),
    
    html.Div(
        dbc.Collapse(
                dbc.Tabs([
                        dbc.Tab(label="First Batch", tab_id="batch1"),
                        dbc.Tab(label="Second Batch", tab_id="batch2"),
                        ], id="tabs", active_tab="education1",style={'font-family': 'Comic Sans MS','fontsize':20}
                    ),
            id='p',is_open=False,
        )
    ),
    
    html.Br(),
    
    html.Div(
        dbc.Collapse(
                html.Div([
                    dcc.Graph('plot1'),
                    dcc.Graph('plot2')
                ],id= 'g_id',style={'display':'flex'}),id='n',is_open=False,
        )
    ),  
    
    html.Br(),
    
    html.Div(dbc.Collapse([
         html.Div([
             html.Div([
            html.H2('Number of Batches',style={'textAlign':'center','color':'#FC0A02','fontsize':40,'font-family': 'Comic Sans MS'}),
            html.Div(id="Num_b",style={'height':35,'textAlign':'center','fontsize':40,'color':'#ffff','font-family': 'Comic Sans MS',
                                        'color':'#0a0a00','border-color':'blue','background-color':'#f0e40c','margin-left':'20px'}),
        ],id='number_box',style={'width':'40%','padding':'3px','fontsize':40}),
        
        html.Div([
            html.H2('Number of Students ',style={'textAlign':'center','color':'#FC0A02','fontsize':40,'font-family': 'Comic Sans MS'}),
            html.Div(id="Num_std",style={'height':35,'textAlign':'center','fontsize':40,'font-family': 'Comic Sans MS',
                                        'color':'#0a0a00','border-color':'blue','background-color':'#f0e40c','margin-left':'20px'}),
        ],id='best_std',style={'width':'40%','padding':'3px','fontsize':40}),
         ],style={'display':'flex'}),
    
    html.Br(),
    
    html.Br(),
    
    html.Div([
        dcc.Graph('plot3'),
        dcc.Graph('plot4'),
    ],style = {'display':'flex'}),
    
    html.Div([
        dcc.Graph('plot5'),
        dcc.Graph('plot6'),
    ],style={'display':'flex'}),],id='col_id', is_open=False),),
    
    
    html.Div(
            dbc.Collapse(
                html.Div([
                html.H2('Select Students',style={'font-family': 'Comic Sans MS','textAlign':'left','color':'#3498db','fontsize':40}),

                dcc.Dropdown(id='std_id',clearable=False,
                            options=[{'label':g,'value':g} for g in students],
                            placeholder='' ,
                             style={'font-family': 'Comic Sans MS','width':'40%','padding':'3px','fontsize':40,'color':'#9932CC'})

            ], style = {'display': 'flex'}),id='coll_id1',is_open=False,
                ),
            ),
    
    html.Div(
        dbc.Collapse(
            html.Div([
                html.Div(
                    [
                        html.H2('Batch :',style={'textAlign':'center','color':'#3498db','fontsize':20,'font-family': 'Comic Sans MS'}),
                        html.Div(id='batch_id', style={'height': 30, 'textAlign':'center', 'fontsize':20,'font-family': 'Comic Sans MS',
                                       'color':'#0a0a00','border-color': 'red','background-color': '#f0e40c','margin-left': '20px'}),
                        
                    ], id = 'batch1', style = {"width": "30%", 'padding': 10}),

                html.Div([
                        html.H2('Rank :',style={'textAlign':'center','color':'#3498db','fontsize':20,'font-family': 'Comic Sans MS'}),
                        html.Div(id='rank_id', style={'height': 30, 'textAlign':'center', 'fontsize':20,'font-family': 'Comic Sans MS',
                                       'color':'#0a0a00','border-color': 'red','background-color': '#f0e40c','margin-left': '20px'}), 
                    ], id = 'rank1', style = {"width": "30%", 'padding': 10},),

                html.Div([
                        html.H2('Overall Grade : ',style={'textAlign':'center','color':'#3498db','fontsize':20}),
                        html.Div(id='overall_id', style={'height': 30, 'textAlign':'center', 'fontsize':20,'font-family': 'Comic Sans MS',
                                       'color':'#0a0a00','border-color': 'red','background-color': '#f0e40c','margin-left': '20px'}), 
                    ], id = 'overall1', style = {"width": "30%", 'padding': 10}),
             ],style = {'display': 'flex'}),id='coll_id2',is_open=False),
    ),
    html.Div(
        dbc.Collapse(
                html.Div([
                    dcc.Graph('plot7'),
                ],id= 'gaph_id',),id='coll_id3',is_open=False,),
    ),
    
    html.Div(
        dbc.Collapse(
            html.Div(id="table"),id='coll',is_open=False,
        ),style={'font-family': 'Comic Sans MS','fontsize':20}
     ),

])


# In[19]:


@app.callback(
        Output('col_id','is_open'),
        Input('overall','n_clicks'),
        State('col_id','is_open'),
)

def grawfig(n,is_open):
    if n:
        return not is_open
    return is_open


# In[20]:


@app.callback(
        Output('n','is_open'),
        Input('batch','n_clicks'),
        State('n','is_open'),
)

def grawfig(n,is_open):
    if n:
        return not is_open
    return is_open


# In[21]:


@app.callback(
        Output('p','is_open'),
        Input('batch','n_clicks'),
        State('p','is_open'),
)

def grawfig(n,is_open):
    if n:
        return not is_open
    return is_open


# In[22]:


@app.callback([
    Output('Num_b','children'),
    Output('Num_std','children'),
    Output('plot3','figure'),
    Output('plot4','figure'),
    Output('plot5','figure'),
    Output('plot6','figure')
],
  Input('overall','n_clicks'))

def draw_graph(std):
    if std is None:
        raise PreventUpdate
    else:
        [fig3,fig4,fig5,fig6]=graphics(std)
        
        [op1,op2] = stdc(std)
        
    return [op1,op2,fig3,fig4,fig5,fig6]


# In[23]:


@app.callback([
    Output('plot1','figure'),
    Output('plot2','figure')
],[Input('tabs','active_tab')])

def draw_graph(tabs): 
    if tabs is None:
        raise PreventUpdate
    elif (tabs=='batch1'):
        fig1=px.treemap(gr,path=['Highest Education','Grade'],values='ID',title='Pefromance vs. Qualification')
        fig1.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
        fig1.update_layout(autosize = False,width = 800,height=500)
        fig1.update_layout(title={'font_size' : 20,'x':0.45,'xanchor': 'center'})
        
        fig2=px.sunburst(gr1,path=['Gender','Age','Grade'],values='ID',title='Performance vs. Gender and Age')
        fig2.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
        fig2.update_layout(autosize = False,width = 800,height=500)
        fig2.update_layout(title={'font_size' : 20,'x':0.45,'xanchor': 'center'})
    else:
        fig1=px.treemap(gp,path=['Education','Overall Grade'],values='ID',title='Pefromance vs. Qualification')
        fig1.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
        fig1.update_layout(autosize = False,width = 800,height=500)
        fig1.update_layout(title={'font_size' : 20,'x':0.45,'xanchor': 'center'})
        
        fig2=px.sunburst(gp1,path=['Gender','Age','Overall Grade'],values='ID',title='Performance vs. Gender and Age')
        fig2.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
        fig2.update_layout(autosize = False,width = 800,height=500)
        fig2.update_layout(title={'font_size' : 20,'x':0.45,'xanchor': 'center'})
        
    return [fig1,fig2]


# In[24]:


@app.callback(
    [
    Output('batch_id','children'),
    Output('rank_id','children'),
    Output('overall_id','children'),
    Output('plot7','figure'),   
],[
    Input('std_id','value')
])

def draw_graph_std(students):
    if students is None:
        raise PreventUpdate
        
    else:
        fig7 = drawfig(students)
        [batch,rank,grade]=getscore(students)

   
    return [batch,rank,grade,fig7]


# In[25]:


@app.callback(
    Output("coll_id1", "is_open"),
    [Input("individual", "n_clicks")],
    [State("coll_id1", "is_open")],
)
def toggle_coll(k, is_open):
    if k:
        return not is_open
    else:
        return is_open


# In[26]:


@app.callback(
        Output('coll_id2','is_open'),
        Input('individual','n_clicks'),
        State('coll_id2','is_open'),
)

def toggle_coll(c,is_open):
    if c:
        return not is_open
    return is_open


# In[27]:


@app.callback(
        Output('coll_id3','is_open'),
        Input('individual','n_clicks'),
        State('coll_id3','is_open'),
)

def toggle_coll(g,is_open):
    if g:
        return not is_open
    return is_open


# In[28]:


@app.callback(
        Output('coll','is_open'),
        Input('project','n_clicks'),
        State('coll','is_open'),
)

def grawfig(n,is_open):
    if n:
        return not is_open
    return is_open


# In[29]:


@app.callback(
    Output("table", "children"),
    Input('project','n_clicks'),
)
def make_table(s):
    df4=pd.read_csv('both_batches.csv')
    df4.drop(['Unnamed: 0', 'LATITUDE', 'LONGITUDE'],axis=1,inplace=True)   
        
    return dbc.Table.from_dataframe(df4.head(5), striped=True, bordered=True, color = "primary", hover=True)


# In[30]:


if __name__ == '__main__':
    port = 5000 + random.randint(0, 999)    
    url = "http://127.0.0.1:{0}".format(port)    
    app.run_server(use_reloader=False, debug=True, port=port)


# In[ ]:




