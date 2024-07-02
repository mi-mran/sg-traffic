import streamlit as st
import requests
import pandas as pd
import datetime
import pydeck as pdk

def get_traffic_images():
    #date = datetime.datetime(INPUT_YEAR, INPUT_MONTH, INPUT_DATE, INPUT_HOUR, INPUT_MINUTE, INPUT_SECOND)

    url = "https://api.data.gov.sg/v1/transport/traffic-images"
    # response contains 2 keys: 'timestamp' and 'cameras'
    response = requests.get(url).json()["items"][0]

    return response

def get_camera_coords(camera_arr):
    coords_df = pd.DataFrame(columns=['lat', 'lon', 'curr_img', 'camera_id'])
    
    for camera in camera_arr:
        #print(camera)

        row_data = {
            'camera_id': [camera['camera_id']],
            'lat': [camera['location']['latitude']],
            'lon': [camera['location']['longitude']],
            'curr_img': [camera['image']]
        }

        new_row = pd.DataFrame(row_data)

        coords_df = pd.concat([coords_df, new_row])
    
    return coords_df


def main():

    traffic_images = get_traffic_images()
    coords_df = get_camera_coords(traffic_images['cameras'])

    st.write(coords_df)

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=1.380812, 
                longitude=103.791963,
                zoom=11,
                pitch=0,
                bearing=0
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=coords_df[['lat', 'lon', 'camera_id', 'curr_img']],
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                    pickable=True
                )
            ],
            tooltip={
                "html": "<b>Camera ID:</b> {camera_id} <br> <img src='{curr_img}' alt='' width='200' height='200'>", 
                "style": {
                    "color": "white"
                    }
                },
        )
    )    

if __name__ == '__main__':
    main()