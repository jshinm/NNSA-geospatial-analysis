import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "plotly_mimetype+notebook_connected"

def render_map(df, color, size, title, zoom_lat, zoom_lon, zoom=False):

    if isinstance(color, str):
        c = df[color]
    elif isinstance(color, int):
        c = df.iloc[:,color]
    else:
        return "None Rendered"

    fig = go.Figure(go.Scattergeo(
        lat=df.Latitude,
        lon=df.Longitude,
        geojson={'center':{'lat':37, 'lon': 141}},
        marker=dict(
            color=c,
            size=c/size,
            colorbar=dict(
                ticks='outside'
            )
        ),
    ))

    fig.update_layout(
        title=title,
        width=900,
        height=700,
        geo={
            'showland': True,
            'showocean': True,
            'resolution':50,
            'center': {'lat':zoom_lat, 'lon':zoom_lon},
            'projection_scale': 10
        }
    )

    if zoom:
        fig.update_layout(
        title=title+' (Zoomed In)',
        geo={
            'center': {'lat':zoom_lat, 'lon': zoom_lon},
            'projection_scale': 350
            }
        )

    fig.show()