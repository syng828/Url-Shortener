export class ApiResponse {
    constructor(error = false, responseData = null) {
        this.error = error;
        this.responseData = responseData;
    }
}