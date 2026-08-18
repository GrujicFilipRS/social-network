import type { DTO } from './DTO';
import type { UserData } from './UserData';

export interface UserGetData extends DTO {
    user: UserData;
}