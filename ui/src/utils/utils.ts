/**
 * Formats the given first, middle, and last names into a single string.
 * Ensures that spaces are properly handled even if one of the inputs is undefined.
 * 
 * @param first - The first name.
 * @param middle - The middle name.
 * @param last - The last name.
 * @returns A string combining the first, middle, and last names.
 */
export function format(first?: string, middle?: string, last?: string): string {
    return [first, middle, last].filter(Boolean).join(' ').trim();
}

/**
 * Calculates the time duration between two Date objects and returns a formatted string
 * in the format "HH:mm:ss:SSS" (hours, minutes, seconds, milliseconds).
 * 
 * @param startDate - The starting Date object.
 * @param endDate - The ending Date object.
 * @returns A string representing the duration in the format "HH:mm:ss:SSS".
 */
export function calculateDuration(startDate: Date, endDate: Date): string {
    const durationMs = Math.abs(endDate.getTime() - startDate.getTime()); // Absolute difference to avoid negative durations

    const seconds = Math.floor((durationMs / 1000) % 60);
    const minutes = Math.floor((durationMs / (1000 * 60)) % 60);
    const hours = Math.floor(durationMs / (1000 * 60 * 60));
    const milliseconds = Math.floor(durationMs % 1000);

    // Formatting with padding for two-digit minutes and seconds, and three-digit milliseconds
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}:${String(milliseconds).padStart(3, '0')}`;
}

/**
 * Generates a simple unique ID based on the current timestamp and a random number.
 * The ID is formatted as "timestamp-random".
 * 
 * @returns A string representing the unique ID.
 */
export function generateSimpleUniqueId(): string {
    const timestamp = Date.now();
    const randomNumber = Math.floor(Math.random() * 1000);
    return `${timestamp}-${String(randomNumber).padStart(3, '0')}`;
}