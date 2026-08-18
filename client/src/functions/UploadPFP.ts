import type { ToastMessageOptions } from 'primevue/toast';
import { eventBus } from '../events';
import axios from 'axios';
import type { DTO } from '../interfaces/DTO';

export const UploadPFP = (
    image: File,
    toastAdd: (message: ToastMessageOptions) => void,
    setLoading: (value: boolean) => void,
    refreshImage: () => void
) => {
    setLoading(true);
    const data = new FormData();
    data.append('image', image);

    axios.post('pfp/create_user_pfp/', data)
    .then(async res => {
        const data: DTO = res.data as DTO;

        if (!data.success) {
            toastAdd({
                severity: 'error',
                summary: 'Error while uploading',
                detail: data.message ?? 'Unknown error',
                life: 3000
            });
            return;
        }

        toastAdd({
            severity: 'success',
            summary: 'Success',
            detail: 'Successfully uploaded new PFP'
        });

        eventBus.emit('header-update');
    }).finally(() => {
        setLoading(false);
        refreshImage();
    });
}