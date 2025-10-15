export interface PostData {
    id: number,
    body: string,
    title: string,
    status: 'PUBLIC' | 'PRIVATE',
    user_id: number,
    created_at: string | null
}