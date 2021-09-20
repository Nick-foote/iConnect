import axios from 'axios';
import { map, Renderer } from 'leaflet';
import React, { useState, useEffect, useRef } from 'react';
import { Alert, Spinner } from 'react-bootstrap';
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import useSWR from "swr";

import './App.css';
import { playlistIcon } from "./constaints.js";

// promise
const fetcher = (url) => axios.get(url).then((res) => res.data);
// default = London
const default_location = [51.51, -0.1]
// const default_lat = 51.51;
// const default_long = -0.1;

const App = () => {
  const [activePlaylists, setActivePlaylists] = useState(null);
  const [location, setLocation] = useState(default_location);
  const { data, error } = useSWR('/api/v1/playlists', fetcher);
  const playlists = data && !error ? data : {};
  const default_zoom = 14;

  function LocationMarker() {
    const map = useMap();

    useEffect(() => {
      map.locate().on("locationfound", function (e) {
        setLocation(e.latlng);
        map.flyTo(e.latlng, map.getZoom());
        const radius = e.accuracy;
        const circle = L.circle(e.latlng, radius);
        circle.addTo(map);
      });
    }, [map]);

    return location === default_location ? null :  (
      <Marker position={location}>
        <Popup>You are here</Popup>
      </Marker>
    );
  }

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
    <> 
      <MapContainer center={location} zoom={default_zoom} watch={true}>
        <TileLayer attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>        
        <div className="msgLoading">Loading your location</div> 
        {playlists.features.map((playlist) => (
          <Marker
            key={playlist.properties.user}
            position={[
              playlist.geometry.coordinates[1],
              playlist.geometry.coordinates[0],
            ]}
            onclick={() => {
              setActivePlaylists(playlist);
            }}
            icon={playlistIcon}>
            <Popup
              position={[
                playlist.geometry.coordinates[1],
                playlist.geometry.coordinates[0],
              ]}
              onclose={() => {
                setActivePlaylists(null);
              }}>
                <div className="playlistWrapper">
                  <h6>👤 {playlist.properties.user}</h6>
                  <p className="playlistName">♫ {playlist.properties.name}</p>
                  <p>{playlist.properties.date_listened}</p>
                  <div className="spotifyWrapper">
                    <a className="spotifylink" href="spotify:playlist:6Nn9XJdB1aqj9dEB0CMIHT">
                      <img className="spotifyIcon" src="/images/spotify_icon.png" />
                      <p className="spotifyText">Play Now</p>
                    </a>
                  </div>
                </div>
            </Popup>
          </Marker>      
        ))}
        <LocationMarker />
      </MapContainer>
  </>
  );
};
export default App;

// export default geolocated({
//   positionOptions: {
//     enableHighAccuracy: false
//   },
//   userDecisionTimeout: 10000        // 10secs
// })(App);



