const API_ROUTE = import.meta.env.VITE_API_ROUTE;

interface FetchOptions {
    method?: string,
    body?: string,
    headers?: Record<string, string>
};

export const Fetch = async (
    endpoint: string,
    {
        method = 'GET',
        body = '{}',
        headers = {}
    }: FetchOptions = {}
): Promise<Response> => {

    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...headers,
        },
        credentials: 'include',
    };

    if (body && method !== 'GET') {
        options.body = body;
    }

    return fetch(`${API_ROUTE}/${endpoint}`, options);
}

export const FetchWithFileUpload = async (
    endpoint: string,
    {
        method = 'GET',
        body = '{}',
        headers = {}
    }: FetchOptions = {},
    file: File,
    fileFieldName: string = 'file'
): Promise<Response> => {

    const formData = new FormData();

    formData.append(fileFieldName, file);

    if (body && typeof body === 'object') {
        Object.entries(body).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                formData.append(key, String(value));
            }
        });
    }

    const options: RequestInit = {
        method,
        credentials: 'include',
        headers: {
            ...headers
        },
        body: formData,
    };

    return fetch(`${API_ROUTE}/${endpoint}`, options);
}

interface FormDataFetchOptions {
    method?: string,
    body?: FormData,
    headers?: Record<string, string>
};

export const FetchWithFormData = async (
    endpoint: string,
    {
        method = 'GET',
        body = new FormData(),
        headers = {}
    }: FormDataFetchOptions = {}
): Promise<Response> => {
    const options: RequestInit = {
        method,
        credentials: 'include',
        headers: {
            ...headers
        },
        body: body,
    };

    return fetch(`${API_ROUTE}/${endpoint}`, options);
}

interface VerificationData {
    statusCode: number;
    result: any;
}

export async function verifyUser(): Promise<VerificationData> {
    return Fetch('user/get_current_user/')
    .then(async (res) => {
        const data = await res.json();
        return {
            statusCode: res.status,
            result: data,
        } as VerificationData;
    })
    .catch((err) => {
        console.log(err);
        return { statusCode: 0, result: '' } as VerificationData;
    });
}

export const createWebSocket = (endpoint: string, onMessage: (event: MessageEvent) => void): WebSocket => {
    const ws = new WebSocket(`${API_ROUTE.replace(/^http/, 'ws')}/${endpoint}`);

    ws.onopen = () => {
        console.log('WebSocket connection established');
    };

    ws.onmessage = onMessage;

    ws.onclose = () => {
        console.log('WebSocket connection closed');
    };

    return ws;
};