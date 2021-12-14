import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Dash Delcartions
external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server


#Data Frame Declartions. These Dataframes have been transformed in another program, then uploaded to github to ease resources and loading times.
Decision_Year_Count_df = pd.read_csv("https://raw.githubusercontent.com/DMRocks/supreme-court-visualization/main/Decision_Year_Count_df.csv", index_col=0)
State_Origin_df_count = pd.read_csv("https://raw.githubusercontent.com/DMRocks/supreme-court-visualization/main/State_Origin_df_count.csv", index_col=0)
Stacked_Area_df = pd.read_csv("https://raw.githubusercontent.com/DMRocks/supreme-court-visualization/main/Stacked_Area_df.csv", index_col=0)

#Define Figures
cases_time_fig = px.line(Decision_Year_Count_df)

cases_time_fig.update_layout(
    title = "Frequency of Supereme Court Cases by Term (1791-2020)",
    yaxis_title = 'Number of Cases',
    xaxis_title = 'Year',
    showlegend= False,
    xaxis = dict(
        dtick = 10
    )
)

#Stacked Isssue Graphs
stacked_area_issue_graph = px.area(Stacked_Area_df)

stacked_area_issue_graph.update_layout(
    title = "Supereme Court Cases by Issue (1791-2020)",
    yaxis_title = 'Number of Cases',
    xaxis_title = 'Term Year',
    legend_title_text='Issue',
    xaxis = dict(
        dtick = 10
    )
)

def stacked_graph_annoations(Year, y_height, text, position):
    stacked_area_issue_graph.add_trace(go.Scatter(
        x=[Year, Year],
        y=[y_height, 0],
        mode="lines+text",
        name=text,
        text=[text],
        textposition=position,
        line=dict(color='LightSeaGreen')
    ))

stacked_graph_annoations(1846, 230, "Start of the <br> Mexican American War", "middle left")
stacked_graph_annoations(1861, 300, "Start of the <br> Civil War", "middle left")
stacked_graph_annoations(1912, 350, "Woodrow Wilson <br> Elected", "middle right")
stacked_graph_annoations(1955, 250, "Start of <br> Vietnam War", "middle right")
stacked_graph_annoations(1941, 275, "US Entered WWII", "middle right")
stacked_graph_annoations(1991, 200, "Soviet Union <br> Dissolution", "top center")
stacked_graph_annoations(1896, 350, "Plessy v. Ferguson", "middle left")
stacked_graph_annoations(1929, 320, "Start of the Great Depression", "top right")

#State Bar Chart
State_Orgin_Count = px.bar(State_Origin_df_count, x=State_Origin_df_count.index, y = State_Origin_df_count["Number of Cases"])

State_Orgin_Count.update_layout(
    title = "Number of Cases Orginated by State (1791-2020)",
    yaxis_title = 'Number of Cases',
    xaxis_title = 'State',
    showlegend= False
)

#Precdent Pie Chart
labels = ['Criminal Procedure', 'Civil Rights', 'First Amendment', 'Due Process',
       'Privacy', 'Attorneys', 'Unions', 'Economic Activity', 'Judicial Power',
       'Federalism', 'Federal Taxation', 'Private Action']

vaules = [71, 38, 15, 11, 3, 1, 6, 72, 21, 20, 8, 4]

pie_chart = go.Figure(data=[go.Pie(labels=labels, values=vaules)])
pie_chart.update_traces(textposition='inside')

pie_chart.update_layout(
    title = "Formal Precedent Alteration by Issue (1791-2020)",
    legend_title_text='Issue',
    uniformtext_minsize=12, 
    uniformtext_mode='hide'
)



app.layout = html.Div([
    html.H1("United States Supreme Court Data Visualization", style={'text-align':'center'}),
    html.Div([ 
        dcc.Link('The Supreme Court Database', href='http://scdb.wustl.edu/index.php')], 
        style={'text-align':'center'}),
    html.H3("What is the Supreme Court?"),
    html.Div([
        "The US Supreme Court serves as one of the three branches of the United States government. The purpose of the Supreme Court is to be the enforcer and interpreter of the Constitution of The United States. The Constitution endows a citizen with certain rights, and it is the Supreme Court's duty to assess if laws, made by the government, violate these rights. For example, these rights include the freedom of religion, speech, press or assembly. Yet, these rights are so absolute in practice. A citizen has freedom of speech, but can they use that to spread communist propaganda during war times? Can a citizen spread hate speech online? Can they encourage others to commit violent acts? These questions are left for the Supreme Court to rule on and decide. "
    ]),
    html.Div([
        dcc.Graph(figure=cases_time_fig)
    ]),
    
    html.H1("--", style={'text-align':'center'}),
    html.H3("Issues Over Time"),
    html.Div([
        dcc.Graph(figure=stacked_area_issue_graph)
    ]),
    html.Div(
        html.P("Here is a graph of Supreme Court cases by issue. The first major trend to notice is the rise of cases after the Civil War. The United States when founded was plagued by the question of state rights vs the Federal Government. After the war, the Federal Government’s power rose more and more. Consequently, there was more jurisdiction allocated to the Court and more cases. Another trend to point out is the issue of the “First Amendment.” In war-time, the United States often finds it needed to limit the right to freedom of speech and press. So, these cases go up to the Supreme Court, and often, the court finds that the government is in their power to limit speech in times of war. This is illustrated in the start of the Vietnam War. The United States at this time was afraid of communism spreading through the country, so to prevent the spread commust idea or the war on communism. The first amendment was limited. When the Soviet Union dissolved, these fears went down and we can see first amendment cases lower in numbers.")
    ),
    
    html.H1("--", style={'text-align':'center'}),
    html.H3("Cases by State"),
    html.Div(
        dcc.Graph(figure=State_Orgin_Count)
    ),
    html.Div(
        html.P("This bar chart illustrates how many cases originated in what state. While there is no legal difference where the cases came from. It is important to understand where this issues of constitutionality are coming from. California and New York are states with large populations and large cities, thus making sense the sheer amount of cases coming from these states.")
    ),

    html.H1("--", style={'text-align':'center'}),
    html.H3("Formal Change in Precedent"),
    html.Div(
        dcc.Graph(figure=pie_chart)
    ),

    html.Div(
        html.P("The Supreme Court may, in a new court case, change their earlier opinion on the constitutionality of a law, this is called altering precedent. A example of this is the Supreme Court case Brown v. Board of Education, 347 US 483 (1954). In this case the Court ruled that segregation schools based on race was in violation of the Equal Protection clause of the 14th Amendment. Overturning a earlier decision in Plessy v. Ferguson, 163 US 537 (1896), that ruled segregation legal as long as both options were equal to each other. The precedent changed. This pie chart is precedent changed by issue over the course of the Supreme Court.")
    ),
    html.Div([ 
        "NOTE: Precedent is not always able to be put into “True” or “False”. This data is analyzing formal change in precedent, in which the judges are directly stating that this court case has been overturned. For more information on how this was calculated look ",
        dcc.Link('here.', href='http://scdb.wustl.edu/documentation.php?var=precedentAlteration')], 
    style={'display': 'inline'}),
])

if __name__ == '__main__':
    app.run_server()
