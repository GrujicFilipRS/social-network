import type { UserData } from './UserData';

export interface GetUserResponse {
    success: boolean;
    message: string | null;
    user: UserData | null;
}