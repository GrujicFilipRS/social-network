import type { DTO } from "./DTO";
import type { PhotoData } from "./PhotoData";

export interface PhotoListResponse extends DTO {
    photos: PhotoData[]
}