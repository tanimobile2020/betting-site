import { API_ENDPOINTS } from '../config'
import { ApiClient } from '../core/apiClient'

// Define the URLs for the authentication endpoints
const AUTH_URLS = {
    LOGIN: 'token/',
    REGISTER: 'register/',
    REFRESH_TOKEN: 'token/refresh/',
    LOGOUT: 'logout/'
}

// Create the AuthAdapter class
class AuthAdapter {
    constructor () {
        this.client = new ApiClient(API_ENDPOINTS.ACCOUNTS)
    }

    async login (credentials) {
        return this.client.post(AUTH_URLS.LOGIN, credentials)
    }

    async register (credentials) {
        return this.client.post(AUTH_URLS.REGISTER, credentials)
    }

    async refreshToken () {
        return this.client.get(AUTH_URLS.REFRESH_TOKEN)
    }

    async logout () {
        return this.client.post(AUTH_URLS.LOGOUT)
    }
}

export const authAdapter = new AuthAdapter()
