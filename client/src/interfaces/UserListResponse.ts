import type { DTO } from "./DTO";
import type { UserData } from "./UserData";

export interface UserListResponse extends DTO {
    users: UserData[];
}