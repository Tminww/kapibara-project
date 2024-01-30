// import auth from "./auth";
// import users from "./users";
// import utils from "./utils";
import statistics from './statistics'
// import { authInterceptor, notificationInterceptor } from "./interceptors";
import http from './http'
// import { useAuth } from "@/user-account/composables/useAuth";

const api = {
	statistics,
	//   auth,
	//   users,
	//   utils,
	init() {
		http.setUrl('http://localhost:8080/')
		// to set token into every request
		// http.setTokenCallback(useAuth().getToken);
		// http.setLogoutCallback(useAuth().logout);
		// http.addResponseInterceptor(notificationInterceptor);
		// http.addResponseInterceptor(authInterceptor);
	},
}

export { api }
export default api
