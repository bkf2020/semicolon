var timers = document.getElementsByClassName('timer');
var endTimes = [];
for(var i = 0; i < timers.length; i++) {
	var secondsDiff = timers[i].getAttribute('end-time') - timers[i].getAttribute('current-server-time');
	endTimes.push(Date.now() + 1000 * secondsDiff);
}

var interval = setInterval(updateTimers, 100);
function updateTimers() {
	var timers = document.getElementsByClassName('timer');
	for(var i = 0; i < timers.length; i++) {
		var millisecondsLeft = endTimes[i] - Date.now();
		if(millisecondsLeft > 0) {
			var totSeconds = Math.ceil(millisecondsLeft / 1000);
			var seconds = totSeconds % 60;
			totSeconds -= totSeconds % 60;
			totSeconds /= 60;
			
			var minutes = totSeconds % 60;
			totSeconds -= totSeconds % 60;
			totSeconds /= 60;

			var hours = totSeconds % 24;
			totSeconds -= totSeconds % 24;
			totSeconds /= 24;
						
			var days = totSeconds;

			var timeToDisplay = days.toString() + "d " + hours.toString() + "h " + minutes.toString() + "m " + seconds.toString() + "s";
			timers[i].innerText = timeToDisplay;

		} else if(millisecondsLeft < 1000) {
			clearInterval(interval);
			setTimeout(location.reload(), 1000);
		}
	}
}
