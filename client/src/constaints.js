import L, { Icon } from 'leaflet';

export const playlistIcon = new Icon ({
    iconUrl: 'images/music_icon.png',
    iconSize: [120, 100],
    iconAnchor: [25, 48],
    shadowUrl: 'images/shadow_darker.png',   
    shadowSize: [80, 50],
    shadowAnchor: [10, -15],
    popupAnchor: [20, -75],
  });

// export const userIcon = new Icon ({
//     iconUrl: 'images/user_icon.png',
//     iconSize: [25, 50],
//     iconAnchor: [0, 0],
//     shadowUrl: 'images/shadow_darker.png',   
//     shadowSize: [15, 20],
//     shadowAnchor: [0, 0],
//     popupAnchor: [-3, -75],
//   });