// Get the hash of the url
const hash = window.location.hash
.substring(1)
.split('&')
.reduce(function (initial, item) {
  if (item) {
    var parts = item.split('=');
    initial[parts[0]] = decodeURIComponent(parts[1]);
  }
  return initial;
}, {});
window.location.hash = '';

// Set token
let _token1 = hash.access_token;
let _token2 = hash.access_token;

const authEndpoint = 'https://accounts.spotify.com/authorize';

// Replace with your app's client ID, redirect URI and desired scopes
const clientId = 'edb26c94b39d44cf8f456452182cfc0e';
const redirectUri = 'http://newuser650.pythonanywhere.com/play/start';
const scopes1 = [
  'streaming',
  'user-read-email',
  'user-read-private'
];
const scopes2 = [
  'user-modify-playback-state'
];

// If there is no token, redirect to Spotify authorization
if (!_token1) {
  window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes1.join('%20')}&response_type=token&show_dialog=true`;
}

if (!_token2) {
  window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes2.join('%20')}&response_type=token&show_dialog=true`;
}

// Set up the Web Playback SDK

window.onSpotifyPlayerAPIReady = () => {
  const player = new Spotify.Player({
    name: 'Web Playback SDK Template',
    getOAuthToken: cb => { cb(_token1); }
  });

  // Error handling
  player.on('initialization_error', e => console.error(e));
  player.on('authentication_error', e => console.error(e));
  player.on('account_error', e => console.error(e));
  player.on('playback_error', e => console.error(e));

  // Playback status updates
  player.on('player_state_changed', state => {
    console.log(state)
    $('#current-track').attr('src', state.track_window.current_track.album.images[0].url);
    $('#current-track-name').text(state.track_window.current_track.name);
  });

  // Ready
  player.on('ready', data => {
    console.log('Ready with Device ID', data.device_id);
    //alert(_token1);
    //alert(_token2);
    // Play a track using our new device ID
    play(data.device_id);
  });

  // Connect to the player!
  player.connect();
}

var ul = uris.split(",");
var len = ul.length
var d = '{"uris": [';

for (var i = 0; i < len-1; i++) {
  d += '"'+ul[i]+'",'
}
d += '"'+ul[len-1]+'"'
d += ']}'

// Play a specified track on the Web Playback SDK's device ID
function play(device_id) {
  $.ajax({
   url: "https://api.spotify.com/v1/me/player/play?device_id=" + device_id,
   type: "PUT",
   data: d,
   beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + _token2 );},
   success: function(data) {
     console.log(data)
   }
  });
}