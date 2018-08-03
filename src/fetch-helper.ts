export default class FetchHelper {

    static status(response: Response) {
        if (response.status >= 200 && response.status < 300) {
            return Promise.resolve(response)
        } else {
            return Promise.reject(new Error(response.statusText))
        }
    }

    static json(response: Response) {
        return response.json()
    }
}