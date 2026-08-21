import type { DTO } from "./DTO";

export interface ExistsGetResponse extends DTO {
    exists: boolean;
}