export class ActivityMonitor extends EventTarget {
    static EVENT_INACTIVITY_TIMEOUT = "inactivityTimeout";

    private inactivityTimeoutId: any = null; // Store the timeout ID to clear it

    // Inactivity timeout is configurable, default is 5 seconds
    // Can be adjusted based on user preferences or requirements
    private inactivityTimeLimit: number = 5000; 

    constructor(timeoutMs?: number) {
        super();
        if (timeoutMs) {
            this.inactivityTimeLimit = timeoutMs;
        }
    }

    public startInactivityTracking()
    {
        // If there's an existing timeout, clear it
        this.stopInactivityTracking();

        // Set a new timeout to trigger inactivity
        this.inactivityTimeoutId = setTimeout(() => {
            this.handleInactivityTimeout();
        }, this.inactivityTimeLimit);
    }
    public stopInactivityTracking() 
    {
        if (this.inactivityTimeoutId) {
            clearTimeout(this.inactivityTimeoutId);
        }
    }

    // Inactivity timeout handler
    private handleInactivityTimeout() {
        this.dispatchEvent(new CustomEvent(ActivityMonitor.EVENT_INACTIVITY_TIMEOUT, {
            detail: { 
                timestamp: Date.now()
            }
        }));
    }
}