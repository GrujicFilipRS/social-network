export const API_ROUTE = import.meta.env.VITE_API_ROUTE;

export async function verifyUser(): Promise<number> {
    const token = localStorage.getItem("jwt");
    if (!token) return -1;

    const res = await fetch(`${API_ROUTE}/user/get_current_user/`, {
        headers: { Authorization: `${token}` },
    });

    if (!res.ok) return -1;

    const data = await res.json();
    return data.userId || -1;
}
