from flask import Flask, render_template
import pandas as pd
import plotly.express as px

data = pd.read_csv("MOCK_DATA.csv")

app = Flask(__name__)

df = data.copy()
percentage = df.groupby('Week')['Policy Adherence'].apply(lambda x: (x == 'Adhered').mean() * 100).reset_index()

@app.route("/")
def index():

    contacts_audited = df.shape[0]
    adherence_percent = (df[df['Policy Adherence'] == 'Adhered'].shape[0] / df.shape[0])
    deviation_percent = (df[df['Policy Adherence'] == 'Deviated'].shape[0] / df.shape[0])

    fig = px.line(percentage, x='Week', y='Policy Adherence', title='Percentage of "Yes" Responses by Week', width=1500)
    fig.update_layout(plot_bgcolor='black',paper_bgcolor='black')

    yes_percent = df[df['Policy Adherence'] == 'Adhered'].count() / len(df)
    fig2 = px.pie(values=[yes_percent[0], 1 - yes_percent[0]], names=['Adhered', 'Deviated'],
                  color_discrete_sequence=['green', 'lightblue'])
    fig2.update_traces(hole=0.6, textinfo='none', hovertemplate='%{label}: %{value:.0%}')
    fig2.add_annotation(x=0.5, y=0.5, text='Adherence: {:.0%}'.format(yes_percent[0]),
                        showarrow=False, font=dict(size=19, color='white'))
    fig2.update_layout(title='Adherence Percentage', font_size=16,plot_bgcolor='black',paper_bgcolor='black')
    fig2.update_traces(rotation=0, direction='clockwise', textposition='inside')

    counts2 = df.groupby(["Site", "Policy Adherence"]).size().reset_index(name="Count")
    total_counts = counts2.groupby("Site")["Count"].transform("sum")
    counts2["Percent"] = counts2["Count"] / total_counts * 100
    color_map = {"Adhered": "green", "Deviated": "red"}
    # Create a Sunburst chart with plotly.express

    fig3 = px.sunburst(counts2, path=["Site", "Policy Adherence"], values="Count", color="Policy Adherence",
                       color_discrete_map=color_map)
    fig3.update_layout(title="SiteWise Adherence Distribution", font_size=16,paper_bgcolor='black')


    # render the template with both figures
    return render_template("index.html", fig=fig, fig2=fig2, fig3=fig3,contacts_audited=contacts_audited,
                           adherence_percent= adherence_percent,deviation_percent=deviation_percent)


if __name__ == "__main__":
    app.run(debug=True)
