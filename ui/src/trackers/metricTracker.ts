import { LoggingService } from "../services/loggingService";

// Define a generic interface for metrics
export interface MetricValue {
    [key: string]: number | string; // This allows for flexibility in defining metric values
}

export class MetricTracker<T extends MetricValue> {
    protected metricName: string;
    protected loggingService: LoggingService;
    protected values: T[] = [];

    constructor(loggingService: LoggingService) {
        this.loggingService = loggingService;
    }

    /**
     * Adds a new value to the metric.
     * @param value An object of type T representing the metric value to add.
     */
    public addValue(value: T): void {
        this.values.push(value);
        // this.logMetrics();
    }

    /**
     * Calculates the average of the stored metric values.
     * @returns {T} An object of type T representing the average of the metric values.
     */
    public getAverage(): T {
        if (this.values.length === 0) return {} as T;

        const total = this.values.reduce((sum: any, value: T) => {
            for (const key in value) {
                sum[key] = (sum[key] || 0) + value[key]; // Accumulate totals
            }
            return sum;
        }, {});

        const average: any = {};
        for (const key in total) {
            average[`average_${key}`] = total[key] / this.values.length; // Calculate averages
        }

        return average;
    }

    public getMetricName() {
        return this.metricName;
    }

    /**
     * Gets the last stored value.
     * @returns {T} The last stored value or an empty object if no values.
     */
    public getLastValue(): T {
        if (this.values.length === 0) return {} as T;
        return this.values[this.values.length - 1];
    }

    /**
     * Gets all recorded values of the metric.
     * @returns {T[]} Array of all metric values.
     */
    public getValues(): T[] {
        return this.values;
    }

    /**
     * Resets the values stored in the metric tracker.
     */
    public reset(): void {
        this.values = [];
    }

    /**
     * Logs the class type, last value, and the average of the stored values.
     */
    protected logMetrics(): void {
        const lastValue = this.getLastValue();
        const average = this.getAverage();

        const json = {
            metric: this.metricName,
            lastValue, 
            average,
        };

        this.loggingService.send(json);
    }

    /**
     * Formats the metric data as a JSON object to be sent to the logging service.
     * @returns The formatted JSON object containing the log name and properties.
     */
    protected toJson(): object {
        return {
            logName: this.metricName,
            properties: this.values,
        };
    }
}
