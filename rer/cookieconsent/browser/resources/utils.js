// See http://firstdoit.com/quick-tip-one-liner-cookie-read/
function getCookieValue(key) {
	return ('; ' + document.cookie).split('; ' + key + '=').pop().split(';').shift();
}
