export const API_ROUTE = import.meta.env.VITE_API_ROUTE;

export async function verifyUser(): Promise<string> {
    const token = localStorage.getItem("jwt");
    if (!token) return '';

    const res = await fetch(`${API_ROUTE}/user/get_current_user/`, {
        headers: { Authorization: `${token}` },
    });


    if (!res.ok) return '';

    const data = await res.json();
    return data.user_id || '';
}
