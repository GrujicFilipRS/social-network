export interface PostData {
    id: string,
    body: string,
    title: string,
    status: 'PUBLIC' | 'PRIVATE',
    user_id: string,
    created_at: string | null
}