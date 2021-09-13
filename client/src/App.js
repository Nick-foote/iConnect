// import logo from './logo.svg';
import './App.css';
import React from 'react';
import { MapContainer, TileLayer } from "react-leaflet";


const App = () => {
  return (
    <MapContainer center={[51.51, -0.1]} zoom={14}>
      <TileLayer 
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  );
};

export default App;