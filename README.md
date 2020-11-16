# iConnect

A program that connects users with each other based on location.
You can find out what Spotify playlists your neighbours are listening to.


## Process

Spotify will first verify the API Client ID and Client Secret keys, asking the user to verify their Spotify Account

<img width="700" alt="iConnect_login" src="https://user-images.githubusercontent.com/68865367/99266260-7c9f2f80-281a-11eb-8e19-7de9f3680ea1.png">

Then the program will automatically locate the user's Latitude & Longitude coordinates, and save their location coordinates and address in PostGreSQL.

```python
user_geo = geocoder.ip('me')
user_latitude, user_longitude = user_geo.latlng[0], user_geo.latlng[1]
area, county, country = user_geo.address.split(", ")
```
    
    

Once completed, the program will print out which neighbour is closest to you and how many miles away. 
<img width="700" alt="iConnect_combined_whole_output" src="https://user-images.githubusercontent.com/68865367/99256796-d9481d80-280d-11eb-8b59-e2ed84b6cef2.png">

Finally openen their most recent Spotify playlist in the Spotify App
<img width="700" alt="iConnect_spot" src="https://user-images.githubusercontent.com/68865367/99266602-d869b880-281a-11eb-8ff6-40ad9f64cf03.png">
