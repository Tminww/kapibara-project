export function getBasicAutorizationHeader() {
	// return authorization header with basic auth credentials
	let user = JSON.parse(localStorage.getItem('user'))

	if (user && user.authdata) {
		return { Authorization: 'Basic ' + user.authdata }
	} else {
		return {}
	}
}

export function getBearerAutorizationHeader() {
	// return authorization header with basic auth credentials
	let user = JSON.parse(localStorage.getItem('user'))

	if (user && user.authdata) {
		return { Authorization: 'Basic ' + user.authdata }
	} else {
		return {}
	}
}

export function getAuthDataFromLocalStorage() {
	return {
		username: localStorage.getItem('username'),
		role: localStorage.getItem('role'),
		rights: localStorage.getItem('rights'),
		token: localStorage.getItem('token'),
	}
}

export function setAuthDataToLocalStorage({
	username = null,
	role = null,
	rights = null,
	token = null,
}) {
	localStorage.setItem('user', username)
	localStorage.setItem('role', role)
	localStorage.setItem('rights', rights)
	localStorage.setItem('token', token)
}
