// import logo from './logo.svg';
import axios from 'axios';
import { Icon } from 'leaflet';
import React, { useState } from 'react';
import { Alert, Spinner } from 'react-bootstrap';
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import useSWR from "swr";
import './App.css';

export const icon = new Icon ({
  iconUrl: 'images/music_icon.png',
  iconSize: [120, 100],
  iconAnchor: [25, 48],

  // TODO:  Make shadow png of marker
  // shadowUrl: 'images/music_icon_shadow.png',   
  // shadowSize: [],
  // shadowAnchor: [],

  popupAnchor: [-3, -75],
});

// promise
const fetcher = (url) => axios.get(url).then((res) => res.data);

const App = () => {
  // declare state
  const [activeActivities, setActiveActivities] = useState(null);
  const { data, error } = useSWR('/api/v1/activities', fetcher);
  const activities = data && !error ? data : {};
  const position = [51.51, -0.1];
  const zoom = 14;

  if (error) {
    return <Alert variant="danger">Please refresh your browser</Alert>;
  }

  if (!data) {
    return (
      <Spinner
        animation="border"
        variant="danger"
        role="status"
        style={{
          width: "400px",
          height: "400px",
          margin: "auto",
          display: "block",
        }}
      />
    );
  }

  return (
    <MapContainer center={position} zoom={zoom}>
      <TileLayer 
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {activities.features.map((activity) => (

        <Marker
          key={activity.properties.user}
          position={[
            activity.geometry.coordinates[1],
            activity.geometry.coordinates[0],
          ]}
          onclick={() => {
            setActiveActivities(activity);
          }}
          icon={icon}>
          <Popup
            position={[
              activity.geometry.coordinates[1],
              activity.geometry.coordinates[0],
            ]}
            onclose={() => {
              setActiveActivities(null);
            }}>
              <div>
                <h6>{activity.properties.user}</h6>
                <p>{activity.properties.playlist_name}</p>
                <p>{activity.properties.created_at}</p>
                <a href="#">Play Now</a>
              </div>
            </Popup>
          </Marker>      
      ))}
    </MapContainer>
  );
};

export default App;