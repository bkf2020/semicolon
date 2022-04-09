var oldUnreadCount = 0;
function sendMessage(unread_count) {
	if(unread_count >= 1 && unread_count != oldUnreadCount) {
		var message = "A new contest announcement has been posted! ";
		message += "Please reload the page and click the announcement link to view it!";
		alert(message);
		oldUnreadCount = unread_count;
	}
}

function getNumberOfNotifications() {
	fetch('/inbox/notifications/api/unread_count/')
		.then(response => response.json())
		.then(data => sendMessage(data["unread_count"]));
}

setInterval(getNumberOfNotifications, 1000);
