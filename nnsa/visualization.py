import plotly.express as px
import plotly.graph_objects as go

def render_map(df, color, size, title, zoom_lat, zoom_lon, zoom=False):
    fig = go.Figure(go.Scattergeo(
        lat=df.Latitude,
        lon=df.Longitude,
        geojson={'center':{'lat':37, 'lon': 141}},
        marker=dict(
            color=df[color],
            size=df[color]/size,
            colorbar=dict(
                ticks='outside'
            )
        ),
    ))

    if zoom:
        fig.update_layout(
        title=title+'<br>Zoomed in',
        geo={
            'center': {'lat':zoom_lat, 'lon': zoom_lon},
            'projection_scale': 350
            }
        )
    else:
        fig.update_layout(
            title=title,
            width=1300,
            height=700,
            geo={
                'showland': True,
                'showocean': True,
                'resolution':50,
                'center': {'lat':zoom_lat, 'lon':zoom_lon},
                'projection_scale': 10
            }
        )