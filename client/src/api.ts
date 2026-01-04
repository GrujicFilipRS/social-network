export const API_ROUTE = import.meta.env.VITE_API_ROUTE;

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

    if (body && method !== "GET") {
        options.body = body;
    }

    return fetch(`${API_ROUTE}/${endpoint}`, options);
}

interface VerificationData {
    statusCode: number;
    result: any;
}

export async function verifyUser(): Promise<VerificationData> {
    return Fetch('user/get_current_user/')
    .then(async (res) => {
        return {
            statusCode: res.status,
            result: res,
        } as VerificationData;
    })
    .catch((err) => {
        console.log(err);
        return { statusCode: 0, result: "" } as VerificationData;
    });
}