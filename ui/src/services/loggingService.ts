export class LoggingService {
    constructor() {
    }

    public async send(data: object) {
        console.log(JSON.stringify(data, null, 2));
    }
}