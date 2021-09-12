# iConnect

A program that connects users with each other based on location.

You can find out what Spotify playlists everyone in your neighbour is listening to.


## Logging In

Firstly you have to log into the program using your Spotify Username, this will keep the users account consistent with their Spotify account. 

Spotify will then verify the API Client ID and Client Secret keys, asking the user to verify their Spotify Account, in order to retrieve data from the API.

<img width="700" alt="iConnect_login" src="https://user-images.githubusercontent.com/68865367/99266260-7c9f2f80-281a-11eb-8e19-7de9f3680ea1.png">

The user's most recent playlist is then retrieved using the Spotify API and stored in the PostGreSQL database.


## Gathering user's location data

Then the program will automatically locate the user's Latitude & Longitude coordinates using Geocoder, saving their location coordinates and address.. 

```python
user_geo = geocoder.ip('me')
user_latitude, user_longitude = user_geo.latlng[0], user_geo.latlng[1]
area, county, country = user_geo.address.split(", ")
```
    
## Playing the closest's users Spotify playlist

Once completed, the program will print out which neighbour is closest to you and how many miles away. 

<img width="800" alt="iConnect_combined_whole_output" src="https://user-images.githubusercontent.com/68865367/99256796-d9481d80-280d-11eb-8b59-e2ed84b6cef2.png">

Finally opening their most recent Spotify playlist in the Spotify App.

<img width="800" alt="iConnect_spot" src="https://user-images.githubusercontent.com/68865367/99266602-d869b880-281a-11eb-8ff6-40ad9f64cf03.png">
